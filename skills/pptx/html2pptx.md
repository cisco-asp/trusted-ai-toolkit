# HTML to PPTX Reference

This document describes how to author PowerPoint slides as HTML and convert
them to `.pptx` using the bundled `scripts/html2pptx.js` tool.

The HTML approach is well-suited for slides built from scratch (no
pre-existing template), where you want full layout control via CSS without
hand-writing PptxGenJS coordinate math.

---

## How it works

1. Each HTML file represents **one slide**.
2. Playwright (headless Chromium) renders the HTML at exact slide
   dimensions and reads the computed bounding box and styles of every
   visible element.
3. Elements are mapped to PptxGenJS objects (text frames, lists, images,
   shapes) at the same on-screen position.
4. PptxGenJS writes a real `.pptx` file.

CSS pixels (96 px/in) are converted to PowerPoint inches.

---

## Slide dimensions

Set the body to the exact slide size you want. For 16:9 at 10in × 5.625in
(720 × 405 px at 72 DPI, or 960 × 540 px at 96 DPI):

```html
<body style="width: 960px; height: 540px; margin: 0; position: relative;">
  ...
</body>
```

Use `position: absolute` on children to place them precisely; PptxGenJS
will preserve those coordinates in the output.

---

## Supported elements

| HTML                          | PowerPoint result                       |
|-------------------------------|------------------------------------------|
| `<h1>`–`<h6>`, `<p>`         | Text frame (with bold/italic/underline runs) |
| `<ul>`, `<ol>`               | Bulleted or numbered list               |
| `<img>`                      | Image (file path, URL, or data URI)     |
| `<div>` with bg/border       | Shape (rectangle, rounded rect, oval)   |
| `<div class="placeholder">`  | Returned in the `placeholders` array — no shape rendered; useful for charts you want to add programmatically |

Inline `<b>`, `<strong>`, `<i>`, `<em>`, `<u>` inside text elements
become formatting runs.

---

## Shape detection

A `<div>` becomes a shape when it has a non-transparent background or a
non-zero border. The shape type is chosen from `border-radius`:

- `border-radius: 0` → `RECTANGLE`
- `border-radius: ≥ 50%` (or ≥ half the smaller side) → `OVAL`
- otherwise → `ROUNDED_RECTANGLE`

---

## Color, font, alignment

- `color`, `background-color`: any CSS color (`rgb()`, `rgba()`, `#hex`).
  Alpha is dropped.
- `font-family`: the first family is taken; quotes stripped.
- `font-size`: converted from CSS px to PowerPoint points.
- `font-weight ≥ 700` → bold.
- `text-align`: left, center, right, justify.

---

## Usage

### From a Node script

```javascript
const pptxgen = require('pptxgenjs');
const html2pptx = require('./scripts/html2pptx');

const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';   // or define a custom layout

const { slide, placeholders } = await html2pptx('slides/01-title.html', pres);

// You can still add things programmatically afterwards:
slide.addText('Footer', { x: 0.5, y: 5.2, w: 9, h: 0.3, fontSize: 10 });

// Render multiple slides
for (const file of ['slides/02.html', 'slides/03.html']) {
  await html2pptx(file, pres);
}

await pres.writeFile({ fileName: 'output.pptx' });
```

### Install dependencies

```
cd skills/pptx/scripts
npm install
npx playwright install chromium
```

---

## Placeholders

If you want to insert a chart, image, or other PptxGenJS object at a
specific spot, mark it in the HTML:

```html
<div class="placeholder" id="revenue-chart"
     style="position: absolute; left: 80px; top: 200px;
            width: 800px; height: 300px;"></div>
```

After calling `html2pptx`, look up the position from the returned array:

```javascript
const { slide, placeholders } = await html2pptx('slide.html', pres);
const chartSpot = placeholders.find(p => p.id === 'revenue-chart');
slide.addChart(pres.charts.BAR, data, chartSpot);  // x, y, w, h are inches
```

---

## Tips

- Test the HTML in a browser at the same dimensions before converting —
  what you see is what you get.
- Avoid CSS transforms (`translate`, `scale`, `rotate`) — bounding boxes
  may not be captured accurately.
- Keep nested layouts shallow: the converter walks the DOM and emits a
  shape per div with background/border.
- Use absolute paths or `data:` URIs for images so Playwright can find
  them.
- For multi-slide decks, write a small driver script that loops over an
  array of HTML files; each file = one slide.
