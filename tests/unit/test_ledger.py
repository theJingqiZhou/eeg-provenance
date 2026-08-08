import json
from copy import deepcopy
from pathlib import Path

from jsonschema import Draft202012Validator

from scripts.validate_ledger import validate_ledger


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = REPO_ROOT / "skill" / "eeg-provenance"


def _template() -> dict:
    return json.loads(
        (SKILL_ROOT / "assets" / "provenance-ledger.template.json").read_text(encoding="utf-8")
    )


def test_template_matches_json_schema_and_project_invariants() -> None:
    schema = json.loads(
        (SKILL_ROOT / "assets" / "provenance-ledger.schema.json").read_text(encoding="utf-8")
    )
    Draft202012Validator.check_schema(schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(_template()), key=lambda error: list(error.path))
    assert errors == []
    assert validate_ledger(_template()) == []


def test_derivative_inside_source_is_rejected() -> None:
    ledger = _template()
    ledger["outputs"][0]["path"] = (
        "/path/to/protected-source/ds-example/derivatives/intake-report.json"
    )
    errors = validate_ledger(ledger)
    assert any("inside source_root" in error for error in errors)


def test_adaptive_predictive_activity_must_fit_on_training_data() -> None:
    ledger = deepcopy(_template())
    ledger["contract"]["evaluation_mode"] = "predictive"
    ledger["activities"][0]["adaptive"] = True
    ledger["activities"][0]["fit_scope"] = "all_data_declared"
    errors = validate_ledger(ledger)
    assert any("training-only" in error for error in errors)


def test_spatial_channel_effect_requires_rank_record() -> None:
    ledger = deepcopy(_template())
    ledger["activities"][0]["channel_effect"] = "interpolate"
    errors = validate_ledger(ledger)
    assert any("rank" in error and "interpolate" in error for error in errors)


def test_unknown_evidence_id_is_rejected() -> None:
    ledger = deepcopy(_template())
    ledger["limitations"][0]["evidence_ids"] = ["S99"]
    errors = validate_ledger(ledger)
    assert any("S99" in error and "not registered" in error for error in errors)


def test_toolchain_phase_requires_a_chosen_candidate() -> None:
    ledger = deepcopy(_template())
    for candidate in ledger["contract"]["toolchain_decisions"][0]["candidates"]:
        candidate["status"] = "rejected"
    errors = validate_ledger(ledger)
    assert any("selected or planned tool" in error for error in errors)


def test_toolchain_requires_at_least_one_phase() -> None:
    ledger = deepcopy(_template())
    ledger["contract"]["toolchain_decisions"] = []
    errors = validate_ledger(ledger)
    assert any("at least one phase" in error for error in errors)


def test_selected_tool_must_be_verified() -> None:
    ledger = deepcopy(_template())
    candidate = ledger["contract"]["toolchain_decisions"][0]["candidates"][0]
    candidate["availability"] = "unknown"
    errors = validate_ledger(ledger)
    assert any("selected tool must be verified" in error for error in errors)


def test_selected_tool_requires_a_version() -> None:
    ledger = deepcopy(_template())
    candidate = ledger["contract"]["toolchain_decisions"][0]["candidates"][0]
    candidate["version"] = None
    errors = validate_ledger(ledger)
    assert any("requires a verified version" in error for error in errors)


def test_planned_tool_can_await_environment_probe() -> None:
    ledger = deepcopy(_template())
    candidate = ledger["contract"]["toolchain_decisions"][0]["candidates"][0]
    candidate["status"] = "planned"
    candidate["availability"] = "unknown"
    assert validate_ledger(ledger) == []


def test_toolchain_phases_are_unique() -> None:
    ledger = deepcopy(_template())
    duplicate = deepcopy(ledger["contract"]["toolchain_decisions"][0])
    ledger["contract"]["toolchain_decisions"].append(duplicate)
    errors = validate_ledger(ledger)
    assert any("duplicate phase" in error for error in errors)
