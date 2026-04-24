#!/usr/bin/env python3
"""Repack a directory of Office Open XML parts into a .pptx / .docx / .xlsx.

Usage:
    python pack.py <input_directory> <output_file>

The script walks *input_directory*, adds every file into a ZIP archive using
deflate compression, and writes the result to *output_file*.  The special file
``[Content_Types].xml`` is always written first (required by the OPC spec).
"""

import sys
import zipfile
from pathlib import Path


# Files that the OPC spec requires at the archive root, written first.
_PRIORITY_FILES = ["[Content_Types].xml", "_rels/.rels"]


def pack(src: str, dst: str) -> None:
    src_path = Path(src)
    dst_path = Path(dst)

    if not src_path.is_dir():
        print(f"ERROR: '{src}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    # Collect all files, separating priority entries.
    all_files = sorted(
        p.relative_to(src_path)
        for p in src_path.rglob("*")
        if p.is_file()
    )

    priority = [f for f in all_files if str(f) in _PRIORITY_FILES]
    rest = [f for f in all_files if str(f) not in _PRIORITY_FILES]

    dst_path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(dst_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel in priority + rest:
            zf.write(src_path / rel, str(rel))

    count = len(priority) + len(rest)
    print(f"Packed {count} files into {dst_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__.strip(), file=sys.stderr)
        sys.exit(1)
    pack(sys.argv[1], sys.argv[2])
