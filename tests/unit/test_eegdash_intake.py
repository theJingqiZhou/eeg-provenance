from pathlib import Path

import mne
import numpy as np
import pytest
from scripts.eegdash_intake import (
    IntakeError,
    build_filters,
    profile_raw,
    record_raw_conflicts,
    require_bounded_recording,
    validate_cache_dir,
)


def test_cache_guard_rejects_archive_and_protected_source(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    with pytest.raises(IntakeError, match="outside protected"):
        validate_cache_dir(source / "cache", [source])

    assert validate_cache_dir(tmp_path / "derivative", [source]) == (
        tmp_path / "derivative"
    ).resolve()


def test_bounded_filters_are_explicit() -> None:
    filters = build_filters(
        "ds003061", subject="001", task="P300", run="1"
    )
    assert filters == {
        "dataset": "ds003061",
        "subject": "001",
        "task": "P300",
        "run": "1",
    }
    require_bounded_recording(filters)
    assert build_filters("nm000133", subject="01", task="rest") == {
        "dataset": "nm000133",
        "subject": "01",
        "task": "rest",
    }
    assert build_filters("on002724", subject="01", task="rest") == {
        "dataset": "on002724",
        "subject": "01",
        "task": "rest",
    }
    with pytest.raises(IntakeError, match="subject and task"):
        require_bounded_recording({"dataset": "ds003061", "subject": "001"})
    with pytest.raises(IntakeError, match="malformed"):
        build_filters("../../archive")


def test_profile_raw_is_bounded_and_descriptive() -> None:
    sfreq = 256.0
    times = np.arange(int(8 * sfreq)) / sfreq
    data = np.vstack(
        [
            10e-6 * np.sin(2 * np.pi * 10 * times),
            4e-6 * np.sin(2 * np.pi * 12 * times),
            np.zeros(times.size),
        ]
    )
    raw = mne.io.RawArray(
        data,
        mne.create_info(["Fz", "Cz", "EOG"], sfreq, ["eeg", "eeg", "eog"]),
        verbose=False,
    )
    raw.info["line_freq"] = 50.0
    raw.set_montage("standard_1020")
    raw.set_annotations(mne.Annotations([1.0, 2.0], [0.0, 0.0], ["a", "b"]))

    report = profile_raw(raw, sample_seconds=1.0)
    assert report["structure"]["channel_type_counts"] == {"eeg": 2, "eog": 1}
    assert report["geometry"]["eeg_channels_with_finite_nonzero_position"] == 2
    assert report["annotations"]["count"] == 2
    assert len(report["bounded_signal_sample"]["windows"]) == 3
    assert report["bounded_signal_sample"]["nonfinite_values"] == 0
    assert report["bounded_signal_sample"]["line_noise"] is not None


def test_record_raw_conflicts_remain_visible() -> None:
    raw = mne.io.RawArray(
        np.zeros((2, 100)),
        mne.create_info(["Fz", "Cz"], 100.0, "eeg"),
        verbose=False,
    )
    conflicts = record_raw_conflicts(
        {"nchans": 1, "ntimes": 99, "sampling_frequency": 100.0}, raw
    )
    assert {conflict["field"] for conflict in conflicts} == {"nchans", "ntimes"}
