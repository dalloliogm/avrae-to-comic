# Play-by-Post Assistant

Play-by-post Dungeons & Dragons games are tabletop RPG campaigns played through written messages instead of a live voice or in-person session. Players post character actions, dialogue, dice rolls, and combat commands over time, often in Discord servers that use Avrae to automate D&D mechanics.

In my spare time, since COVID, I like to play these games. They are a way for me to keep my mind healthy, stay connected to collaborative storytelling, and practice writing skills.

With the advent of LLMs and diffusion models, I have become curious about automatically generating comic books from the textual chats of these games. This project is a local knowledge base and comic-generation workspace for Play-by-Post Dungeons & Dragons campaigns, and it contains AI skills for preserving logs, understanding Avrae-heavy scenes, and adapting those scenes into comics.

Use it to collect and adapt:

- raw Discord chat pasted from previous adventures
- character summaries, current sheets, portraits, and visual continuity notes
- Avrae aliases, snippets, embeds, command notes, rolls, and combat outcomes
- session or scene summaries
- campaign lore, NPCs, quests, factions, and unresolved threads
- comic plans, page scripts, thumbnails, generated art, lettering JSON, and finished comic readers
- reusable prompts and Codex skills for summarizing logs, catching up, drafting posts, and turning text into comic-book pages

One main purpose of this repository is to turn play-by-post campaign text into readable comics while preserving the original logs as source material.

## Campaigns

- [The Gates](campaigns/the-gates/campaign.md): a combat-focused Gates server where Defenders answer Gate-specific missions that prevent incursions from evil dimensions. Current comic work is focused on Don Explodicus's Weave Gate mission against Dominion.
- [Curse of Strahd](campaigns/curse-of-strahd/campaign.md): Barovia play-by-post threads involving Marcel, Seventius, Pyxis, Soren, Widget, Inge, and others, with active Watchful Star and aboleth ship-cove threads.
- [Tortugia](campaigns/tortugia/campaign.md): a long-running west-march-style demi-plane campaign centered on Rovers, monoliths, Princes, Wardens, shadowmists, and maritime dark fantasy.
- [FIREBALL Dataset](campaigns/fireball/campaign.md): an imported, anonymized corpus of Discord D&D/Avrae sessions from the FIREBALL dataset, used for analysis and comic-adaptation experiments rather than as a normal campaign.

## Examples And Current Work In Progress

| Comic | Notes | Links |
| --- | --- | --- |
| Don Explodicus vs Dominion | Current The Gates comic work in progress, with generated reader pages, visual drafts, and multi-page scripts. | [comic](campaigns/the-gates/gates/weave-gate/08-comic-planning/comic-book.md) [visual draft](campaigns/the-gates/gates/weave-gate/08-comic-planning/visual-drafts/index.md) [script](campaigns/the-gates/gates/weave-gate/08-comic-planning/2026-03-10-weave-gate-origin-gem-dominion-comic-plan.md) |
| The Watchful Star | Current Curse of Strahd comic work in progress, adapting Marcel and Pyxis's hilltop astronomy scene into generated reader pages. | [comic](campaigns/curse-of-strahd/08-comic-planning/comic-book.md) [visual drafts](campaigns/curse-of-strahd/08-comic-planning/visual-drafts/) [script](campaigns/curse-of-strahd/08-comic-planning/2026-05-05-watchful-star-part-01-comic-plan.md) |
| Return to Tortugia | Single-page invitation comic for former Tortugia players, using no-text generated art plus editable caption lettering. | [lettered page](campaigns/tortugia/08-comic-planning/visual-drafts/tortugia-return-invitation-page-lettered-v5.png) [base art](campaigns/tortugia/08-comic-planning/visual-drafts/tortugia-return-invitation-page-rough-thumbnail-v5.webp) [script](campaigns/tortugia/08-comic-planning/tortugia-return-invitation-page-script.md) |
| FIREBALL Stonefire vs Revenant | Experimental FIREBALL adaptation with a generated page and an eight-page script set. | [comic](campaigns/fireball/08-comic-planning/0149d30b-stonefire-revenant-comic-page-v2-lettered.png) [visual draft](campaigns/fireball/08-comic-planning/0149d30b-stonefire-revenant-comic-page-v2-art-base.png) [script](campaigns/fireball/08-comic-planning/0149d30b-stonefire-revenant-comic-plan.md) |
| FIREBALL Lythra vs Banjo Bear | Generated one-page comic from FIREBALL source material. | [comic](campaigns/fireball/08-comic-planning/0408134b-lythra-banjo-bear-page-01-lettered.png) [visual draft](campaigns/fireball/08-comic-planning/0408134b-lythra-banjo-bear-page-01-art-base.png) [script](campaigns/fireball/03-session-summaries/0408134bff023e90d26ceecd1c4669ef.md) |

## Why Use This Repository For Play-By-Post Comics

This repository keeps the whole adaptation chain in one place: source logs, cleaned summaries, campaign memory, page scripts, image prompts, base art, editable lettering, and rendered pages.

The custom skills in [.codex/skills/](.codex/skills/) support that workflow:

- `pbp-log-importer`: preserves and organizes raw Discord and Avrae logs before any summarization or adaptation.
- `avrae-combat-summarizer`: reconstructs combat-heavy logs into turn order, mechanical outcomes, and story consequences.
- `campaign-memory-curator`: extracts durable facts into character, lore, quest, faction, item, and unresolved-thread notes.
- `character-voice-drafter`: drafts Discord-ready in-character replies while respecting character voice and table etiquette.
- `comic-adaptation-planner`: turns play-by-post scenes into panel beats, page layouts, captions, dialogue, visual continuity notes, and image-generation prompts.
- `character-stats-analyzer`: computes evidence-tagged character statistics from campaign indexes, summaries, raw logs, and Avrae notes.

For multi-agent page work, [comic-agent-orchestration.md](docs/comic-agent-orchestration.md) defines page packets, role prompts, and the main-thread orchestration workflow for continuity, scripting, prompting, lettering, and review.

Public-safe versions of the reusable skills and agentic comic workflow should also be kept in the sibling public repository, `avrae-to-comic`, so the workflow can be shared without raw logs, private notes, private portraits, or uncensored table material.

## Comic Generation Workflow

Comic pages are built in stages:

1. Write a page script and visual continuity notes.
2. Generate no-text base art with `scripts/generate_openrouter_image.py`.
3. Pass only relevant approved visual references with repeated `--reference-image` arguments when portraits, setting art, or selected prior pages should guide the generation.
4. Inspect the generated image for panel readability, unwanted text, face/prop clarity, and caption space.
5. Add final text with `scripts/letter_comic_page.py` and an editable JSON layout.
6. Rerender lettering after moving caption boxes; regenerate art only when the composition itself needs to change.

## Folder Map

```text
campaigns/
  _template/              Copy this folder when starting a new campaign.
    00-inbox/             Temporary holding area for unsorted pasted material.
    01-characters/        PC and NPC notes for this campaign.
    02-chat-logs/         Raw Discord / Avrae chat logs, kept as source material.
    03-session-summaries/ Clean summaries by session, scene, or date.
    04-lore/              Places, factions, NPCs, quests, items, clues.
    05-avrae/             Campaign-specific Avrae commands, aliases, snippets.
    06-prompts/           Campaign-specific assistant prompts.
    07-private-notes/     Spoilers, DM-only notes, or things not for sharing.
    08-comic-planning/    Comic plans, page scripts, thumbnails, lettering JSON.
characters/              Cross-campaign character profiles.
prompts/                 Reusable prompts that work across campaigns.
scripts/                 Import, lettering, packet setup, and utility scripts.
docs/                    Project-level notes, workflows, and imported summaries.
.codex/skills/           Custom Codex skills for this play-by-post workspace.
archive/                 Retired campaigns or old imports.
```
