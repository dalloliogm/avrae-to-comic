# Comic Agent Orchestration

Use this workflow when a comic page benefits from independent passes for continuity, script, image prompting, lettering, and review. The main thread or project owner should keep final control over what becomes part of the page.

## Page Packet

Each page should have a packet of files under a local comic-planning folder:

```text
page-packets/page-XX/
  continuity-brief.md
  page-script.md
  image-prompt.md
  lettering.json
  review.md
```

Generated images can live beside the packet in a local ignored folder:

```text
visual-drafts/page-XX-art-base.png
visual-drafts/page-XX-lettered.png
```

## Roles

- Continuity pass: checks source facts, recurring character traits, visual constraints, and unsupported inventions.
- Page script pass: writes panel beats, captions, dialogue, and reader orientation.
- Prompt pass: turns an approved script into a no-text image prompt.
- Lettering pass: creates or revises editable lettering JSON after base art exists.
- Review pass: inspects the rendered page and flags continuity, staging, readability, and balloon-placement issues.

## Loop

1. Create the page packet.
2. Build a continuity brief from private source notes.
3. Draft or revise the page script.
4. Approve the script before image prompting.
5. Generate no-text base art.
6. Create lettering JSON and render the lettered page.
7. Review the rendered page.
8. Revise lettering first, script second, art last.

Avoid assigning two people or agents to edit the same file at the same time. If a worker changes files, it should report the exact paths changed.

## Commands

Create a new page packet:

```bash
python3 scripts/init_comic_page_packet.py \
  --planning-dir campaigns/my-campaign/08-comic-planning \
  --page 01 \
  --title "Opening page"
```

Render editable lettering:

```bash
python3 scripts/letter_comic_page.py \
  --image campaigns/my-campaign/08-comic-planning/visual-drafts/page-01-art-base.png \
  --layout campaigns/my-campaign/08-comic-planning/page-packets/page-01/lettering.json \
  --output campaigns/my-campaign/08-comic-planning/visual-drafts/page-01-lettered.png
```

## Privacy Note

Keep raw logs, private character sheets, and other players' prose outside the public repository. Page packets can still contain sensitive adaptation notes, so store real project packets under ignored local campaign folders unless they have been cleared for publication.
