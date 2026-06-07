"""Import FIREBALL sessions into the campaign workspace.

Each filtered/<hash>.jsonl in the dataset is one combat session.
Downloads files on demand via huggingface_hub (does not load the full 2 GB).

Usage:
    uv run scripts/fireball_import.py --limit 5
    uv run scripts/fireball_import.py --session 00068c6b03adc2c102756053cf6edd05
    uv run scripts/fireball_import.py --limit 20 --out-dir campaigns/fireball
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import typer
from huggingface_hub import HfFileSystem, hf_hub_download

REPO_ID = "lara-martin/FIREBALL"
REPO_ROOT = Path(__file__).parent.parent


app = typer.Typer(add_completion=False)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _speaker_map(turns: list[dict]) -> dict[str, str]:
    """Return a stable {speaker_id: 'Player N'} mapping for a session."""
    seen: dict[str, str] = {}
    n = 1
    for turn in turns:
        sid = turn.get("speaker_id", "")
        if sid and sid not in seen:
            seen[sid] = f"Player {n}"
            n += 1
        for actor in (turn.get("combat_state_before") or []):
            cid = actor.get("controller_id", "")
            if cid and cid not in seen:
                seen[cid] = f"Player {n}"
                n += 1
    return seen


def _actor_label(actor: dict | None, speakers: dict[str, str]) -> str:
    if not actor:
        return ""
    name = actor.get("name", "?")
    pid = speakers.get(actor.get("controller_id", ""), "")
    return f"{name} ({pid})" if pid else name


def _unique_characters(turns: list[dict]) -> list[dict]:
    """Collect all PC-like actors seen across turns (deduplicated by name)."""
    seen: dict[str, dict] = {}
    for turn in turns:
        for state_key in ("combat_state_before", "combat_state_after"):
            for actor in (turn.get(state_key) or []):
                name = actor.get("name", "")
                if name and name not in seen and actor.get("class"):
                    seen[name] = actor
    return list(seen.values())


def _render_session(session_hash: str, turns: list[dict]) -> str:
    speakers = _speaker_map(turns)
    characters = _unique_characters(turns)

    lines: list[str] = [
        f"# FIREBALL Session: {session_hash}",
        "",
        f"Source: FIREBALL dataset (lara-martin/FIREBALL, ACL 2023)",
        f"Session ID: {session_hash}",
        f"Turns: {len(turns)}",
        f"Participants: {len({t.get('speaker_id') for t in turns if t.get('speaker_id')})} speakers",
        "",
    ]

    if characters:
        lines += ["## Characters", ""]
        for ch in characters:
            parts = [f"**{ch['name']}**"]
            if ch.get("class"):
                parts.append(ch["class"])
            if ch.get("race"):
                parts.append(ch["race"])
            if ch.get("description"):
                desc = re.sub(r"\s+", " ", ch["description"]).strip()
                if len(desc) > 120:
                    desc = desc[:117] + "…"
                parts.append(f"— {desc}")
            lines.append("- " + ", ".join(parts[:3]) + (f" {parts[3]}" if len(parts) > 3 else ""))
        lines += [""]

    lines += ["## Combat Log", ""]

    for turn in turns:
        sid = turn.get("speaker_id", "")
        player_label = speakers.get(sid, "Unknown")
        actor = turn.get("current_actor")
        actor_label = _actor_label(actor, speakers) if actor else ""

        for utt in (turn.get("before_utterances") or []):
            utt = utt.strip()
            if not utt:
                continue
            if actor and actor.get("name"):
                actor_pid = speakers.get(actor.get("controller_id", ""), "")
                label = f"**{actor['name']}** ({actor_pid})" if actor_pid else f"**{actor['name']}**"
                lines.append(f"{label}: {utt}")
            else:
                lines.append(f"**{player_label}**: {utt}")

        for i, cmd in enumerate(turn.get("commands_norm") or []):
            cmd = cmd.strip()
            if not cmd:
                continue
            lines.append(f"`{cmd}`")
            result = (turn.get("automation_results") or [])[i] if i < len(turn.get("automation_results") or []) else None
            if result:
                for rline in result.strip().splitlines():
                    lines.append(f"> {rline}")

        for utt in (turn.get("after_utterances") or []):
            utt = utt.strip()
            if not utt:
                continue
            if actor and actor.get("name"):
                actor_pid = speakers.get(actor.get("controller_id", ""), "")
                label = f"**{actor['name']}** ({actor_pid})" if actor_pid else f"**{actor['name']}**"
                lines.append(f"{label}: {utt}")
            else:
                lines.append(f"**{player_label}**: {utt}")

        lines.append("")

    return "\n".join(lines)


def _import_session(session_hash: str, out_dir: Path) -> Path:
    filename = f"filtered/{session_hash}.jsonl"
    local_path = hf_hub_download(
        repo_id=REPO_ID,
        filename=filename,
        repo_type="dataset",
    )
    with open(local_path) as f:
        turns = [json.loads(line) for line in f if line.strip()]

    markdown = _render_session(session_hash, turns)

    log_dir = out_dir / "02-chat-logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    out_file = log_dir / f"{session_hash}.md"
    out_file.write_text(markdown)
    return out_file


def _list_session_hashes() -> list[str]:
    fs = HfFileSystem()
    paths = fs.ls(f"datasets/{REPO_ID}/filtered", detail=False)
    hashes = []
    for p in paths:
        name = Path(p).name
        if name.endswith(".jsonl"):
            hashes.append(name[:-6])
    return sorted(hashes)


# ---------------------------------------------------------------------------
# CLI commands
# ---------------------------------------------------------------------------

@app.command()
def main(
    limit: int = typer.Option(None, help="Max number of sessions to import"),
    session: str = typer.Option(None, help="Import a single session by hash"),
    out_dir: Path = typer.Option(
        REPO_ROOT / "campaigns" / "fireball",
        help="Destination campaign folder",
    ),
):
    """Import FIREBALL play-by-post sessions into the campaign workspace."""
    if session:
        hashes = [session]
    else:
        typer.echo("Listing sessions…")
        hashes = _list_session_hashes()
        log_dir = out_dir / "02-chat-logs"
        hashes = [h for h in hashes if not (log_dir / f"{h}.md").exists()]
        if limit:
            hashes = hashes[:limit]
        typer.echo(f"Importing {len(hashes)} sessions into {out_dir}")

    for i, h in enumerate(hashes, 1):
        out_file = _import_session(h, out_dir)
        typer.echo(f"[{i}/{len(hashes)}] {h} → {out_file.relative_to(REPO_ROOT)}")

    typer.echo(f"\nDone. {len(hashes)} session(s) written to {out_dir}.")


if __name__ == "__main__":
    app()
