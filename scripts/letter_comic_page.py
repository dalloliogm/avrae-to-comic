#!/usr/bin/env python3
"""Apply editable lettering boxes to a comic page image.

The layout file is JSON:

[
  {
    "kind": "caption",
    "text": "When the chamber fell silent...",
    "x": 80,
    "y": 120,
    "w": 620,
    "h": 120
  }
]

Coordinates are pixels in the base image. Text is wrapped and auto-shrunk to
fit within the box.
"""

from __future__ import annotations

import argparse
import json
import textwrap
from pathlib import Path
from typing import Any

DEFAULT_FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True, help="Base page image")
    parser.add_argument("--layout", required=True, help="JSON lettering layout")
    parser.add_argument("--output", required=True, help="Output image path")
    parser.add_argument("--font", help="Optional TrueType/OpenType font path")
    return parser.parse_args()


def load_font(size: int, preferred: str | None = None) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [preferred] if preferred else []
    candidates.extend(DEFAULT_FONT_CANDIDATES)
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default(size=size)


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> tuple[int, int]:
    bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=4)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> str:
    words = text.split()
    if not words:
        return ""

    lines: list[str] = []
    line: list[str] = []
    for word in words:
        trial = " ".join([*line, word])
        width, _ = text_size(draw, trial, font)
        if width <= max_width or not line:
            line.append(word)
        else:
            lines.append(" ".join(line))
            line = [word]
    if line:
        lines.append(" ".join(line))
    return "\n".join(lines)


def fit_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    max_width: int,
    max_height: int,
    start_size: int,
    min_size: int,
    font_path: str | None,
) -> tuple[str, ImageFont.ImageFont]:
    for size in range(start_size, min_size - 1, -1):
        font = load_font(size, font_path)
        wrapped = wrap_text(draw, text, font, max_width)
        width, height = text_size(draw, wrapped, font)
        if width <= max_width and height <= max_height:
            return wrapped, font
    font = load_font(min_size, font_path)
    return wrap_text(draw, textwrap.shorten(text, width=120, placeholder="..."), font, max_width), font


def colors(kind: str) -> dict[str, tuple[int, int, int, int]]:
    if kind == "speech-dark":
        return {
            "fill": (20, 20, 24, 238),
            "outline": (245, 245, 230, 255),
            "text": (245, 245, 230, 255),
        }
    if kind == "sfx":
        return {
            "fill": (255, 255, 255, 0),
            "outline": (255, 255, 255, 0),
            "text": (20, 20, 20, 255),
        }
    return {
        "fill": (244, 232, 190, 238),
        "outline": (45, 35, 25, 255),
        "text": (20, 20, 20, 255),
    }


def draw_box(draw: ImageDraw.ImageDraw, item: dict[str, Any], font_path: str | None) -> None:
    kind = item.get("kind", "caption")
    text = str(item["text"])
    x = int(item["x"])
    y = int(item["y"])
    w = int(item["w"])
    h = int(item["h"])
    pad = int(item.get("padding", 16))
    radius = int(item.get("radius", 10))
    font_size = int(item.get("font_size", 32))
    min_font_size = int(item.get("min_font_size", 18))

    palette = colors(kind)
    if kind != "sfx":
        draw.rounded_rectangle(
            (x, y, x + w, y + h),
            radius=radius,
            fill=palette["fill"],
            outline=palette["outline"],
            width=int(item.get("border", 3)),
        )

    max_width = max(1, w - pad * 2)
    max_height = max(1, h - pad * 2)
    wrapped, font = fit_text(draw, text, max_width, max_height, font_size, min_font_size, font_path)
    tw, th = text_size(draw, wrapped, font)
    tx = x + (w - tw) // 2 if item.get("align", "center") == "center" else x + pad
    ty = y + (h - th) // 2
    stroke_width = int(item.get("stroke_width", 0))
    stroke_fill = tuple(item.get("stroke_fill", (255, 255, 255, 255)))
    draw.multiline_text(
        (tx, ty),
        wrapped,
        font=font,
        fill=palette["text"],
        spacing=4,
        align=item.get("align", "center"),
        stroke_width=stroke_width,
        stroke_fill=stroke_fill,
    )


def main() -> None:
    args = parse_args()
    global Image, ImageDraw, ImageFont
    from PIL import Image, ImageDraw, ImageFont

    image = Image.open(args.image).convert("RGBA")
    overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    layout = json.loads(Path(args.layout).read_text())

    for item in layout:
        draw_box(draw, item, args.font)

    output = Image.alpha_composite(image, overlay).convert("RGB")
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    output.save(args.output)


if __name__ == "__main__":
    main()
