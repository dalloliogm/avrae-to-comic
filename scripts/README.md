# Scripts

Utilities can live here, such as:

- Discord export cleanup
- Avrae command extraction
- session summary generation
- character index generation
- comic page packet creation
- comic lettering renders

Current scripts:

- [letter_comic_page.py](letter_comic_page.py): render editable captions, balloons, and SFX over no-text comic art.
- [init_comic_page_packet.py](init_comic_page_packet.py): create a reusable page-packet folder for independent comic agent passes.
- [generate_openrouter_image.py](generate_openrouter_image.py): generate image drafts through OpenRouter image models and save returned base64 images as local files.

## OpenRouter Image Generation

Use the OpenRouter helper when you want image generation to use an OpenRouter key instead of ChatGPT's built-in image tool. The script looks for `OPENROUTER_API_KEY_AVRAE2COMIC` in the process environment or local `.env` file and does not print the key.

Dry-run a request:

```bash
uv run scripts/generate_openrouter_image.py \
  --prompt "Single comic panel, inked fantasy art, a wizard studies a glowing gate." \
  --output-dir campaigns/the-gates/08-comic-planning/visual-drafts \
  --filename-stem test-panel \
  --dry-run
```

Generate with the current default model:

```bash
uv run scripts/generate_openrouter_image.py \
  --prompt-file campaigns/the-gates/gates/weave-gate/08-comic-planning/visual-drafts/page-01-prompt.md \
  --output-dir campaigns/the-gates/gates/weave-gate/08-comic-planning/visual-drafts \
  --filename-stem page-01-openrouter-draft \
  --aspect-ratio 2:3 \
  --image-size 1K
```

Add reference images when character portraits, setting art, or previous page drafts should influence the generation:

```bash
uv run scripts/generate_openrouter_image.py \
  --prompt-file campaigns/the-gates/gates/weave-gate/08-comic-planning/page-packets/page-02/image-prompt.md \
  --reference-image campaigns/the-gates/gates/weave-gate/01-characters/portraits/tobias.webp \
  --reference-image campaigns/the-gates/gates/weave-gate/08-comic-planning/visual-drafts/page-01-art-base.png \
  --output-dir campaigns/the-gates/gates/weave-gate/08-comic-planning/visual-drafts \
  --filename-stem page-02-openrouter-draft \
  --aspect-ratio 2:3 \
  --image-size 1K
```

Reference images are sent as base64 `image_url` parts in the OpenRouter chat request. The dry-run output redacts the base64 data and prints only the local paths, MIME types, and file sizes.
