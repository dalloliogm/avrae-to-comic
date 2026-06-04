# Private And Public Repo Workflow

Use two sibling folders:

```text
workspace/play-by-post-assistant/  private source archive
workspace/avrae-to-comic/          public publishing repo
```

Do not use the same folder for both repositories. One folder can only have one normal `.git` directory, and mixing a private archive with a public publishing repo makes accidental raw-log commits much more likely.

## What To Copy Publicly

Allowed public files:

- `03-session-summaries/*.md`
- `08-comic-planning/*.md`
- `08-comic-planning/*.json`
- `08-comic-planning/**/*.md`
- `08-comic-planning/**/*.json`
- generated comic images such as `.png`

Keep local only:

- `02-chat-logs/`
- Discord exports
- private character sheets
- private portraits
- private notes
- any file containing user IDs, message IDs, server names, private channels, or other players' unpublished prose that has not been cleared

## Commit Order

Use a private-first workflow:

1. Commit source work in `play-by-post-assistant`.
2. Copy the public-safe subset into `avrae-to-comic`.
3. Commit and push the public repo.

This keeps the private archive as the complete source of truth and the public repo as a curated publishing output.

You can skip the private commit only for purely public tooling changes that belong only in `avrae-to-comic`, such as README cleanup, templates, scripts, or docs that do not depend on private campaign files.

## Publish Loop

1. Work normally in `play-by-post-assistant`.
2. Decide which summaries, scripts, lettering files, and generated pages are public-safe.
3. Copy only those files into matching paths in `avrae-to-comic`.
4. Run `git status` in `avrae-to-comic`.
5. Confirm no `00-inbox/`, `02-chat-logs/`, or `07-private-notes/` files are listed.
6. Commit and push from `avrae-to-comic`.

The public repo's `.gitignore` allows the current public campaign sections while keeping raw-log paths ignored.

## Quick Safety Check

Before committing in `avrae-to-comic`, run:

```bash
git diff --cached --name-only | rg '00-inbox|02-chat-logs|07-private-notes|\.DS_Store|\.Rhistory'
```

If this prints anything, unstage those files before committing.
