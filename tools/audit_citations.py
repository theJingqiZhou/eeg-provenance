#!/usr/bin/env python3
"""Audit the evidence register and block-level scientific citations."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SOURCE_ID_RE = re.compile(r'<a id="(s\d{2})"></a>', re.IGNORECASE)
CITATION_RE = re.compile(r"\[\[(S\d{2})\]\]\(([^)]+)#(s\d{2})\)", re.IGNORECASE)
EVIDENCE_TEXT_RE = re.compile(r"Evidence:\s*([^\n)]*)", re.IGNORECASE)
EVIDENCE_TABLE_RE = re.compile(
    r"^\|\s*Evidence\s*\|\s*([^|]+)\|", re.IGNORECASE | re.MULTILINE
)
ID_RANGE_RE = re.compile(r"S(\d{2})(?:\s*[–-]\s*S?(\d{2}))?", re.IGNORECASE)
CLAIM_RE = re.compile(
    r"\b(?:must|should|shall|never|do not|cannot|requires?|depends?|affects?|changes?|"
    r"improve|inflates?|distort|filter(?:ing|ed|s)?|reference|interpolat\w*|channel|"
    r"electrode|rank|event|sampling|artifact|provenance|BIDS|EEG|MNE|EEGLAB|ICA|ASR)\b",
    re.IGNORECASE,
)
DEFAULT_SKILL_ROOT = Path(__file__).resolve().parents[1] / "skill" / "eeg-provenance"


def _expand_ids(value: str) -> set[str]:
    ids: set[str] = set()
    for match in ID_RANGE_RE.finditer(value):
        start = int(match.group(1))
        end = int(match.group(2) or match.group(1))
        if end < start:
            start, end = end, start
        ids.update(f"S{number:02d}" for number in range(start, end + 1))
    return ids


def _declared_ids(text: str) -> set[str]:
    ids = {match.group(1).upper() for match in CITATION_RE.finditer(text)}
    for match in EVIDENCE_TEXT_RE.finditer(text):
        ids.update(_expand_ids(match.group(1)))
    for match in EVIDENCE_TABLE_RE.finditer(text):
        ids.update(_expand_ids(match.group(1)))
    return ids


def _markdown_blocks(path: Path) -> list[tuple[int, str]]:
    """Return prose/list/table blocks while excluding metadata and code."""

    blocks: list[tuple[int, str]] = []
    current: list[str] = []
    start = 0
    in_fence = False
    in_frontmatter = False

    def flush() -> None:
        nonlocal current, start
        if current:
            blocks.append((start, "\n".join(current)))
            current = []
            start = 0

    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = raw.strip()
        if number == 1 and stripped == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if stripped == "---":
                in_frontmatter = False
            continue
        if stripped.startswith("```"):
            flush()
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not stripped or stripped.startswith(("#", "<!--")):
            flush()
            continue
        if not current:
            start = number
        current.append(stripped)
    flush()
    return blocks


def audit(root: Path) -> list[str]:
    errors: list[str] = []
    register = root / "references" / "evidence-register.md"
    if not register.is_file():
        return ["references/evidence-register.md is missing"]

    register_text = register.read_text(encoding="utf-8")
    anchors = [match.lower() for match in SOURCE_ID_RE.findall(register_text)]
    anchor_set = set(anchors)
    if len(anchors) != len(anchor_set):
        errors.append("evidence register contains duplicate source anchors")
    expected = [f"s{index:02d}" for index in range(1, len(anchors) + 1)]
    if anchors != expected:
        errors.append(
            f"evidence source anchors must be ordered and contiguous: expected {expected}"
        )
    for anchor in anchors:
        start = register_text.find(f'<a id="{anchor}"></a>')
        next_start = register_text.find('<a id="s', start + 1)
        section = register_text[start : next_start if next_start >= 0 else None]
        for field in ("**Type / class:**", "**Source:**", "**Supports:**", "**Limits:**"):
            if field not in section:
                errors.append(f"{anchor.upper()}: missing {field}")

    files = [root / "SKILL.md"] + sorted((root / "references").glob("*.md"))
    registered = {anchor.upper() for anchor in anchors}
    for path in files:
        if path == register:
            continue
        text = path.read_text(encoding="utf-8")
        for match in CITATION_RE.finditer(text):
            source_id, target, anchor = match.groups()
            if source_id.casefold() != anchor.casefold():
                errors.append(
                    f"{path.relative_to(root)}: citation ID/anchor mismatch: {match.group(0)}"
                )
            if Path(target).name.casefold() != "evidence-register.md":
                errors.append(
                    f"{path.relative_to(root)}: citation does not target evidence-register.md: {match.group(0)}"
                )

        declared = _declared_ids(text)
        for source_id in sorted(declared - registered):
            errors.append(f"{path.relative_to(root)}: unknown evidence ID {source_id}")

        blocks = _markdown_blocks(path)
        for index, (line_number, block) in enumerate(blocks):
            block_lines = block.splitlines()
            if all(
                re.fullmatch(r"- \[[^]]+\]\(#[^)]+\)", line)
                for line in block_lines
            ):
                continue
            if block.startswith("| Topic |") and "PDF pages" in block_lines[0]:
                continue
            if not CLAIM_RE.search(block) or _declared_ids(block):
                continue
            next_block = blocks[index + 1][1] if index + 1 < len(blocks) else ""
            if next_block.casefold().startswith("evidence:") and _declared_ids(next_block):
                continue
            if all(line.startswith(("Use [", "- Use [")) for line in block.splitlines()):
                continue
            errors.append(
                f"{path.relative_to(root)}:{line_number}: "
                f"uncited scientific/normative block: {block}"
            )
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_SKILL_ROOT)
    args = parser.parse_args(argv)
    errors = audit(args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Citation audit failed: {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("Citation audit passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
