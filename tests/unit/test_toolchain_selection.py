from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = REPO_ROOT / "skill" / "eeg-provenance"


def test_pipeline_covers_each_process_stage() -> None:
    text = (SKILL_ROOT / "references" / "pipeline.md").read_text(encoding="utf-8")
    for stage in (
        "Resolve and acquire",
        "Inspect",
        "Normalize representation",
        "Temporal operations",
        "Spatial operations",
        "Segment or window",
        "Construct labels or tasks",
        "Fit adaptive operations",
        "Cache and hand off",
        "QC and close",
    ):
        assert f"## {stage}" in text
    for group in (
        "tools-data-access.md",
        "tools-signal.md",
        "tools-eeglab.md",
        "tools-frameworks.md",
    ):
        assert group in text


def test_pipeline_is_proportional_and_semantics_first() -> None:
    text = (SKILL_ROOT / "references" / "pipeline.md").read_text(encoding="utf-8")
    flattened = " ".join(text.split())
    assert "a bounded inspection need not manufacture a full" in (
        SKILL_ROOT / "SKILL.md"
    ).read_text(encoding="utf-8")
    assert "Do not create records" in flattened
    assert "Compare candidates only when" in flattened
    assert "Preferences rank only surviving candidates" in flattened
    for field in (
        "`input -> output`",
        "`assumptions`",
        "`read/write scope`",
        "`fit_state`",
        "`implementation`",
        "`parameters`",
        "`QC/stop`",
    ):
        assert field in text


def test_grouped_tool_references_preserve_implementation_deltas() -> None:
    access = (SKILL_ROOT / "references" / "tools-data-access.md").read_text(
        encoding="utf-8"
    )
    signal = (SKILL_ROOT / "references" / "tools-signal.md").read_text(
        encoding="utf-8"
    )
    eeglab = (SKILL_ROOT / "references" / "tools-eeglab.md").read_text(
        encoding="utf-8"
    )
    extensions = (
        SKILL_ROOT / "references" / "tools-eeglab-extensions.md"
    ).read_text(encoding="utf-8")
    frameworks = (SKILL_ROOT / "references" / "tools-frameworks.md").read_text(
        encoding="utf-8"
    )
    for route in (
        "EEGDash",
        "DataLad/git-annex",
        "BIDS Validator",
        "PyBIDS",
        "PyEDFlib",
        "whosmat",
    ):
        assert route in access
    for route in (
        "MNE-BIDS",
        "read_raw_edf",
        "mne.Epochs",
    ):
        assert route in signal
    for route in (
        "eeglab('nogui')",
        "std_editset",
        "pop_importbids",
        "EEG.BIDS",
        "pop_loadbv",
        "pop_biosig",
    ):
        assert route in eeglab
    for route in (
        "plugin_getweb",
        "versioned ZIP",
        "bva-io",
        "BIOSIG",
        "GEDAI(",
        "rndreset",
    ):
        assert route in extensions
    for route in ("MOABB", "Braindecode", "PyHealth", "TorchEEG"):
        assert route in frameworks
    assert "full end-aligned overlapping window" in frameworks
    assert "pre-fitted processors" in frameworks
    assert "toolchain_decision_id" in (
        SKILL_ROOT / "references" / "provenance-ledger.md"
    ).read_text(encoding="utf-8")


def test_progressive_router_stays_within_context_budget() -> None:
    skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    pipeline = (SKILL_ROOT / "references" / "pipeline.md").read_text(
        encoding="utf-8"
    )
    bids = (SKILL_ROOT / "references" / "bids-eeg-1.11.1.md").read_text(
        encoding="utf-8"
    )
    non_bids = (SKILL_ROOT / "references" / "non-bids-intake.md").read_text(
        encoding="utf-8"
    )
    assert len(skill) <= 8_000
    assert len(skill.splitlines()) <= 140
    assert len(pipeline) <= 14_000
    assert len(pipeline.splitlines()) <= 250
    assert len(skill) + len(bids) + len(pipeline) <= 40_000
    assert len(skill) + len(non_bids) + len(pipeline) <= 45_000
    for name in (
        "tools-data-access.md",
        "tools-signal.md",
        "tools-eeglab.md",
        "tools-eeglab-extensions.md",
        "tools-frameworks.md",
    ):
        text = (SKILL_ROOT / "references" / name).read_text(encoding="utf-8")
        assert len(text) <= 13_000
        assert len(text.splitlines()) <= 210
    for mode in ("**Inspect**", "**Design**", "**Execute**"):
        assert mode in skill
    assert "Do not create a full ledger" in skill
    assert "Add at most one primary implementation reference" in skill
    assert not (SKILL_ROOT / "references" / "research-scenarios.md").exists()
    for retired in (
        "toolchain-selection.md",
        "operation-semantics.md",
        "tool-recipes-bids.md",
        "tool-recipes-eegdash.md",
        "tool-recipes-eeglab.md",
        "tool-recipes-mne.md",
        "tool-recipes-torcheeg.md",
    ):
        assert not (SKILL_ROOT / "references" / retired).exists()


def test_evals_cover_complementary_and_matlab_selection() -> None:
    cases = json.loads((REPO_ROOT / "evals" / "cases.json").read_text(encoding="utf-8"))[
        "cases"
    ]
    by_id = {case["id"]: case for case in cases}
    assert "bids-tools-are-complementary" in by_id
    assert "matlab-is-not-eeglab" in by_id
    assert "edf-native-header-and-mne-view" in by_id
    assert "makoto-recipe-is-not-a-default" in by_id
    assert "light-edf-inspection" in by_id
    assert "operation-window-semantics" in by_id
    assert "activity-tool-mismatch" in by_id
    assert "no-safe-fallback" in by_id
    assert "legacy-pinned-python-inspection" in by_id
    assert "pyhealth-core-stack-conflict" in by_id
    assert "prerelease-python-upper-bound" in by_id
    assert "eeglab-study-is-not-bids-copy" in by_id
    assert "eeglab-metadata-mode-is-format-specific" in by_id
    assert "eeglab-plugin-distribution-is-explicit" in by_id
    assert "gedai-headless-public-api" in by_id


def test_matlab_probe_checks_core_and_plugin_entry_points() -> None:
    text = (SKILL_ROOT / "scripts" / "probe_eeglab.m").read_text(encoding="utf-8")
    for entry_point in (
        "eeg_getversion",
        "eeg_checkset",
        "eegh",
        "pop_saveset",
        "std_editset",
        "pop_importbids",
        "plugin_getweb",
        "plugin_install",
        "pop_loadbv",
        "pop_biosig",
        "sopen",
        "pop_fileio",
        "pop_eegfiltnew",
        "pop_runica",
        "pop_iclabel",
        "pop_clean_rawdata",
        "pop_dipfit_settings",
        "GEDAI",
        "pop_GEDAI",
    ):
        assert entry_point in text
    for plugin in (
        "EEG-BIDS",
        "ICLabel",
        "clean_rawdata",
        "dipfit",
        "firfilt",
        "bva-io",
        "Biosig",
        "File-IO",
        "MEF3",
        "GEDAI",
    ):
        assert plugin in text
    assert "plugin_status" in text
    assert "jsonencode" in text


def test_eeglab_bids_verifier_is_parameterized_and_source_safe() -> None:
    text = (REPO_ROOT / "tools" / "verifyEeglabBids.m").read_text(
        encoding="utf-8"
    )
    for parameter in (
        "bidsRoot",
        "subjectLabel",
        "taskLabel",
        "runLabel",
        "SessionLabel",
    ):
        assert parameter in text
    for safeguard in (
        "tempname",
        "snapshotTree",
        "sourceUnchanged",
        "metadata', 'on",
        "metadata', 'off",
        "selectorArguments",
        "expectedBidsFields",
        "expectedDatasetInfoFields",
        "sample_payload_materialized",
        "derivative_sidecar_copy_count",
        "verifyTextReadContract",
        "do not shadow fileread",
    ):
        assert safeguard in text
    assert "ds003061" not in text
    assert "X:" not in text


def test_eeglab_recipe_requires_complete_non_gui_calls() -> None:
    text = (SKILL_ROOT / "references" / "tools-eeglab-extensions.md").read_text(
        encoding="utf-8"
    )
    assert "Supply every selector, option, and output path" in text
    assert "identify the documented public computational function" in text
    assert "Do not copy private helpers" in text


def test_eeglab_guidance_preserves_study_and_distribution_boundaries() -> None:
    core = (SKILL_ROOT / "references" / "tools-eeglab.md").read_text(
        encoding="utf-8"
    )
    extensions = (
        SKILL_ROOT / "references" / "tools-eeglab-extensions.md"
    ).read_text(encoding="utf-8")
    for field in (
        "gInfo",
        "pInfo",
        "pInfoDesc",
        "eInfo",
        "eInfoDesc",
        "tInfo",
        "bidsstats",
        "scannedElectrodes",
        "behavioral",
    ):
        assert field in core
    assert "does not byte-copy" in core
    assert "not a universal source-metadata-only reader" in core
    assert "Do not translate “EEGLAB plugin” into `git clone`" in extensions
    assert "addpath(genpath(pluginRoot))" in extensions
    assert "PolyForm" not in core
    assert "noncommercial license" in extensions


def test_eeglab_verifier_exercises_study_and_metadata_sentinels() -> None:
    text = (REPO_ROOT / "tools" / "verify_eeglab.m").read_text(encoding="utf-8")
    for behavior in (
        "std_editset",
        "oneFileInfo",
        "twoFileInfo",
        "data_materialized",
        "study_datasetinfo_fields",
    ):
        assert behavior in text
