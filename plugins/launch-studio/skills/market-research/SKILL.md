---
name: market-research
description: Competitor and market research from public sources. Finds the direct competitors, the indirect ones and the substitutes, and records what each sells, at what price, how it positions itself and what its customers complain about, every fact with a link and an access date. Then draws a positioning map and names the gap the product can own. Use when the user says "competitor analysis", "rakip analizi", "who are my competitors", "is this market crowded", "market research", "find the gap", or "how big is the market".
argument-hint: "[market or competitor names, optional]"
---

# Market research

The goal is a competitor map the founder can trust and act on. Accuracy beats volume: 8 well-sourced competitors are worth more than 30 guesses.

Reply in the user's language.

## Inputs

- `studio/brief.md`. If it is missing, run `studio-start`, or ask the three essentials: the product, the buyer, and the market or country.
- Names the founder already knows. Ask once: "Which competitors or alternatives do your customers mention?"

## 1. Define the job

Write one line: "When <buyer> wants to <job>, they currently use …". A competitor is anything that does that job, not only a product that looks similar.

## 2. Find candidates

Aim for 8–15 candidates that cover all three kinds:
- **Direct:** the same job for the same buyer, with a similar product.
- **Indirect:** the same job done another way, such as an agency, a consultant, a course, a marketplace or a general AI assistant.
- **Substitutes:** a spreadsheet, a template, a free government or non-profit resource, or doing nothing.

Search in the market's own language as well as in English, because local players often show up only in local-language searches. Use WebSearch and WebFetch when they are available. Without them, ask the user to paste the pages and record the gap.

## 3. Profile each competitor

Record only what you can link:

| Field | Rule |
|---|---|
| What they sell | their own words, quoted, with the link |
| Price | the exact public price, the currency and the date seen; "not public" when hidden |
| Who it is for | from their site or pricing page |
| Positioning claim | their headline, quoted word for word |
| Channels | where they visibly win customers: ad libraries, social, search, partners |
| Customer complaints | quotes from public reviews (app stores, review sites, forums, Reddit, local communities) with links; at least 2 for each major competitor where they exist |
| Strength to respect | what they clearly do well |

Add every fact to `studio/sources.md` as `S<n> | URL | accessed YYYY-MM-DD | supports: …` and cite it inline as `[S<n>]`.

Label each statement as one of:
- **fact**: sourced;
- **inference**: your reasoning from facts, and say so;
- **assumption**: still needs checking.

Boundaries: public pages only. No logins, no scraping behind paywalls, and respect robots.txt and each site's terms. Never contact competitors or their customers.

## 4. Positioning map

Pick two axes that buyers actually care about. Take them from the complaints and claims you found, for example price against hands-on help, or speed against depth. Place each competitor with a one-line reason, and draw the map as a text grid or a Mermaid quadrant chart.

## 5. The gap and the threats

- **The gap:** one paragraph on the unmet need the product can own, backed by complaint quotes.
- **Why the gap might be empty:** perhaps nobody pays for it. Say so when the evidence is thin.
- **What would make us lose:** 3–5 concrete threats, for example a big player adding the feature, or the free substitute being good enough.
- **Open questions for the founder:** add them to `studio/decisions.md`.

## 6. Market size (only if asked or needed)

Size the market bottom-up from sourced inputs only: the number of reachable buyers [S] × the share you could plausibly win × the price. Show the arithmetic and label every input. Never quote a "the global market is worth $X billion" figure without naming the report it comes from and saying what the figure does and does not measure.

## Output

Write `studio/research/competitors.md` with these sections:
1. Summary in 5 lines: crowded or not, the gap, the biggest threat, and your confidence.
2. The competitor table.
3. The profiles.
4. The positioning map.
5. The gap, the threats and the open questions.
6. The research date and a "refresh by" date 3 months later.

Finish by telling the founder the 3 findings that matter most, and suggest `marketing-strategy` next.
