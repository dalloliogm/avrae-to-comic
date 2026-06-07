---
name: character-stats-analyzer
description: Compute evidence-tagged statistics for Play-by-Post D&D characters from campaign indexes, Markdown summaries, raw Discord logs, and Avrae-heavy combat notes. Use when the user asks for character mission counts, gates visited, allies or opponents, spell usage, Fireball counts, action/cast totals, or a reusable stats report for a character such as Don Explodicus.
---

# Character Stats Analyzer

## Workflow

1. Identify the character name, aliases, campaign folder, mission index, and desired output format.
2. Prefer campaign indexes for mission lists, summaries for scene context, and raw logs for exact spell/action evidence.
   For The Gates campaign, spell usage is usually in structured message footers, not free prose.
3. Generate per-mission stats sidecars first, then aggregate those sidecars into the campaign-level report.
   This makes each mission auditable and keeps mixed/archive issues localized.
4. Keep counts evidence-tagged rather than pretending ambiguous logs are precise.
5. Use the bundled helper when scanning a local Markdown campaign workspace:

```bash
python3 .codex/skills/character-stats-analyzer/scripts/character_stats.py \
  --workspace /path/to/workspace \
  --campaign campaigns/the-gates \
  --character "Don Explodicus" \
  --alias Don \
  --alias Donthrakis \
  --alias Dan \
  --alias Simulacrus \
  --speaker "Giovanni D" \
  --mission-index campaigns/the-gates/00-inbox/2026-05-15-don-explodicus-missions-import-index.md \
  --output campaigns/the-gates/don-explodicus-stats.md
```

6. After generation, spot-check high-interest counts against the cited source lines before presenting the report.

## Evidence Policy

- `confirmed`: exact action/cast/precast/reaction footer line tied to the target character or their message speaker.
- `probable`: prose clearly says the target character cast or used a spell/action, but lacks strict action syntax; do not use this for The Gates spell totals when action footers are available.
- `uncertain`: mixed exports, duplicate archive material, simulacrum/clone ambiguity, unclear actor, or parent archive rows with split child segments.

When duplicate or mixed archives have split segment files, prefer the split segment summaries/logs over the parent archive for detailed counts. Keep parent archive rows in mission totals, but mark their detailed spell/action counts as uncertain unless no split exists.

## Per-Mission Sidecars

For campaign-scale stats, write one sidecar per mission row before writing the aggregate report:

- Path pattern: `campaigns/<campaign>/gates/<gate>/06-stats/<mission-summary-stem>-<character-slug>-stats.md`.
- Each sidecar should include mission metadata, linked summaries/raw logs, spell/action counts, evidence rows, co-appearances, and local notes.
- If a mission summary declares split segments, scan those split summaries/logs for that mission sidecar instead of scanning the parent mixed archive directly.
- The campaign-level report should link to every sidecar in the mission list and aggregate totals from the same per-mission records used to write the sidecars.

## What To Count

- Mission rows by gate, source block, status, date span, and linked summary.
- Gates visited and complete vs mixed/in-progress rows.
- Spell/action mentions from raw log footer lines starting with `A`, `Action`, `BA`, `Bonus Action`, `R`, `Reaction`, `Precast`, `Perpetual Cast`, `Wish Perpetual Cast`, `Perpetual Wish Cast`, `Wish Perpetual`, or `Perpetual Wish`.
- Treat exact actor-block headings such as `Don`, `Dan`, or `Simulacrus` as ownership for the following structured footer lines.
- For Crown of Stars, Dawn, and Bigby's Hand / Arcane Hand, split initial action/precasts from later bonus-action uses.
- Normalize Telekinetic, Telekinetic Shove, and bare bonus-action shove footer lines into `Telekinetic Shove`.
- Fireball-specific evidence with source links.
- Frequent allies/opponents when extractable from summaries, character files, or strongly named log lines.

Do not count every casual mention of a spell as a cast. Merge a character's simulacrum only when the user explicitly asks for it or provides the simulacrum name as an alias.

## Report Shape

Prefer a Markdown report with:

- generated timestamp and source scope
- mission list first, sorted oldest-to-newest, with `Mission #` as the chronological row index
  and a link to the per-mission stats sidecar
- top spell/action counts with confirmed/probable/uncertain columns
- frequent named co-appearances
- summary metrics and missions by gate/status
- Fireball evidence table
- notes on mixed exports, duplicates, aliases, and assumptions

Keep raw logs separate from reports. Reports are derived artifacts and should cite source paths so the user can audit funny-looking numbers.
