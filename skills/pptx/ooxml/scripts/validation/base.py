"""Base OOXML validation utilities.

Provides helpers for loading XSD schemas and validating XML parts
within an unpacked Office Open XML package.
"""

from pathlib import Path
from typing import List, Optional, Tuple

try:
    from lxml import etree
except ImportError:
    etree = None  # type: ignore[assignment]


SCHEMA_DIR = Path(__file__).resolve().parent.parent.parent / "schemas"


def load_schema(xsd_path: Path) -> Optional["etree.XMLSchema"]:
    """Load and compile an XSD schema file.  Returns None if lxml is missing."""
    if etree is None:
        return None
    doc = etree.parse(str(xsd_path))
    return etree.XMLSchema(doc)


def validate_xml_file(
    xml_path: Path, schema: "etree.XMLSchema"
) -> List[str]:
    """Validate a single XML file against a compiled schema.

    Returns a list of human-readable error strings (empty == valid).
    """
    if etree is None:
        return ["lxml is not installed – cannot validate"]
    try:
        doc = etree.parse(str(xml_path))
    except etree.XMLSyntaxError as exc:
        return [f"XML syntax error: {exc}"]
    if schema.validate(doc):
        return []
    return [str(e) for e in schema.error_log]


def check_content_types(unpacked_dir: Path) -> List[str]:
    """Verify that [Content_Types].xml exists and references all slide parts."""
    ct_path = unpacked_dir / "[Content_Types].xml"
    errors: List[str] = []
    if not ct_path.exists():
        errors.append("[Content_Types].xml is missing")
        return errors

    if etree is None:
        return errors

    tree = etree.parse(str(ct_path))
    root = tree.getroot()
    ns = {"ct": "http://schemas.openxmlformats.org/package/2006/content-types"}

    # Collect all declared part names
    declared = set()
    for override in root.findall("ct:Override", ns):
        part = override.get("PartName", "")
        declared.add(part.lstrip("/"))

    # Check that every slide XML on disk is declared
    slides_dir = unpacked_dir / "ppt" / "slides"
    if slides_dir.is_dir():
        for slide_xml in sorted(slides_dir.glob("slide*.xml")):
            rel = f"ppt/slides/{slide_xml.name}"
            if rel not in declared:
                errors.append(
                    f"Slide '{rel}' exists on disk but is not declared in [Content_Types].xml"
                )

    return errors


def check_relationships(unpacked_dir: Path) -> List[str]:
    """Check that relationship files reference targets that exist on disk."""
    errors: List[str] = []
    for rels_file in unpacked_dir.rglob("*.rels"):
        if etree is None:
            break
        tree = etree.parse(str(rels_file))
        root = tree.getroot()
        ns = {"r": "http://schemas.openxmlformats.org/package/2006/relationships"}
        base_dir = rels_file.parent.parent  # _rels is a subdirectory

        for rel in root.findall("r:Relationship", ns):
            target = rel.get("Target", "")
            # Skip external targets (URLs, mailto:, file:, etc.)
            if "://" in target or target.startswith("mailto:") or rel.get("TargetMode") == "External":
                continue
            target_path = (base_dir / target).resolve()
            if not target_path.exists():
                errors.append(
                    f"{rels_file.relative_to(unpacked_dir)}: "
                    f"target '{target}' does not exist"
                )

    return errors
