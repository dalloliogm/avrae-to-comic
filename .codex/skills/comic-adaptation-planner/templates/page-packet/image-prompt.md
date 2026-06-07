# Page {{PAGE}} Image Prompt

## Page Goal

{{TITLE}}

## No-Text Constraint

No text, no captions, no speech bubbles, no SFX, no placeholder text boxes, no labels, no readable writing.

## Style

First-pass comic page, simple limited-palette illustration, strong ink shapes, readable silhouettes, flat or lightly textured color blocks, clear panel staging.

## Page Layout

- Panel count:
- Panel emphasis:
- Negative space for later lettering:

## Character Constraints

- Don Explodicus:
- Dan / simulacrum:
- Dominion:
- Other visible characters:

## Reference Images

- `path/to/reference.webp` — what this image should constrain:

## Prompt

Draft prompt goes here.

## Generation Command

Default to OpenRouter generation unless the user explicitly asks for ChatGPT/Codex built-in image generation:

```bash
uv run scripts/generate_openrouter_image.py \
  --prompt-file campaigns/<campaign>/gates/<gate-name>/08-comic-planning/page-packets/page-{{PAGE}}/image-prompt.md \
  --reference-image path/to/reference.webp \
  --output-dir campaigns/<campaign>/gates/<gate-name>/08-comic-planning/visual-drafts \
  --filename-stem page-{{PAGE}}-rough-thumbnail \
  --aspect-ratio 2:3 \
  --image-size 1K
```

For non-Gates campaigns, replace the output path with that campaign's `08-comic-planning/visual-drafts/` folder.
