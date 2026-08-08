#!/usr/bin/env python3
"""Acquire EEGDash metadata or profile one cached recording without transforming it."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import math
import os
import re
import sys
import warnings
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


class IntakeError(RuntimeError):
    """A bounded-intake safeguard or acquisition requirement was not met."""


def _jsonable(value: Any) -> Any:
    """Convert common scientific-Python values into strict JSON values."""
    if value is None or isinstance(value, (str, int, bool)):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_jsonable(item) for item in value]
    if hasattr(value, "item"):
        try:
            return _jsonable(value.item())
        except (TypeError, ValueError):
            pass
    if hasattr(value, "to_dict"):
        return _jsonable(value.to_dict())
    return str(value)


def validate_cache_dir(
    cache_dir: str | Path, protected_sources: Iterable[str | Path] = ()
) -> Path:
    """Resolve a cache and reject known archive roots or protected source trees."""
    supplied = str(cache_dir).replace("\\", "/").casefold()
    resolved = Path(cache_dir).expanduser().resolve()
    normalized = str(resolved).replace("\\", "/").casefold().rstrip("/")
    drive = resolved.drive.casefold()
    if (
        drive == "x:"
        or supplied == "x:"
        or supplied.startswith("x:/")
        or normalized == "/mnt/x"
        or normalized.startswith("/mnt/x/")
    ):
        raise IntakeError("Refusing to use the read-only X: archive as an EEGDash cache")

    for source in protected_sources:
        protected = Path(source).expanduser().resolve()
        try:
            resolved.relative_to(protected)
        except ValueError:
            continue
        raise IntakeError(f"Cache must be outside protected source tree: {protected}")
    return resolved


def build_filters(
    dataset: str,
    *,
    subject: str | None = None,
    session: str | None = None,
    task: str | None = None,
    run: str | None = None,
) -> dict[str, str]:
    """Build an exact EEGDash/BIDS-entity query without inventing entities."""
    dataset = dataset.strip()
    if not re.fullmatch(r"(?:ds|nm|on)\d{6}|EEG[A-Za-z0-9_-]+", dataset):
        raise IntakeError(f"Unsupported or malformed EEGDash dataset identifier: {dataset!r}")
    filters = {"dataset": dataset}
    for key, value in {
        "subject": subject,
        "session": session,
        "task": task,
        "run": run,
    }.items():
        if value is not None and str(value).strip():
            filters[key] = str(value).strip()
    return filters


def require_bounded_recording(filters: dict[str, str]) -> None:
    """Require enough selectors before any signal-bearing operation."""
    missing = [key for key in ("subject", "task") if key not in filters]
    if missing:
        raise IntakeError(
            "Signal access requires exact subject and task selectors; missing "
            + ", ".join(missing)
        )


def software_versions() -> dict[str, str | None]:
    """Return the installed versions material to this intake."""
    versions: dict[str, str | None] = {"python": sys.version.split()[0]}
    for distribution in ("eegdash", "mne", "mne-bids", "numpy", "scipy"):
        try:
            versions[distribution] = importlib.metadata.version(distribution)
        except importlib.metadata.PackageNotFoundError:
            versions[distribution] = None
    return versions


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _file_identity(path: Path, root: Path) -> dict[str, Any]:
    return {
        "path": path.relative_to(root).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": _sha256(path),
    }


def _git_head(dataset_root: Path) -> str | None:
    git_dir = dataset_root / ".git"
    if git_dir.is_file():
        match = re.search(r"gitdir:\s*(.+)", git_dir.read_text(encoding="utf-8"))
        if not match:
            return None
        git_dir = (dataset_root / match.group(1).strip()).resolve()
    head = git_dir / "HEAD"
    if not head.is_file():
        return None
    value = head.read_text(encoding="utf-8").strip()
    if value.startswith("ref: "):
        ref = git_dir / value[5:]
        return ref.read_text(encoding="utf-8").strip() if ref.is_file() else None
    return value or None


def _brainvision_companions(header: Path) -> list[Path]:
    companions: list[Path] = []
    if header.suffix.casefold() != ".vhdr" or not header.is_file():
        return companions
    text = header.read_text(encoding="utf-8-sig", errors="replace")
    for field in ("DataFile", "MarkerFile"):
        match = re.search(rf"^{field}=(.+)$", text, flags=re.MULTILINE)
        if match:
            candidate = header.with_name(match.group(1).strip())
            if candidate.is_file():
                companions.append(candidate)
    return companions


def source_identity(dataset_root: Path, raw: Any, record: dict[str, Any] | None) -> dict[str, Any]:
    """Hash the MNE-reported payloads and primary dataset descriptor."""
    paths: list[Path] = []
    root = dataset_root.resolve()
    if record:
        relpath = record.get("bids_relpath")
        if relpath:
            primary = root / str(relpath)
            if primary.is_file():
                paths.append(primary)
                paths.extend(_brainvision_companions(primary))
                entity_prefix = re.sub(r"_eeg(?:\.[^.]+)?$", "", primary.name)
                paths.extend(
                    path
                    for path in primary.parent.glob(f"{entity_prefix}_*")
                    if path.is_file()
                )
        task = (record.get("entities") or {}).get("task")
        if task:
            inherited_events = root / f"task-{task}_events.json"
            if inherited_events.is_file():
                paths.append(inherited_events)
    for filename in raw.filenames or []:
        if filename:
            path = Path(filename).absolute()
            if path.is_file():
                try:
                    relative = path.relative_to(root)
                except ValueError:
                    continue
                if ".git" not in relative.parts:
                    paths.append(path)
                    paths.extend(_brainvision_companions(path))
    for name in ("participants.tsv", "participants.json"):
        participant_file = root / name
        if participant_file.is_file():
            paths.append(participant_file)
    descriptor = dataset_root / "dataset_description.json"
    if descriptor.is_file():
        paths.append(descriptor.absolute())

    unique: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        if path in seen:
            continue
        try:
            path.relative_to(root)
        except ValueError:
            raise IntakeError(f"MNE resolved a payload outside the dataset cache: {path}")
        seen.add(path)
        unique.append(path)

    description = None
    if descriptor.is_file():
        description = json.loads(descriptor.read_text(encoding="utf-8"))
    return {
        "dataset_root": str(dataset_root.resolve()),
        "git_commit": _git_head(dataset_root),
        "dataset_description": description,
        "files": [_file_identity(path, root) for path in unique],
    }


def _quantiles(values: Any) -> dict[str, float] | None:
    import numpy as np

    finite = np.asarray(values, dtype=float)
    finite = finite[np.isfinite(finite)]
    if not finite.size:
        return None
    points = np.quantile(finite, [0.0, 0.05, 0.5, 0.95, 1.0])
    return {
        "min": float(points[0]),
        "p05": float(points[1]),
        "median": float(points[2]),
        "p95": float(points[3]),
        "max": float(points[4]),
    }


def _sample_raw(raw: Any, seconds: float) -> tuple[Any, list[Any], list[dict[str, int]]]:
    import numpy as np

    sfreq = float(raw.info["sfreq"])
    length = min(raw.n_times, max(1, int(round(seconds * sfreq))))
    starts = sorted({0, max(0, (raw.n_times - length) // 2), max(0, raw.n_times - length)})
    windows = []
    plan = []
    for start in starts:
        stop = min(raw.n_times, start + length)
        windows.append(raw.get_data(start=start, stop=stop))
        plan.append({"start_sample": start, "stop_sample": stop})
    return np.concatenate(windows, axis=1), windows, plan


def _line_noise_summary(raw: Any, windows: list[Any], channel_types: list[str]) -> dict[str, Any] | None:
    import numpy as np
    from scipy.signal import welch

    line_freq = raw.info.get("line_freq")
    if line_freq is None or not math.isfinite(float(line_freq)):
        return None
    eeg_picks = [index for index, kind in enumerate(channel_types) if kind == "eeg"]
    if not eeg_picks:
        return None
    sfreq = float(raw.info["sfreq"])
    segment_powers = []
    frequencies = None
    for window in windows:
        nperseg = min(window.shape[1], max(8, int(round(2 * sfreq))))
        frequencies, power = welch(window[eeg_picks], fs=sfreq, nperseg=nperseg, axis=1)
        segment_powers.append(power)
    if frequencies is None:
        return None
    power = np.mean(segment_powers, axis=0)
    line = float(line_freq)
    line_mask = np.abs(frequencies - line) <= 0.5
    neighbor_mask = ((frequencies >= line - 3) & (frequencies <= line - 1)) | (
        (frequencies >= line + 1) & (frequencies <= line + 3)
    )
    if not line_mask.any() or not neighbor_mask.any():
        return None
    line_power = np.mean(power[:, line_mask], axis=1)
    neighbor_power = np.mean(power[:, neighbor_mask], axis=1)
    ratio_db = 10 * np.log10(np.maximum(line_power, np.finfo(float).tiny) / np.maximum(neighbor_power, np.finfo(float).tiny))
    return {
        "line_frequency_hz": line,
        "line_to_neighbor_db_across_eeg_channels": _quantiles(ratio_db),
        "interpretation": "descriptive sampled-window ratio; no pass/fail threshold applied",
    }


def profile_raw(raw: Any, *, sample_seconds: float = 10.0) -> dict[str, Any]:
    """Profile structure, geometry, events, and bounded signal samples."""
    import numpy as np

    data, sampled_windows, windows = _sample_raw(raw, sample_seconds)
    channel_types = list(raw.get_channel_types())
    type_counts = dict(sorted(Counter(channel_types).items()))
    finite = np.isfinite(data)
    eeg_picks = [index for index, kind in enumerate(channel_types) if kind == "eeg"]
    eeg_data_uv = data[eeg_picks] * 1e6 if eeg_picks else np.empty((0, data.shape[1]))
    peak_to_peak = np.ptp(eeg_data_uv, axis=1) if eeg_picks else np.array([])
    medians = np.median(eeg_data_uv, axis=1, keepdims=True) if eeg_picks else np.empty((0, 1))
    mad = np.median(np.abs(eeg_data_uv - medians), axis=1) if eeg_picks else np.array([])

    eeg_positions_present = 0
    for channel, kind in zip(raw.info["chs"], channel_types, strict=True):
        if kind != "eeg":
            continue
        position = np.asarray(channel["loc"][:3], dtype=float)
        if np.all(np.isfinite(position)) and not np.allclose(position, 0.0):
            eeg_positions_present += 1

    annotations = raw.annotations
    descriptions = [str(value) for value in annotations.description]
    onsets = np.asarray(annotations.onset, dtype=float)
    durations = np.asarray(annotations.duration, dtype=float)
    recording_end = float(raw.times[-1]) if raw.n_times else 0.0
    out_of_bounds = int(np.sum((onsets < 0) | ((onsets + durations) > recording_end + 1 / float(raw.info["sfreq"]))))

    sampled_rank = None
    if eeg_picks:
        matrix = eeg_data_uv - np.mean(eeg_data_uv, axis=1, keepdims=True)
        sampled_rank = int(np.linalg.matrix_rank(matrix))

    flat_names = [
        raw.ch_names[pick]
        for pick, spread in zip(eeg_picks, peak_to_peak, strict=True)
        if spread == 0
    ]

    return {
        "structure": {
            "mne_raw_type": type(raw).__name__,
            "sampling_frequency_hz": float(raw.info["sfreq"]),
            "channels": int(raw.info["nchan"]),
            "channel_type_counts": type_counts,
            "samples": int(raw.n_times),
            "duration_seconds": recording_end,
            "highpass_hz": float(raw.info["highpass"]),
            "lowpass_hz": float(raw.info["lowpass"]),
            "line_frequency_hz": _jsonable(raw.info.get("line_freq")),
            "bads": list(raw.info["bads"]),
            "projectors": len(raw.info["projs"]),
        },
        "geometry": {
            "eeg_channels": len(eeg_picks),
            "eeg_channels_with_finite_nonzero_position": eeg_positions_present,
            "eeg_channels_without_position": len(eeg_picks) - eeg_positions_present,
        },
        "annotations": {
            "count": len(annotations),
            "description_counts": dict(sorted(Counter(descriptions).items())),
            "onsets_monotonic": bool(np.all(np.diff(onsets) >= 0)) if len(onsets) > 1 else True,
            "out_of_bounds_count": out_of_bounds,
        },
        "bounded_signal_sample": {
            "windows": windows,
            "requested_seconds_per_window": sample_seconds,
            "values": int(data.size),
            "nonfinite_values": int(data.size - finite.sum()),
            "eeg_peak_to_peak_uv_across_channels": _quantiles(peak_to_peak),
            "eeg_mad_uv_across_channels": _quantiles(mad),
            "flat_eeg_channels_in_sample": flat_names,
            "sampled_numeric_eeg_rank": sampled_rank,
            "rank_warning": "sampled numerical matrix rank is diagnostic, not a covariance or forward-model rank claim",
            "line_noise": _line_noise_summary(raw, sampled_windows, channel_types),
            "not_assessed": [
                "ADC clipping without device range or integer counts",
                "scientific acceptability without endpoint-specific thresholds",
            ],
        },
    }


def _warning_messages(caught: list[warnings.WarningMessage]) -> list[dict[str, str]]:
    return [
        {"category": item.category.__name__, "message": str(item.message)}
        for item in caught
    ]


def record_raw_conflicts(record: dict[str, Any] | None, raw: Any) -> list[dict[str, Any]]:
    """Expose catalogue/local-discovery fields that disagree with the loaded object."""
    if not record:
        return []
    comparisons = {
        "nchans": (record.get("nchans"), int(raw.info["nchan"])),
        "ntimes": (record.get("ntimes"), int(raw.n_times)),
        "sampling_frequency": (record.get("sampling_frequency"), float(raw.info["sfreq"])),
        "ch_names_length": (
            len(record["ch_names"]) if isinstance(record.get("ch_names"), list) else None,
            len(raw.ch_names),
        ),
    }
    conflicts = []
    for field, (record_value, raw_value) in comparisons.items():
        if record_value is None:
            continue
        if isinstance(raw_value, float):
            differs = not math.isclose(float(record_value), raw_value, rel_tol=0, abs_tol=1e-9)
        else:
            differs = int(record_value) != raw_value
        if differs:
            conflicts.append(
                {"field": field, "record_value": record_value, "loaded_raw_value": raw_value}
            )
    return conflicts


def catalogue_only(filters: dict[str, str]) -> dict[str, Any]:
    """Query at most two records so ambiguity is visible without downloading samples."""
    from eegdash import EEGDash

    records = list(EEGDash().find(filters, limit=2))
    return {
        "status": "one_match" if len(records) == 1 else ("no_match" if not records else "ambiguous"),
        "records_returned": len(records),
        "records": _jsonable(records),
        "signal_bytes_downloaded": False,
    }


def _load_one(
    cache_dir: Path,
    filters: dict[str, str],
    *,
    download: bool,
    sample_seconds: float,
) -> dict[str, Any]:
    from eegdash import EEGDashDataset

    require_bounded_recording(filters)
    if download and filters["dataset"].startswith(("nm", "on")):
        raise IntakeError(
            "EEGDash 0.8.4 marks NeMAR storage as non-fetchable; retrieve exact annex "
            "objects into a separate cache, then use --offline-qc"
        )
    if download:
        cache_dir.mkdir(parents=True, exist_ok=True)
    elif not (cache_dir / filters["dataset"]).is_dir():
        raise IntakeError(f"Offline dataset cache is absent: {cache_dir / filters['dataset']}")

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        dataset = EEGDashDataset(
            cache_dir=cache_dir,
            download=download,
            n_jobs=1,
            **filters,
        )
        count = len(dataset.datasets)
        if count != 1:
            raise IntakeError(f"Expected exactly one recording, EEGDash selected {count}")
        recording = dataset.datasets[0]
        raw = recording.raw
        if raw is None:
            raise IntakeError("EEGDash returned no MNE Raw object for the selected recording")
        qc = profile_raw(raw, sample_seconds=sample_seconds)

    dataset_root = cache_dir / filters["dataset"]
    record = getattr(recording, "record", None)
    return {
        "status": "profiled",
        "recordings": 1,
        "description": _jsonable(recording.description),
        "record": _jsonable(record),
        "record_vs_loaded_raw_conflicts": record_raw_conflicts(record, raw),
        "source_identity": source_identity(dataset_root, raw, record),
        "qc": qc,
        "warnings": _warning_messages(caught),
        "signal_bytes_downloaded": download,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--subject")
    parser.add_argument("--session")
    parser.add_argument("--task")
    parser.add_argument("--run")
    parser.add_argument("--cache-dir", type=Path)
    parser.add_argument("--protected-source", action="append", default=[])
    parser.add_argument("--sample-seconds", type=float, default=10.0)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--catalogue-only", action="store_true")
    mode.add_argument("--download-one", action="store_true")
    mode.add_argument("--offline-qc", action="store_true")
    args = parser.parse_args(argv)
    if args.sample_seconds <= 0 or args.sample_seconds > 60:
        parser.error("--sample-seconds must be in (0, 60]")
    if not args.catalogue_only and args.cache_dir is None:
        parser.error("--cache-dir is required for signal-bearing modes")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report: dict[str, Any] = {
        "schema_version": 1,
        "software": software_versions(),
        "request": {},
    }
    try:
        filters = build_filters(
            args.dataset,
            subject=args.subject,
            session=args.session,
            task=args.task,
            run=args.run,
        )
        report["request"]["filters"] = filters
        if args.catalogue_only:
            report["mode"] = "catalogue_only"
            report.update(catalogue_only(filters))
        else:
            cache_dir = validate_cache_dir(args.cache_dir, args.protected_source)
            report["request"]["cache_dir"] = str(cache_dir)
            report["mode"] = "download_one" if args.download_one else "offline_qc"
            report.update(
                _load_one(
                    cache_dir,
                    filters,
                    download=args.download_one,
                    sample_seconds=args.sample_seconds,
                )
            )
        print(json.dumps(_jsonable(report), indent=2, sort_keys=True, allow_nan=False))
        return 0
    except Exception as exc:
        report.update(
            {
                "status": "error",
                "error_type": type(exc).__name__,
                "error": str(exc),
            }
        )
        print(json.dumps(_jsonable(report), indent=2, sort_keys=True, allow_nan=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
