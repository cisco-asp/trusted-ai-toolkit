#!/usr/bin/env python3
"""Generate a thumbnail grid image from a PowerPoint presentation.

Usage:
    python thumbnail.py <input.pptx> [output_prefix] [--cols N]

Examples:
    python thumbnail.py presentation.pptx
    python thumbnail.py presentation.pptx workspace/grid --cols 4

Output:
    Creates thumbnails.jpg (or thumbnails-1.jpg, thumbnails-2.jpg for
    large decks that exceed the per-grid slide limit).

Requires: LibreOffice (soffice) and Pillow.
Optionally uses pdftoppm (poppler-utils) for higher quality.

Dependencies: Pillow
"""

import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


# Grid limits by column count
_GRID_LIMITS = {3: 12, 4: 20, 5: 30, 6: 42}
_DEFAULT_COLS = 5
_THUMB_WIDTH = 320  # pixels per thumbnail
_LABEL_HEIGHT = 24
_PADDING = 8


def _convert_to_images(pptx_path: str, work_dir: Path) -> list[Path]:
    """Convert PPTX → PDF → individual JPEG images."""
    # Step 1: PPTX → PDF via LibreOffice
    subprocess.run(
        [
            "soffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(work_dir),
            pptx_path,
        ],
        check=True,
        capture_output=True,
    )

    pdf_name = Path(pptx_path).stem + ".pdf"
    pdf_path = work_dir / pdf_name

    if not pdf_path.exists():
        print("ERROR: LibreOffice failed to produce a PDF.", file=sys.stderr)
        sys.exit(1)

    # Step 2: PDF → JPEG images
    # Try pdftoppm first (higher quality), fall back to Pillow
    prefix = str(work_dir / "slide")
    try:
        subprocess.run(
            ["pdftoppm", "-jpeg", "-r", "150", str(pdf_path), prefix],
            check=True,
            capture_output=True,
        )
        images = sorted(work_dir.glob("slide-*.jpg"))
    except (FileNotFoundError, subprocess.CalledProcessError):
        # Fallback: use pdf2image or manual extraction
        images = _pdf_to_images_pillow(pdf_path, work_dir)

    return images


def _pdf_to_images_pillow(pdf_path: Path, work_dir: Path) -> list[Path]:
    """Fallback: convert PDF pages to images using pdf2image (if available)."""
    try:
        from pdf2image import convert_from_path

        pil_images = convert_from_path(str(pdf_path), dpi=150, fmt="jpeg")
        paths = []
        for i, img in enumerate(pil_images):
            p = work_dir / f"slide-{i + 1:03d}.jpg"
            img.save(str(p), "JPEG")
            paths.append(p)
        return paths
    except ImportError:
        print(
            "ERROR: Neither pdftoppm nor pdf2image is available. "
            "Install poppler-utils or pip install pdf2image.",
            file=sys.stderr,
        )
        sys.exit(1)


def _create_grid(
    slide_images: list[Path],
    output_path: str,
    cols: int,
    start_index: int = 0,
) -> None:
    """Assemble slide thumbnail images into a labeled grid."""
    n = len(slide_images)
    rows = (n + cols - 1) // cols

    # Calculate aspect ratio from first image
    with Image.open(slide_images[0]) as sample:
        aspect = sample.width / sample.height

    thumb_h = int(_THUMB_WIDTH / aspect)
    cell_w = _THUMB_WIDTH + _PADDING * 2
    cell_h = thumb_h + _LABEL_HEIGHT + _PADDING * 2

    grid_w = cell_w * cols + _PADDING
    grid_h = cell_h * rows + _PADDING

    grid = Image.new("RGB", (grid_w, grid_h), "white")
    draw = ImageDraw.Draw(grid)

    # Try to use a basic font
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
    except (OSError, IOError):
        try:
            font = ImageFont.truetype("arial.ttf", 14)
        except (OSError, IOError):
            font = ImageFont.load_default()

    for i, img_path in enumerate(slide_images):
        row = i // cols
        col = i % cols
        x = col * cell_w + _PADDING
        y = row * cell_h + _PADDING

        with Image.open(img_path) as thumb:
            thumb = thumb.resize((_THUMB_WIDTH, thumb_h), Image.LANCZOS)
            grid.paste(thumb, (x, y))

        # Label
        label = f"Slide {start_index + i}"
        draw.text(
            (x + _THUMB_WIDTH // 2, y + thumb_h + 4),
            label,
            fill="black",
            font=font,
            anchor="mt",
        )

    grid.save(output_path, "JPEG", quality=90)
    print(f"Grid saved: {output_path} ({n} slides, {cols}x{rows})")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__.strip(), file=sys.stderr)
        sys.exit(1)

    pptx_path = args[0]
    if not Path(pptx_path).is_file():
        print(f"ERROR: '{pptx_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    # Parse optional arguments
    prefix = "thumbnails"
    cols = _DEFAULT_COLS

    remaining = args[1:]
    if remaining and not remaining[0].startswith("--"):
        prefix = remaining.pop(0)

    if "--cols" in remaining:
        idx = remaining.index("--cols")
        if idx + 1 < len(remaining):
            cols = int(remaining[idx + 1])
            cols = max(3, min(6, cols))

    max_per_grid = _GRID_LIMITS.get(cols, 30)

    with tempfile.TemporaryDirectory() as tmpdir:
        work_dir = Path(tmpdir)
        images = _convert_to_images(pptx_path, work_dir)

        if not images:
            print("ERROR: No slide images generated.", file=sys.stderr)
            sys.exit(1)

        # Split into grid pages if needed
        if len(images) <= max_per_grid:
            out = f"{prefix}.jpg"
            _create_grid(images, out, cols, start_index=0)
        else:
            page = 1
            for start in range(0, len(images), max_per_grid):
                chunk = images[start : start + max_per_grid]
                out = f"{prefix}-{page}.jpg"
                _create_grid(chunk, out, cols, start_index=start)
                page += 1


if __name__ == "__main__":
    main()
