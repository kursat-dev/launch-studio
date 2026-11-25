# Launch Studio

**An honest marketing, research, design, SEO and review toolkit for founders building their product with [Claude Code](https://claude.com/claude-code).**

[Türkçe](README.tr.md)

Building a product alone with an AI agent works. Getting the agent to also do the marketing, competitor research, document analysis, site design, SEO and an independent review usually means typing the same long instructions again and again. Launch Studio packages those instructions as skills, with the rules that keep the output trustworthy built in:

- **Every fact has a source** (URL or file + page, and the access date). No source → "unknown", never a guess.
- **No fake proof.** No invented testimonials, user counts, logos or reviews.
- **Simulations are not evidence.** AI buyer panels are labelled as simulations.
- **The founder keeps the gates.** Money, production releases, accounts, legal texts, database changes and contacting real people need the founder's own words.

## What's inside

| Skill | What it does | Say something like |
|---|---|---|
| `studio-start` | Reads your project, asks at most 8 questions, writes the brief, your rules and approval gates, and recommends the next step | "set up the studio", "where do I begin" |
| `market-research` | Direct, indirect and substitute competitors: what they sell, prices, positioning, public customer complaints (all linked), a positioning map and the gap | "competitor analysis", "is this market crowded" |
| `doc-analysis` | PDFs, contracts, grant calls, spreadsheets, decks, transcripts, reference sites: a summary, a requirements checklist with page references, numbers, risks and open questions. Treats files as untrusted. | "analyse this PDF", "what does this require" |
| `marketing-strategy` | One segment, positioning, a one-line pitch, messages that answer real objections, 2–3 channels, a cheap demand test, a 30-day calendar, 10 hooks (drafts), budget, metrics | "marketing plan", "how do I get customers" |
| `site-design` | A brand brief and 2–3 rendered directions, **or** an exact rebuild of a reference template measured in a real browser; then `DESIGN.md`, tokens and the landing page, checked for contrast, focus and phone width | "landing page", "use this template", "redesign" |
| `seo-audit` | Technical SEO and content SEO, with a checker script that needs no dependencies; keywords from real data only | "SEO", "why can't Google find my site" |
| `independent-review` | Second opinions that are not anchored to Claude's own view: fresh reviewer sub-agents, an owner-proxy, a three-lens panel for business decisions, and `/code-review` + `/security-review`. Findings are verified before anyone acts on them. | "second opinion", "pressure-test this" |
| `roadmap-loop` | One numbered roadmap, one item at a time: plan → proxy review → build → verify with evidence → review → PR → report. It stops only at your gates, and works with `/loop`. | "what's next", "keep going on your own" |

Agent: **`owner-proxy`**, a read-only stand-in for the founder. It reviews plans the way you would and writes your likely next instruction, but it can never approve a gate.

Scripts (no API keys, no network except the URL you give):
- `seo-audit/scripts/seo_check.py`: on-page SEO check of a URL or a built HTML file (Python standard library only).
- `site-design/scripts/contrast.py`: WCAG contrast ratios for colour pairs (Python standard library only).
- `site-design/scripts/measure_reference.mjs`: measures a reference page's fonts, sizes, colours and sections at 1440 and 390 px (needs Playwright).

## Install

In Claude Code:

```
/plugin marketplace add kursat-dev/launch-studio
/plugin install launch-studio@launch-studio
```

Restart Claude Code if it asks you to. Then start with:

```
/launch-studio:studio-start
```

You can also just describe what you want ("do a competitor analysis for my app") and Claude picks the right skill.

**Manual install** (without the plugin system): copy the folders in `plugins/launch-studio/skills/` into `~/.claude/skills/` (or into `.claude/skills/` in one project), and copy `plugins/launch-studio/agents/owner-proxy.md` into `~/.claude/agents/`.

## How it fits together

```
studio-start ─► market-research ─► marketing-strategy ─► site-design ─► seo-audit
                     ▲                    │                   │              │
               doc-analysis               └──────── independent-review ◄─────┘
                                                        │
                                   roadmap-loop (build the product, item by item)
```

Everything is written to a `studio/` folder in your project (`brief.md`, `owner.md`, `decisions.md`, `sources.md`, `research/`, `marketing/`, `seo/`, `reviews/`), so every session starts from the same facts. You choose whether `studio/` is committed or kept private.

The skills reply in your language.

## Limits

- Research uses public sources only. It respects robots.txt and site terms, and never contacts anyone.
- Nothing here is legal, tax or financial advice. The skills flag what a professional should check.
- Simulated reviews and panels prepare you for real customers; they do not replace them.

## Contributing

Issues and pull requests are welcome. Keep the house rules intact: sourced facts, no fake proof, founder-owned gates.

## License

[MIT](LICENSE)
