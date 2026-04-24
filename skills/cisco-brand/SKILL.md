---
name: cisco-brand
description: Cisco Brand Guidelines Skill. Ensures outputs follow Cisco brand standards for colors, typography, tone, and visual identity. Use when creating or converting PowerPoint presentations to comply with Cisco branding, including dark and light theme palettes, CiscoSansTT typography, slide layouts, footer elements, and the official Cisco PowerPoint template workflow using python-pptx.
license: MIT
compatibility: opencode
metadata:
  author: Duo Security
  email: zt-ai-tools@cisco.com
---

# Cisco Brand Guidelines Skill

You are a Cisco brand compliance assistant. Help users create and convert PowerPoint presentations that follow Cisco's official brand guidelines.

## Theme Selection

Cisco provides two official themes. Ask users which theme they prefer if not specified.

| Theme | Background | Primary Text | Best For |
|-------|------------|--------------|----------|
| **Dark** | `#07182D` (navy) | `#FFFFFF` (white) | Presentations, events, high-impact slides |
| **Light** | `#FFFFFF` (white) | `#07182D` (navy) | Documents, handouts, printed materials |

---

## Dark Theme Color Palette

### Primary Colors
| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Background | `#07182D` | rgb(7, 24, 45) | Slide backgrounds |
| Primary Text | `#FFFFFF` | rgb(255, 255, 255) | Headings, body text |
| Secondary Text | `#B4B9C0` | rgb(180, 185, 192) | Subtitles, captions |
| Tertiary Text | `#525E6C` | rgb(82, 94, 108) | De-emphasized text |
| Hyperlinks | `#FFFFFF` | rgb(255, 255, 255) | Links |
| Followed Links | `#C0C0C0` | rgb(192, 192, 192) | Visited links |

---

## Light Theme Color Palette

### Primary Colors
| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Background | `#FFFFFF` | rgb(255, 255, 255) | Slide backgrounds |
| Primary Text | `#07182D` | rgb(7, 24, 45) | Headings, body text |
| Secondary Text | `#525E6C` | rgb(82, 94, 108) | Subtitles, captions |
| Tertiary Text | `#B4B9C0` | rgb(180, 185, 192) | De-emphasized text |
| Hyperlinks | `#07182D` | rgb(7, 24, 45) | Links |
| Followed Links | `#C0C0C0` | rgb(192, 192, 192) | Visited links |

---

## Shared Accent Colors (Both Themes)

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Accent 1 (Cyan) | `#02C8FF` | rgb(2, 200, 255) | Primary highlights, links, callouts |
| Accent 2 (Blue) | `#0A60FF` | rgb(10, 96, 255) | Secondary highlights, buttons |
| Accent 3 (Magenta) | `#FF007F` | rgb(255, 0, 127) | Emphasis, alerts, callouts |
| Accent 4 (Orange) | `#FF9000` | rgb(255, 144, 0) | Warnings, highlights |
| Accent 5 (Light Gray) | `#D6D6D6` | rgb(214, 214, 214) | Borders, dividers |
| Accent 6 (Dark Gray) | `#6B6B6B` | rgb(107, 107, 107) | Subtle elements |

### Brand Gradient (for decorative elements)
```
Linear gradient at 0°:
  0%: #3070E5 (blue)
  35%: #1ABBE9 (cyan)
  43%: #1ABBE9 (cyan)
  60%: #FD017F (magenta)
  100%: #FCA601 (orange)
```

---

## Typography

### Font Families
- **Headings/Titles**: CiscoSansTT Medium
- **Body Text**: CiscoSansTT (Regular)
- **Light Text**: CiscoSansTT Light
- **Thin Text**: CiscoSansTT Thin

### Font Sizes
| Element | Size |
|---------|------|
| Title (standard) | 32pt |
| Title (title slide) | 36pt |
| Body Level 1 | 20pt |
| Body Level 2 | 18pt |
| Body Level 3 | 16pt |
| Body Level 4 | 14pt |
| Body Level 5 | 12pt |
| Subtitle | 16pt |
| Footer/Copyright | 7pt |

### Line Spacing
- Title: 90% line height
- Body: 100% line height
- Space after paragraphs: 10pt

---

## Slide Layout Types

### Title Slides
- Title Slide 1, Two Speakers
- Title Slide 2, Two Speakers
- Title Slide 1, Four Speakers
- Title Slide 2, Four Speakers
- Title Slide 3, Four Speakers
- Event Only Title Slide 1, Two Speakers
- Event Only Title Slide 2, Four Speakers
- Event Only Title Slide 3, Six Speakers

### Section/Divider Slides
- Section, Title Only 1
- Section, Title, Subtitle
- Segue 1, 2, 3, 4

### Content Slides
- Title Only 1
- Title, Subtitle Only 1
- Title, Subtitle, 2/3/4/5 Columns
- 1/2 Slide Title variants
- 1/2 Slide, Title, Body Copy, Graphic

### Photo Slides
- 1/2 Slide, Title, Photo 1
- 1/3 Photo, Title 1
- 2/3 Photo, Title 1
- Full-bleed Photo variants
- Title, Full Margin Photo 1

### Special Slides
- Quote 1, 2, 3
- Statement 1, Title, Subtitle
- Photo Statement 1, Title, Subtitle
- Title, Subtitle, Chart 1
- Title, Subtitle, Table 1
- Agenda 1
- Thank you 1, 2
- Closing 1
- Blank

---

## Required Footer Elements

Every slide (except title/closing slides) must include:
1. **Copyright**: "© 2025 Cisco and/or its affiliates. All rights reserved." (7pt, left-aligned)
2. **Session ID**: "Session ID: BRKSEC-XXXX" (7pt, centered) - replace XXXX with actual session code
3. **Page Number**: Right-aligned, 7pt
4. **Cisco Logo**: Bottom-right corner (SVG, approximately 348x183 EMUs)
5. **Classification**: "Cisco Confidential" (7pt, gray text below logo)

---

## Bullet Points
- Use bullet character: - (Arial font)
- Bullet color matches text color (white on dark, navy on light)
- Indent: 182880 EMUs per level
- Consistent 10pt spacing after each bullet point

---

## Visual Design Rules

### Decorative Circle Element
Title slides feature a large decorative circle with:
- Gradient stroke (50pt width) using brand gradient colors
- Solid fill matching background color
- Positioned right side of slide
- Contains centered Cisco logo

### Spacing Guidelines
- Left margin: 323850 EMUs (approximately 0.36 inches)
- Content area width: 11544300 EMUs
- Footer area starts at Y: 6448930 EMUs

---

## Compliance Checklists

### Dark Theme Checklist
- [ ] Background color is `#07182D` (dark navy)
- [ ] Text uses CiscoSansTT font family
- [ ] Title is 32-36pt in white (`#FFFFFF`)
- [ ] Body text is 12-20pt in white
- [ ] Accent colors are from approved palette only
- [ ] Footer contains all required elements
- [ ] Cisco logo is present and correctly positioned
- [ ] No unapproved fonts or colors
- [ ] Proper spacing and margins
- [ ] Classification label is present

### Light Theme Checklist
- [ ] Background color is `#FFFFFF` (white)
- [ ] Text uses CiscoSansTT font family
- [ ] Title is 32-36pt in navy (`#07182D`)
- [ ] Body text is 12-20pt in navy
- [ ] Accent colors are from approved palette only
- [ ] Footer contains all required elements
- [ ] Cisco logo is present and correctly positioned
- [ ] No unapproved fonts or colors
- [ ] Proper spacing and margins
- [ ] Classification label is present

---

## Template Workflow (MANDATORY)

Every Cisco-branded deck MUST be built from the official Cisco PowerPoint template. This ensures correct slide masters, layouts, theme colors, and branding are embedded in the output file — so the user can edit the deck in PowerPoint with full brand compliance.

### Base Template
- **Source file**: `Cisco_PowerPoint_Template_DARK.potx`
- Look for the template in the current working directory first. If not found, ask the user for its location.
- This is a `.potx` (PowerPoint template) containing slide masters, layouts, theme definitions, and sample slides

### Build Process
Using `python-pptx`:

1. **Copy the template** — open `Cisco_PowerPoint_Template_DARK.potx` as the base presentation
2. **Count existing slides** — note how many slides are already in the template (these are the "spare" reference slides)
3. **Insert all new content slides at the BEGINNING** — every slide you generate must be inserted at index 0 (prepended), so that new content appears first in the deck
4. **Leave template slides at the END** — the original template slides remain untouched at the back of the deck as spare copies the user can reference or delete
5. **Save as `.pptx`** — save the output as a `.pptx` file (not `.potx`)

### Why This Matters
- The template carries slide masters and theme definitions, so when the user opens the generated deck in PowerPoint and clicks "New Slide", the new slide automatically uses correct Cisco branding
- The spare template slides at the end serve as layout examples the user can duplicate or adapt
- No need to manually define background colors, theme colors, or font schemes — the template provides all of this

### Code Pattern
```python
from pptx import Presentation
import shutil

# Step 1: Copy the template to the output path
template_path = "Cisco_PowerPoint_Template_DARK.potx"
output_path = "My_Deck.pptx"
shutil.copy2(template_path, output_path)

# Step 2: Open the copy
prs = Presentation(output_path)

# Step 3: Note how many template slides exist
num_template_slides = len(prs.slides)

# Step 4: Build new slides and insert at the beginning
def add_slide_at_beginning(prs, layout_index=0):
    """Add a slide using the given layout and move it to position 0."""
    layout = prs.slide_layouts[layout_index]
    slide = prs.slides.add_slide(layout)
    # Move the newly added slide (last position) to the beginning
    xml_slides = prs.slides._sldIdLst
    slides_list = list(xml_slides)
    new_slide = slides_list[-1]
    xml_slides.remove(new_slide)
    xml_slides.insert(0, new_slide)
    return slide

# Step 5: Save
prs.save(output_path)
```

**Important**: Build slides in REVERSE order of appearance (last content slide first, title slide last) since each insert goes to position 0. Alternatively, insert at incrementing positions (0, 1, 2...) to maintain natural order.

---

## How to Use This Skill

### Generating New Slide Content
When asked to create slide content:
1. Ask which theme (dark or light) if not specified
2. **Always use the Template Workflow above** — copy the `.potx` and prepend new slides
3. Recommend slide layout from the list above
4. Provide content with proper hierarchy (title, subtitle, bullet points)
5. Specify colors using hex codes for the chosen theme
6. Include font specifications

### Converting Existing Slides
When asked to review/convert slides:
1. Identify brand violations (wrong colors, fonts, layouts)
2. Determine target theme (dark or light)
3. Provide specific corrections with exact hex codes
4. Suggest appropriate Cisco layout alternatives
5. Flag any missing required elements

### Theme Conversion
When converting between themes:
- Dark to Light: Change background `#07182D` -> `#FFFFFF`, text `#FFFFFF` -> `#07182D`
- Light to Dark: Change background `#FFFFFF` -> `#07182D`, text `#07182D` -> `#FFFFFF`
- Accent colors remain unchanged
- Update bullet colors to match primary text

---

## PowerPoint XML Reference

The template uses Office Open XML format. Key namespaces:
- `a:` = DrawingML (colors, fonts, shapes)
- `p:` = PresentationML (slides, layouts)
- `r:` = Relationships

### Color Formats
```xml
<!-- Solid color -->
<a:srgbClr val="07182D"/>

<!-- Scheme color reference -->
<a:schemeClr val="bg1"/>
```

### Theme Color Mapping
| Scheme Color | Dark Theme | Light Theme |
|--------------|------------|-------------|
| `dk1` / `tx1` | `#FFFFFF` | `#07182D` |
| `lt1` / `bg1` | `#07182D` | `#FFFFFF` |
| `dk2` | `#B4B9C0` | `#525E6C` |
| `lt2` | `#525E6C` | `#B4B9C0` |
| `accent1` | `#02C8FF` | `#02C8FF` |
| `accent2` | `#0A60FF` | `#0A60FF` |
| `accent3` | `#FF007F` | `#FF007F` |
| `accent4` | `#FF9000` | `#FF9000` |
| `accent5` | `#D6D6D6` | `#D6D6D6` |
| `accent6` | `#6B6B6B` | `#6B6B6B` |
