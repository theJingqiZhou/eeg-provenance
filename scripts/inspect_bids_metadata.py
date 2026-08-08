#!/usr/bin/env python3
"""Read BIDS EEG sidecars and print a provenance-oriented JSON intake summary."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
from collections import Counter
from pathlib import Path
from typing import Any


def _inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        rows = list(reader)
        return list(reader.fieldnames or []), rows


def _file_record(path: Path, root: Path) -> dict[str, Any]:
    relative = path.relative_to(root).as_posix()
    record: dict[str, Any] = {
        "relative_path": relative,
        "bytes": path.stat().st_size,
        "sha256": _sha256(path),
    }
    if path.suffix.casefold() == ".json":
        record["content"] = _read_json(path)
    elif path.suffix.casefold() == ".tsv":
        columns, rows = _read_tsv(path)
        record["columns"] = columns
        record["row_count"] = len(rows)
        if path.name.endswith("_channels.tsv"):
            record["summary"] = {
                "types": dict(Counter(row.get("type", "") for row in rows)),
                "units": dict(Counter(row.get("units", "") for row in rows)),
                "statuses": dict(Counter(row.get("status", "") for row in rows)),
                "names": [row.get("name", "") for row in rows],
            }
        elif path.name.endswith("_events.tsv"):
            record["summary"] = {
                "trial_types": dict(Counter(row.get("trial_type", "") for row in rows))
                if "trial_type" in columns
                else {},
                "missing_onset_count": sum(row.get("onset", "").casefold() in {"", "n/a"} for row in rows),
            }
    return record


def _candidate_sidecars(root: Path, recording: str | None, max_recordings: int) -> list[Path]:
    candidates: set[Path] = set()
    description = root / "dataset_description.json"
    if description.is_file():
        candidates.add(description)
    participants = root / "participants.tsv"
    if participants.is_file():
        candidates.add(participants)

    if recording:
        relative = Path(recording.replace("\\", "/"))
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("--recording must be a safe path relative to the dataset root")
        base = (root / relative).resolve(strict=False)
        if not _inside(base, root):
            raise ValueError("--recording resolves outside the dataset root")
        name = base.name
        if name.endswith("_eeg"):
            stem = name
        else:
            stem = f"{name}_eeg"
        target_entities = set(stem.removesuffix("_eeg").split("_"))
        parent = base.parent
        exact_names = {
            f"{stem}.json",
            f"{stem.replace('_eeg', '_channels')}.tsv",
            f"{stem.replace('_eeg', '_events')}.tsv",
            f"{stem.replace('_eeg', '_events')}.json",
        }
        subject_prefix = stem.split("_task-")[0]
        exact_names.update(
            {
                f"{subject_prefix}_electrodes.tsv",
                f"{subject_prefix}_coordsystem.json",
            }
        )
        for filename in exact_names:
            path = parent / filename
            if path.is_file():
                candidates.add(path)
        for ancestor in [parent, *parent.parents]:
            if not _inside(ancestor, root):
                break
            for path in ancestor.glob("*_eeg.json"):
                candidate_entities = set(path.stem.removesuffix("_eeg").split("_"))
                if path.is_file() and candidate_entities <= target_entities:
                    candidates.add(path)
    else:
        patterns = ("*_eeg.json", "*_channels.tsv", "*_electrodes.tsv", "*_coordsystem.json", "*_events.tsv", "*_events.json")
        eeg_sidecars = sorted(root.rglob("*_eeg.json"))
        if len(eeg_sidecars) > max_recordings:
            raise ValueError(
                f"found {len(eeg_sidecars)} EEG sidecars; use --recording or raise --max-recordings"
            )
        for pattern in patterns:
            candidates.update(path for path in root.rglob(pattern) if path.is_file())
    return sorted(candidates, key=lambda path: path.relative_to(root).as_posix())


def inspect_dataset(root: Path, recording: str | None = None, max_recordings: int = 100) -> dict[str, Any]:
    resolved = root.resolve(strict=True)
    if not resolved.is_dir():
        raise ValueError(f"dataset root is not a directory: {resolved}")
    description = resolved / "dataset_description.json"
    if not description.is_file():
        raise ValueError("dataset_description.json is required for a BIDS dataset intake")
    files = _candidate_sidecars(resolved, recording, max_recordings)
    stat_before = {path: (path.stat().st_size, path.stat().st_mtime_ns) for path in files}
    records = [_file_record(path, resolved) for path in files]
    stat_after = {path: (path.stat().st_size, path.stat().st_mtime_ns) for path in files}
    if stat_before != stat_after:
        raise RuntimeError("a source sidecar changed during inspection")
    description_content = _read_json(description)
    return {
        "inspector": "eeg-provenance/inspect_bids_metadata.py",
        "mode": "metadata-only-read",
        "source_root": os.fspath(resolved),
        "recording_filter": recording,
        "dataset": {
            key: description_content.get(key)
            for key in (
                "Name",
                "BIDSVersion",
                "DatasetType",
                "License",
                "DatasetDOI",
                "GeneratedBy",
                "SourceDatasets",
                "DatasetLinks",
            )
            if key in description_content
        },
        "files": records,
        "signal_payload_read": False,
        "writes_performed": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset_root", type=Path)
    parser.add_argument("--recording", help="Relative recording prefix ending in _eeg")
    parser.add_argument("--max-recordings", type=int, default=100)
    args = parser.parse_args(argv)
    try:
        report = inspect_dataset(args.dataset_root, args.recording, args.max_recordings)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError, csv.Error) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
