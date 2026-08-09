from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = REPO_ROOT / "skill" / "eeg-provenance"
REFERENCE = SKILL_ROOT / "references" / "runtime-compatibility.md"


def test_matrix_covers_supported_cpython_lanes_and_meaning() -> None:
    text = REFERENCE.read_text(encoding="utf-8")
    for version in ("3.10", "3.11", "3.12", "3.13", "3.14"):
        assert f"| {version} |" in text
    for state in ("`E` means exercised", "`M` means package", "`X` means", "`?` means"):
        assert state in text
    assert "not a universal lock file" in text
    assert "not proof" in text
    assert "CPython `>=3.10,<3.15`" in text
    assert "Python 3.15 is" in text
    assert "3.16 is the feature-development branch" in text


def test_matrix_records_key_python_and_framework_boundaries() -> None:
    text = REFERENCE.read_text(encoding="utf-8")
    for boundary in (
        "NumPy `<=2.2.6`",
        "SciPy `<=1.15.3`",
        "MNE-BIDS `<=0.17`",
        "h5py / pymatreader",
        "PyEDFlib",
        "AutoReject / MNE-ICALabel",
        "DataLad / MOABB",
        "EEGDash `0.8.4`: `X`",
        "Braindecode `1.7`: `X`",
        "PyHealth `2.0.1`: `X`",
        "NumPy 1.x to 2.x",
        "pandas 2.x to 3.x",
        "MOABB 1.1 to 1.4+",
        "PyHealth 1.x to 2.x",
        "TorchEEG 1.1.3",
    ):
        assert boundary in text


def test_runtime_policy_does_not_make_uv_or_base_mutation_a_default() -> None:
    text = REFERENCE.read_text(encoding="utf-8")
    assert "`uv` is optional" in text
    assert "`python -m pip`" in text
    assert "never use bare `pip`" in text
    assert "override `EXTERNALLY-MANAGED`" in text
    assert "light inspection does not justify" in text
    assert "install uv" not in text.casefold()
    assert "pip install --upgrade" not in text


def test_lifecycle_preference_is_a_weak_tie_breaker() -> None:
    text = REFERENCE.read_text(encoding="utf-8")
    assert "newest in-window CPython release whose bugfix period has ended" in text
    assert "stability tie-breaker, not a compatibility rule" in text
    assert "On 2026-08-09 this points to Python 3.12" in text
    for override in (
        "package constraints",
        "target wheels/ABI",
        "accelerator and vendor support",
        "security policy",
        "measured behavior",
        "provisioned environment",
    ):
        assert override in text


def test_runtime_reference_is_directly_routed_from_skill() -> None:
    skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert "(references/runtime-compatibility.md)" in skill
    assert "Pinned, legacy, or uncertain Python host" in skill
