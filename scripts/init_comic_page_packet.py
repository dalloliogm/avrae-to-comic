#!/usr/bin/env python3
"""Create a reusable comic page packet from skill templates."""

from __future__ import annotations

import argparse
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = (
    REPO_ROOT
    / ".codex"
    / "skills"
    / "comic-adaptation-planner"
    / "templates"
    / "page-packet"
)


def render_template(path: Path, page: str, title: str) -> str:
    text = path.read_text(encoding="utf-8")
    return text.replace("{{PAGE}}", page).replace("{{TITLE}}", title)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--planning-dir",
        required=True,
        type=Path,
        help="Mission comic-planning directory, usually campaigns/.../08-comic-planning.",
    )
    parser.add_argument(
        "--page",
        required=True,
        help="Page number, for example 06. Values are normalized to two digits when numeric.",
    )
    parser.add_argument(
        "--title",
        default="Untitled page",
        help="Short page goal used in generated template files.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing packet files.",
    )
    args = parser.parse_args()

    page = args.page.zfill(2) if args.page.isdigit() else args.page
    planning_dir = args.planning_dir
    packet_dir = planning_dir / "page-packets" / f"page-{page}"

    if not TEMPLATE_DIR.exists():
        raise SystemExit(f"Template directory not found: {TEMPLATE_DIR}")

    packet_dir.mkdir(parents=True, exist_ok=True)

    created: list[Path] = []
    skipped: list[Path] = []

    for template in sorted(TEMPLATE_DIR.iterdir()):
        if not template.is_file():
            continue

        target = packet_dir / template.name
        if target.exists() and not args.force:
            skipped.append(target)
            continue

        target.write_text(
            render_template(template, page=page, title=args.title),
            encoding="utf-8",
        )
        created.append(target)

    for path in created:
        print(f"created {path}")
    for path in skipped:
        print(f"skipped existing {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
