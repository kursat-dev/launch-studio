#!/usr/bin/env node
// Measures a reference page's design language in a real browser.
// Usage: node measure_reference.mjs <url> [out-dir]
// Needs Playwright: `npm i -D playwright && npx playwright install chromium`
// (or set PLAYWRIGHT_DIR to a folder whose node_modules has playwright).
//
// Writes, per viewport (1440 and 390 px wide):
//   <out>/<width>.png   full-page screenshot
//   <out>/<width>.json  computed styles of key elements, the type scale,
//                       the colours in use and the top-level section boxes
// It only reads the page. It does not save the page's text or images.

import { createRequire } from 'node:module';
import { mkdirSync, writeFileSync } from 'node:fs';
import { join, resolve } from 'node:path';

const [url, outDir = 'reference-measurements'] = process.argv.slice(2);
if (!url) {
  console.error('Usage: node measure_reference.mjs <url> [out-dir]');
  process.exit(2);
}

const require = createRequire(join(resolve(process.env.PLAYWRIGHT_DIR || process.cwd()), 'noop.js'));
let chromium;
try {
  ({ chromium } = require('playwright'));
} catch {
  console.error('Playwright not found. Install it: npm i -D playwright && npx playwright install chromium');
  process.exit(3);
}

mkdirSync(outDir, { recursive: true });
const browser = await chromium.launch();
try {
  for (const width of [1440, 390]) {
    const page = await browser.newPage({ viewport: { width, height: 900 } });
    await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(1000);
    await page.screenshot({ path: join(outDir, `${width}.png`), fullPage: true });

    const data = await page.evaluate(() => {
      const props = [
        'fontFamily', 'fontSize', 'fontWeight', 'lineHeight', 'letterSpacing', 'textTransform',
        'color', 'backgroundColor', 'borderRadius', 'borderTopWidth', 'borderTopColor',
        'paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft', 'maxWidth', 'boxShadow',
      ];
      const pick = (el) => {
        const cs = getComputedStyle(el);
        const r = el.getBoundingClientRect();
        const out = { tag: el.tagName.toLowerCase(), cls: (el.className && String(el.className).slice(0, 80)) || '', w: Math.round(r.width), h: Math.round(r.height) };
        for (const p of props) out[p] = cs[p];
        return out;
      };
      const first = (sel, n = 3) => [...document.querySelectorAll(sel)].filter((e) => e.offsetParent !== null).slice(0, n).map(pick);

      const sizes = {}, colours = {}, fonts = {};
      for (const el of document.querySelectorAll('body *')) {
        if (el.offsetParent === null || !el.childNodes.length) continue;
        const hasText = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
        const cs = getComputedStyle(el);
        if (hasText) {
          const k = `${cs.fontSize} / ${cs.fontWeight}`;
          sizes[k] = (sizes[k] || 0) + 1;
          colours[cs.color] = (colours[cs.color] || 0) + 1;
          fonts[cs.fontFamily] = (fonts[cs.fontFamily] || 0) + 1;
        }
        if (cs.backgroundColor !== 'rgba(0, 0, 0, 0)') colours[`bg ${cs.backgroundColor}`] = (colours[`bg ${cs.backgroundColor}`] || 0) + 1;
      }
      const sort = (o) => Object.entries(o).sort((a, b) => b[1] - a[1]).slice(0, 25);

      const main = document.querySelector('main') || document.body;
      const sections = [...main.children].filter((e) => e.offsetParent !== null).map((e) => {
        const r = e.getBoundingClientRect();
        const cs = getComputedStyle(e);
        return { tag: e.tagName.toLowerCase(), id: e.id || '', top: Math.round(r.top + scrollY), height: Math.round(r.height), paddingTop: cs.paddingTop, paddingBottom: cs.paddingBottom, background: cs.backgroundColor };
      });

      return {
        url: location.href,
        viewportWidth: innerWidth,
        pageHeight: document.documentElement.scrollHeight,
        horizontalScroll: document.documentElement.scrollWidth > innerWidth,
        body: pick(document.body),
        headings: { h1: first('h1', 2), h2: first('h2'), h3: first('h3') },
        text: first('p'),
        links: first('a'),
        buttons: first('button, a[class*="button" i], a[class*="btn" i]'),
        typeScale: sort(sizes),
        colours: sort(colours),
        fonts: sort(fonts),
        sections,
      };
    });
    writeFileSync(join(outDir, `${width}.json`), JSON.stringify(data, null, 2));
    console.log(`${width}px: ${data.sections.length} sections, page height ${data.pageHeight}px, horizontal scroll: ${data.horizontalScroll}`);
    await page.close();
  }
} finally {
  await browser.close();
}
console.log(`Saved to ${outDir}/`);
