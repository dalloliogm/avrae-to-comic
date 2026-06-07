---
name: comic-adaptation-planner
description: Adapt Play-by-Post D&D scenes into comic-book planning artifacts. Use when Codex needs to turn Discord logs, campaign summaries, Avrae combat, character descriptions, or fantasy scenes into panel beats, page layouts, captions, dialogue bubbles, visual references, continuity notes, or image-generation prompts while preserving story logic and character voice.
---

# Comic Adaptation Planner

## Workflow

1. Identify the scene's dramatic question, emotional turn, and required continuity.
2. Separate narration, dialogue, mechanics, and OOC chatter.
3. Choose the adaptation unit: strip, single page, multi-page scene, splash panel, or character moment.
4. Convert events into visual beats, not transcript chunks.
5. Plan rough pages before polished art.
6. Establish reader context before the climax or action beat.
7. Preserve character agency and avoid adding unsupported outcomes.

## Reader Orientation

Before scripting or generating a page, make the scene legible to someone who has not read the source log. Add a short orientation block to the plan or page script that answers:

- who the visible characters are
- what each character wants in this scene
- where the scene is taking place
- where the characters came from, if the page depends on that context
- what danger, mystery, or unresolved relationship the reader needs to understand

For a first comic page or standalone image, include this context visually or in editable captions before the main action. Do not open only on a dramatic pose unless the reader can infer who is present and why it matters.

Use recap captions sparingly, but prefer one or two clear setup captions over an unexplained action page. Good first-page captions identify the source situation, not the mechanics behind it.

## Panel Planning

For each panel, specify:

- panel size or emphasis
- visible characters
- action or pose
- setting and atmosphere
- caption text, if any
- dialogue or sound effects
- continuity notes from the log

Prefer fewer, stronger panels over mechanically representing every roll.

## First-Pass Page Workflow

For comic-book pages, use a staged workflow:

1. Write or update the page script first.
2. Generate rough thumbnail art with no text.
3. Add captions, dialogue, balloons, and SFX afterward as editable lettering.
4. Iterate text and placement without regenerating the art.
5. Regenerate art only when staging, character design, or composition needs to change.

When generating rough thumbnails, prompt for:

- rough storyboard, manga thumbnail, or indie comic layout sketch
- simple silhouettes and readable staging
- minimal detail and no polished rendering
- no text, captions, speech bubbles, SFX, placeholder text boxes, or blank label boxes
- natural negative space where lettering can be added later

Use polished rendering only after the page sequence works in rough form.

## Default Image Generation Route

When this skill needs to generate comic art, rough thumbnails, visual drafts, or no-text base art in this repository, use the OpenRouter helper script by default instead of Codex/ChatGPT's built-in image generation tool.

Use the built-in image generation tool only when the user explicitly asks for ChatGPT image generation, Codex image generation, `imagegen`, DALL-E/GPT Image, or otherwise clearly asks for the built-in image tool.

Default command shape:

```bash
uv run scripts/generate_openrouter_image.py \
  --prompt-file path/to/image-prompt.md \
  --reference-image path/to/character-or-setting-reference.webp \
  --output-dir campaigns/<campaign>/gates/<gate-name>/08-comic-planning/visual-drafts \
  --filename-stem page-XX-rough-thumbnail \
  --aspect-ratio 2:3 \
  --image-size 1K
```

For campaigns that do not use Gate folders, adapt the output directory to the campaign's `08-comic-planning/visual-drafts/` folder.

The script defaults to `sourceful/riverflow-v2.5-pro:free` and reads `OPENROUTER_API_KEY_AVRAE2COMIC` at runtime. Do not print, inspect, or expose the API key. Use `--dry-run` when checking payloads without consuming OpenRouter quota; dry-run output redacts reference-image base64 data.

When relevant visual references already exist, pass them explicitly with repeated `--reference-image` arguments. Prefer:

- character portraits from `01-characters/portraits/`
- selected no-text base art from earlier pages
- approved setting or location references
- prior visual drafts only when they are good enough to preserve

Do not pass every available image automatically. Choose only references that matter for the requested panel or page, and describe in `image-prompt.md` which character or location each reference is meant to constrain.

If a user supplies reference images from outside the repository, use them as references without copying them into the repo unless they should become durable campaign assets. Do not expose private source paths in public-ready artifacts.

Choose output names that preserve the existing workflow:

- `page-XX-rough-thumbnail.png` for first-pass exploratory drafts
- `page-XX-art-base.png` for selected no-text base art
- `page-XX-openrouter-draft.png` for model-specific experiments

After generation, inspect the saved image before lettering. If the image response fails or the OpenRouter model is unavailable, report that failure and ask whether to switch models or use the built-in image generator; do not silently fall back to ChatGPT image generation.

## Independent Agent Orchestration

When the user asks to use independent agents, keep the main thread as the orchestrator. The orchestrator owns final decisions, image generation, file integration, commits, and pushes. Worker agents should produce bounded artifacts and should not make broad comic decisions.

Use a page packet under the mission comic-planning folder:

```text
page-packets/page-XX/
  continuity-brief.md
  page-script.md
  image-prompt.md
  lettering.json
  review.md
```

Create page packets with:

```bash
python3 scripts/init_comic_page_packet.py \
  --planning-dir campaigns/<campaign>/gates/<gate-name>/08-comic-planning \
  --page XX \
  --title "Short page goal"
```

Agent role prompts live in `templates/agent-prompts/` next to this skill. Use them to spawn narrowly scoped workers:

- continuity agent edits only `continuity-brief.md`
- page script agent edits only `page-script.md`
- prompt agent edits only `image-prompt.md`
- lettering agent edits only `lettering.json`
- reviewer agent edits only `review.md`

Use cheaper models for disposable first drafts of scripts, prompts, and lettering layouts. Use a stronger model for continuity review, final dialogue and caption judgment, and deciding whether a page needs art regeneration. Do not assign two agents to edit the same file at once.

## First-Version Visual Style

For first visual versions, default to a stylized limited-palette comic treatment rather than fully rendered dark fantasy painting. Prompt for:

- 2 to 4 dominant colors plus black and off-white
- strong ink shapes, clear silhouettes, and graphic shadows
- flat or lightly textured color blocks
- restrained highlights reserved for story signals such as fire, magic, eyes, blood, or a key prop
- readable staging over surface detail

Avoid first drafts that look like polished concept art, fully painted splash art, or color-heavy cinematic rendering. Save high-render polish for later passes after the page's context, composition, and sequence are working.

## Lettering Workflow

Do not rely on image generation for final text. Generated text is hard to revise and often misaligns or misspells.

Keep page text in a separate editable layout file, such as JSON, and render it over the no-text art. In this repo, prefer:

```bash
python3 scripts/letter_comic_page.py \
  --image path/to/page-art-base.png \
  --layout path/to/page-lettering.json \
  --output path/to/page-lettered.png
```

Use this workflow for:

- changing caption wording
- moving balloons between panels
- removing captions or dialogue
- fixing typos without regenerating art
- keeping a clean base-art file for later relayout

Save generated visual drafts under the relevant mission's comic-planning folder, usually:

```text
campaigns/<campaign>/gates/<gate-name>/08-comic-planning/visual-drafts/
```

Prefer these names:

- `page-XX-art-base.png` for no-text art
- `page-XX-lettering.json` for editable text placement
- `page-XX-lettered.png` for rendered output
- `page-XX-rough-thumbnail.png` for exploratory one-off drafts

## Default Lettering Style

Use this balloon and caption treatment for comic pages unless the user asks for a different house style:

- small readable sans-serif lettering, roughly 21-22 px on 1024 x 1536 pages
- light cream-gray balloon and caption backgrounds, not pure white
- thin dark brown or near-black outlines, about 2 px
- modest corner radii: captions slightly rounded, speech balloons more rounded
- compact padding so balloons do not dominate the art
- no all-caps dialogue in speech balloons unless the character is shouting or the source calls for it
- captions may use all caps when they are short narration boxes
- SFX can be unboxed, small, and tinted warm gold or another scene-appropriate accent

Place lettering after checking the actual generated image. Avoid covering faces, hands performing key actions, important props, spell effects, or panel focal points. Prefer open sky, empty ground, cloak areas, or background architecture for captions. If a caption or balloon covers a character's face or weakens the panel read, regenerate only the lettered output from the no-text art; do not regenerate the art.

When a page has regular panel bands, align captions inside the intended panel rather than on gutters or borders. For revision requests about lettering placement, update the JSON layout and rerender the lettered page; keep the no-text base art unchanged.

## Output Shapes

For a quick adaptation:

```markdown
## Reader Orientation

- Characters: ...
- Scene context: ...
- Stakes: ...
- Required prior knowledge: ...

## Adaptation Approach

...

## Panel Beats

1. ...
2. ...
3. ...

## Dialogue And Captions

- ...

## Visual Continuity Notes

- ...
```

For image generation or artist briefs, add:

```markdown
## Character Visual References

- ...

## First-Version Style

- Limited palette: ...
- Graphic treatment: ...
- No-text art constraints: ...

## Prompt Drafts

- ...
```

## Style Guidance

- Treat Avrae rolls as invisible causes unless the story needs a visible magic or combat beat.
- Use cinematic fantasy staging with clear silhouettes and readable action.
- Keep jokes visually timed: setup, reaction, release.
- Keep dialogue shorter than prose; let posture, expression, and composition carry meaning.
- Mark invented connective tissue as an adaptation choice when it is not explicit in the source.
- Use recap captions when a page needs to orient a reader who has not read the campaign log.
- Give each caption a distinct job: setting, crisis, problem, character turn, or hook.
- Avoid repeating the same idea across adjacent captions.
- For first versions, bias toward stylized, limited-color pages until the storytelling is clear.

## Visual Continuity

Before generating art, collect available portraits and text references. For each recurring character, name the traits that must remain stable across panels.

Examples of useful continuity constraints:

- "Dan is an icy orc simulacrum of Don, not a human ice mage."
- "Dominion's antimagic suppresses others' magic, but its own flames and aura continue."
- "If a spell effect is suppressed, show the visible consequence: vanishing summons, failed wards, dimmed weapons, or empty space where a magical creature stood."

Correct character continuity in the script and prompt before regenerating art. If only the text is wrong, update lettering instead of regenerating the image.
