#!/usr/bin/env python3
"""Generate evidence-tagged character statistics from PbP Markdown workspaces."""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


MISSION_ROW_RE = re.compile(r"^\|\s*(Main|Partial|Clover|User paste)\b")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
RAW_LOG_RE = re.compile(r"Raw log:\s*\[[^\]]+\]\(([^)]+)\)")
DATE_RE = re.compile(r"\b(20\d{2}(?:-\d{2})?(?:-\d{2})?)\b")
MESSAGE_HEADER_RE = re.compile(r"^\[[^\]]+\]\s+([^:]+):\s*$")
ACTION_PREFIX_RE = re.compile(
    r"^\s*(?:\*\*)?\s*(?:"
    r"A|Action|BA|Bonus Action|R|Reaction|"
    r"Pre-?cast|Precast|Perpetual Cast|Wish Perpetual Cast|"
    r"Perpetual Wish Cast|Wish Perpetual|Perpetual Wish"
    r")\b",
    re.IGNORECASE,
)
MULTI_SPELL_PREFIX_RE = re.compile(
    r"^\s*(?:\*\*)?\s*(?:"
    r"Pre-?cast|Precast|Perpetual Cast|Wish Perpetual Cast|"
    r"Perpetual Wish Cast|Wish Perpetual|Perpetual Wish"
    r")\b",
    re.IGNORECASE,
)
PROSE_CAST_RE = re.compile(
    r"\b(?:casts?|cast|uses?|used|summons?|summoned|counterspells?|counterspelled|pre-?casts?|precast)\b",
    re.IGNORECASE,
)

KNOWN_SPELLS = [
    "Absorb Elements",
    "Adrenaline Rush",
    "Arcane Hand",
    "Bigby's Hand",
    "Bless",
    "Comprehend Languages",
    "Cone of Cold",
    "Contingency",
    "Counterspell",
    "Crown of Stars",
    "Cure Wounds",
    "Dawn",
    "Dispel Magic",
    "False Life",
    "Fireball",
    "Fire Shield",
    "Firebolt",
    "Fire Bolt",
    "Forcecage",
    "Freezing Sphere",
    "Guiding Bolt",
    "Hold Monster",
    "Implode",
    "Lightning Strike",
    "Longstrider",
    "Magic Missile",
    "Mass Cure Wounds",
    "Mass Heal",
    "Meteor Swarm",
    "Mind Fire",
    "Prestidigitation",
    "Rime Binding Ice",
    "See Invisibility",
    "Shield",
    "Shield of Faith",
    "Shocking Grasp",
    "Silvery Barbs",
    "Simulacrum",
    "Song of Defense",
    "Summon Draconic Spirit",
    "Summon Undead",
    "Sunburst",
    "Telekinetic Shove",
    "Telekinetic",
    "Thunder Step",
    "Toll the Dead",
    "Tongues",
    "Vitriolic Sphere",
    "Web",
    "Wish",
]

STOP_NAMES = {
    "Action",
    "A",
    "Bonus Action",
    "Reaction",
    "Precast",
    "Source Metadata",
    "Summary",
    "Extracted Details",
    "Uncertainty",
    "Raw Log",
    "Campaign",
    "Gate",
    "Discord",
    "Messages",
    "Import",
    "Status",
    "Don Explodicus",
    "Don",
    "Donthrakis",
    "Dan",
    "Avrae",
    "Complete",
    "Date",
    "Dates",
    "Defenders",
    "Discord",
    "Downloads",
    "Evidence",
    "Export",
    "Files",
    "Fireball",
    "Import Status",
    "Mission",
    "Preserve",
    "Raw",
    "Source",
    "The",
    "This",
    "Uncertainty",
    "Users",
    "Verify",
}


@dataclass
class Mission:
    source: str
    mission_number: str
    gate: str
    dates: str
    title: str
    status: str
    summary_label: str
    summary_path: Path | None
    split_summary_paths: list[Path] = field(default_factory=list)


@dataclass
class Evidence:
    spell: str
    tag: str
    path: Path
    line_no: int
    line: str


@dataclass
class MissionStats:
    mission: Mission
    stats_path: Path
    summaries: list[Path]
    raw_logs: list[Path]
    evidence: list[Evidence]
    coappearances: collections.Counter[str]


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def resolve_link(base_file: Path, link: str, workspace: Path) -> Path:
    link_path = Path(link)
    if link_path.is_absolute():
        return link_path
    return (base_file.parent / link_path).resolve()


def rel(path: Path, workspace: Path) -> str:
    try:
        return str(path.resolve().relative_to(workspace.resolve()))
    except ValueError:
        return str(path)


def parse_mission_index(index_path: Path, workspace: Path) -> list[Mission]:
    missions: list[Mission] = []
    for line in index_path.read_text(encoding="utf-8").splitlines():
        if not MISSION_ROW_RE.match(line):
            continue
        cells = split_table_row(line)
        if len(cells) < 6:
            continue
        source, gate, dates, title, status, summary_cell = cells[:6]
        number_match = re.search(r"\b(\d+)\b", source)
        mission_number = number_match.group(1) if number_match else "-"
        link_match = LINK_RE.search(summary_cell)
        summary_label = link_match.group(1) if link_match else summary_cell
        summary_path = resolve_link(index_path, link_match.group(2), workspace) if link_match else None
        mission = Mission(source, mission_number, gate, dates, title, status, summary_label, summary_path)
        if summary_path and summary_path.exists():
            mission.split_summary_paths = find_split_summaries(summary_path, workspace)
        missions.append(mission)
    return missions


def find_split_summaries(summary_path: Path, workspace: Path) -> list[Path]:
    text = summary_path.read_text(encoding="utf-8")
    if "## Split Segments" not in text:
        return []
    paths: list[Path] = []
    in_split_section = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_split_section = line.strip() == "## Split Segments"
            continue
        if not in_split_section:
            continue
        for _, link in LINK_RE.findall(line):
            path = resolve_link(summary_path, link, workspace)
            if path.exists():
                paths.append(path)
    return paths


def raw_log_from_summary(summary_path: Path, workspace: Path) -> Path | None:
    if not summary_path.exists():
        return None
    text = summary_path.read_text(encoding="utf-8")
    match = RAW_LOG_RE.search(text)
    if match:
        path = resolve_link(summary_path, match.group(1), workspace)
        return path if path.exists() else None
    guessed = summary_path.parent.parent / "02-chat-logs" / summary_path.name
    return guessed if guessed.exists() else None


def detailed_summary_paths(missions: Iterable[Mission]) -> list[Path]:
    paths: list[Path] = []
    seen: set[Path] = set()
    for mission in missions:
        candidates = mission_summary_paths(mission)
        for path in candidates:
            if path and path.exists() and path not in seen:
                paths.append(path)
                seen.add(path)
    return paths


def mission_summary_paths(mission: Mission) -> list[Path]:
    return mission.split_summary_paths or ([mission.summary_path] if mission.summary_path else [])


def compile_alias_re(character: str, aliases: list[str]) -> re.Pattern[str]:
    names = [character, *aliases]
    names = sorted({name for name in names if name}, key=len, reverse=True)
    return re.compile(r"\b(?:" + "|".join(re.escape(name) for name in names) + r")\b", re.IGNORECASE)


def alias_target_re(character: str, aliases: list[str]) -> re.Pattern[str]:
    names = [character, *aliases]
    names = sorted({name for name in names if name}, key=len, reverse=True)
    alias_group = "|".join(re.escape(name) for name in names)
    return re.compile(
        rf"(?:@\s*(?:{alias_group})\b|\b(?:to|vs|versus|against|at)\b[^*\n|]{{0,80}}\b(?:{alias_group})\b)",
        re.IGNORECASE,
    )


def alias_actor_re(character: str, aliases: list[str]) -> re.Pattern[str]:
    names = [character, *aliases]
    names = sorted({name for name in names if name}, key=len, reverse=True)
    return re.compile(r"^\s*(?:\*\*)?(?:" + "|".join(re.escape(name) for name in names) + r")\b", re.IGNORECASE)


def compile_speaker_re(speakers: list[str]) -> re.Pattern[str] | None:
    speakers = sorted({speaker for speaker in speakers if speaker}, key=len, reverse=True)
    if not speakers:
        return None
    return re.compile("|".join(re.escape(speaker) for speaker in speakers), re.IGNORECASE)


def canonical_spell(spell: str) -> str:
    if spell.lower() == "fire bolt":
        return "Firebolt"
    if spell.lower() == "arcane hand":
        return "Bigby's Hand"
    if spell.lower() == "telekinetic":
        return "Telekinetic Shove"
    return spell


def spells_in_line(line: str) -> list[str]:
    found = []
    lower = line.lower()
    for spell in sorted(KNOWN_SPELLS, key=len, reverse=True):
        if re.search(r"\b" + re.escape(spell.lower()) + r"\b", lower):
            found.append(canonical_spell(spell))
    deduped = []
    for spell in found:
        if spell == "Shield" and re.search(r"\b(?:carrying|holding)\s+(?:a\s+)?shield\b|shield in one hand", line, re.IGNORECASE):
            continue
        if re.search(r"\bcomponent\s+for\s+" + re.escape(spell) + r"\b", line, re.IGNORECASE):
            continue
        spell_lower = spell.lower()
        if any(spell_lower in existing.lower() and spell_lower != existing.lower() for existing in deduped):
            continue
        if spell not in deduped:
            deduped.append(spell)
    return deduped


def is_structured_action_line(line: str) -> bool:
    if not ACTION_PREFIX_RE.match(line):
        return False
    cleaned = re.sub(r"\*+", "", line.strip()).strip()
    shorthand_match = re.match(r"^(A|BA|R)\b[:\s]*(.*)$", cleaned, re.IGNORECASE)
    if not shorthand_match:
        return True
    remainder = shorthand_match.group(2).strip()
    if re.match(r"(?:telekinetic\s+)?shove\b", remainder, re.IGNORECASE):
        return True
    if re.match(r"(?:move|command|use|clenched|grapple|push|shove)\b.*\bdawn\b", remainder, re.IGNORECASE):
        return True
    if re.match(
        r"(?:move|command|use|clenched|grapple|push|shove)\b.*\b(?:bigby's hand|arcane hand)\b",
        remainder,
        re.IGNORECASE,
    ):
        return True
    spells = spells_in_line(remainder)
    if not spells:
        return False
    earliest_spell_pos = min(remainder.lower().find(spell.lower()) for spell in spells)
    return earliest_spell_pos <= 2


def action_prefix_kind(line: str) -> str:
    cleaned = re.sub(r"\*+", "", line.strip()).strip()
    if re.match(r"^(BA|Bonus Action)\b", cleaned, re.IGNORECASE):
        return "bonus"
    if re.match(r"^(R|Reaction)\b", cleaned, re.IGNORECASE):
        return "reaction"
    if re.match(
        r"^(Pre-?cast|Precast|Perpetual Cast|Wish Perpetual Cast|Perpetual Wish Cast|Wish Perpetual|Perpetual Wish)\b",
        cleaned,
        re.IGNORECASE,
    ):
        return "precast"
    if re.match(r"^(A|Action)\b", cleaned, re.IGNORECASE):
        return "action"
    return "other"


def action_spells_in_line(line: str) -> list[str]:
    """Return spells used by the actor, excluding target or trigger spell names."""
    match = ACTION_PREFIX_RE.match(line)
    if not match:
        return spells_in_line(line)
    action_text = line[match.end() :]
    action_clean = re.sub(r"^[\s:*]+", "", action_text)
    if re.search(r"\b(?:telekinetic\s+)?shove\b", action_text, re.IGNORECASE):
        return ["Telekinetic Shove"]
    if re.search(r"\bcounterspell\b", action_text, re.IGNORECASE):
        return ["Counterspell"]
    if re.match(r"[:\s*]*dispel\b", action_text, re.IGNORECASE):
        return ["Dispel Magic"]
    kind = action_prefix_kind(line)
    if re.search(r"\bsimulacr(?:um|us)\b", action_text, re.IGNORECASE) and (
        re.search(r"\bwish\b", line, re.IGNORECASE) or re.search(r"\bcreate\b", action_text, re.IGNORECASE)
    ):
        return ["Simulacrum"]
    if re.search(r"\bcrown of stars\b", action_text, re.IGNORECASE):
        if kind in {"bonus", "reaction"}:
            return ["Crown of Stars Attack"]
        return ["Crown of Stars Cast"]
    if re.search(r"\bdawn\b", action_text, re.IGNORECASE):
        if kind in {"bonus", "reaction"} or re.search(r"\bmove\b", action_text, re.IGNORECASE):
            return ["Dawn Move"]
        if re.match(r"(?:cast\s+)?dawn\b", action_clean, re.IGNORECASE):
            return ["Dawn Cast"]
    if re.search(r"\b(?:bigby's hand|arcane hand)\b", action_text, re.IGNORECASE):
        if kind in {"bonus", "reaction"}:
            return ["Bigby's Hand Use"]
        if re.match(r"(?:cast\s+)?(?:bigby's hand|arcane hand)\b", action_clean, re.IGNORECASE):
            return ["Bigby's Hand Cast"]
    if MULTI_SPELL_PREFIX_RE.match(line):
        return spells_in_line(action_text)

    primary_text = re.split(
        r"\s+(?:at|on|vs|versus|against|@)\b|\s+@|\(",
        action_text,
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0]
    primary_spells = spells_in_line(primary_text)
    primary_spells.sort(key=lambda spell: primary_text.lower().find(spell.lower()))
    return primary_spells[:1] or spells_in_line(line)[:1]


def scan_file_for_evidence(
    path: Path,
    workspace: Path,
    alias_re: re.Pattern[str],
    target_re: re.Pattern[str],
    actor_re: re.Pattern[str],
    speaker_re: re.Pattern[str] | None,
    source_kind: str,
) -> list[Evidence]:
    evidence: list[Evidence] = []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    target_context = 0
    uncertain_context = 0
    speaker_context = False
    actor_context = 0
    for i, line in enumerate(lines, start=1):
        header_match = MESSAGE_HEADER_RE.match(line)
        if header_match:
            speaker = header_match.group(1)
            speaker_context = bool(speaker_re and speaker_re.search(speaker))
            target_context = 0
            uncertain_context = 0
            actor_context = 0
            continue

        stripped = line.strip().strip("*")
        if actor_re.fullmatch(stripped.rstrip(":")):
            actor_context = 8
            target_context = 8
            continue
        elif actor_context > 0:
            actor_context -= 1

        alias_here = bool(alias_re.search(line))
        alias_targeted = bool(target_re.search(line))
        is_map_or_url = "http://" in line or "https://" in line or "otfbm.io" in line
        if alias_here and not alias_targeted and not is_map_or_url:
            target_context = 8
            if re.search(r"\b(duplicate|clone)\b", line, re.IGNORECASE):
                uncertain_context = 4
        elif target_context > 0:
            target_context -= 1
        if uncertain_context > 0:
            uncertain_context -= 1

        action_line = is_structured_action_line(line)
        spells = action_spells_in_line(line) if action_line else spells_in_line(line)
        if not spells:
            continue

        prose_cast = bool(PROSE_CAST_RE.search(line))
        if alias_here and alias_targeted and not actor_re.match(line):
            continue

        for spell in spells:
            spell_pos = line.lower().find(spell.lower())
            if spell == "Firebolt":
                spell_pos = min(pos for pos in [line.lower().find("firebolt"), line.lower().find("fire bolt")] if pos >= 0)
            alias_match = alias_re.search(line)
            alias_pos = alias_match.start() if alias_match else -1
            target_action = action_line and (speaker_context or actor_context > 0 or actor_re.match(line))
            target_prose = alias_here and prose_cast and (alias_pos >= 0 and alias_pos <= spell_pos)
            direct_summary = source_kind == "summary" and target_prose

            if source_kind == "raw":
                if not target_action:
                    continue
            elif not direct_summary:
                continue

            if uncertain_context or re.search(r"\b(duplicate|clone|mixed archive|mixed export)\b", line, re.IGNORECASE):
                tag = "uncertain"
            elif target_action:
                tag = "confirmed"
            else:
                tag = "probable"
            evidence.append(Evidence(spell, tag, path, i, line.strip()))
    return evidence


def extract_named_coappearances(paths: Iterable[Path], alias_re: re.Pattern[str]) -> collections.Counter[str]:
    counter: collections.Counter[str] = collections.Counter()
    name_re = re.compile(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b")
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        if not alias_re.search(text):
            continue
        for name in name_re.findall(text):
            if name in STOP_NAMES or any(part in STOP_NAMES for part in name.split()) or len(name) < 3:
                continue
            if name.startswith(("The ", "This ", "Gate ", "Source ", "Raw ", "Mission ")):
                continue
            if any(word in name for word in ("Gate", "Mission", "Export", "Source", "Date", "Raw")):
                continue
            counter[name] += 1
    return counter


def status_is_complete(status: str) -> bool:
    s = status.lower()
    return "complete" in s and "mixed" not in s and "in-progress" not in s and "partial" not in s


def summarize_dates(missions: Iterable[Mission]) -> tuple[str, str]:
    dates = []
    for mission in missions:
        dates.extend(DATE_RE.findall(mission.dates))
    return (min(dates), max(dates)) if dates else ("unknown", "unknown")


def mission_sort_key(mission: Mission) -> tuple[str, str, str]:
    dates = DATE_RE.findall(mission.dates)
    first_date = min(dates) if dates else "9999-99-99"
    return (first_date, mission.gate, mission.title)


def markdown_link(path: Path, workspace: Path, line_no: int | None = None, base_dir: Path | None = None) -> str:
    label = rel(path, workspace)
    if base_dir:
        target = os.path.relpath(path.resolve(), base_dir.resolve())
    else:
        target = label
    suffix = f"#L{line_no}" if line_no else ""
    return f"[{label}]({target}{suffix})"


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "character"


def mission_stats_path(mission: Mission, character: str, workspace: Path) -> Path:
    if mission.summary_path:
        gate_root = mission.summary_path.parent.parent
        stem = mission.summary_path.stem
    else:
        gate_slug = slugify(mission.gate)
        gate_root = workspace / "campaigns" / "the-gates" / "gates" / gate_slug
        stem = slugify(mission.title)
    return gate_root / "06-stats" / f"{stem}-{slugify(character)}-stats.md"


def count_evidence(evidence: Iterable[Evidence]) -> dict[str, collections.Counter[str]]:
    spell_counts: dict[str, collections.Counter[str]] = collections.defaultdict(collections.Counter)
    for item in evidence:
        spell_counts[item.spell][item.tag] += 1
    return spell_counts


def build_mission_stats(
    mission: Mission,
    workspace: Path,
    character: str,
    alias_re: re.Pattern[str],
    target_re: re.Pattern[str],
    actor_re: re.Pattern[str],
    speaker_re: re.Pattern[str] | None,
) -> MissionStats:
    summaries = [path for path in mission_summary_paths(mission) if path and path.exists()]
    raw_logs = [path for summary in summaries if (path := raw_log_from_summary(summary, workspace))]
    evidence: list[Evidence] = []
    for raw_log in raw_logs:
        evidence.extend(scan_file_for_evidence(raw_log, workspace, alias_re, target_re, actor_re, speaker_re, "raw"))
    return MissionStats(
        mission=mission,
        stats_path=mission_stats_path(mission, character, workspace),
        summaries=summaries,
        raw_logs=raw_logs,
        evidence=evidence,
        coappearances=extract_named_coappearances(summaries, alias_re),
    )


def render_mission_stats(
    stats: MissionStats,
    workspace: Path,
    campaign: Path,
    character: str,
    aliases: list[str],
    speakers: list[str],
) -> str:
    now = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
    mission = stats.mission
    spell_counts = count_evidence(stats.evidence)
    base_dir = stats.stats_path.parent
    lines = [
        f"# {character} Mission Stats: {mission.title}",
        "",
        f"Generated: {now}",
        "",
        "## Scope",
        "",
        f"- Campaign: `{rel(campaign, workspace)}`",
        f"- Source: {mission.source}",
        f"- Gate: {mission.gate}",
        f"- Dates: {mission.dates}",
        f"- Status: {mission.status}",
        f"- Character aliases: {', '.join([character, *aliases])}",
        f"- Message speakers: {', '.join(speakers) if speakers else 'not specified'}",
        "",
        "## Sources",
        "",
        "| Type | Link |",
        "|---|---|",
    ]
    if mission.summary_path and mission.summary_path.exists():
        lines.append(f"| Mission summary | {markdown_link(mission.summary_path, workspace, base_dir=base_dir)} |")
    for summary in stats.summaries:
        if summary != mission.summary_path:
            lines.append(f"| Split summary | {markdown_link(summary, workspace, base_dir=base_dir)} |")
    for raw_log in stats.raw_logs:
        lines.append(f"| Raw log | {markdown_link(raw_log, workspace, base_dir=base_dir)} |")
    if not stats.summaries and not stats.raw_logs:
        lines.append("| none | No linked summaries or raw logs found. |")

    lines.extend(
        [
            "",
            "## Spell And Action Counts",
            "",
            "| Spell or action | Confirmed | Probable | Uncertain | Total |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for spell, counts in sorted(spell_counts.items(), key=lambda kv: (-sum(kv[1].values()), kv[0])):
        confirmed = counts["confirmed"]
        probable = counts["probable"]
        uncertain = counts["uncertain"]
        total = confirmed + probable + uncertain
        lines.append(f"| {spell} | {confirmed} | {probable} | {uncertain} | {total} |")
    if not spell_counts:
        lines.append("| none | 0 | 0 | 0 | 0 |")

    lines.extend(["", "## Evidence", "", "| Spell or action | Tag | Source | Evidence |", "|---|---|---|---|"])
    for item in stats.evidence:
        source = markdown_link(item.path, workspace, item.line_no, base_dir=base_dir)
        snippet = item.line.replace("|", "\\|")
        if len(snippet) > 180:
            snippet = snippet[:177] + "..."
        lines.append(f"| {item.spell} | {item.tag} | {source} | {snippet} |")
    if not stats.evidence:
        lines.append("| none | - | - | No structured evidence found. |")

    lines.extend(["", "## Frequent Named Co-Appearances", "", "| Name | Mentions in scanned summaries |", "|---|---:|"])
    for name, count in stats.coappearances.most_common(25):
        lines.append(f"| {name} | {count} |")
    if not stats.coappearances:
        lines.append("| none | 0 |")

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- This is a per-mission sidecar. The campaign-level stats report aggregates these mission stats.",
            "- Counts come from structured raw-log action footers where available.",
            "- Split summaries are scanned instead of parent mixed archives when the mission summary declares split segments.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_report(
    workspace: Path,
    campaign: Path,
    character: str,
    aliases: list[str],
    speakers: list[str],
    index_path: Path,
    mission_stats: list[MissionStats],
    report_dir: Path | None = None,
) -> str:
    now = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
    missions = [stats.mission for stats in mission_stats]
    evidence = [item for stats in mission_stats for item in stats.evidence]
    coappearances: collections.Counter[str] = collections.Counter()
    for stats in mission_stats:
        coappearances.update(stats.coappearances)
    gate_counts = collections.Counter(m.gate for m in missions)
    status_counts = collections.Counter(m.status for m in missions)
    spell_counts = count_evidence(evidence)
    start_date, end_date = summarize_dates(missions)
    complete_count = sum(1 for m in missions if status_is_complete(m.status))
    mixed_count = sum(1 for m in missions if re.search(r"mixed|in-progress|partial", m.status, re.IGNORECASE))
    sorted_stats = sorted(mission_stats, key=lambda stats: mission_sort_key(stats.mission))

    lines = [
        f"# {character} Stats",
        "",
        f"Generated: {now}",
        "",
        "## Scope",
        "",
        f"- Campaign: `{rel(campaign, workspace)}`",
        f"- Mission index: {markdown_link(index_path, workspace, base_dir=report_dir)}",
        f"- Character aliases: {', '.join([character, *aliases])}",
        f"- Message speakers: {', '.join(speakers) if speakers else 'not specified'}",
        "- Evidence mode: confirmed/probable/uncertain counts are kept separate.",
        "",
        "## Mission List",
        "",
        "| Mission # | Source | Gate | Dates | Title | Status | Summary | Stats |",
        "|---:|---|---|---|---|---|---|---|",
    ]
    for index, stats in enumerate(sorted_stats, start=1):
        mission = stats.mission
        summary = (
            markdown_link(mission.summary_path, workspace, base_dir=report_dir)
            if mission.summary_path and mission.summary_path.exists()
            else mission.summary_label
        )
        stats_link = markdown_link(stats.stats_path, workspace, base_dir=report_dir)
        lines.append(
            f"| {index} | {mission.source} | {mission.gate} | "
            f"{mission.dates} | {mission.title} | {mission.status} | {summary} | {stats_link} |"
        )

    lines.extend(["", "## Spell And Action Counts", "", "| Spell or action | Confirmed | Probable | Uncertain | Total |", "|---|---:|---:|---:|---:|"])
    for spell, counts in sorted(spell_counts.items(), key=lambda kv: (-sum(kv[1].values()), kv[0])):
        confirmed = counts["confirmed"]
        probable = counts["probable"]
        uncertain = counts["uncertain"]
        total = confirmed + probable + uncertain
        lines.append(f"| {spell} | {confirmed} | {probable} | {uncertain} | {total} |")

    lines.extend(["", "## Frequent Named Co-Appearances", "", "| Name | Mentions in scanned summaries |", "|---|---:|"])
    for name, count in coappearances.most_common(25):
        lines.append(f"| {name} | {count} |")
    if not coappearances:
        lines.append("| none | 0 |")

    lines.extend(
        [
            "",
            "## Summary Metrics",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| Mission/archive rows | {len(missions)} |",
            f"| Confirmed complete mission rows | {complete_count} |",
            f"| Mixed, partial, or in-progress rows | {mixed_count} |",
            f"| Gates visited | {len(gate_counts)} |",
            f"| Date span | {start_date} to {end_date} |",
            f"| Spell/action evidence rows | {len(evidence)} |",
            "",
            "## Missions By Gate",
            "",
            "| Gate | Rows |",
            "|---|---:|",
        ]
    )
    for gate, count in sorted(gate_counts.items()):
        lines.append(f"| {gate} | {count} |")

    lines.extend(["", "## Mission Statuses", "", "| Status | Rows |", "|---|---:|"])
    for status, count in sorted(status_counts.items()):
        lines.append(f"| {status} | {count} |")

    fireballs = [item for item in evidence if item.spell == "Fireball"]
    lines.extend(["", "## Fireball Evidence", "", "| Tag | Source | Evidence |", "|---|---|---|"])
    for item in fireballs:
        source = markdown_link(item.path, workspace, item.line_no, base_dir=report_dir)
        snippet = item.line.replace("|", "\\|")
        if len(snippet) > 180:
            snippet = snippet[:177] + "..."
        lines.append(f"| {item.tag} | {source} | {snippet} |")
    if not fireballs:
        lines.append("| none | - | No Fireball evidence found. |")

    lines.extend(
        [
            "",
            "## Notes And Assumptions",
            "",
            "- Mission rows come from the mission index; detailed spell/action evidence comes from raw log action footers.",
            "- Campaign totals are aggregated from the per-mission stats sidecars linked in the mission list.",
            "- For The Gates logs, spell/action counts use structured lines beginning with `A`, `Action`, `BA`, `Bonus Action`, `R`, `Reaction`, `Precast`, `Perpetual Cast`, or `Wish Perpetual Cast`.",
            "- Crown of Stars is split into initial spell casts/precasts and later mote attacks.",
            "- Telekinetic Shove includes Telekinetic, Telekinetic Shove, and bare bonus-action shove footer lines.",
            "- Parent mixed archives remain in mission totals, but split segment files are preferred for detailed scans when available.",
            "- Dan / Simulacrus is merged into Don when provided as an alias.",
            "- Co-appearance names are heuristic and should be treated as a starting index, not a canon cast list.",
        ]
    )
    return "\n".join(lines) + "\n"


def run(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).resolve()
    campaign = (workspace / args.campaign).resolve() if not Path(args.campaign).is_absolute() else Path(args.campaign)
    index_path = (workspace / args.mission_index).resolve() if not Path(args.mission_index).is_absolute() else Path(args.mission_index)
    if not index_path.exists():
        raise SystemExit(f"Mission index not found: {index_path}")

    missions = parse_mission_index(index_path, workspace)
    alias_re = compile_alias_re(args.character, args.alias)
    target_re = alias_target_re(args.character, args.alias)
    actor_re = alias_actor_re(args.character, args.alias)
    speaker_re = compile_speaker_re(args.speaker)
    mission_stats = [
        build_mission_stats(mission, workspace, args.character, alias_re, target_re, actor_re, speaker_re)
        for mission in missions
    ]
    summaries = [summary for stats in mission_stats for summary in stats.summaries]
    raw_logs = [raw_log for stats in mission_stats for raw_log in stats.raw_logs]
    evidence = [item for stats in mission_stats for item in stats.evidence]

    if args.dry_run:
        print(f"mission_rows={len(missions)}")
        print(f"summary_files={len(summaries)}")
        print(f"raw_log_files={len(raw_logs)}")
        print(f"mission_stats_files={len(mission_stats)}")
        print(f"evidence_rows={len(evidence)}")
        fireballs = sum(1 for item in evidence if item.spell == "Fireball")
        print(f"fireball_evidence_rows={fireballs}")
        return 0

    output = (workspace / args.output).resolve() if args.output and not Path(args.output).is_absolute() else Path(args.output)
    for stats in mission_stats:
        stats.stats_path.parent.mkdir(parents=True, exist_ok=True)
        stats.stats_path.write_text(
            render_mission_stats(stats, workspace, campaign, args.character, args.alias, args.speaker),
            encoding="utf-8",
        )
    report = build_report(
        workspace,
        campaign,
        args.character,
        args.alias,
        args.speaker,
        index_path,
        mission_stats,
        output.parent,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")
    print(f"Wrote {output}")
    print(f"mission_stats_files={len(mission_stats)}")
    print(f"mission_rows={len(missions)} evidence_rows={len(evidence)}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True, help="Workspace root.")
    parser.add_argument("--campaign", required=True, help="Campaign path, relative to workspace or absolute.")
    parser.add_argument("--character", required=True, help="Character name.")
    parser.add_argument("--alias", action="append", default=[], help="Character alias; repeat as needed.")
    parser.add_argument("--speaker", action="append", default=[], help="Message speaker associated with the character; repeat as needed.")
    parser.add_argument("--mission-index", required=True, help="Mission index Markdown path.")
    parser.add_argument("--output", help="Output Markdown report path.")
    parser.add_argument("--dry-run", action="store_true", help="Print counts without writing a report.")
    args = parser.parse_args()
    if not args.dry_run and not args.output:
        parser.error("--output is required unless --dry-run is used")
    return args


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
