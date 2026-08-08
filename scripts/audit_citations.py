#!/usr/bin/env python3
"""Audit evidence-register integrity and citations on scientific/normative lines."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SOURCE_ID_RE = re.compile(r'<a id="(s\d{2})"></a>', re.IGNORECASE)
CITATION_RE = re.compile(r"\[\[(S\d{2})\]\]\(([^)]+)#(s\d{2})\)", re.IGNORECASE)
CLAIM_RE = re.compile(
    r"\b(?:must|should|shall|never|do not|cannot|requires?|depends?|affects?|changes?|"
    r"improve|inflates?|distort|filter(?:ing|ed|s)?|reference|interpolat\w*|channel|"
    r"electrode|rank|event|sampling|artifact|provenance|BIDS|EEG|MNE|EEGLAB|ICA|ASR)\b",
    re.IGNORECASE,
)


def _scientific_lines(path: Path) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    in_fence = False
    in_frontmatter = False
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = raw.strip()
        if number == 1 and stripped == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if stripped == "---":
                in_frontmatter = False
            continue
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not stripped or stripped.startswith(("#", "<!--")):
            continue
        if stripped.startswith(("Use [", "- Use [")):
            continue
        if stripped.startswith("|") and "[[" not in stripped:
            continue
        if stripped.startswith("|") and set(stripped) <= {"|", "-", ":", " "}:
            continue
        if CLAIM_RE.search(stripped):
            lines.append((number, stripped))
    return lines


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
        errors.append(f"evidence source anchors must be ordered and contiguous: expected {expected}")
    for anchor in anchors:
        start = register_text.find(f'<a id="{anchor}"></a>')
        next_start = register_text.find('<a id="s', start + 1)
        section = register_text[start : next_start if next_start >= 0 else None]
        for field in ("**Type / class:**", "**Source:**", "**Supports:**", "**Limits:**"):
            if field not in section:
                errors.append(f"{anchor.upper()}: missing {field}")

    files = [root / "SKILL.md"] + sorted((root / "references").glob("*.md"))
    for path in files:
        if path == register:
            continue
        text = path.read_text(encoding="utf-8")
        for match in CITATION_RE.finditer(text):
            source_id, target, anchor = match.groups()
            if source_id.casefold() != anchor.casefold():
                errors.append(f"{path.relative_to(root)}: citation ID/anchor mismatch: {match.group(0)}")
            if anchor.casefold() not in anchor_set:
                errors.append(f"{path.relative_to(root)}: unknown evidence ID {source_id}")
            if Path(target).name.casefold() != "evidence-register.md":
                errors.append(f"{path.relative_to(root)}: citation does not target evidence-register.md: {match.group(0)}")
        for line_number, line in _scientific_lines(path):
            if not CITATION_RE.search(line):
                errors.append(f"{path.relative_to(root)}:{line_number}: uncited scientific/normative line: {line}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
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
