# Avrae To Comic

Play-by-post Dungeons & Dragons games are tabletop RPG campaigns played through written messages instead of a live voice or in-person session. Players post character actions, dialogue, dice rolls, and combat commands over time, often in Discord servers that use Avrae to automate D&D mechanics.

This repository is a public toolkit for adapting Avrae-heavy play-by-post scenes into comic pages. It keeps raw source logs local while publishing selected summaries, scripts, lettering files, and generated comics.

Use it to organize and adapt:

- local-only raw Discord chat pasted from previous adventures
- selected public summaries, page scripts, comic plans, and lettering layouts
- local-only character sheets, private portraits, and visual continuity notes
- local-only Avrae aliases, snippets, embeds, command notes, rolls, and combat outcomes
- scene summaries written in your own words
- comic plans, page scripts, thumbnails, generated art, lettering JSON, and finished comic readers
- public examples from material that is safe to share, such as your own character-focused pages or appropriately licensed public datasets
- reusable prompts and templates for summarizing logs, catching up, drafting posts, and turning text into comic-book pages

One main purpose of this repository is to turn play-by-post campaign text into readable comics without publishing private table logs or other players' writing.

## What This Repo Contains

- campaign and scene templates for local private workspaces
- reusable prompts for summarizing logs and drafting posts
- reusable Codex skills for importing logs, summarizing Avrae combat, curating campaign memory, drafting character voice, analyzing character stats, and planning comics
- reusable agent prompts for continuity, scripting, image prompting, lettering, and review passes
- page-packet templates for comic adaptation
- simple scripts for page-packet setup and editable lettering
- workflow notes for turning text scenes into no-text art plus separate lettering
- public-safe example areas for cleared comic pages and public dataset experiments

## Campaigns

This public repo includes campaign folders for generated comic pages plus selected non-raw adaptation files. Raw Discord logs remain local.

- [The Gates](campaigns/the-gates/README.md): summaries, scripts, lettering JSON, generated pages, and thumbnails from the Weave Gate comic work.
- [Barovia](campaigns/barovia/README.md): summary, comic plan, and generated pages from Curse of Strahd / Watchful Star comic work.
- [FIREBALL](campaigns/fireball/README.md): generated comic experiments based on FIREBALL dataset scenes.
- [Tortugia](campaigns/tortugia/README.md): generated invitation page and Comic 00 planning materials from the Tortugia campaign.

Private campaign work can still live in ignored local folders such as `campaigns/<campaign>/` when it is not part of one of the public campaign sections. Those local folders can contain raw logs, private character notes, portraits, page packets, generated art, and finished local readers without being committed.

Public campaign-derived material should be limited to cleared adaptation outputs, for example:

- comics focused on your own characters
- rewritten summaries that do not quote other players' posts
- generated pages where private names, handles, channels, and unreleased table context have been removed
- material from public datasets, with license and attribution notes
- invitation or recap comics created through `scripts/generate_openrouter_image.py`

Public examples and generated campaign pages can live in:

```text
campaigns/the-gates/gates/weave-gate/
campaigns/barovia/
campaigns/fireball/
campaigns/tortugia/
examples/
public-comics/
datasets/fireball/
```

Suggested example categories:

| Example Type | Notes | Public Location |
| --- | --- | --- |
| The Gates comics | Summary, scripts, lettering JSON, generated pages, and thumbnails focused on the Weave Gate adaptation. | `campaigns/the-gates/gates/weave-gate/` |
| Barovia comics | Summary, plan, and generated pages from the Barovia / Curse of Strahd adaptation work. | `campaigns/barovia/` |
| FIREBALL adaptations | Summaries, plans, scripts, lettering JSON, and comic experiments based on the FIREBALL dataset, subject to dataset license and attribution requirements. | `campaigns/fireball/` |
| Character-focused comics | Additional generated pages centered on your own characters, with other players' contributions minimized or rewritten. | `public-comics/` |
| Workflow samples | Small fictional or synthetic examples that demonstrate page packets, image prompts, and lettering JSON. | `examples/workflow/` |

Keep raw campaign logs local even when summaries, scripts, lettering JSON, and final comic pages are public.

## Why Use This Repository For Play-By-Post Comics

This repository keeps the adaptation chain organized: source logs stay local, while selected summaries, page scripts, image prompts, editable lettering, and rendered pages can be shared.

The workflow is designed around a few practical rules:

- Preserve raw logs locally as source material, but do not publish them by default.
- Convert events into visual beats rather than transcript chunks.
- Generate no-text art first, then add captions, dialogue, balloons, and sound effects as editable lettering.
- Keep page text in JSON or another editable format so typos and placement can be fixed without regenerating art.
- Mark invented connective tissue as an adaptation choice when it is not explicit in the source.

For multi-pass page work, [comic-agent-orchestration.md](docs/comic-agent-orchestration.md) defines page packets, role prompts, and a review loop for continuity, scripting, prompting, lettering, and rendered-page review.

For keeping the private source repo and this public repo aligned, see [repo-workflow.md](docs/repo-workflow.md).

## Reusable Skills And Agents

This repo includes public-safe versions of the play-by-post Codex skills developed in the private source workspace:

- `pbp-log-importer`: preserve and organize raw Discord and Avrae logs before summarization.
- `avrae-combat-summarizer`: reconstruct combat-heavy logs into turn order, mechanics, and story consequences.
- `campaign-memory-curator`: extract durable facts into character, lore, quest, faction, item, and unresolved-thread notes.
- `character-voice-drafter`: draft Discord-ready in-character replies while respecting voice and table etiquette.
- `comic-adaptation-planner`: turn scenes into page scripts, panel beats, image prompts, lettering plans, and review notes.
- `character-stats-analyzer`: compute evidence-tagged character statistics from indexes, summaries, raw logs, and Avrae notes.

Codex skill files live under [.codex/skills/](.codex/skills/). The comic agent prompts are also available under [templates/agent-prompts/](templates/agent-prompts/) for users who want to copy them into page packets or run the workflow without Codex skill discovery.

Keep these workflow assets public-safe. They should describe processes, templates, and scripts, not private campaign source text.

## Privacy Model

Keep source campaign data local and out of git unless everyone involved has agreed that it can be published.

Do not commit:

- raw private Discord logs
- other players' prose or dialogue without permission
- private channels, server names, user IDs, or message IDs
- campaign-specific character sheets, portraits, lore, or spoiler notes that were not cleared for publication
- generated art based on private characters or scenes unless the final page has been reviewed for privacy

The default `.gitignore` blocks common local campaign-data folders while allowing explicit public areas for examples, generated comics, and public datasets.

## Folder Map

```text
campaign-template/       Copy this folder when starting a local campaign workspace.
campaigns/               Public campaign sections plus ignored raw-log paths.
campaigns/the-gates/     Public Gates summaries, scripts, lettering, and comic pages.
campaigns/barovia/       Public Barovia summary, plan, and comic pages.
campaigns/fireball/      Public FIREBALL summaries, scripts, lettering, and comic pages.
campaigns/tortugia/      Public Tortugia summaries, scripts, lettering, and comic pages.
examples/                Public-safe examples and workflow demos.
public-comics/           Cleared rendered comic pages and readers.
datasets/fireball/       FIREBALL-derived public material, with license notes.
prompts/                 Reusable prompts that work across campaigns.
templates/page-packet/   Comic page planning files.
templates/agent-prompts/ Optional role prompts for independent review passes.
.codex/skills/           Public-safe Codex skills for play-by-post workflows.
scripts/                 Packet setup, lettering, and utility scripts.
docs/                    Project-level workflow notes.
```

## Suggested Local Workflow

1. Copy `campaign-template/` into an ignored local folder such as `campaigns/my-campaign/`.
2. Keep raw pasted logs in that local campaign folder.
3. Summarize scenes into your own words before adapting them.
4. Create comic page packets with `scripts/init_comic_page_packet.py`.
5. Generate no-text art first.
6. Add captions, balloons, and sound effects using editable JSON and `scripts/letter_comic_page.py`.
7. Copy only cleared final outputs into `public-comics/` or `examples/`.

## Page Packet Example

```bash
python3 scripts/init_comic_page_packet.py \
  --planning-dir campaigns/my-campaign/08-comic-planning \
  --page 01 \
  --title "Opening page"
```

Render lettering over no-text art:

```bash
python3 scripts/letter_comic_page.py \
  --image campaigns/my-campaign/08-comic-planning/visual-drafts/page-01-art-base.png \
  --layout campaigns/my-campaign/08-comic-planning/page-packets/page-01/lettering.json \
  --output campaigns/my-campaign/08-comic-planning/visual-drafts/page-01-lettered.png
```

## Requirements

- Python 3.11 or newer
- Pillow for `letter_comic_page.py`

Install the package in editable mode:

```bash
python3 -m pip install -e .
```
