"""PowerPoint-specific OOXML validation.

Checks presentation.xml slide list consistency, layout references,
and other PPTX-specific structural requirements.
"""

from pathlib import Path
from typing import List

try:
    from lxml import etree
except ImportError:
    etree = None  # type: ignore[assignment]


def check_presentation_slides(unpacked_dir: Path) -> List[str]:
    """Verify that presentation.xml slide references match files on disk."""
    errors: List[str] = []
    pres_path = unpacked_dir / "ppt" / "presentation.xml"
    if not pres_path.exists():
        errors.append("ppt/presentation.xml is missing")
        return errors

    if etree is None:
        return errors

    tree = etree.parse(str(pres_path))
    root = tree.getroot()

    ns = {
        "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
        "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    }

    # Get relationship IDs referenced in sldIdLst
    slide_rids = []
    for sld_id in root.findall(".//p:sldIdLst/p:sldId", ns):
        rid = sld_id.get(f"{{{ns['r']}}}id")
        if rid:
            slide_rids.append(rid)

    # Resolve rIds to file targets via presentation.xml.rels
    rels_path = unpacked_dir / "ppt" / "_rels" / "presentation.xml.rels"
    if not rels_path.exists():
        errors.append("ppt/_rels/presentation.xml.rels is missing")
        return errors

    rels_tree = etree.parse(str(rels_path))
    rels_root = rels_tree.getroot()
    rns = {"r": "http://schemas.openxmlformats.org/package/2006/relationships"}

    rid_to_target = {}
    for rel in rels_root.findall("r:Relationship", rns):
        rid_to_target[rel.get("Id", "")] = rel.get("Target", "")

    for rid in slide_rids:
        target = rid_to_target.get(rid)
        if target is None:
            errors.append(
                f"presentation.xml references {rid} but no matching relationship exists"
            )
            continue
        slide_path = (unpacked_dir / "ppt" / target).resolve()
        if not slide_path.exists():
            errors.append(
                f"Relationship {rid} targets '{target}' which does not exist"
            )

    # Check that slide files on disk are referenced
    slides_dir = unpacked_dir / "ppt" / "slides"
    if slides_dir.is_dir():
        referenced_targets = set(rid_to_target.get(r, "") for r in slide_rids)
        for slide_xml in sorted(slides_dir.glob("slide*.xml")):
            rel_target = f"slides/{slide_xml.name}"
            if rel_target not in referenced_targets:
                errors.append(
                    f"Slide file '{rel_target}' exists but is not referenced "
                    f"in presentation.xml sldIdLst"
                )

    return errors


def check_slide_layouts(unpacked_dir: Path) -> List[str]:
    """Verify that each slide references a layout that exists."""
    errors: List[str] = []
    slides_rels = unpacked_dir / "ppt" / "slides" / "_rels"
    if not slides_rels.is_dir():
        return errors

    if etree is None:
        return errors

    rns = {"r": "http://schemas.openxmlformats.org/package/2006/relationships"}
    layout_type = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout"
    )

    for rels_file in sorted(slides_rels.glob("*.xml.rels")):
        tree = etree.parse(str(rels_file))
        for rel in tree.getroot().findall("r:Relationship", rns):
            if rel.get("Type") == layout_type:
                target = rel.get("Target", "")
                layout_path = (rels_file.parent.parent / target).resolve()
                if not layout_path.exists():
                    errors.append(
                        f"{rels_file.name}: layout target '{target}' does not exist"
                    )

    return errors
