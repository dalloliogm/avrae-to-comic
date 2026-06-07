# Repository Instructions

This repository is the public publishing repo for Avrae-to-comic work. Its private source archive is the sibling repo:

```text
/Users/giovannidallolio/workspace/play-by-post-assistant  private source archive
/Users/giovannidallolio/workspace/avrae-to-comic          public publishing repo
```

## Default Workflow

Commit new campaign work to the private source repo first. Publish to this repo only after deciding which files are public-safe.

This repo may include:

- public scene summaries in `03-session-summaries/`
- comic plans and page scripts in `08-comic-planning/`
- lettering JSON in `08-comic-planning/` or subfolders
- generated comic images such as `.png`
- reusable templates, prompts, scripts, skills, agent prompts, and workflow docs

Do not commit raw or private source material:

- `00-inbox/`
- `02-chat-logs/`
- `07-private-notes/`
- Discord exports
- message IDs, server IDs, private channel names, or user IDs
- private character sheets or private portraits
- other players' unpublished prose unless it has been cleared for publication

## Public Campaign Folders

Current public campaign sections are:

- `campaigns/the-gates/gates/weave-gate/`
- `campaigns/barovia/`
- `campaigns/fireball/`

For The Gates, preserve the private repo convention: gate-specific work belongs under `campaigns/the-gates/gates/<gate-name>/`.

## Pre-Commit Check

Before committing or pushing, run:

```bash
git status --short
git diff --cached --name-only | rg '00-inbox|02-chat-logs|07-private-notes|\.DS_Store|\.Rhistory'
```

If the second command prints any paths, stop and unstage them before committing.

## README Links

When adding or moving public comic material, update the top-level `README.md` and the relevant campaign `README.md` so generated comics remain discoverable from the repository front page.

## Skills And Agentic System

This public repo should carry the reusable play-by-post skills and agent templates developed in the private source repo when they are workflow-level assets rather than campaign-private content.

- Keep public-safe skills under `.codex/skills/`.
- Keep reusable agent prompts under both `.codex/skills/<skill>/agents/` where the Codex skill expects them and `templates/agent-prompts/` where repo users can copy them without Codex.
- Do not include raw logs, private notes, private portraits, Discord IDs, or uncensored player prose inside public skills, templates, or examples.
- When syncing from the private repo, review staged paths before committing and confirm no `00-inbox/`, `02-chat-logs/`, or `07-private-notes/` files are included.
