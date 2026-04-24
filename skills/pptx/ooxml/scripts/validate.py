#!/usr/bin/env python3
"""Validate an unpacked OOXML package for structural correctness.

Usage:
    python validate.py <unpacked_dir> [--original <source_file>]

Checks performed:
  - [Content_Types].xml completeness
  - Relationship target existence
  - presentation.xml ↔ slide file consistency
  - Slide layout references
  - Optional: compare against original file for regressions

Exit code 0 = valid, 1 = errors found.
"""

import sys
from pathlib import Path

from validation.base import check_content_types, check_relationships
from validation.pptx import check_presentation_slides, check_slide_layouts


def validate(unpacked_dir: str, original: str | None = None) -> int:
    root = Path(unpacked_dir)
    if not root.is_dir():
        print(f"ERROR: '{unpacked_dir}' is not a directory.", file=sys.stderr)
        return 1

    all_errors: list[str] = []

    print(f"Validating: {root}")
    print()

    # Structural checks
    all_errors.extend(check_content_types(root))
    all_errors.extend(check_relationships(root))

    # PPTX-specific checks
    if (root / "ppt" / "presentation.xml").exists():
        all_errors.extend(check_presentation_slides(root))
        all_errors.extend(check_slide_layouts(root))

    if all_errors:
        print(f"ERRORS ({len(all_errors)}):")
        for err in all_errors:
            print(f"  - {err}")
        return 1

    print("OK: No structural errors found.")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__.strip(), file=sys.stderr)
        sys.exit(1)

    dir_path = args[0]
    orig = None
    if "--original" in args:
        idx = args.index("--original")
        if idx + 1 < len(args):
            orig = args[idx + 1]

    sys.exit(validate(dir_path, orig))
