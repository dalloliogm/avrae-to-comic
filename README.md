# Avrae To Comic

Utilities and templates for adapting Discord play-by-post Dungeons & Dragons scenes, especially Avrae-heavy logs, into comic planning artifacts.

This public repository is intentionally content-light. It is meant to hold reusable workflow material, not private campaign logs or other players' writing.

## What This Repo Contains

- campaign and scene templates
- reusable prompts for summarizing logs and drafting posts
- page-packet templates for comic adaptation
- simple scripts for page-packet setup and editable lettering
- workflow notes for turning text scenes into no-text art plus separate lettering

## Privacy Model

Keep source campaign data local and out of git unless everyone involved has agreed that it can be published.

Do not commit:

- raw Discord logs
- other players' prose or dialogue
- private channels, server names, user IDs, or message IDs
- generated art based on private characters or scenes
- campaign-specific character sheets, portraits, lore, or spoiler notes

The default `.gitignore` blocks common local campaign-data folders so this repository can stay public while your source material stays private.

## Suggested Local Workflow

1. Copy `campaign-template/` into a local ignored folder such as `campaigns/my-campaign/`.
2. Keep raw pasted logs in that local campaign folder.
3. Summarize scenes into your own words before adapting them.
4. Create comic page packets with `scripts/init_comic_page_packet.py`.
5. Generate no-text art first.
6. Add captions, balloons, and sound effects using editable JSON and `scripts/letter_comic_page.py`.

## Repository Layout

```text
campaign-template/       Local campaign folder template.
prompts/                 Reusable prompt snippets.
templates/page-packet/   Comic page planning files.
templates/agent-prompts/ Optional role prompts for independent review passes.
scripts/                 Small utilities for packet setup and lettering.
docs/                    Workflow notes.
```

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
