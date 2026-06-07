---
name: pbp-log-importer
description: Import and organize Play-by-Post Discord and Avrae logs into a campaign workspace. Use when Codex is given pasted chat, Discord exports, Avrae output, mixed IC/OOC text, or raw campaign logs and needs to classify, preserve, summarize, and place them into folders such as 00-inbox, 02-chat-logs, 03-session-summaries, 05-avrae, character notes, or lore notes.
---

# PbP Log Importer

## Workflow

1. Identify the campaign, channel, approximate date, scene name, and whether the material is raw chat, a cleaned summary, Avrae output, OOC discussion, or mixed material.
2. Preserve raw logs with minimal edits. Do not rewrite source chat except to remove clearly unrelated or explicitly unwanted material.
3. Put unsorted or ambiguous material in `00-inbox/`; put source chat in `02-chat-logs/`; put cleaned summaries in `03-session-summaries/`.
4. Extract durable facts into the appropriate campaign files only after preserving the raw source.
5. Mark uncertainty instead of inventing missing continuity.

## Classification

- **IC roleplay**: dialogue, actions, narration, scene descriptions.
- **OOC**: scheduling, rules discussion, table talk, jokes outside the fiction.
- **Avrae mechanics**: commands, rolls, attacks, saves, spell casts, initiative, conditions, damage, counters.
- **Memory-worthy facts**: NPC names, locations, quests, items, faction moves, character decisions, unresolved threads.

If IC, OOC, and Avrae are interleaved, keep the original order in the raw log and separate only in the derived summary.

## File Placement

Use the repo's existing campaign structure when present:

```text
campaigns/<campaign>/00-inbox/
campaigns/<campaign>/02-chat-logs/
campaigns/<campaign>/03-session-summaries/
campaigns/<campaign>/04-lore/
campaigns/<campaign>/05-avrae/
```

Prefer dated filenames:

```text
YYYY-MM-DD-channel-or-scene.md
```

If the campaign folder does not exist, create it from `campaigns/_template` when available. If the campaign name is unclear, use `00-inbox/` and ask only if placement would be risky.

## Output Shape

When importing, produce or update:

- a raw log file, with source/date/channel metadata at the top when known
- a short summary file for the scene/session when enough context exists
- a brief import note listing extracted characters, locations, Avrae events, and unresolved questions

Do not discard raw material after summarizing.
