# Image Prompt - Marcel: The Mourner

Subject: character portrait for the design in `marcel-the-mourner-visual-continuity.md`.
Output: `visual-drafts/marcel-the-mourner.png` and `visual-drafts/marcel-the-mourner-pencil.png`.

Per repository rules the prompt asks for **no readable text, numerals, labels, or symbols the model
must render legibly**. The polyhedra are described as geometric shapes, the die pendant is described
without numbered faces, and no writing is requested anywhere.

No real person's likeness is requested. The brief describes a quality — a kid who looks too young
for the room he is standing in — rather than any individual's features.

## Base Prompt

```text
Character portrait of a gaunt, moon-pale teenage boy, roughly sixteen, standing in a dim
Gothic-horror village street at dusk. Painted illustration, muted desaturated palette of black,
charcoal, cold grey and deep violet, with a single warm lantern glow far behind him. Melancholy,
restrained, Eastern-European folk-horror atmosphere. Head-and-chest framing, slight low angle,
shallow depth of field.

His face is soft, round and unfinished at the jaw, and reads clearly younger than he is trying to
look. Prominent ears. Skin is unnaturally chalk-white, almost lunar. Dark fine straight hair in a
shaggy overgrown cut, falling forward into his eyes and over his ears, pushed back and not staying.
He wears heavy oversized dark-framed spectacles that are slightly too large for his face.

Black eye makeup smudged unevenly around both eyes, heavier on one side, clumsily self-applied. A
delicate violet star-shaped marking sits at the outer corner of his right eye and is drawn
downward into a long smeared tear-track along his cheek, like weeping that was never wiped away.

He wears a heavy oversized black coat with sleeves past his knuckles, over a high black ribbon
choker at his throat. The black fabric is embroidered in fine tarnished silver thread with
scattered angular geometric solids - faceted crystalline polyhedra, twenty-sided and eight-sided
forms - which catch the light faintly like a night sky folded into hard shapes. A small tarnished
silver locket hangs open and empty on a chain. Many mismatched silver rings.

His hands are in fingerless black lace mitts pulled over pristine white gloves underneath, the
white unmistakable at the fingertips. A single small faceted twenty-sided stone pendant hangs on a
cord at his chest where a holy symbol would sit, its facets completely smooth and blank.

Expression: sullen, guarded, exhausted, and very young. Not menacing. A child in armor that does
not fit him.

No text, no lettering, no numerals, no runes, no writing of any kind anywhere in the image.
```

## Instrument Pass

Added in a second generation using the first as `--reference-image`:

```text
1. A LUTE CARRIED ACROSS HIS BACK. A pear-shaped wooden stringed instrument with a rounded deep
body worn behind his shoulder, its long fretted neck rising diagonally up past his left shoulder
with the pegbox angled sharply backwards at the top. A simple dark leather strap crosses his chest
to hold it. A black mourning ribbon is knotted around the neck of the instrument near the pegbox,
with short trailing ends.

2. A CONCERTINA HELD IN BOTH HANDS at chest height, drawn slightly open as though he is mid-breath
in playing it. It is a small hexagonal squeezebox: two flat hexagonal end plates of dark aged wood
with tarnished silver fittings, joined by black folded leather bellows. One end plate rests in each
hand, his fingers curled over the sides. The bellows are pulled a little apart so the folds are
clearly visible.
```

## Pencil Restyle Pass

Restyled from the painted result as reference, so design, pose and instruments carry over and only
the medium changes:

```text
Redraw the supplied image completely as a traditional GRAPHITE PENCIL DRAWING on paper. Keep the
character design, pose, framing, instruments and setting exactly the same, but change the medium
entirely.

Style: hand-drawn graphite pencil sketch on off-white paper with visible paper tooth and grain.
Strong visible pencil work - directional hatching and cross-hatching to build the shadows, soft
graphite shading blended with a blending stump in the mid-tones, crisp dark 6B pencil for the
deepest darks, and bright clean eraser highlights on the face, the knuckles and the metal fittings.
Loose construction lines and searching strokes left visible at the edges of the drawing, especially
around the shoulders, the coat hem and the background buildings, so it reads as a real artist's
drawing rather than a photograph. The background street should be more lightly and loosely drawn
than the figure, fading towards bare paper at the corners.

Entirely monochrome greyscale - graphite grey, black and the off-white of the paper only. No colour
anywhere. Not a painting, not digital art, not smooth airbrushing: pencil on paper, with the marks
of the pencil clearly visible throughout.
```

## Review Checklist Used

- Any rendered text, numerals on the pendant facets, or writing on fabric. Regenerate if present.
- Face reading as an adult in their twenties. The whole brief fails if he does not look too young.
- Over-stylised "cool" goth. He should look sad and slightly ridiculous, not fashionable.
- Spectacles missing — they are the load-bearing prop.

## Findings

Model: `google/gemini-2.5-flash-image` through `scripts/generate_openrouter_image.py`, 2:3, 1K.
Eight generations total.

**What worked.**

- Restyling through `--reference-image` preserves design reliably. Ask for the medium to change and
  state explicitly that everything else stays.
- "Loose construction lines left visible at the edges, fading to bare paper" is what makes a pencil
  restyle read as a real drawing rather than a filter.
- Describing embroidery as "faceted crystalline polyhedra" produced clean blank geometric shapes
  with no numerals, avoiding the usual failure where dice-like objects acquire pips or numbers.

**What did not work.**

- **White gloves on pale skin.** Three passes failed; the model conflated white gloves with the
  character's chalk-white hands. The pass that finally produced real white fabric distorted both
  hands into fused, mannequin-like shapes and was discarded. Accepted as a text-only detail.
- **Left versus right placement.** Two passes could not put a small violet star beside a named eye.
  The first spread the colour symmetrically into a mask across both eyes; the second placed it on
  the wrong side. If a small asymmetric detail must land on a specific side, consider generating it
  mirrored deliberately and flipping the image afterwards.

**Incidental discovery worth reusing.** Giving the hands an object to hold fixed the hand anatomy
that had been the weakest part of every earlier version. If a portrait has hand trouble, occupy the
hands rather than describing them more precisely.
