#!/usr/bin/env python3
"""Unpack an Office Open XML file (.pptx, .docx, .xlsx) into a directory.

Usage:
    python unpack.py <office_file> <output_dir>

The output directory is created if it does not exist.  If it already exists
the contents are overwritten.
"""

import sys
import zipfile
from pathlib import Path


def unpack(src: str, dst: str) -> None:
    src_path = Path(src)
    dst_path = Path(dst)

    if not src_path.is_file():
        print(f"ERROR: '{src}' does not exist or is not a file.", file=sys.stderr)
        sys.exit(1)

    dst_path.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(src_path, "r") as zf:
        zf.extractall(dst_path)

    count = sum(1 for _ in dst_path.rglob("*") if _.is_file())
    print(f"Unpacked {count} files to {dst_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__.strip(), file=sys.stderr)
        sys.exit(1)
    unpack(sys.argv[1], sys.argv[2])
