#!/usr/bin/env python3
"""Extract a text and shape inventory from a PowerPoint presentation.

Usage:
    python inventory.py <input.pptx> <output.json>

Produces a JSON file describing every text-bearing shape in the
presentation, organized by slide.  Each shape includes position, size,
placeholder type, and paragraph details (text, formatting, bullets).

Dependencies: python-pptx
"""

import json
import sys
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

# Local import — make script runnable from any cwd
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _pptx_utils import ensure_pptx  # noqa: E402


# Map alignment enum to string
_ALIGN_MAP = {
    PP_ALIGN.LEFT: "LEFT",
    PP_ALIGN.CENTER: "CENTER",
    PP_ALIGN.RIGHT: "RIGHT",
    PP_ALIGN.JUSTIFY: "JUSTIFY",
    PP_ALIGN.DISTRIBUTE: "DISTRIBUTE",
}


def _emu_to_inches(emu_val) -> float | None:
    """Convert EMU to inches, rounding to 2 decimal places."""
    if emu_val is None:
        return None
    return round(emu_val / 914400, 2)


def _pt_value(pt_val) -> float | None:
    """Extract numeric point value."""
    if pt_val is None:
        return None
    if hasattr(pt_val, "pt"):
        return round(pt_val.pt, 1)
    return round(float(pt_val), 1)


def _color_to_str(color) -> str | None:
    """Convert a color object to hex string."""
    try:
        if color and color.rgb:
            return str(color.rgb)
    except (AttributeError, TypeError, ValueError):
        pass
    try:
        if color and color.theme_color:
            return None  # theme colors handled separately
    except (AttributeError, TypeError):
        pass
    return None


def _theme_color_name(color) -> str | None:
    """Extract theme color name if present."""
    try:
        if color and color.theme_color:
            return str(color.theme_color).replace("THEME_COLOR.", "")
    except (AttributeError, TypeError, ValueError):
        pass
    return None


def _extract_paragraph(para) -> dict:
    """Extract paragraph info including text, formatting, and bullet state."""
    info: dict = {}

    # Concatenate all runs
    text = para.text.strip()
    info["text"] = text

    # Indent / bullet level
    if para.level is not None and para.level >= 0:
        # Has indentation level — check if it has bullet formatting
        pPr = para._p.find(
            "{http://schemas.openxmlformats.org/drawingml/2006/main}pPr"
        )
        if pPr is not None:
            bu_none = pPr.find(
                "{http://schemas.openxmlformats.org/drawingml/2006/main}buNone"
            )
            if bu_none is None:
                info["bullet"] = True
                info["level"] = para.level

    # Alignment
    if para.alignment and para.alignment in _ALIGN_MAP:
        info["alignment"] = _ALIGN_MAP[para.alignment]

    # Spacing
    if para.space_before is not None:
        val = _pt_value(para.space_before)
        if val is not None:
            info["space_before"] = val
    if para.space_after is not None:
        val = _pt_value(para.space_after)
        if val is not None:
            info["space_after"] = val
    if para.line_spacing is not None:
        val = _pt_value(para.line_spacing)
        if val is not None:
            info["line_spacing"] = val

    # Font properties from first run (representative)
    if para.runs:
        run = para.runs[0]
        font = run.font
        if font.name:
            info["font_name"] = font.name
        if font.size:
            info["font_size"] = _pt_value(font.size)
        if font.bold:
            info["bold"] = True
        if font.italic:
            info["italic"] = True
        if font.underline:
            info["underline"] = True

        color_str = _color_to_str(font.color)
        if color_str:
            info["color"] = color_str
        theme = _theme_color_name(font.color)
        if theme:
            info["theme_color"] = theme

    return info


def _extract_shape(shape) -> dict | None:
    """Extract shape info if it contains text."""
    if not shape.has_text_frame:
        return None

    tf = shape.text_frame
    if not tf.text.strip():
        # Skip empty shapes
        return None

    info: dict = {}

    # Placeholder type
    if shape.is_placeholder:
        ph_type = shape.placeholder_format.type
        if ph_type is not None:
            type_name = str(ph_type).replace("PP_PLACEHOLDER_TYPE.", "")
            if type_name == "SLIDE_NUMBER":
                return None  # Skip slide number placeholders
            info["placeholder_type"] = type_name

    # Position and size
    info["left"] = _emu_to_inches(shape.left)
    info["top"] = _emu_to_inches(shape.top)
    info["width"] = _emu_to_inches(shape.width)
    info["height"] = _emu_to_inches(shape.height)

    # Default font size from layout placeholder (if available)
    if shape.is_placeholder:
        try:
            layout_ph = shape.placeholder_format._sp
            body_pr = layout_ph.find(
                ".//{http://schemas.openxmlformats.org/drawingml/2006/main}defRPr"
            )
            if body_pr is not None and body_pr.get("sz"):
                info["default_font_size"] = round(int(body_pr.get("sz")) / 100, 1)
        except (AttributeError, TypeError, ValueError):
            pass

    # Paragraphs
    paragraphs = []
    for para in tf.paragraphs:
        p_info = _extract_paragraph(para)
        if p_info.get("text"):  # Skip empty paragraphs
            paragraphs.append(p_info)

    if not paragraphs:
        return None

    info["paragraphs"] = paragraphs
    return info


def inventory(pptx_path: str) -> dict:
    """Build a full text inventory of the presentation."""
    # Auto-convert .potx → .pptx if needed
    usable = ensure_pptx(pptx_path)
    prs = Presentation(str(usable))
    result: dict = {}

    for slide_idx, slide in enumerate(prs.slides):
        slide_key = f"slide-{slide_idx}"
        shapes_data: dict = {}

        # Sort shapes by visual position: top-to-bottom, then left-to-right
        text_shapes = [s for s in slide.shapes if s.has_text_frame]
        text_shapes.sort(key=lambda s: (s.top or 0, s.left or 0))

        shape_counter = 0
        for shape in text_shapes:
            shape_info = _extract_shape(shape)
            if shape_info is not None:
                shapes_data[f"shape-{shape_counter}"] = shape_info
                shape_counter += 1

        if shapes_data:
            result[slide_key] = shapes_data

    return result


def main():
    if len(sys.argv) != 3:
        print(__doc__.strip(), file=sys.stderr)
        sys.exit(1)

    pptx_path = sys.argv[1]
    output_path = sys.argv[2]

    if not Path(pptx_path).is_file():
        print(f"ERROR: '{pptx_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    result = inventory(pptx_path)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    total_shapes = sum(len(v) for v in result.values())
    print(f"Extracted {total_shapes} shapes from {len(result)} slides → {output_path}")


if __name__ == "__main__":
    main()
