#!/usr/bin/env python3
"""Rearrange slides from a source presentation into a new file.

Usage:
    python rearrange.py <source.pptx> <output.pptx> <slide_indices>

    slide_indices: comma-separated 0-based indices, e.g. "0,3,3,7,1"
                   Duplicate indices create copies of that slide.

Example:
    python rearrange.py template.pptx working.pptx 0,5,5,12,18

This creates working.pptx containing slides 0, 5, 5 (duplicate), 12, 18
from template.pptx in that order.

Implementation: works at the OPC package level. The source .pptx is
unpacked, slides are reordered/duplicated by rewriting presentation.xml
and its relationships, and the result is repacked. This preserves
masters, layouts, themes, media, and all other parts exactly.

Dependencies: lxml
"""

import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

from lxml import etree


P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PR_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
SLIDE_REL_TYPE = (
    "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide"
)
SLIDE_CT = (
    "application/vnd.openxmlformats-officedocument.presentationml.slide+xml"
)
TEMPLATE_MAIN_CT = (
    "application/vnd.openxmlformats-officedocument.presentationml.template.main+xml"
)
PRESENTATION_MAIN_CT = (
    "application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"
)


def _unpack(src: Path, dst: Path) -> None:
    with zipfile.ZipFile(src, "r") as zf:
        zf.extractall(dst)


def _pack(src_dir: Path, dst: Path) -> None:
    priority = ["[Content_Types].xml", "_rels/.rels"]
    files = sorted(p.relative_to(src_dir) for p in src_dir.rglob("*") if p.is_file())
    pri = [f for f in files if str(f) in priority]
    rest = [f for f in files if str(f) not in priority]
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel in pri + rest:
            zf.write(src_dir / rel, str(rel))


def rearrange(src_path: str, dst_path: str, indices: list[int]) -> None:
    src_path_p = Path(src_path)
    dst_path_p = Path(dst_path)

    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        _unpack(src_path_p, work)

        ppt_dir = work / "ppt"
        pres_xml = ppt_dir / "presentation.xml"
        pres_rels = ppt_dir / "_rels" / "presentation.xml.rels"
        ct_xml = work / "[Content_Types].xml"

        if not pres_xml.exists():
            print(f"ERROR: not a valid PPTX (no ppt/presentation.xml).", file=sys.stderr)
            sys.exit(1)

        # Parse presentation.xml.rels — build rId -> target map
        rels_tree = etree.parse(str(pres_rels))
        rels_root = rels_tree.getroot()
        rid_to_target = {}
        for rel in rels_root.findall(f"{{{PR_NS}}}Relationship"):
            rid_to_target[rel.get("Id")] = rel.get("Target")

        # Parse presentation.xml — get current slide order via sldIdLst
        pres_tree = etree.parse(str(pres_xml))
        pres_root = pres_tree.getroot()
        sld_id_lst = pres_root.find(f"{{{P_NS}}}sldIdLst")
        if sld_id_lst is None:
            print("ERROR: presentation.xml has no sldIdLst.", file=sys.stderr)
            sys.exit(1)

        # Existing slide order: list of (sldId element, rId, target path)
        existing_slides = []
        for sld_id in sld_id_lst.findall(f"{{{P_NS}}}sldId"):
            rid = sld_id.get(f"{{{R_NS}}}id")
            target = rid_to_target.get(rid)
            existing_slides.append({
                "rid": rid,
                "target": target,  # e.g. "slides/slide5.xml"
            })

        total = len(existing_slides)
        bad = [i for i in indices if i < 0 or i >= total]
        if bad:
            print(
                f"ERROR: Indices {bad} out of range. Source has {total} slides "
                f"(0-{total - 1}).",
                file=sys.stderr,
            )
            sys.exit(1)

        # Identify which source slides we keep (any index referenced)
        used_indices = set(indices)

        # Plan: assign new slide numbers 1..N for the output sequence.
        # When a source slide is duplicated, copy its XML to a new file.
        slides_dir = ppt_dir / "slides"
        slide_rels_dir = slides_dir / "_rels"

        # Tracker of "used" original targets to detect duplicates.
        # Map output position -> {'src_target', 'new_target', 'src_rels_path'}
        plan = []
        first_seen: dict[str, str] = {}  # src_target -> first new_target assigned
        dup_counter = total + 1  # new slide files start after original max

        for out_pos, src_idx in enumerate(indices, start=1):
            src = existing_slides[src_idx]
            src_target = src["target"]

            if src_target not in first_seen:
                # First use — keep the original file in place
                new_target = src_target
                first_seen[src_target] = new_target
            else:
                # Duplicate — create new slide file
                new_filename = f"slides/slide{dup_counter}.xml"
                dup_counter += 1
                src_xml = ppt_dir / src_target
                new_xml = ppt_dir / new_filename
                shutil.copyfile(src_xml, new_xml)
                # Copy rels too
                src_rels = slide_rels_dir / (Path(src_target).name + ".rels")
                if src_rels.exists():
                    new_rels = slide_rels_dir / (Path(new_filename).name + ".rels")
                    shutil.copyfile(src_rels, new_rels)
                new_target = new_filename

            plan.append({"src_target": src_target, "new_target": new_target})

        # Determine which original slide files to delete (not in any new_target)
        kept_targets = {p["new_target"] for p in plan}
        original_targets = {s["target"] for s in existing_slides}
        to_delete = original_targets - kept_targets
        for t in to_delete:
            f = ppt_dir / t
            if f.exists():
                f.unlink()
            r = slide_rels_dir / (Path(t).name + ".rels")
            if r.exists():
                r.unlink()

        # Delete orphan notesSlides whose target slide no longer exists,
        # then strip stale notesSlide entries from notesMaster rels.
        notes_dir = ppt_dir / "notesSlides"
        notes_rels_dir = notes_dir / "_rels"
        deleted_notes = set()  # filenames like "notesSlide5.xml"
        if notes_rels_dir.is_dir():
            for nrels in list(notes_rels_dir.glob("*.xml.rels")):
                ntree = etree.parse(str(nrels))
                nroot = ntree.getroot()
                orphan = False
                for r in nroot.findall(f"{{{PR_NS}}}Relationship"):
                    tgt = r.get("Target", "")
                    if tgt.startswith("../slides/"):
                        slide_name = tgt[len("../slides/"):]
                        slide_path = slides_dir / slide_name
                        if not slide_path.exists():
                            orphan = True
                            break
                if orphan:
                    notes_xml_name = nrels.name[:-len(".rels")]
                    notes_xml = notes_dir / notes_xml_name
                    if notes_xml.exists():
                        notes_xml.unlink()
                    nrels.unlink()
                    deleted_notes.add(notes_xml_name)

        # Strip the deleted notes from notesMaster rels and Content Types
        if deleted_notes:
            nm_rels_dir = ppt_dir / "notesMasters" / "_rels"
            if nm_rels_dir.is_dir():
                for nm_rels in nm_rels_dir.glob("*.xml.rels"):
                    nmt = etree.parse(str(nm_rels))
                    nmr = nmt.getroot()
                    changed = False
                    for r in list(nmr.findall(f"{{{PR_NS}}}Relationship")):
                        tgt = r.get("Target", "")
                        if tgt.startswith("../notesSlides/"):
                            nname = tgt[len("../notesSlides/"):]
                            if nname in deleted_notes:
                                nmr.remove(r)
                                changed = True
                    if changed:
                        nmt.write(
                            str(nm_rels), xml_declaration=True,
                            encoding="UTF-8", standalone=True,
                        )

        # Also strip broken slide-to-slide hyperlink rels in surviving slides
        # (e.g. agenda slides that link to slides we removed).
        if slide_rels_dir.is_dir():
            for srels in slide_rels_dir.glob("*.xml.rels"):
                stree = etree.parse(str(srels))
                sroot = stree.getroot()
                changed = False
                for r in list(sroot.findall(f"{{{PR_NS}}}Relationship")):
                    if r.get("TargetMode") == "External":
                        continue
                    tgt = r.get("Target", "")
                    if "://" in tgt or tgt.startswith("mailto:"):
                        continue
                    # Resolve target relative to the slide's directory
                    resolved = (slides_dir / tgt).resolve()
                    if not resolved.exists():
                        sroot.remove(r)
                        changed = True
                if changed:
                    stree.write(
                        str(srels), xml_declaration=True,
                        encoding="UTF-8", standalone=True,
                    )

        # Rebuild presentation.xml.rels — keep non-slide rels, add new slide rels
        new_rels_root = etree.Element(f"{{{PR_NS}}}Relationships", nsmap={None: PR_NS})
        next_rid = 1

        # Preserve all non-slide relationships
        for rel in rels_root.findall(f"{{{PR_NS}}}Relationship"):
            if rel.get("Type") == SLIDE_REL_TYPE:
                continue
            # Reuse rId numerically; track max
            rid = rel.get("Id", "")
            if rid.startswith("rId"):
                try:
                    n = int(rid[3:])
                    next_rid = max(next_rid, n + 1)
                except ValueError:
                    pass
            new_rels_root.append(rel)

        # Add new slide relationships in the new order
        new_slide_rids = []
        for entry in plan:
            rid = f"rId{next_rid}"
            next_rid += 1
            etree.SubElement(
                new_rels_root,
                f"{{{PR_NS}}}Relationship",
                Id=rid,
                Type=SLIDE_REL_TYPE,
                Target=entry["new_target"],
            )
            new_slide_rids.append(rid)

        new_rels_tree = etree.ElementTree(new_rels_root)
        new_rels_tree.write(
            str(pres_rels), xml_declaration=True, encoding="UTF-8", standalone=True
        )

        # Rebuild sldIdLst in presentation.xml
        for child in list(sld_id_lst):
            sld_id_lst.remove(child)
        sld_id_num = 256  # PowerPoint convention: slide IDs start at 256
        for rid in new_slide_rids:
            etree.SubElement(
                sld_id_lst,
                f"{{{P_NS}}}sldId",
                id=str(sld_id_num),
                **{f"{{{R_NS}}}id": rid},
            )
            sld_id_num += 1

        pres_tree.write(
            str(pres_xml), xml_declaration=True, encoding="UTF-8", standalone=True
        )

        # Update [Content_Types].xml — drop deleted overrides, add for new slides,
        # and convert template content type to presentation content type so the
        # result is always a usable .pptx (even when the source was a .potx).
        ct_tree = etree.parse(str(ct_xml))
        ct_root = ct_tree.getroot()
        existing_overrides = {}
        for ovr in ct_root.findall(f"{{{CT_NS}}}Override"):
            ct = ovr.get("ContentType", "")
            if ct == TEMPLATE_MAIN_CT:
                ovr.set("ContentType", PRESENTATION_MAIN_CT)
            existing_overrides[ovr.get("PartName", "")] = ovr

        # Remove overrides for deleted files
        for t in to_delete:
            part_name = f"/ppt/{t}"
            if part_name in existing_overrides:
                ct_root.remove(existing_overrides[part_name])
                del existing_overrides[part_name]
        for nname in deleted_notes:
            part_name = f"/ppt/notesSlides/{nname}"
            if part_name in existing_overrides:
                ct_root.remove(existing_overrides[part_name])
                del existing_overrides[part_name]

        # Add overrides for any new slide files that aren't already declared
        for entry in plan:
            part_name = f"/ppt/{entry['new_target']}"
            if part_name not in existing_overrides:
                etree.SubElement(
                    ct_root,
                    f"{{{CT_NS}}}Override",
                    PartName=part_name,
                    ContentType=SLIDE_CT,
                )
                existing_overrides[part_name] = True  # marker

        ct_tree.write(
            str(ct_xml), xml_declaration=True, encoding="UTF-8", standalone=True
        )

        # Pack into output
        dst_path_p.parent.mkdir(parents=True, exist_ok=True)
        if dst_path_p.exists():
            dst_path_p.unlink()
        _pack(work, dst_path_p)

    print(f"Created {dst_path} with {len(indices)} slides from {src_path}")


def main():
    if len(sys.argv) != 4:
        print(__doc__.strip(), file=sys.stderr)
        sys.exit(1)

    src_path = sys.argv[1]
    dst_path = sys.argv[2]

    try:
        indices = [int(x.strip()) for x in sys.argv[3].split(",")]
    except ValueError:
        print("ERROR: slide_indices must be comma-separated integers.", file=sys.stderr)
        sys.exit(1)

    if not Path(src_path).is_file():
        print(f"ERROR: '{src_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    rearrange(src_path, dst_path, indices)


if __name__ == "__main__":
    main()
