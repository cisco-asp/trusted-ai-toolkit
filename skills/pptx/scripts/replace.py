#!/usr/bin/env python3
"""Replace text in a PowerPoint presentation using a replacement JSON file.

Usage:
    python replace.py <input.pptx> <replacement.json> <output.pptx>

The replacement JSON has the same structure as inventory.py output:
{
  "slide-0": {
    "shape-0": {
      "paragraphs": [
        {"text": "New title", "bold": true, "alignment": "CENTER"},
        {"text": "Bullet item", "bullet": true, "level": 0}
      ]
    }
  }
}

Shapes listed in the replacement JSON get their text replaced.
ALL other text shapes (from inventory) are cleared automatically.
This ensures no leftover template text remains.

Dependencies: python-pptx
"""

import json
import sys
from pathlib import Path

from pptx import Presentation
from pptx.util import Pt, Emu
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

# Local import — make script runnable from any cwd
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _pptx_utils import ensure_pptx  # noqa: E402


_ALIGN_MAP = {
    "LEFT": PP_ALIGN.LEFT,
    "CENTER": PP_ALIGN.CENTER,
    "RIGHT": PP_ALIGN.RIGHT,
    "JUSTIFY": PP_ALIGN.JUSTIFY,
    "DISTRIBUTE": PP_ALIGN.DISTRIBUTE,
}


def _clear_text_frame(text_frame):
    """Remove all text from a text frame while keeping the frame itself."""
    for para in text_frame.paragraphs:
        for run in para.runs:
            run.text = ""
        # Clear direct text on paragraph element
        el = para._p
        for child in list(el):
            tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
            if tag in ("r", "br"):
                el.remove(child)


def _apply_paragraph(text_frame, para_data: dict, para_idx: int):
    """Apply a single paragraph's content and formatting to the text frame."""
    # Get or create paragraph
    if para_idx < len(text_frame.paragraphs):
        para = text_frame.paragraphs[para_idx]
    else:
        para = text_frame.add_paragraph()

    # Clear existing runs
    for run in para.runs:
        run.text = ""
    el = para._p
    for child in list(el):
        tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if tag in ("r", "br"):
            el.remove(child)

    # Add new run with text
    run = para.add_run()
    run.text = para_data.get("text", "")

    # Font properties
    font = run.font
    if "font_name" in para_data:
        font.name = para_data["font_name"]
    if "font_size" in para_data:
        font.size = Pt(para_data["font_size"])
    if para_data.get("bold"):
        font.bold = True
    if para_data.get("italic"):
        font.italic = True
    if para_data.get("underline"):
        font.underline = True

    # Color
    if "color" in para_data:
        try:
            font.color.rgb = RGBColor.from_string(para_data["color"])
        except (ValueError, TypeError):
            pass

    # Alignment
    alignment = para_data.get("alignment")
    if alignment and alignment in _ALIGN_MAP:
        para.alignment = _ALIGN_MAP[alignment]

    # Bullets — auto-set left alignment when bullet is true
    if para_data.get("bullet"):
        para.level = para_data.get("level", 0)
        # Set bullet character via XML
        from lxml import etree
        nsmap = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
        pPr = para._p.find(f"{{{nsmap['a']}}}pPr")
        if pPr is None:
            pPr = etree.SubElement(
                para._p, f"{{{nsmap['a']}}}pPr"
            )
            # Insert pPr as first child
            para._p.insert(0, pPr)
        # Ensure there's a buChar element
        bu_char = pPr.find(f"{{{nsmap['a']}}}buChar")
        if bu_char is None:
            bu_char = etree.SubElement(pPr, f"{{{nsmap['a']}}}buChar")
            bu_char.set("char", "\u2022")

    # Spacing
    if "space_before" in para_data:
        para.space_before = Pt(para_data["space_before"])
    if "space_after" in para_data:
        para.space_after = Pt(para_data["space_after"])
    if "line_spacing" in para_data:
        para.line_spacing = Pt(para_data["line_spacing"])


def replace(pptx_path: str, replacement_path: str, output_path: str) -> None:
    """Apply replacements from JSON to the presentation."""
    with open(replacement_path, "r", encoding="utf-8") as f:
        replacements = json.load(f)

    # Auto-convert .potx → .pptx if needed
    usable = ensure_pptx(pptx_path)
    prs = Presentation(str(usable))

    # First pass: build a mapping of (slide_idx, shape_order) → shape object
    # Mirrors the ordering logic from inventory.py
    slide_shape_map: dict[str, dict[str, object]] = {}
    for slide_idx, slide in enumerate(prs.slides):
        slide_key = f"slide-{slide_idx}"
        text_shapes = [s for s in slide.shapes if s.has_text_frame]
        text_shapes.sort(key=lambda s: (s.top or 0, s.left or 0))

        shape_map: dict[str, object] = {}
        counter = 0
        for shape in text_shapes:
            # Skip slide number placeholders (same as inventory.py)
            if shape.is_placeholder:
                ph_type = shape.placeholder_format.type
                if ph_type is not None:
                    type_name = str(ph_type).replace("PP_PLACEHOLDER_TYPE.", "")
                    if type_name == "SLIDE_NUMBER":
                        continue

            if shape.text_frame.text.strip():
                shape_map[f"shape-{counter}"] = shape
                counter += 1

        slide_shape_map[slide_key] = shape_map

    # Validate replacement references
    errors: list[str] = []
    for slide_key, shapes in replacements.items():
        if slide_key not in slide_shape_map:
            errors.append(f"Slide '{slide_key}' not found in presentation")
            continue
        for shape_key in shapes:
            if shape_key not in slide_shape_map[slide_key]:
                avail = ", ".join(sorted(slide_shape_map[slide_key].keys()))
                errors.append(
                    f"Shape '{shape_key}' not found on '{slide_key}'. "
                    f"Available shapes: {avail}"
                )

    if errors:
        print("ERROR: Invalid shapes in replacement JSON:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    # Clear ALL text shapes, then apply replacements
    for slide_key, shape_map in slide_shape_map.items():
        replacement_slide = replacements.get(slide_key, {})
        for shape_key, shape in shape_map.items():
            _clear_text_frame(shape.text_frame)

            if shape_key in replacement_slide:
                paras = replacement_slide[shape_key].get("paragraphs", [])
                for i, para_data in enumerate(paras):
                    _apply_paragraph(shape.text_frame, para_data, i)

    prs.save(output_path)
    total_replaced = sum(
        len(shapes) for shapes in replacements.values()
    )
    print(f"Applied {total_replaced} shape replacements → {output_path}")


def main():
    if len(sys.argv) != 4:
        print(__doc__.strip(), file=sys.stderr)
        sys.exit(1)

    pptx_path = sys.argv[1]
    replacement_path = sys.argv[2]
    output_path = sys.argv[3]

    for path, label in [(pptx_path, "PPTX"), (replacement_path, "JSON")]:
        if not Path(path).is_file():
            print(f"ERROR: {label} file '{path}' does not exist.", file=sys.stderr)
            sys.exit(1)

    replace(pptx_path, replacement_path, output_path)


if __name__ == "__main__":
    main()
