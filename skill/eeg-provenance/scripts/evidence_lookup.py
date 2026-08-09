#!/usr/bin/env python3
"""Return only requested entries from the EEG evidence register."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ENTRY_RE = re.compile(r'^<a id="(s\d{2})"></a>\s*$', re.IGNORECASE | re.MULTILINE)
FIELD_RE = re.compile(r"^- \*\*(Type / class|Source|Supports|Limits):\*\* (.+)$", re.MULTILINE)
DEFAULT_REGISTER = Path(__file__).resolve().parents[1] / "references" / "evidence-register.md"


def load_entries(register: Path = DEFAULT_REGISTER) -> dict[str, str]:
    """Parse evidence sections without loading unrelated entries into output."""

    text = register.read_text(encoding="utf-8")
    matches = list(ENTRY_RE.finditer(text))
    entries: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        entries[match.group(1).upper()] = text[match.start() : end].strip()
    return entries


def entry_record(source_id: str, section: str) -> dict[str, str]:
    """Convert one canonical Markdown section into a compact JSON record."""

    heading = next(
        (line.removeprefix("## ") for line in section.splitlines() if line.startswith("## ")),
        source_id,
    )
    fields = {name.casefold().replace(" / ", "_").replace(" ", "_"): value for name, value in FIELD_RE.findall(section)}
    return {"id": source_id, "title": heading, **fields}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ids", nargs="+", help="Evidence IDs such as S03 S20 S52")
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output selected canonical sections or compact JSON records.",
    )
    parser.add_argument("--register", type=Path, default=DEFAULT_REGISTER)
    args = parser.parse_args(argv)

    try:
        entries = load_entries(args.register)
    except OSError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    requested = [source_id.upper() for source_id in args.ids]
    missing = [source_id for source_id in requested if source_id not in entries]
    if missing:
        print(f"ERROR: unknown evidence ID(s): {', '.join(missing)}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps([entry_record(source_id, entries[source_id]) for source_id in requested], indent=2))
    else:
        print("\n\n".join(entries[source_id] for source_id in requested))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
