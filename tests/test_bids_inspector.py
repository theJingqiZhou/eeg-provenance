import hashlib
import json
from pathlib import Path

import pytest

from scripts.inspect_bids_metadata import inspect_dataset


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_inspector_reads_metadata_without_changing_source(tmp_path: Path) -> None:
    root = tmp_path / "ds-test"
    eeg = root / "sub-001" / "eeg"
    eeg.mkdir(parents=True)
    (root / "dataset_description.json").write_text(
        json.dumps({"Name": "Synthetic intake", "BIDSVersion": "1.11.1"}), encoding="utf-8"
    )
    prefix = eeg / "sub-001_task-test_run-1"
    (prefix.with_name(prefix.name + "_eeg.json")).write_text(
        json.dumps(
            {
                "TaskName": "test",
                "SamplingFrequency": 256,
                "PowerLineFrequency": 50,
                "EEGReference": "Cz",
            }
        ),
        encoding="utf-8",
    )
    channels = prefix.with_name(prefix.name + "_channels.tsv")
    channels.write_text(
        "name\ttype\tunits\tstatus\nFz\tEEG\tuV\tgood\nCz\tEEG\tuV\tgood\n",
        encoding="utf-8",
    )
    before = {path: _digest(path) for path in root.rglob("*") if path.is_file()}
    report = inspect_dataset(root, "sub-001/eeg/sub-001_task-test_run-1_eeg")
    after = {path: _digest(path) for path in root.rglob("*") if path.is_file()}
    assert before == after
    assert report["writes_performed"] is False
    assert report["signal_payload_read"] is False
    channel_records = [record for record in report["files"] if record["relative_path"].endswith("_channels.tsv")]
    assert channel_records[0]["summary"]["types"] == {"EEG": 2}


@pytest.mark.archive
def test_real_openneuro_metadata_read_only() -> None:
    root = Path("X:/openneurodatasets/ds003061")
    if not root.is_dir():
        pytest.skip("OpenNeuro archive is not mounted")
    description = root / "dataset_description.json"
    before = (_digest(description), description.stat().st_mtime_ns)
    report = inspect_dataset(root, "sub-001/eeg/sub-001_task-P300_run-1_eeg")
    after = (_digest(description), description.stat().st_mtime_ns)
    assert before == after
    assert "auditory oddball" in report["dataset"]["Name"].casefold()
    assert any(record["relative_path"].endswith("_channels.tsv") for record in report["files"])


@pytest.mark.archive
def test_real_nemar_generated_provenance_is_preserved() -> None:
    root = Path("X:/nemardatasets/nm000166")
    if not root.is_dir():
        pytest.skip("NEMAR archive is not mounted")
    description = root / "dataset_description.json"
    before = (_digest(description), description.stat().st_mtime_ns)
    report = inspect_dataset(root, "sub-001/ses-01/eeg/sub-001_ses-01_task-aep_eeg")
    after = (_digest(description), description.stat().st_mtime_ns)
    assert before == after
    generated = report["dataset"]["GeneratedBy"]
    assert "pseudo-continuous" in generated[0]["Description"].casefold()
    assert report["dataset"]["SourceDatasets"]
