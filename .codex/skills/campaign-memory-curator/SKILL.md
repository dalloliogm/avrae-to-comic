---
name: campaign-memory-curator
description: Curate durable campaign memory for Play-by-Post D&D workspaces. Use when Codex needs to extract, update, reconcile, or organize facts from chat logs, summaries, Avrae combat, character notes, imported ChatGPT summaries, or campaign documents into lore, NPC, quest, faction, item, character, timeline, and unresolved-thread notes.
---

# Campaign Memory Curator

## Workflow

1. Read the source material and identify whether it is raw log, summary, character note, Avrae output, or imported conversation note.
2. Preserve source facts and separate them from interpretation.
3. Update only durable memory: facts likely to matter later.
4. Place facts in the most specific existing file. Avoid duplicating the same fact across many files unless cross-linking is useful.
5. Record uncertainty, contradictions, and source gaps explicitly.

## What To Extract

- characters: goals, voice, relationships, decisions, injuries, resources, secrets known to the user
- NPCs: names, roles, factions, attitudes, last known status
- locations: descriptions, dangers, access, unresolved events
- quests: objective, stakes, current blocker, next lead
- items: owner, powers, costs, activation, Avrae mechanics
- factions: agenda, relationship to party, recent moves
- timeline: dates, scene order, cause-and-effect
- unresolved threads: mysteries, promises, threats, pending rolls, open choices

## What Not To Do

- Do not overwrite raw logs.
- Do not treat jokes or table chatter as canon unless they became in-fiction.
- Do not invent missing names, motives, outcomes, or rules.
- Do not expose private/spoiler notes in shareable summaries.
- Do not flatten uncertainty into false confidence.

## Update Style

Prefer concise entries with source pointers:

```markdown
- NPC Name: role/status. Last seen doing X in `02-chat-logs/YYYY-MM-DD-scene.md`. Uncertainty: ...
```

When a contradiction appears, keep both claims and mark the conflict:

```markdown
- Conflict: Log A implies X, but summary B says Y. Needs confirmation.
```

## Final Response

Report what changed, what files were updated, and any unresolved questions that would improve the memory.
