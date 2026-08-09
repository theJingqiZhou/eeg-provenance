from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = REPO_ROOT / "skill" / "eeg-provenance"


def test_selector_covers_each_decision_phase_and_major_route() -> None:
    text = (SKILL_ROOT / "references" / "toolchain-selection.md").read_text(
        encoding="utf-8"
    )
    for phase in (
        "Resolve",
        "Acquire",
        "Validate BIDS conformance",
        "Query BIDS metadata",
        "native EDF/BDF header",
        "signal-read",
        "signal preprocessing",
        "cache/export",
        "Run QC",
    ):
        assert phase.casefold() in text.casefold()
    for route in (
        "EEGDash",
        "DataLad/git-annex",
        "MOABB",
        "BIDS Validator",
        "PyBIDS",
        "MNE-BIDS",
        "PyEDFlib",
        "EEGLAB/EEG-BIDS",
        "Braindecode",
        "PyHealth",
        "TorchEEG",
    ):
        assert route in text


def test_selector_distinguishes_hard_constraints_from_preferences() -> None:
    text = (SKILL_ROOT / "references" / "toolchain-selection.md").read_text(
        encoding="utf-8"
    )
    assert "Preferences rank only candidates that pass every hard constraint" in text
    assert "Do not score a candidate that fails one" in text
    assert "least sufficient observation level" in text
    assert "read scope" in text
    assert "write scope" in text
    assert "fallback_condition" in text


def test_operation_cards_define_cross_framework_semantics() -> None:
    text = (SKILL_ROOT / "references" / "operation-semantics.md").read_text(
        encoding="utf-8"
    )
    for operation in (
        "Read or normalize a recording",
        "Apply a deterministic temporal transform",
        "Materialize epochs or windows",
        "Construct tasks and labels",
        "Fit adaptive preprocessing",
        "Build a model-ready cache or handoff",
    ):
        assert f"## {operation}" in text
    for semantic_field in (
        "Intent",
        "Side effects",
        "Fit state",
        "Prefer / avoid",
        "Known surprise",
        "Ledger",
        "Evidence",
    ):
        assert f"| {semantic_field} |" in text
    assert "full end-aligned overlapping window" in text
    assert "pre-fitted processors" in text
    assert "toolchain_decision_id" in (
        SKILL_ROOT / "references" / "provenance-ledger.md"
    ).read_text(encoding="utf-8")


def test_progressive_router_stays_within_context_budget() -> None:
    skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    selector = (SKILL_ROOT / "references" / "toolchain-selection.md").read_text(
        encoding="utf-8"
    )
    operations = (SKILL_ROOT / "references" / "operation-semantics.md").read_text(
        encoding="utf-8"
    )
    assert len(skill) <= 8_000
    assert len(skill.splitlines()) <= 140
    assert len(selector) <= 8_000
    assert len(selector.splitlines()) <= 100
    assert len(operations) <= 12_000
    assert len(operations.splitlines()) <= 110
    for mode in ("**Inspect**", "**Design**", "**Execute**"):
        assert mode in skill
    assert "Do not create a full ledger" in skill
    assert "current phase only" in skill
    assert not (SKILL_ROOT / "references" / "research-scenarios.md").exists()
    assert not (
        SKILL_ROOT / "references" / "tool-recipes-braindecode-pyhealth.md"
    ).exists()


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


def test_matlab_probe_checks_core_and_plugin_entry_points() -> None:
    text = (SKILL_ROOT / "scripts" / "probe_eeglab.m").read_text(encoding="utf-8")
    for entry_point in (
        "eeg_getversion",
        "eeg_checkset",
        "eegh",
        "pop_saveset",
        "pop_importbids",
        "pop_eegfiltnew",
        "pop_runica",
        "pop_iclabel",
        "pop_clean_rawdata",
        "pop_dipfit_settings",
    ):
        assert entry_point in text
    for plugin in ("EEG-BIDS", "ICLabel", "clean_rawdata", "dipfit", "firfilt"):
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
    ):
        assert safeguard in text
    assert "ds003061" not in text
    assert "X:" not in text


def test_eeglab_recipe_requires_complete_non_gui_calls() -> None:
    text = (SKILL_ROOT / "references" / "tool-recipes-eeglab.md").read_text(
        encoding="utf-8"
    )
    assert "Supply every selector, option, and output path" in text
    assert "identify the public function it delegates to" in text
    assert "Do not copy a private helper" in text
