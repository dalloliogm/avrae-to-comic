---
name: avrae-combat-summarizer
description: Summarize and explain Avrae combat logs from Play-by-Post D&D games. Use when Codex is given Avrae initiative output, attack rolls, saves, spell casts, damage, conditions, concentration checks, combat commands, or crowded Discord combat transcripts and needs to reconstruct turn order, key mechanical events, tactical state, and story consequences.
---

# Avrae Combat Summarizer

## Workflow

1. Preserve the original log or point to its source before summarizing.
2. Reconstruct combat in chronological order; keep initiative order separate from event order when both matter.
3. Extract only mechanics supported by the log. Do not infer hidden DCs, monster stats, or intentions unless stated.
4. Translate mechanics into story consequences for play-by-post continuity.
5. End with what a player likely needs next: current threats, conditions, resources, and possible next actions.

## Extract

Capture:

- round and turn markers
- actor names and targets
- attacks, hits, misses, crits, damage, healing
- saves, checks, DCs if visible
- spells, concentration, spell slots, durations
- conditions, resistances, immunities, advantage/disadvantage
- initiative changes, deaths, unconsciousness, summons, lair effects
- Avrae snippets, aliases, counters, and custom automation that affect the outcome

## Summary Format

Use this shape unless the user asks otherwise:

```markdown
## Combat State

- Round / turn:
- Active combatants:
- Downed or removed:
- Conditions:
- Concentration:

## Timeline

- ...

## Key Mechanical Outcomes

- ...

## Story Consequences

- ...

## What Matters For The Next Post

- ...

## Uncertainties

- ...
```

## Guardrails

- Distinguish Avrae output from player narration.
- Preserve exact roll totals when they matter.
- Mark "unclear from log" instead of filling gaps.
- Do not tell the user what their character must do; offer tactical options.
