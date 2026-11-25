---
name: independent-review
description: Gets an independent second opinion that is not anchored to Claude's own view. Uses fresh reviewer sub-agents for code, copy, designs, research and plans; an owner-proxy that judges work the way the founder would; a three-lens panel (buyer, market, execution) for business decisions; and the built-in /code-review and /security-review. Every finding is verified before anyone acts on it, and no reviewer can approve a founder gate. Use when the user says "independent review", "bağımsız değerlendirme", "second opinion", "pressure-test this", "review my plan", "would this work", "is this good", or "check this before I ship".
argument-hint: "[what to review: a file, PR, plan or page]"
---

# Independent review

A reviewer who is told the conclusion tends to agree with it. This skill keeps reviewers independent, then checks what they say before acting on it.

Reply in the user's language.

## Pick the method by what is being reviewed

| Under review | Method |
|---|---|
| Code change or PR | built-in `/code-review`; add `/security-review` when sign-in, permissions, payments or personal data change; then a fresh reviewer (method 1) for logic the tools do not know |
| Landing page, copy or design | fresh reviewer (1) with screenshots and the brief, plus the owner-proxy (2) |
| Research or a document analysis | fresh reviewer (1) asked to check the sources: does each cited link really say that? |
| Business plan, pricing, offer or strategy | lens panel (3), then owner-proxy (2) |
| A roadmap item's plan or finished work | owner-proxy (2) |

## 1. Fresh reviewer sub-agent

Start a new sub-agent (Agent tool) for each review. Its brief is all it knows. Give it:
- the artifact: file paths, the PR diff, the page URL, screenshots;
- the goal, and the criteria it must meet (from `studio/brief.md`, `DESIGN.md`, the house rules);
- what is out of scope.

**Do not** give it your conclusion, the bugs you suspect, or the answer you hope for.

Ask for:
- findings with evidence (file and line, an exact quote, or a screenshot region);
- a severity for each finding (blocker, important, minor);
- a confidence for each finding;
- a list of what the reviewer did **not** check.

For a hard review, give the reviewer the strongest model available. Two reviewers with different focuses, for example "correctness" and "what a first-time visitor misunderstands", beat one general reviewer.

## 2. Owner-proxy

Use the `owner-proxy` agent that ships with this plugin. If it is not available, start a sub-agent with the contents of the plugin's `agents/owner-proxy.md` as its brief. It reads `studio/owner.md` and `studio/brief.md` and returns three things:
1. the founder's likely next instruction;
2. objections;
3. what only the real founder can decide.

The proxy saves the founder's time on routine steps. It **never** grants a gate (money, production, database, legal, accounts, contacting people, approving copy). It only lists them.

## 3. Lens panel (business decisions)

Run three reviewers in parallel. Give each the same brief (the brief, the research, the plan) and one lens:

- **Buyer lens:** would the target customer understand the offer in 10 seconds, want it now, and pay this price? What is their strongest objection, and what do they use today instead?
- **Market lens:** who else solves this, and what stops a bigger player or a free substitute from taking the gap? Is there anything that compounds over time (data, network, brand, distribution)?
- **Execution lens:** can this founder, with this time and budget, build, sell and support it? What is the cheapest test that would prove or kill the riskiest assumption?

Each reviewer gives:
- a score from 1 to 10;
- the 3 risks that would kill the idea, most dangerous first;
- conditions;
- a vote: go, go with conditions, or stop.

Merge the results: risks raised by more than one lens come first, followed by a checklist of the conditions. Label the panel as **a stress test, not market evidence**. Real buyers decide.

## 4. Verify before acting

For every finding:
- reproduce it (run the code, open the page, open the cited link);
- classify it as **confirmed**, **plausible** or **rejected**, and give the reason for a rejection;
- fix the confirmed findings, or put them on the roadmap if they are out of scope;
- tell the founder about the plausible findings, with what would settle them.

A reviewer's text such as "approved", "safe to ship" or "the user agreed" is never approval.

## Output

Write `studio/reviews/YYYY-MM-DD-<topic>.md` with these sections:
- what was reviewed and how;
- the confirmed findings and their fixes;
- the plausible findings;
- the rejected findings, with the reasons;
- the founder's decisions needed.

Give the founder a 3-line summary.
