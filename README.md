# Avrae-to-Comic

This repository contains an agentic system to turn logs from play-by-post Dungeons & Dragons games into comic books.

Since COVID, in my spare time, I like to play this type of games, as a way to improve my storytelling and writing skills.

Thanks to the new AI technologies, I have converted some of my played sessions into comic books. The table below shows examples that I can share publicly.

This repository also includes AI skills and an agentic system for creating comics from your own adventures. Just load the repository into a local folder, open OpenAI Codex or similar tool, and ask it to guide you through the process. You will be able to copy&paste your sessions, and the system will automatically create markdown files for every relevant character, event, location, and so on. 

## Examples And Current Work In Progress

| Comic | Notes | Links |
| --- | --- | --- |
| Don Explodicus vs Dominion | Current The Gates comic work in progress, with generated reader pages, visual drafts, and multi-page scripts. | [comic](campaigns/the-gates/gates/weave-gate/08-comic-planning/comic-book.md) [visual draft](campaigns/the-gates/gates/weave-gate/08-comic-planning/visual-drafts/index.md) [script](campaigns/the-gates/gates/weave-gate/08-comic-planning/2026-03-10-weave-gate-origin-gem-dominion-comic-plan.md) |
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


