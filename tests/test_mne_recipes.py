import os
import warnings
from pathlib import Path

import mne
import pytest

from scripts.verify_mne_recipes import run_verification


def test_synthetic_mne_recipe_contract() -> None:
    result = run_verification()
    assert result["versions"]["mne"] == "1.12.1"
    assert result["event_count"] == 3
    assert result["output_sfreq_hz"] == 128.0
    assert result["ica_components"] == 5
    assert result["interpolated_channel_retained_in_bads"] == ["P4"]
    assert result["rank"]["average_reference"] <= result["rank"]["native"]


@pytest.mark.archive
def test_real_annex_eeglab_set_metadata() -> None:
    value = os.environ.get("EEG_ARCHIVE_SET")
    if not value:
        pytest.skip("EEG_ARCHIVE_SET was not supplied")
    path = Path(value)
    if not path.is_file():
        pytest.skip(f"archive SET object is unavailable: {path}")
    before = (path.stat().st_size, path.stat().st_mtime_ns)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        raw = mne.io.read_raw_eeglab(path, preload=False, verbose=False)
    after = (path.stat().st_size, path.stat().st_mtime_ns)
    assert before == after
    assert raw.info["nchan"] > 0
    assert raw.info["sfreq"] > 0
    assert raw.n_times > 0
    messages = [str(item.message) for item in caught]
    assert any("Unknown types" in message and "Temp" in message for message in messages)
    assert any("gsr/misc/resp channels" in message for message in messages)
