---
name: pptx
description: Presentation creation, editing, and analysis. Use when working with PowerPoint (.pptx) files for creating new presentations, modifying or editing content, working with layouts, adding comments or speaker notes, converting HTML to PPTX, or any other presentation tasks. Includes bundled scripts for HTML-to-PPTX conversion, OOXML editing, slide rearrangement, text inventory/replacement, and thumbnail generation.
author: mfierbau@cisco.com
license: Apache-2.0
---

# PowerPoint (PPTX) Skill

Tooling for creating, editing, and analyzing PowerPoint presentations.
Three workflows are supported, each suited to a different starting point:

1. **Template-based** — start from an existing `.pptx` (e.g. a Cisco
   branded deck) and replace text/images while preserving layout.
2. **HTML-to-PPTX** — author slides as HTML files and convert them to a
   `.pptx` with PptxGenJS + Playwright.
3. **Raw OOXML editing** — unpack the `.pptx`, edit XML directly, and
   repack. Use this only when the higher-level tools cannot express the
   change.

---

## Workflows

### 1. Template-based editing (most common)

Use this when the user provides an existing deck or asks for a Cisco
branded presentation. The bundled `templates/` directory contains the
official Cisco PowerPoint templates (light/dark themes and icon kits).

> **Note on `.potx` templates:** All scripts accept `.potx` (PowerPoint
> template) files directly. They are auto-converted to `.pptx`
> internally — you don't need to convert them by hand. The output is
> always written as a regular `.pptx` so it opens normally in
> PowerPoint and can be edited with `python-pptx`.

**Step 1 — Pick slides from a template:**
```
python scripts/rearrange.py templates/Cisco_PowerPoint_Template_LIGHT_04-01-2026.potx \
  working.pptx 0,2,5,5,12
```
Creates `working.pptx` with the listed slides (duplicates allowed) in the
given order.

**Step 2 — Inventory the existing text:**
```
python scripts/inventory.py working.pptx inventory.json
```
Produces a JSON file listing every text-bearing shape on every slide,
with position, formatting, and current text.

**Step 3 — Edit the JSON.** Keep the same `slide-N` / `shape-N` keys.
Only include shapes you want to change; everything else listed in
inventory will be **cleared** automatically (this prevents leftover
template text). Example replacement:
```json
{
  "slide-0": {
    "shape-0": {
      "paragraphs": [
        {"text": "Customer Briefing", "bold": true, "font_size": 36, "alignment": "CENTER"}
      ]
    },
    "shape-1": {
      "paragraphs": [
        {"text": "Key point one", "bullet": true, "level": 0},
        {"text": "Key point two", "bullet": true, "level": 0}
      ]
    }
  }
}
```

**Step 4 — Apply replacements:**
```
python scripts/replace.py working.pptx replacements.json final.pptx
```

**Step 5 (optional) — Generate thumbnails to verify:**
```
python scripts/thumbnail.py final.pptx
```
Outputs `thumbnails.jpg` (or paged variants for large decks). Requires
LibreOffice (`soffice`) and either `pdftoppm` or the `pdf2image` Python
package.

#### Cisco branding
When the user asks for a Cisco branded deck, also load the `cisco-brand`
skill for color palettes, typography rules, and footer requirements.
Always start from one of the `templates/` files rather than building from
scratch.

---

### 2. HTML-to-PPTX (build from scratch)

Use this when the user wants a custom design and there is no template to
start from. Author each slide as an HTML file and let
`scripts/html2pptx.js` convert it to a real `.pptx` while preserving
positions and formatting.

```
cd skills/pptx/scripts
npm install
npx playwright install chromium
```

Then write a small driver script:
```javascript
const pptxgen = require('pptxgenjs');
const html2pptx = require('./scripts/html2pptx');

const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';

for (const file of ['slides/01.html', 'slides/02.html', 'slides/03.html']) {
  await html2pptx(file, pres);
}
await pres.writeFile({ fileName: 'output.pptx' });
```

See `html2pptx.md` for full details — supported elements, dimensions,
shape detection, placeholders, and tips.

---

### 3. Raw OOXML editing (advanced)

Use this only when needed: animations, transitions, SmartArt, custom XML
parts, repairing broken files, or anything else not exposed by
`python-pptx` or `PptxGenJS`.

```
python ooxml/scripts/unpack.py input.pptx workdir/
# edit XML files in workdir/
python ooxml/scripts/validate.py workdir/
python ooxml/scripts/pack.py workdir/ output.pptx
```

See `ooxml.md` for the package structure, namespaces, common edits, and
schema reference.

---

## Files in this skill

```
SKILL.md                    # This file
ooxml.md                    # Raw XML editing reference
html2pptx.md                # HTML authoring reference
LICENSE                     # Apache-2.0
scripts/
  inventory.py              # Extract text + shape inventory → JSON
  replace.py                # Apply replacement JSON to a .pptx
  rearrange.py              # Pick & duplicate slides from a source deck
  thumbnail.py              # Render thumbnail grid (needs soffice)
  html2pptx.js              # HTML → PPTX converter (Playwright + PptxGenJS)
  _pptx_utils.py            # Shared helpers (e.g. .potx → .pptx auto-conversion)
  package.json              # Node deps
ooxml/
  scripts/
    unpack.py               # .pptx → directory
    pack.py                 # directory → .pptx
    validate.py             # Structural validation
    validation/             # Helpers for content types, rels, slide refs
  schemas/                  # Public XSD schemas (ECMA-376, ISO/IEC 29500)
templates/                  # Official Cisco PPTX templates
```

---

## Dependencies

**Python:** `python-pptx`, `lxml`, `Pillow`
```
pip install python-pptx lxml Pillow
# Optional for thumbnail.py fallback path:
pip install pdf2image
```

**Node (for HTML→PPTX):** `pptxgenjs`, `playwright`
```
cd scripts && npm install && npx playwright install chromium
```

**System (for thumbnails):** `libreoffice` (provides `soffice`),
optionally `poppler-utils` (provides `pdftoppm`).

---

## Decision guide

| If the user wants…                              | Use                          |
|--------------------------------------------------|------------------------------|
| Cisco branded slides                             | template-based + cisco-brand |
| Quick text edits to an existing deck             | template-based               |
| Custom design with no template                   | HTML-to-PPTX                 |
| Animations, transitions, SmartArt, repairs       | raw OOXML                    |
| Thumbnails for review                            | `scripts/thumbnail.py`       |
| Inspecting what's in a deck                      | `scripts/inventory.py`       |

When in doubt, start with template-based — it's the fastest path to a
clean, on-brand deliverable.
