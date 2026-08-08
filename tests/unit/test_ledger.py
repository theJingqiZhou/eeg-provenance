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
