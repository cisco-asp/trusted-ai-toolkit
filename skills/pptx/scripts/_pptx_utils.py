"""Helper utilities shared across pptx skill scripts.

Provides:
- ensure_pptx(path): converts .potx (PowerPoint template) to .pptx
  in-place at the OOXML content-type level, no LibreOffice required.
  Returns the path to a usable .pptx file.

Copyright 2026 Cisco Systems, Inc.
SPDX-License-Identifier: Apache-2.0
"""

import shutil
import sys
import tempfile
import zipfile
from pathlib import Path


# OOXML content types
TEMPLATE_MAIN_CT = (
    "application/vnd.openxmlformats-officedocument.presentationml.template.main+xml"
)
PRESENTATION_MAIN_CT = (
    "application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"
)


def is_template(path: Path) -> bool:
    """Return True if the file declares the .potx (template) content type."""
    if not path.is_file():
        return False
    try:
        with zipfile.ZipFile(path, "r") as zf:
            with zf.open("[Content_Types].xml") as f:
                ct = f.read().decode("utf-8", errors="ignore")
                return TEMPLATE_MAIN_CT in ct
    except (zipfile.BadZipFile, KeyError):
        return False


def convert_template_to_presentation(src: Path, dst: Path) -> None:
    """Copy `src` to `dst`, swapping the template content type for presentation.

    This is a structural rewrite of `[Content_Types].xml` only — all slides,
    layouts, masters, and media are preserved untouched.
    """
    with zipfile.ZipFile(src, "r") as zin:
        with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == "[Content_Types].xml":
                    text = data.decode("utf-8")
                    text = text.replace(TEMPLATE_MAIN_CT, PRESENTATION_MAIN_CT)
                    data = text.encode("utf-8")
                zout.writestr(item, data)


def ensure_pptx(path: str | Path, workdir: Path | None = None) -> Path:
    """Return a path to a .pptx version of the input file.

    If `path` is already a .pptx (presentation content type), it is returned
    as-is. If it is a .potx, a converted copy is written to `workdir`
    (or a temp directory) and that path is returned.

    The caller is responsible for not modifying the returned file in a way
    that would corrupt the original when the same path is returned.
    """
    p = Path(path)
    if not p.is_file():
        print(f"ERROR: '{p}' does not exist.", file=sys.stderr)
        sys.exit(1)

    if not is_template(p):
        return p

    if workdir is None:
        workdir = Path(tempfile.mkdtemp(prefix="pptx_skill_"))
    else:
        workdir.mkdir(parents=True, exist_ok=True)

    converted = workdir / (p.stem + ".pptx")
    convert_template_to_presentation(p, converted)
    return converted
