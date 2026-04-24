# OOXML Reference

This document explains the Office Open XML (OOXML) package format used by
PowerPoint (`.pptx`), Word (`.docx`), and Excel (`.xlsx`) files, and how to
edit them directly at the XML level.

Use this reference when you need precise control beyond what `python-pptx`
or `PptxGenJS` exposes — for example, manipulating animations, transitions,
SmartArt, custom XML parts, embedded fonts, or repairing damaged files.

---

## Package structure

An OOXML file is a ZIP archive containing XML "parts" plus media. The key
top-level entries are:

```
[Content_Types].xml      # MIME types for every part in the package
_rels/.rels              # Root relationships (points to the main document)
docProps/                # Core, app, and custom properties
ppt/                     # PowerPoint payload (or word/, xl/)
  presentation.xml       # Main document; lists slide IDs and references
  _rels/presentation.xml.rels
  slides/
    slide1.xml
    slide2.xml
    _rels/slide1.xml.rels
  slideLayouts/
  slideMasters/
  theme/
  media/                 # Images, audio, video
```

### Content Types
`[Content_Types].xml` declares the MIME type of every part. New parts must
be registered here either by extension (`<Default>`) or by exact path
(`<Override>`). Adding a slide without registering it produces a corrupt
file that PowerPoint will refuse to open.

### Relationships
Each `*.rels` file describes outbound links from a part. Relationship
targets are resolved relative to the *parent directory* of the `_rels`
folder. A `slide1.xml.rels` entry with `Target="../media/image1.png"`
resolves to `ppt/media/image1.png`.

### Slide referencing
The slide order shown in PowerPoint is determined by the
`<p:sldIdLst>` element inside `ppt/presentation.xml`, which references
slides by relationship ID (`r:id`). The relationship file
`ppt/_rels/presentation.xml.rels` then maps each rId to a slide XML file.

---

## Workflow

```
unpack → edit XML → validate → pack
```

### 1. Unpack
```
python ooxml/scripts/unpack.py input.pptx workdir/
```
Extracts the archive into a directory you can browse and edit.

### 2. Edit
Edit XML files directly. Keep namespaces intact. The most common
namespaces:

| Prefix | URI                                                                   |
|--------|------------------------------------------------------------------------|
| `a`    | `http://schemas.openxmlformats.org/drawingml/2006/main`               |
| `p`    | `http://schemas.openxmlformats.org/presentationml/2006/main`          |
| `r`    | `http://schemas.openxmlformats.org/officeDocument/2006/relationships` |
| `mc`   | `http://schemas.openxmlformats.org/markup-compatibility/2006`         |

### 3. Validate
```
python ooxml/scripts/validate.py workdir/
```
Performs structural checks:
- `[Content_Types].xml` declares every slide on disk
- All relationship targets resolve to real files
- `presentation.xml` slide list matches files in `ppt/slides/`
- Each slide references a layout that exists

### 4. Pack
```
python ooxml/scripts/pack.py workdir/ output.pptx
```
Repacks the directory into a valid OOXML archive. `[Content_Types].xml`
and `_rels/.rels` are written first as required by the OPC specification.

---

## Schema reference

The `ooxml/schemas/` directory contains the public XSD schemas used by
OOXML. They are sourced from:

- **ECMA-376 4th edition** — Office Open XML File Formats
- **ISO/IEC 29500-4:2016** — Transitional and Strict conformance schemas
- **Microsoft extensions** — published vendor namespaces

These are open standards; they are bundled here for offline reference only.

---

## Common edits

### Add a slide
1. Copy `slide1.xml` to `slideN.xml`.
2. Create `slideN.xml.rels` with the layout relationship.
3. Add `<Override>` for the new part in `[Content_Types].xml`.
4. Add a relationship in `presentation.xml.rels` (new rId).
5. Add `<p:sldId>` in `presentation.xml`'s `<p:sldIdLst>`.

### Reorder slides
Reorder `<p:sldId>` entries in `presentation.xml`. File names do *not*
need to match display order — they're just references.

### Replace an image
Drop the new image into `ppt/media/` (same name) or update the relationship
target in `slideN.xml.rels`.

### Remove a slide
1. Delete `slideN.xml` and its `_rels/slideN.xml.rels`.
2. Remove the `<Override>` from `[Content_Types].xml`.
3. Remove the relationship from `presentation.xml.rels`.
4. Remove the `<p:sldId>` from `presentation.xml`.

---

## Tips

- Always validate before repacking. Most "PowerPoint cannot open this
  file" errors come from missing content type declarations or broken
  relationships.
- Preserve XML declarations (`<?xml version="1.0" encoding="UTF-8"
  standalone="yes"?>`) at the top of each part.
- Don't reformat XML files unnecessarily — whitespace inside `<a:t>` text
  runs is significant.
- When in doubt, diff your unpacked directory against a freshly unpacked
  copy of the original to find regressions.
