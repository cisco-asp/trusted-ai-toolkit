# Changelog

All notable changes to the `crd-builder` skill are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This skill uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html):
- **MAJOR** — breaking changes to the `DATA` dict schema or template structure
- **MINOR** — new DATA keys, new optional capabilities, template updates
- **PATCH** — bug fixes, documentation corrections, helper function improvements

---

## [1.0.0] — 2026-04-16

### Added
- `build_crd.py` — generic Python builder script; agent edits `DATA` dict and runs it
- `template.docx` — bundled canonical CRD template
- `SKILL.md` — full workflow, DATA dict reference, and template map
- Support for multiple features (auto-duplicates feature block)
- Support for extra narrative sections before §5
- Support for requirements gap tables
- Support for appendix spreadsheet table
- Auto-discovery of `_pydeps/` vendored library directory
