# Image Generation Findings

Accumulated, campaign-agnostic notes on getting usable art out of the image models used by
`scripts/generate_openrouter_image.py`. Process only — no campaign source text.

Add to this as new failure modes and fixes turn up, rather than rediscovering them per page.

## Reference Images

**Restyling through `--reference-image` is reliable.** To change medium while keeping a design,
pass the existing render as a reference, describe the new medium in detail, and state explicitly
that everything else stays the same. Design, pose, props and framing carry over intact.

This is a better route than regenerating from scratch with a modified prompt, which drifts.

**Iterating on a detail also works through references**, but with the limits below.

## Known Failure Modes

### Small asymmetric details on a named side

The models do not reliably place a detail on a specified left or right side. Attempts to put a
small mark beside one particular eye produced first a symmetrical version across both, then the
correct mark on the wrong side.

**Workaround:** if a small asymmetric detail must land on a specific side, generate it deliberately
mirrored and flip the finished image, or accept the placement and note the deviation.

### Colours that collide with a nearby colour

A request for white gloves on a character with chalk-white skin failed three times: the model read
the gloves as bare pale hands. Escalating the material description ("bright white satin, visible
fabric sheen, hemmed cuff, creases at the knuckles") finally produced real fabric, but distorted
the hands into fused mannequin shapes.

**Workaround:** either accept the detail as text-only canon, or generate a close-cropped pass of
just that region and composite. Do not expect a full portrait to fix a small conflicting-colour
detail in place.

### Hands

Hands were the weakest element of every version of one portrait until the character was given an
object to hold, at which point they rendered naturally on the first try.

**Rule of thumb: occupy the hands rather than describing them more precisely.** An instrument, a
prop, a held object — anything that gives the fingers a defined job.

## Things That Work Well

**Blank geometric shapes instead of named objects with markings.** Asking for "dice" invites pips
and numerals, which violates the no-text rule. Asking for "faceted crystalline polyhedra,
twenty-sided and eight-sided forms" with "facets completely smooth and blank" produces the same
silhouette with nothing to render illegibly.

Generalises: describe the *shape* you want, not the object whose name implies text.

**Pencil and traditional-media restyles need the artefacts named explicitly.** What sells a graphite
restyle as a real drawing rather than a filter:

- visible paper tooth and grain
- directional hatching and cross-hatching for shadow
- mid-tones blended with a blending stump
- eraser highlights called out on specific features
- **loose construction lines left visible at the edges, fading towards bare paper at the corners**
- background drawn more lightly and loosely than the figure

The construction-lines instruction does the most work of any single element.

**Negative instructions about text should be repeated at the end of the prompt**, listing the
variants: no text, no lettering, no numerals, no runes, no signature, no writing of any kind.

## Cost And Iteration

Eight generations on one portrait at 1K / 2:3 cost roughly USD 0.30 on
`google/gemini-2.5-flash-image`. Cheap enough to iterate, expensive enough not to brute-force a
known failure mode — after two failed attempts at the same detail, change approach rather than
rewording.

## Model Availability

`sourceful/riverflow-v2.5-pro:free` returns HTTP 404 as of August 2026; the free tier was withdrawn
and only the paid slug remains. `google/gemini-2.5-flash-image` works well for both painted and
traditional-media styles and accepts reference images.

Note that the API key environment variable name may differ between checkouts; pass
`--api-key-env <NAME>` when it is not the script default.
