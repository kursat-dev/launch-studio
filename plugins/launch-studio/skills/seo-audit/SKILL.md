---
name: seo-audit
description: Audits and fixes a site's search visibility. Checks indexability, canonicals and redirects, titles and descriptions, headings, sitemap and robots.txt, structured data, share cards, language tags, page speed and the pitfalls of JavaScript-rendered pages. Then plans keywords from real data (never invented search volumes) and pages that answer real questions. Includes a checker script with no dependencies. Use when the user says "SEO", "arama motoru", "why can't Google find my site", "meta tags", "sitemap", "rank on Google", "Search Console", "Open Graph", or "share preview".
argument-hint: "[URL or built HTML file]"
---

# SEO audit

The goal is that search engines can find, understand and show the site, and that each public page answers a question real people search for. Honest SEO only: no keyword stuffing, no mass-produced thin pages, no fake reviews in structured data.

Reply in the user's language.

## 1. Run the checker

```bash
python3 <this skill's folder>/scripts/seo_check.py https://the-site.com/
python3 <this skill's folder>/scripts/seo_check.py dist/index.html   # a built page, before deploy
```

Run it on the home page and on each important public page. It reports title, description, canonical, robots and noindex, lang, h1, Open Graph and Twitter tags, JSON-LD, hreflang, missing alt text, JavaScript-only content, robots.txt and the sitemap.

## 2. Technical checklist

Go through every item, and record the evidence for each.

**Can it be indexed?**
- The page returns HTTP 200; moved pages use 301 redirects; there are no redirect chains.
- One host only: `www` or the bare domain, `https`, with the other forms redirecting to it.
- `robots.txt` does not block the public site and lists the sitemap.
- Staging and preview sites are **not** indexable: they use noindex or password protection. Production pages do **not** use noindex.
- `sitemap.xml` lists only canonical, indexable 200 URLs.

**Does it read well to a search engine?**
- A unique `<title>` of about 50–60 characters, with the main topic first and the brand last.
- A unique meta description of about 150–160 characters, written as an honest promise of the page.
- Exactly one `<h1>`, and headings in order.
- `<html lang>` matches the language. With several languages, add `hreflang` alternates, including `x-default`.
- An absolute `rel=canonical` on every page.
- Readable URLs in the site's language, lowercase, words joined by hyphens.

**Pages built by JavaScript (single-page apps such as React or Vue):**
- If the HTML has almost no text before JavaScript runs, search engines and link previews may see an empty page. Pre-render or server-render the public pages (landing, pricing, FAQ, blog).
- Title, meta and Open Graph tags must be in the initial HTML, not only set later by JavaScript.

**Share preview:**
- `og:title`, `og:description`, `og:url` and `og:image`, where the image is 1200 × 630 and has an absolute URL.
- `twitter:card` set to `summary_large_image`.
- Test with each platform's own preview or debugger tool.

**Structured data (JSON-LD):**
- `Organization` (name, url, logo, sameAs for the real social profiles), `WebSite`, and `SoftwareApplication` or `Product` where it fits.
- `FAQPage` only when the FAQ is visible on the page.
- Never add ratings or reviews that do not exist.
- Validate with Google's Rich Results Test.

**Speed and mobile (Core Web Vitals):**
- LCP under 2.5 s, INP under 200 ms, CLS under 0.1. Measure with PageSpeed Insights or Lighthouse.
- Size and compress the hero image, add `width` and `height` to images, lazy-load images below the fold, and use `font-display: swap`.

**Hygiene:**
- A real 404 page that returns HTTP 404, a favicon, alt text on content images, and no broken internal links.

## 3. Content and keywords

- **Use real demand data only:** Google Search Console queries (once the site is live), autocomplete and "People also ask" suggestions, questions from the market research, competitors' pages, and the free Keyword Planner. Never invent search volumes; write "volume unknown" where you have none.
- **Map keywords to pages:** one main search intent per page. Write the table with the columns page, main query, related questions and the evidence for the demand.
- **Write for the reader:** answer the question in the first paragraph, use the customer's own words, and show who is behind the site with a real founder or about page.
- **Plan the first 5–10 pages or posts** from the questions buyers really ask, and link them to each other and to the product.
- **Local market:** search in the local language. If the business is local, set up a business profile (the founder does this in their own account).

## 4. Accounts (the founder's gate)

Google Search Console, Bing Webmaster Tools and any analytics live in the founder's own accounts. Write the exact click path:
1. add the property;
2. verify it with a DNS record or an HTML tag;
3. submit the sitemap.

Then wait for the founder to confirm. Analytics needs a privacy notice, and consent where the law requires it.

## Output

`studio/seo/audit-YYYY-MM-DD.md` with:
1. a summary of the top 5 fixes;
2. the findings, most severe first, each with the evidence, the fix and the effort;
3. the keyword-to-page table;
4. the content plan.

After fixing, run the checker again and record the before and after counts of errors and warnings.
