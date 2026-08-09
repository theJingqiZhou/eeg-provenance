import json
from copy import deepcopy
from pathlib import Path

from jsonschema import Draft202012Validator
from scripts.validate_ledger import main, validate_ledger

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = REPO_ROOT / "skill" / "eeg-provenance"


def _template() -> dict:
    return json.loads(
        (SKILL_ROOT / "assets" / "provenance-ledger.template.json").read_text(
            encoding="utf-8"
        )
    )


def _remove_execution(ledger: dict) -> None:
    ledger["activities"] = []
    ledger["outputs"] = []


def test_template_matches_json_schema_and_project_invariants() -> None:
    schema = json.loads(
        (SKILL_ROOT / "assets" / "provenance-ledger.schema.json").read_text(
            encoding="utf-8"
        )
    )
    assert schema["$id"].startswith(
        "https://raw.githubusercontent.com/theJingqiZhou/eeg-provenance/"
    )
    assert "example.org/eeg-provenance" not in schema["$id"]
    assert schema["properties"]["schema_version"] == {"const": "2.0.0"}
    Draft202012Validator.check_schema(schema)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(_template()),
        key=lambda error: tuple(str(part) for part in error.path),
    )
    assert errors == []
    assert validate_ledger(_template()) == []


def test_cli_rejects_schema_type_error(tmp_path, capsys) -> None:
    ledger = _template()
    ledger["contract"]["toolchain_decisions"][0]["candidates"][0][
        "read_scope"
    ] = 42
    path = tmp_path / "invalid-ledger.json"
    path.write_text(json.dumps(ledger), encoding="utf-8")

    assert main([str(path)]) == 1
    error = capsys.readouterr().err
    assert "schema $.contract.toolchain_decisions[0].candidates[0].read_scope" in error
    assert "is not of type 'string'" in error


def test_schema_rejects_unexpected_fields() -> None:
    ledger = _template()
    ledger["contract"]["toolchain_decisions"][0]["candidates"][0][
        "untracked_side_effect"
    ] = True
    errors = validate_ledger(ledger)
    assert any(error.startswith("schema ") and "Additional properties" in error for error in errors)


def test_schema_checks_date_time_format() -> None:
    ledger = _template()
    ledger["created_at"] = "sometime today"
    errors = validate_ledger(ledger)
    assert any("schema $.created_at" in error and "date-time" in error for error in errors)


def test_derivative_inside_source_is_rejected() -> None:
    ledger = _template()
    ledger["dataset"]["authorized_output_roots"] = [
        "/path/to/protected-source/ds-example/derivatives"
    ]
    ledger["outputs"][0]["path"] = (
        "/path/to/protected-source/ds-example/derivatives/intake-report.json"
    )
    errors = validate_ledger(ledger)
    assert any("protected source_root" in error for error in errors)


def test_writable_bids_derivative_is_allowed_when_explicitly_authorized() -> None:
    ledger = _template()
    ledger["dataset"]["protected_source_tree"] = False
    ledger["dataset"]["authorized_output_roots"] = [
        "/path/to/writable-dataset/derivatives/eeg-provenance"
    ]
    ledger["dataset"]["source_root"] = "/path/to/writable-dataset"
    ledger["outputs"][0]["path"] = (
        "/path/to/writable-dataset/derivatives/eeg-provenance/intake-report.json"
    )
    assert validate_ledger(ledger) == []


def test_output_outside_authorized_roots_is_rejected() -> None:
    ledger = _template()
    ledger["outputs"][0]["path"] = "C:/unapproved/intake-report.json"
    errors = validate_ledger(ledger)
    assert any("outside authorized_output_roots" in error for error in errors)


def test_authorized_output_root_cannot_contain_source_root() -> None:
    ledger = _template()
    ledger["dataset"]["protected_source_tree"] = False
    ledger["dataset"]["authorized_output_roots"] = ["/path/to"]
    errors = validate_ledger(ledger)
    assert any("authorized root must not contain source_root" in error for error in errors)


def test_adaptive_predictive_activity_requires_pre_prediction_availability() -> None:
    ledger = deepcopy(_template())
    ledger["contract"]["evaluation_mode"] = "predictive"
    ledger["activities"][0]["adaptive"] = True
    ledger["activities"][0]["fit_scope"] = {
        "population": "held-out test participants",
        "uses_labels": True,
        "uses_target_distribution": True,
        "fit_unit": "participant",
        "deployment_available": False,
        "state_reused_on": ["same held-out participant"],
    }
    errors = validate_ledger(ledger)
    assert any("available and authorized before prediction" in error for error in errors)


def test_adaptive_predictive_activity_accepts_authorized_calibration() -> None:
    ledger = deepcopy(_template())
    ledger["contract"]["evaluation_mode"] = "predictive"
    ledger["activities"][0]["adaptive"] = True
    ledger["activities"][0]["fit_scope"] = {
        "population": "independent subject calibration partition",
        "uses_labels": True,
        "uses_target_distribution": False,
        "fit_unit": "participant",
        "deployment_available": True,
        "state_reused_on": ["post-calibration trials for the same participant"],
    }
    assert validate_ledger(ledger) == []


def test_adaptive_predictive_activity_accepts_unlabeled_recording_fit() -> None:
    ledger = deepcopy(_template())
    ledger["contract"]["evaluation_mode"] = "predictive"
    ledger["activities"][0]["adaptive"] = True
    ledger["activities"][0]["fit_scope"] = {
        "population": "current deployment recording",
        "uses_labels": False,
        "uses_target_distribution": True,
        "fit_unit": "recording",
        "deployment_available": True,
        "state_reused_on": ["windows from the same recording"],
    }
    assert validate_ledger(ledger) == []


def test_descriptive_adaptive_activity_declares_population() -> None:
    ledger = deepcopy(_template())
    ledger["activities"][0]["adaptive"] = True
    ledger["activities"][0]["fit_scope"] = {
        "population": "all records in the descriptive cohort",
        "uses_labels": False,
        "uses_target_distribution": True,
        "fit_unit": "cohort",
        "deployment_available": None,
        "state_reused_on": ["same descriptive cohort"],
    }
    assert validate_ledger(ledger) == []


def test_fixed_activity_rejects_noncanonical_fit_scope() -> None:
    ledger = deepcopy(_template())
    ledger["activities"][0]["fit_scope"]["population"] = "all records"
    errors = validate_ledger(ledger)
    assert any("canonical non-adaptive scope" in error for error in errors)


def test_qc_requires_the_common_transition_skeleton() -> None:
    ledger = deepcopy(_template())
    del ledger["qc"]["event_transition"]
    errors = validate_ledger(ledger)
    assert any(
        error.startswith("schema $.qc") and "event_transition" in error
        for error in errors
    )


def test_qc_retention_fraction_is_bounded() -> None:
    ledger = deepcopy(_template())
    ledger["qc"]["retention"]["duration_fraction"] = 1.1
    errors = validate_ledger(ledger)
    assert any(
        error.startswith("schema $.qc.retention.duration_fraction")
        for error in errors
    )


def test_qc_pass_cannot_hide_warnings() -> None:
    ledger = deepcopy(_template())
    ledger["qc"]["warnings"] = ["Event count changed unexpectedly"]
    errors = validate_ledger(ledger)
    assert any("$.qc.status: pass cannot contain warnings" in error for error in errors)


def test_qc_failed_observation_requires_fail_status() -> None:
    ledger = deepcopy(_template())
    ledger["qc"]["observations"][0]["status"] = "failed"
    errors = validate_ledger(ledger)
    assert any("failed observations require fail status" in error for error in errors)


def test_qc_fail_status_requires_failed_observation() -> None:
    ledger = deepcopy(_template())
    ledger["qc"]["status"] = "fail"
    errors = validate_ledger(ledger)
    assert any("fail requires a failed observation" in error for error in errors)


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


def test_selected_decision_requires_a_selected_candidate() -> None:
    ledger = deepcopy(_template())
    for candidate in ledger["contract"]["toolchain_decisions"][0]["candidates"]:
        candidate["status"] = "rejected"
    errors = validate_ledger(ledger)
    assert any(error.startswith("schema ") and ".candidates" in error for error in errors)


def test_execute_ledger_requires_at_least_one_reached_phase() -> None:
    ledger = deepcopy(_template())
    ledger["contract"]["toolchain_decisions"] = []
    errors = validate_ledger(ledger)
    assert any(error.startswith("schema ") and "should be non-empty" in error for error in errors)


def test_failure_policy_stop_uses_null_condition() -> None:
    ledger = deepcopy(_template())
    decision = ledger["contract"]["toolchain_decisions"][0]
    decision["failure_policy"] = "stop"
    decision["fallback_condition"] = None
    assert validate_ledger(ledger) == []


def test_fallback_policy_requires_an_activation_condition() -> None:
    ledger = deepcopy(_template())
    decision = ledger["contract"]["toolchain_decisions"][0]
    decision["failure_policy"] = "fallback"
    errors = validate_ledger(ledger)
    assert any(error.startswith("schema ") and "fallback_condition" in error for error in errors)


def test_execute_ledger_does_not_invent_harmonization() -> None:
    ledger = deepcopy(_template())
    ledger["contract"]["harmonization_decisions"] = []
    assert validate_ledger(ledger) == []


def test_stopped_decision_needs_no_fake_fallback_or_activity() -> None:
    ledger = deepcopy(_template())
    decision = ledger["contract"]["toolchain_decisions"][0]
    decision["status"] = "stopped"
    decision["failure_policy"] = "stop"
    decision["fallback_condition"] = None
    for candidate in decision["candidates"]:
        candidate["status"] = "rejected"
    _remove_execution(ledger)
    assert validate_ledger(ledger) == []


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
    decision = ledger["contract"]["toolchain_decisions"][0]
    decision["status"] = "planned"
    candidate = decision["candidates"][0]
    candidate["status"] = "planned"
    candidate["availability"] = "unknown"
    candidate["version"] = None
    _remove_execution(ledger)
    assert validate_ledger(ledger) == []


def test_activity_must_reference_selected_candidate() -> None:
    ledger = deepcopy(_template())
    ledger["activities"][0]["tool_candidate_id"] = "candidate-pybids"
    errors = validate_ledger(ledger)
    assert any("activity requires a selected candidate" in error for error in errors)


def test_activity_software_must_match_candidate() -> None:
    ledger = deepcopy(_template())
    ledger["activities"][0]["software"]["name"] = "pybids"
    ledger["activities"][0]["software"]["version"] = "0.22.0"
    errors = validate_ledger(ledger)
    assert any("software.name" in error and "does not match" in error for error in errors)
    assert any("software.version" in error and "does not match" in error for error in errors)


def test_activity_candidate_must_belong_to_referenced_decision() -> None:
    ledger = deepcopy(_template())
    second = deepcopy(ledger["contract"]["toolchain_decisions"][0])
    second["id"] = "decision-second-phase"
    second["phase"] = "metadata_query"
    for candidate in second["candidates"]:
        candidate["id"] += "-second"
    ledger["contract"]["toolchain_decisions"].append(second)
    ledger["activities"][0]["tool_candidate_id"] = second["candidates"][0]["id"]
    errors = validate_ledger(ledger)
    assert any("candidate belongs to another decision" in error for error in errors)


def test_toolchain_phases_are_unique() -> None:
    ledger = deepcopy(_template())
    duplicate = deepcopy(ledger["contract"]["toolchain_decisions"][0])
    duplicate["id"] = "decision-duplicate-phase"
    for candidate in duplicate["candidates"]:
        candidate["id"] += "-duplicate"
    ledger["contract"]["toolchain_decisions"].append(duplicate)
    errors = validate_ledger(ledger)
    assert any("duplicate phase" in error for error in errors)
