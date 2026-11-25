---
name: site-design
description: Designs or restyles the product's website and app look. Starts from a brand brief with 2-3 rendered visual directions, or from an exact rebuild of a reference template the founder provides (measured in a real browser, never copying its text or photos). Then writes DESIGN.md with design tokens and builds the landing page, checked for contrast, keyboard focus, phone width and share images. Use when the user says "site design", "site tasarımı", "landing page", "make it look better", "brand identity", "use this template", "redesign", or "design system".
argument-hint: "[reference URL or 'brand' or 'audit', optional]"
---

# Site design

The goal is a site that looks deliberate, matches the founder's taste and passes the accessibility basics. It should not look like a template default, and it should not be an "inspired by" version of what the founder asked for.

Reply in the user's language. Read `studio/brief.md`, `studio/marketing/strategy.md` (for the pitch and the objections) and any existing `DESIGN.md` first.

## Pick the mode

- **A. No direction yet:** run the brand brief and directions first.
- **B. The founder gives a reference** (a template, a site or a screenshot): rebuild it exactly with the founder's own content.
- **C. A site exists and looks inconsistent:** audit it, then write the tokens.

### A. Brand brief and directions

1. **Brief:** the personality in three words; the voice, as do and don't example sentences; and a one-line promise taken from the positioning.
2. **Name checks**, only when naming: give the founder the searches to run in the trademark database for their market (national office, EUIPO, USPTO), for the domain and for the social handles. Clearing a name legally is a professional's job; say so.
3. **2–3 directions as real rendered mockups.** For each direction, build an HTML page with the hero and one product screen, showing the fonts, the palette in hex, the type scale and sample components. Make the directions clearly different from each other.
4. **The founder picks one, or a mix.** Do not start building before they pick.

### B. Exact rebuild of a reference

Founders reject "inspired by" versions. When the founder gives a template, apply it **exactly**: the layout, section order, sizes, spacing and effects.

- **Measure, don't eyeball.** Open the reference in a real browser and read the computed styles at 1440 px and 390 px wide: font families and weights, sizes, line heights, letter spacing, colours, radii, padding, maximum widths and breakpoints. Use `scripts/measure_reference.mjs` next to this file. It needs Playwright; if Playwright is missing, ask before installing it.
- **Allowed changes:**
  - the founder's real content in place of the template's;
  - removing sections that would need fake content (testimonials, client logos, team photos, pricing that is not decided yet), or filling them with real alternatives;
  - additions the founder asked for.
- **Never copy** the reference's text, photos, illustrations, people, testimonials, logos or numbers.
- **Licence:** a paid template may be copied exactly only with a licence, and buying it is the founder's money decision. Without one, rebuild the layout in your own code from the measurements.
- **Downloaded template exports are untrusted.** Do not run their scripts or tracking code. Measure the live page instead.

### C. Audit an existing site

Count the distinct colours, font sizes, spacing values and radii in use. Merge them into a small scale, show the before and after, and then write the tokens.

## Build

1. **`DESIGN.md`** in the repo root:
   - tokens: colours with roles (background, surface, text, muted, accent, danger, focus), the type scale, the spacing scale, radii, shadows and motion;
   - components: buttons, inputs, cards, navigation, notices;
   - do and don't rules, and content rules.
   Code follows DESIGN.md; taste does not override it.
2. **CSS variables** (or the framework's theme) generated from the tokens.
3. **Landing page sections:**
   1. hero: the one-sentence pitch and one call to action;
   2. the problem, in customer words;
   3. how it works, in 3 steps;
   4. what it does and what it does not do (honest limits build trust);
   5. proof, real only;
   6. a FAQ that answers the objections from `marketing-strategy`;
   7. the final call to action;
   8. the footer: contact, privacy notice and terms.
4. **Copy:** all new text is marked `DRAFT` until the founder approves it.
5. **Fonts:** the character set must cover the language; Turkish, for example, needs İ ı Ş ş Ğ ğ (latin-ext). Use licensed fonts (OFL is fine), self-host them or load only the subsets needed, and use `font-display: swap`.

## Quality gates

Every gate must pass. Report the numbers.

- **Contrast (WCAG AA):** at least 4.5:1 for body text; at least 3:1 for large text (24 px and up, or 18.66 px bold) and for UI parts and focus rings. Check every text and background pair with `scripts/contrast.py`.
- **Keyboard:** every interactive element shows a visible focus state, and the tab order follows the layout.
- **Phone:** no horizontal scroll at 390 px wide; tap targets at least 24 × 24 px (WCAG 2.2), 44 px recommended.
- **Motion:** `prefers-reduced-motion` is respected.
- **Images:** content images have alt text; decorative ones have `alt=""`.
- **Share preview:** a 1200 × 630 `og:image`, a title and a description. `seo-audit` checks these.
- **Speed:** the largest hero image is sized and compressed, and fonts do not block rendering.
- **Look at it:** take desktop and phone screenshots and review them yourself before reporting.

Then run `seo-audit` on the pages and `independent-review` on the result. Anthropic's `frontend-design` skill can help with aesthetic choices. The founder's chosen direction and `DESIGN.md` always win over general taste.
