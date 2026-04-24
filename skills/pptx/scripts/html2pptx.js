#!/usr/bin/env node
/**
 * html2pptx.js — Convert HTML slide files to PowerPoint presentations.
 *
 * Renders HTML files using Playwright (headless Chromium), extracts element
 * positions and styles, then maps them to PptxGenJS objects with accurate
 * coordinates.
 *
 * Usage as a library:
 *   const pptxgen = require('pptxgenjs');
 *   const html2pptx = require('./html2pptx');
 *   const pptx = new pptxgen();
 *   pptx.layout = 'LAYOUT_16x9';
 *   const { slide, placeholders } = await html2pptx('slide.html', pptx);
 *   await pptx.writeFile('output.pptx');
 *
 * Copyright 2026 Cisco Systems, Inc.
 * SPDX-License-Identifier: Apache-2.0
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

// Points-per-inch for coordinate conversion
const PPI = 96;  // CSS px per inch (standard)
const PT_PER_IN = 72;

/**
 * Convert an HTML slide file to a PptxGenJS slide.
 *
 * @param {string} htmlFile - Path to an HTML file
 * @param {object} pres - PptxGenJS presentation instance
 * @param {object} [options] - Options
 * @param {string} [options.tmpDir] - Temp directory for generated files
 * @param {object} [options.slide] - Existing slide to reuse
 * @returns {Promise<{slide: object, placeholders: Array}>}
 */
async function html2pptx(htmlFile, pres, options = {}) {
  const tmpDir = options.tmpDir || process.env.TMPDIR || '/tmp';
  const htmlPath = path.resolve(htmlFile);

  if (!fs.existsSync(htmlPath)) {
    throw new Error(`HTML file not found: ${htmlPath}`);
  }

  // Launch browser and render the HTML
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle' });

  // Extract body dimensions and validate
  const bodyInfo = await page.evaluate(() => {
    const body = document.body;
    const style = getComputedStyle(body);
    return {
      width: parseFloat(style.width),
      height: parseFloat(style.height),
      bgColor: style.backgroundColor,
    };
  });

  // Extract all renderable elements
  const elements = await page.evaluate(() => {
    const results = [];

    function getComputedStyles(el) {
      const s = getComputedStyle(el);
      return {
        fontFamily: s.fontFamily,
        fontSize: parseFloat(s.fontSize),
        fontWeight: s.fontWeight,
        fontStyle: s.fontStyle,
        textDecoration: s.textDecoration,
        textAlign: s.textAlign,
        color: s.color,
        backgroundColor: s.backgroundColor,
        borderLeft: s.borderLeft,
        borderRight: s.borderRight,
        borderTop: s.borderTop,
        borderBottom: s.borderBottom,
        border: s.border,
        borderRadius: s.borderRadius,
        boxShadow: s.boxShadow,
        display: s.display,
        backgroundImage: s.backgroundImage,
      };
    }

    function isVisible(el) {
      const s = getComputedStyle(el);
      return s.display !== 'none' && s.visibility !== 'hidden' && s.opacity !== '0';
    }

    function walk(el) {
      if (!isVisible(el)) return;

      const rect = el.getBoundingClientRect();
      const tag = el.tagName.toLowerCase();
      const styles = getComputedStyles(el);

      // Text elements
      if (['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'].includes(tag)) {
        const runs = [];
        for (const node of el.childNodes) {
          if (node.nodeType === 3) {
            // Text node
            runs.push({ text: node.textContent, bold: false, italic: false, underline: false, color: styles.color });
          } else if (node.nodeType === 1) {
            const childTag = node.tagName.toLowerCase();
            const childStyle = getComputedStyle(node);
            runs.push({
              text: node.textContent,
              bold: childTag === 'b' || childTag === 'strong' || childStyle.fontWeight >= 700,
              italic: childTag === 'i' || childTag === 'em' || childStyle.fontStyle === 'italic',
              underline: childTag === 'u' || childStyle.textDecoration.includes('underline'),
              color: childStyle.color,
            });
          }
        }
        results.push({
          type: 'text', tag, rect: { x: rect.x, y: rect.y, w: rect.width, h: rect.height },
          runs, styles,
        });
        return; // Don't recurse into text elements
      }

      // List elements
      if (tag === 'ul' || tag === 'ol') {
        const items = [];
        for (const li of el.querySelectorAll(':scope > li')) {
          const liRect = li.getBoundingClientRect();
          items.push({
            text: li.textContent.trim(),
            rect: { x: liRect.x, y: liRect.y, w: liRect.width, h: liRect.height },
          });
        }
        results.push({
          type: 'list', ordered: tag === 'ol',
          rect: { x: rect.x, y: rect.y, w: rect.width, h: rect.height },
          items, styles,
        });
        return;
      }

      // Images
      if (tag === 'img') {
        results.push({
          type: 'image',
          rect: { x: rect.x, y: rect.y, w: rect.width, h: rect.height },
          src: el.src,
        });
        return;
      }

      // Placeholder divs
      if (el.classList.contains('placeholder')) {
        results.push({
          type: 'placeholder',
          id: el.id || `placeholder-${results.length}`,
          rect: { x: rect.x, y: rect.y, w: rect.width, h: rect.height },
        });
        return;
      }

      // Div shapes (with background or border)
      if (tag === 'div') {
        const hasBg = styles.backgroundColor !== 'rgba(0, 0, 0, 0)' &&
                       styles.backgroundColor !== 'transparent';
        const hasBorder = styles.border && !styles.border.startsWith('0px');

        if (hasBg || hasBorder) {
          results.push({
            type: 'shape',
            rect: { x: rect.x, y: rect.y, w: rect.width, h: rect.height },
            styles,
          });
        }

        // Always recurse into divs
        for (const child of el.children) {
          walk(child);
        }
        return;
      }

      // Default: recurse
      for (const child of el.children) {
        walk(child);
      }
    }

    walk(document.body);
    return results;
  });

  await browser.close();

  // Convert to PptxGenJS slide
  const slide = options.slide || pres.addSlide();
  const placeholders = [];

  // Convert body background
  const bgColor = parseColor(bodyInfo.bgColor);
  if (bgColor) {
    slide.background = { fill: bgColor };
  }

  // Scale factor: CSS pixels → inches (PptxGenJS uses inches)
  const pxToIn = (px) => px / PPI;

  for (const el of elements) {
    const x = pxToIn(el.rect.x);
    const y = pxToIn(el.rect.y);
    const w = pxToIn(el.rect.w);
    const h = pxToIn(el.rect.h);

    switch (el.type) {
      case 'text': {
        const textRuns = (el.runs || []).map(run => ({
          text: run.text,
          options: {
            bold: run.bold || false,
            italic: run.italic || false,
            underline: run.underline ? { style: 'sng' } : undefined,
            color: parseColor(run.color),
            fontFace: parseFontFamily(el.styles.fontFamily),
            fontSize: ptFromPx(el.styles.fontSize),
          },
        }));
        const alignMap = { left: 'left', center: 'center', right: 'right', justify: 'justify' };
        slide.addText(textRuns, {
          x, y, w, h,
          align: alignMap[el.styles.textAlign] || 'left',
          valign: 'top',
          margin: 0,
          wrap: true,
        });
        break;
      }

      case 'list': {
        const listItems = (el.items || []).map((item, idx) => ({
          text: item.text,
          options: {
            bullet: el.ordered ? { type: 'number' } : true,
            indentLevel: 0,
            color: parseColor(el.styles.color),
            fontFace: parseFontFamily(el.styles.fontFamily),
            fontSize: ptFromPx(el.styles.fontSize),
          },
        }));
        slide.addText(listItems, {
          x, y, w, h,
          valign: 'top',
          margin: 0,
          wrap: true,
        });
        break;
      }

      case 'image': {
        const imgOpts = { x, y, w, h };
        if (el.src.startsWith('data:')) {
          imgOpts.data = el.src;
        } else if (el.src.startsWith('file://')) {
          imgOpts.path = el.src.replace('file://', '');
        } else {
          imgOpts.path = el.src;
        }
        slide.addImage(imgOpts);
        break;
      }

      case 'shape': {
        const shapeOpts = { x, y, w, h };
        const fillColor = parseColor(el.styles.backgroundColor);
        if (fillColor) {
          shapeOpts.fill = { color: fillColor };
        }
        const borderInfo = parseBorder(el.styles.border);
        if (borderInfo) {
          shapeOpts.line = { color: borderInfo.color, width: borderInfo.width };
        }
        const radius = parseBorderRadius(el.styles.borderRadius, el.rect.w, el.rect.h);
        if (radius > 0 && radius >= Math.min(el.rect.w, el.rect.h) / 2) {
          slide.addShape(pres.shapes.OVAL, shapeOpts);
        } else if (radius > 0) {
          shapeOpts.rectRadius = pxToIn(radius);
          slide.addShape(pres.shapes.ROUNDED_RECTANGLE, shapeOpts);
        } else {
          slide.addShape(pres.shapes.RECTANGLE, shapeOpts);
        }
        break;
      }

      case 'placeholder': {
        placeholders.push({ id: el.id, x, y, w, h });
        break;
      }
    }
  }

  return { slide, placeholders };
}


// --- Utility functions ---

function parseColor(cssColor) {
  if (!cssColor || cssColor === 'transparent' || cssColor === 'rgba(0, 0, 0, 0)') {
    return null;
  }
  // Handle rgb(r, g, b) and rgba(r, g, b, a)
  const rgbMatch = cssColor.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
  if (rgbMatch) {
    const r = parseInt(rgbMatch[1]).toString(16).padStart(2, '0');
    const g = parseInt(rgbMatch[2]).toString(16).padStart(2, '0');
    const b = parseInt(rgbMatch[3]).toString(16).padStart(2, '0');
    return `${r}${g}${b}`.toUpperCase();
  }
  // Handle #rrggbb
  const hexMatch = cssColor.match(/#([0-9a-fA-F]{6})/);
  if (hexMatch) {
    return hexMatch[1].toUpperCase();
  }
  // Handle #rgb
  const shortHex = cssColor.match(/#([0-9a-fA-F]{3})\b/);
  if (shortHex) {
    return shortHex[1].split('').map(c => c + c).join('').toUpperCase();
  }
  return null;
}

function parseFontFamily(cssFontFamily) {
  if (!cssFontFamily) return 'Arial';
  // Take the first font in the list, strip quotes
  const first = cssFontFamily.split(',')[0].trim().replace(/['"]/g, '');
  return first || 'Arial';
}

function ptFromPx(px) {
  // CSS px to PowerPoint points
  return Math.round((px / PPI) * PT_PER_IN * 10) / 10;
}

function parseBorder(cssBorder) {
  if (!cssBorder || cssBorder.startsWith('0px')) return null;
  const match = cssBorder.match(/([\d.]+)px\s+(\w+)\s+(.*)/);
  if (!match) return null;
  return {
    width: parseFloat(match[1]),
    style: match[2],
    color: parseColor(match[3]) || '000000',
  };
}

function parseBorderRadius(cssRadius, elWidth, elHeight) {
  if (!cssRadius || cssRadius === '0px') return 0;
  const match = cssRadius.match(/([\d.]+)(px|pt|%)/);
  if (!match) return 0;
  const value = parseFloat(match[1]);
  const unit = match[2];
  if (unit === '%') {
    return (value / 100) * Math.min(elWidth, elHeight);
  }
  return value; // px or pt
}


module.exports = html2pptx;
