---
name: crd-builder
version: 1.0.0
description: Build a Customer Requirements Document (CRD) from template.docx for any customer or project. Use when the user asks to create, fill, or generate a CRD, customer requirements document, or product requirements document using the Cisco CRD template.
---

# Customer Requirements Document (CRD) Builder

This skill produces a filled `.docx` CRD derived from `template.docx`. The output must match the structure, styles, and tables of the template exactly.

## Bundled Files

| File | Purpose |
|------|---------|
| `template.docx` | Canonical CRD template — never overwrite |
| `build_crd.py` | Generic builder script — agent edits the `DATA` dict and runs it |

Both files live in the skill directory:

```
/Users/mfierbau/.agents/skills/crd-builder/
```

---

## Required Workflow

### Step 1 — Clarify Inputs

Before doing anything, list what the user provided and confirm:

- Source materials (PDF paths, pasted text, Excel files, links, Airtable data, meeting notes)
- Customer name and short project tag (used in the output filename)
- Number of features (one feature block per feature)
- Author (Cisco UserID), reviewers, and date
- Output directory (default: current working directory)

If any of these are ambiguous, **ask before drafting**. Do not fabricate customer data.

### Step 2 — Ingest Sources

Read all specified materials. Extract:

- Customer identity, region, segment, and contact
- Feature names, Aha IDs, descriptions, platforms, dependencies
- Scale targets, protocol requirements, and acceptance criteria
- Goals and success criteria (aim for 3 rows)
- Design checklist answers (Y/N/EFT per row)
- Reviewers by department
- Any appendix attachments or spreadsheet extracts

### Step 3 — Populate and Run the Builder Script

1. **Copy** `build_crd.py` from the skill directory into the project working directory (or run it directly from the skill directory — either works).
2. **Edit the `DATA` dict** at the bottom of the script with all customer-specific values extracted in Step 2.
3. **Run** the script:

   ```bash
   python build_crd.py
   ```

   If `python-docx` is not installed system-wide, the script automatically detects and uses a `_pydeps/` vendored directory if one exists in the working directory or skill directory.

4. The script writes `CRD_<Customer>_<Project>_<YYYYMMDD>.docx` to the configured `out_dir`.

### Step 4 — Quality Check

Before handing off, verify:

- [ ] Output is a `.docx` derived from `template.docx`, not a blank document
- [ ] Instruction/removal pages are gone; title page ("Customer Requirements Document") is first
- [ ] Section numbers match: 1, 2, 3, **5**, 6 (no section 4 — template skips it)
- [ ] All required table cells filled; N/A sections noted with rationale
- [ ] Reviewers, modification history, and dates reflect source inputs
- [ ] Feature and use-case sections cover every feature from the source material
- [ ] No hardcoded secrets or customer-internal data the user asked to exclude

---

## DATA Dict Reference

The `DATA` dict in `build_crd.py` maps directly to every section of the template. All keys are optional except where marked **required**.

### Top-level keys

| Key | Required | Type | Description |
|-----|----------|------|-------------|
| `customer` | **yes** | str | Customer name |
| `project` | **yes** | str | Short project tag for the filename |
| `author` | **yes** | str | Cisco UserID (e.g. `userid@cisco.com`) |
| `product_platform` | **yes** | str | Cover table row 1 |
| `technology_solution` | **yes** | str | Cover table row 2 |
| `date` | no | str | `MM/DD/YYYY`; blank = today |
| `out_dir` | no | str | Output directory path; default `.` |
| `mod_history_comments` | no | str | Modification history comments |
| `overview` | no | dict | Executive overview — see below |
| `goals` | no | list | Up to 3 `(description, target_date, measurement)` tuples |
| `business_case` | no | dict | Business case fields — see below |
| `reviewers` | no | list | `(department, name/title)` tuples |
| `features` | no | list | One dict per feature — see below |
| `extra_sections` | no | list | `(heading, body)` tuples inserted before §5 |
| `gap_table` | no | dict or None | Requirements gap table — see below |
| `checklist` | no | dict | Design checklist — row index → `{yn, eft}` |
| `appendix_sources` | no | list | Source file description strings for §6 |
| `appendix_table_rows` | no | list or None | Rows for an appendix spreadsheet table |
| `appendix_table_heading` | no | str | Heading for the appendix table |

### `overview` keys

| Key | Template prompt replaced |
|-----|--------------------------|
| `purpose` | `"Provide a description that covers what the purpose of this request?"` |
| `problems` | `"What are the problems it will solve?"` |
| `technical_detail` | `"Provide a description of the problems that this request is attempting to solve?"` |

### `business_case` keys

`customer`, `region`, `segment`, `contact`, `advanced_services`

### Feature dict keys

| Key | Maps to |
|-----|---------|
| `title` | Feature Details table header row |
| `name` | Feature Name |
| `aha_id` | Aha Idea # |
| `customer_feature_id` | Customer Feature ID |
| `contract_section` | Contract Section |
| `description` | Feature Description |
| `platforms` | Platforms |
| `critical` | Critical Feature? |
| `scalability` | Scalability and Performance Expectations Details |
| `golden_architecture` | Golden Architecture Model |
| `acceptance_criteria` | Acceptance Criteria |
| `solution_validation` | Solution Validation |
| `hw_requirements` | HW Requirements and Dependencies |
| `backward_compatibility` | Backward Compatibility |
| `deployment_plan` | Deployment Plan |
| `use_cases` | List of two use-case narrative strings |

For **more than one feature**, add additional dicts to the `features` list. The script duplicates the feature block automatically.

### `gap_table` keys

| Key | Type | Description |
|-----|------|-------------|
| `heading` | str | Must match one of the `extra_sections` headings |
| `col_headers` | list[str] | Column header strings |
| `rows` | list[tuple] | Data rows; each tuple length must equal `len(col_headers)` |

---

## Template Map (reference)

| Table index | Section |
|-------------|---------|
| `doc.tables[0]` | Cover |
| `doc.tables[1]` | Reviewers |
| `doc.tables[2]` | Modification History |
| `doc.tables[3]` | Goals and Success Criteria |
| `doc.tables[4]` | Business Case |
| `doc.tables[5]` | Feature 1 – Details |
| `doc.tables[6]` | Feature 1 – Use Case 1 |
| `doc.tables[7]` | Feature 1 – Use Case 2 |
| `doc.tables[8]` | Feature 2 – Details (if duplicated) |
| … | … |
| last table | Design Considerations Checklist (found by scanning for "High Availability" in first cell) |

Section numbering in the template: **1, 2, 3, 5, 6** — section 4 is intentionally absent.

---

## Style and Formatting Rules

- Section headings use paragraph style **`ToCSubhead1`** — do not change this style.
- Table structure is fixed — do not add or remove columns. Add rows only for reviewers or mod-history entries.
- Keep bold/colored label runs in tables intact; only replace value cells.
- Preserve headers/footers unless the user supplies replacement content.

Base directory for this skill: file:///Users/mfierbau/.agents/skills/crd-builder
