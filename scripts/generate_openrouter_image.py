#!/usr/bin/env python3
"""Generate comic art through OpenRouter image models."""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = "sourceful/riverflow-v2.5-pro:free"
DEFAULT_KEY_NAME = "OPENROUTER_API_KEY_AVRAE2COMIC"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DATA_URL_RE = re.compile(r"^data:(?P<mime>[-\w.+/]+);base64,(?P<data>.*)$", re.DOTALL)
MAX_REFERENCE_IMAGES = 10


def load_env_value(key_name: str, env_file: Path) -> str | None:
    """Load a single key from the process environment or a local .env file."""

    existing = os.environ.get(key_name)
    if existing:
        return existing

    if not env_file.exists():
        return None

    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        name, value = line.split("=", 1)
        if name.strip() != key_name:
            continue

        value = value.strip()
        if (
            len(value) >= 2
            and value[0] == value[-1]
            and value[0] in {"'", '"'}
        ):
            value = value[1:-1]
        return value

    return None


def read_prompt(args: argparse.Namespace) -> str:
    parts: list[str] = []

    if args.prompt:
        parts.append(args.prompt)

    if args.prompt_file:
        parts.append(args.prompt_file.read_text(encoding="utf-8").strip())

    prompt = "\n\n".join(part for part in parts if part).strip()
    if not prompt:
        raise SystemExit("Provide --prompt, --prompt-file, or both.")

    return prompt


def image_path_to_data_url(path: Path) -> tuple[str, str]:
    if not path.exists():
        raise SystemExit(f"Reference image not found: {path}")
    if not path.is_file():
        raise SystemExit(f"Reference image is not a file: {path}")

    mime_type = mimetypes.guess_type(path)[0]
    if not mime_type or not mime_type.startswith("image/"):
        raise SystemExit(f"Reference image does not look like an image file: {path}")

    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}", mime_type


def build_message_content(prompt: str, reference_images: list[Path]) -> list[dict[str, Any]] | str:
    if not reference_images:
        return prompt

    if len(reference_images) > MAX_REFERENCE_IMAGES:
        raise SystemExit(
            f"Too many reference images: {len(reference_images)}. "
            f"This model supports up to {MAX_REFERENCE_IMAGES}."
        )

    content: list[dict[str, Any]] = [{"type": "text", "text": prompt}]
    for path in reference_images:
        data_url, _mime_type = image_path_to_data_url(path)
        content.append({"type": "image_url", "image_url": {"url": data_url}})

    return content


def summarize_reference_images(reference_images: list[Path]) -> list[dict[str, str]]:
    summary: list[dict[str, str]] = []
    for path in reference_images:
        mime_type = mimetypes.guess_type(path)[0] or "application/octet-stream"
        size_bytes = path.stat().st_size if path.exists() else 0
        summary.append(
            {
                "path": str(path),
                "mime_type": mime_type,
                "size_bytes": str(size_bytes),
            }
        )
    return summary


def redacted_payload(payload: dict[str, Any], reference_images: list[Path]) -> dict[str, Any]:
    if not reference_images:
        return payload

    safe_payload = dict(payload)
    messages = []
    for message in payload.get("messages", []):
        safe_message = dict(message)
        content = safe_message.get("content")
        if isinstance(content, list):
            safe_content: list[dict[str, Any]] = []
            for part in content:
                if part.get("type") == "image_url":
                    safe_content.append(
                        {
                            "type": "image_url",
                            "image_url": {"url": "<base64 image data redacted>"},
                        }
                    )
                else:
                    safe_content.append(part)
            safe_message["content"] = safe_content
        messages.append(safe_message)
    safe_payload["messages"] = messages
    safe_payload["reference_images"] = summarize_reference_images(reference_images)
    return safe_payload


def build_payload(args: argparse.Namespace, prompt: str) -> dict[str, Any]:
    image_config: dict[str, Any] = {}
    if args.aspect_ratio:
        image_config["aspect_ratio"] = args.aspect_ratio
    if args.image_size:
        image_config["image_size"] = args.image_size
    if args.background_mode:
        image_config["background_mode"] = args.background_mode
    if args.background_hex_color:
        image_config["background_hex_color"] = args.background_hex_color
    if args.scoring_prompt:
        image_config["scoring_prompt"] = args.scoring_prompt
    if args.scoring_rubric:
        image_config["scoring_rubric"] = args.scoring_rubric

    payload: dict[str, Any] = {
        "model": args.model,
        "messages": [
            {
                "role": "user",
                "content": build_message_content(prompt, args.reference_image),
            }
        ],
        "modalities": args.modalities,
        "stream": False,
    }

    if image_config:
        payload["image_config"] = image_config

    if args.reasoning_effort:
        payload["reasoning"] = {"effort": args.reasoning_effort}

    return payload


def post_openrouter(api_key: str, payload: dict[str, Any]) -> dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/local/play-by-post-assistant",
        "X-Title": "play-by-post-assistant",
    }
    request = urllib.request.Request(
        OPENROUTER_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"OpenRouter HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"OpenRouter request failed: {exc.reason}") from exc


def image_extension(mime_type: str) -> str:
    if mime_type == "image/jpeg":
        return ".jpg"
    return mimetypes.guess_extension(mime_type) or ".png"


def save_images(result: dict[str, Any], output_dir: Path, filename_stem: str) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    saved: list[Path] = []

    choices = result.get("choices") or []
    for choice_index, choice in enumerate(choices, start=1):
        message = choice.get("message") or {}
        images = message.get("images") or []

        for image_index, image in enumerate(images, start=1):
            image_url = image.get("image_url") or {}
            data_url = image_url.get("url")
            if not isinstance(data_url, str):
                continue

            match = DATA_URL_RE.match(data_url)
            if not match:
                continue

            mime_type = match.group("mime")
            extension = image_extension(mime_type)
            suffix = "" if len(choices) == 1 and len(images) == 1 else f"-{choice_index}-{image_index}"
            output_path = output_dir / f"{filename_stem}{suffix}{extension}"
            output_path.write_bytes(base64.b64decode(match.group("data")))
            saved.append(output_path)

    return saved


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt", help="Text prompt to generate from.")
    parser.add_argument(
        "--prompt-file",
        type=Path,
        help="Markdown or text file containing the generation prompt.",
    )
    parser.add_argument(
        "--reference-image",
        action="append",
        default=[],
        type=Path,
        help=(
            "Local image to send as visual reference. Can be repeated up to "
            f"{MAX_REFERENCE_IMAGES} times."
        ),
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory where generated images should be saved.",
    )
    parser.add_argument(
        "--filename-stem",
        default="openrouter-generation",
        help="Output filename stem, without extension.",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument(
        "--api-key-env",
        default=DEFAULT_KEY_NAME,
        help="Environment variable name that contains the OpenRouter API key.",
    )
    parser.add_argument(
        "--env-file",
        default=REPO_ROOT / ".env",
        type=Path,
        help="Optional .env file to load the named API key from.",
    )
    parser.add_argument(
        "--modalities",
        nargs="+",
        default=["image"],
        choices=["image", "text"],
        help="OpenRouter output modalities. Sourceful image models usually use: image",
    )
    parser.add_argument(
        "--aspect-ratio",
        default="2:3",
        help="Requested aspect ratio, for example 1:1, 2:3, 3:2, or 16:9.",
    )
    parser.add_argument(
        "--image-size",
        default="1K",
        choices=["1K", "2K", "4K"],
        help="Requested image size.",
    )
    parser.add_argument(
        "--reasoning-effort",
        choices=["low", "medium", "high", "xhigh"],
        help="Riverflow reasoning effort. Higher can cost/rate-limit more.",
    )
    parser.add_argument(
        "--background-mode",
        choices=["original", "transparent", "solid"],
        help="Riverflow background mode.",
    )
    parser.add_argument("--background-hex-color")
    parser.add_argument("--scoring-prompt")
    parser.add_argument("--scoring-rubric")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Print the request payload without sending it. Does not print the API key "
            "or reference-image base64 data."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    prompt = read_prompt(args)
    payload = build_payload(args, prompt)

    if args.dry_run:
        print(json.dumps(redacted_payload(payload, args.reference_image), indent=2))
        return 0

    api_key = load_env_value(args.api_key_env, args.env_file)
    if not api_key:
        raise SystemExit(
            f"Missing OpenRouter API key. Set {args.api_key_env} in the environment "
            f"or in {args.env_file}."
        )

    result = post_openrouter(api_key, payload)
    saved = save_images(result, args.output_dir, args.filename_stem)

    if not saved:
        print(json.dumps(result, indent=2), file=sys.stderr)
        raise SystemExit("OpenRouter response did not contain generated images.")

    for path in saved:
        print(f"saved {path}")

    usage = result.get("usage")
    if usage:
        print(f"usage {json.dumps(usage, sort_keys=True)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
