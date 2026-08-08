#!/usr/bin/env python3
"""Validate eeg-provenance ledger structure and project invariants."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any


SCHEMA_VERSION = "1.0.0"
EVIDENCE_RE = re.compile(r"^S\d{2}$")
EVIDENCE_ANCHOR_RE = re.compile(r'<a id="(s\d{2})"></a>', re.IGNORECASE)
CHANNEL_STATES = {"native", "bad", "missing", "dropped", "interpolated", "virtual"}
CLASSIFICATIONS = {"must_harmonize", "may_harmonize", "cannot_harmonize"}
RANK_EFFECTS = {"drop", "interpolate", "rereference", "virtual"}
TRAINING_SCOPES = {"training_only", "within_train_fold"}


def _require_mapping(value: Any, path: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{path}: expected object")
        return {}
    return value


def _require_list(value: Any, path: str, errors: list[str]) -> list[Any]:
    if not isinstance(value, list):
        errors.append(f"{path}: expected array")
        return []
    return value


def _required(obj: dict[str, Any], keys: set[str], path: str, errors: list[str]) -> None:
    for key in sorted(keys - obj.keys()):
        errors.append(f"{path}.{key}: missing required field")


def _normalize_path(value: str) -> PurePosixPath:
    normalized = value.replace("\\", "/").rstrip("/").casefold()
    return PurePosixPath(normalized)


def _is_within(child: str, parent: str) -> bool:
    child_path = _normalize_path(child)
    parent_path = _normalize_path(parent)
    return child_path == parent_path or parent_path in child_path.parents


def _registered_evidence_ids() -> set[str]:
    register = Path(__file__).resolve().parents[1] / "references" / "evidence-register.md"
    if not register.is_file():
        return set()
    return {match.upper() for match in EVIDENCE_ANCHOR_RE.findall(register.read_text(encoding="utf-8"))}


def _check_evidence_ids(
    value: Any,
    path: str,
    errors: list[str],
    registered: set[str],
) -> None:
    ids = _require_list(value, path, errors)
    if not ids:
        errors.append(f"{path}: at least one evidence ID is required")
    for index, evidence_id in enumerate(ids):
        if not isinstance(evidence_id, str) or not EVIDENCE_RE.fullmatch(evidence_id):
            errors.append(f"{path}[{index}]: expected evidence ID like S01")
        elif evidence_id not in registered:
            errors.append(f"{path}[{index}]: evidence ID {evidence_id} is not registered")


def validate_ledger(data: Any) -> list[str]:
    errors: list[str] = []
    registered_evidence = _registered_evidence_ids()
    if not registered_evidence:
        errors.append("references/evidence-register.md: no registered evidence IDs found")
    ledger = _require_mapping(data, "$", errors)
    _required(
        ledger,
        {
            "schema_version",
            "ledger_id",
            "created_at",
            "dataset",
            "objective",
            "inputs",
            "contract",
            "activities",
            "qc",
            "outputs",
            "limitations",
        },
        "$",
        errors,
    )
    if ledger.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"$.schema_version: expected {SCHEMA_VERSION!r}")

    dataset = _require_mapping(ledger.get("dataset"), "$.dataset", errors)
    _required(
        dataset,
        {"dataset_id", "dataset_version", "source_root", "source_uri", "recordings", "acquisition_history"},
        "$.dataset",
        errors,
    )
    source_root = dataset.get("source_root")
    if not isinstance(source_root, str) or not source_root.strip():
        errors.append("$.dataset.source_root: expected non-empty path")
        source_root = ""
    history = _require_mapping(dataset.get("acquisition_history"), "$.dataset.acquisition_history", errors)
    if history.get("status") not in {"known", "partial", "unknown"}:
        errors.append("$.dataset.acquisition_history.status: expected known, partial, or unknown")

    recording_ids: set[str] = set()
    for index, value in enumerate(_require_list(dataset.get("recordings"), "$.dataset.recordings", errors)):
        recording = _require_mapping(value, f"$.dataset.recordings[{index}]", errors)
        _required(recording, {"id", "relative_paths", "identities"}, f"$.dataset.recordings[{index}]", errors)
        recording_id = recording.get("id")
        if not isinstance(recording_id, str) or not recording_id:
            errors.append(f"$.dataset.recordings[{index}].id: expected non-empty string")
        elif recording_id in recording_ids:
            errors.append(f"$.dataset.recordings[{index}].id: duplicate ID {recording_id!r}")
        else:
            recording_ids.add(recording_id)
        identities = _require_list(recording.get("identities"), f"$.dataset.recordings[{index}].identities", errors)
        if not identities:
            errors.append(f"$.dataset.recordings[{index}].identities: immutable identity required")

    inputs = _require_mapping(ledger.get("inputs"), "$.inputs", errors)
    _required(inputs, {"entities", "channel_support"}, "$.inputs", errors)
    entity_ids: set[str] = set()
    for index, value in enumerate(_require_list(inputs.get("entities"), "$.inputs.entities", errors)):
        entity = _require_mapping(value, f"$.inputs.entities[{index}]", errors)
        entity_id = entity.get("id")
        if not isinstance(entity_id, str) or not entity_id:
            errors.append(f"$.inputs.entities[{index}].id: expected non-empty string")
        elif entity_id in entity_ids:
            errors.append(f"$.inputs.entities[{index}].id: duplicate ID {entity_id!r}")
        else:
            entity_ids.add(entity_id)
        if entity.get("recording_id") not in recording_ids:
            errors.append(f"$.inputs.entities[{index}].recording_id: unknown recording")

    channel_names: set[str] = set()
    for index, value in enumerate(_require_list(inputs.get("channel_support"), "$.inputs.channel_support", errors)):
        channel = _require_mapping(value, f"$.inputs.channel_support[{index}]", errors)
        _required(channel, {"name", "type", "state", "unit", "reference", "geometry_source"}, f"$.inputs.channel_support[{index}]", errors)
        name = channel.get("name")
        if not isinstance(name, str) or not name:
            errors.append(f"$.inputs.channel_support[{index}].name: expected non-empty string")
        elif name.casefold() in channel_names:
            errors.append(f"$.inputs.channel_support[{index}].name: duplicate channel {name!r}")
        else:
            channel_names.add(name.casefold())
        if channel.get("state") not in CHANNEL_STATES:
            errors.append(f"$.inputs.channel_support[{index}].state: invalid channel state")

    contract = _require_mapping(ledger.get("contract"), "$.contract", errors)
    _required(contract, {"evaluation_mode", "split_policy", "invariants", "harmonization_decisions"}, "$.contract", errors)
    evaluation_mode = contract.get("evaluation_mode")
    if evaluation_mode not in {"descriptive", "predictive"}:
        errors.append("$.contract.evaluation_mode: expected descriptive or predictive")
    for index, value in enumerate(_require_list(contract.get("harmonization_decisions"), "$.contract.harmonization_decisions", errors)):
        decision = _require_mapping(value, f"$.contract.harmonization_decisions[{index}]", errors)
        if decision.get("classification") not in CLASSIFICATIONS:
            errors.append(f"$.contract.harmonization_decisions[{index}].classification: invalid class")
        _check_evidence_ids(
            decision.get("evidence_ids"),
            f"$.contract.harmonization_decisions[{index}].evidence_ids",
            errors,
            registered_evidence,
        )

    activity_ids: set[str] = set()
    output_entity_ids: set[str] = set()
    sequences: list[int] = []
    activities = _require_list(ledger.get("activities"), "$.activities", errors)
    for index, value in enumerate(activities):
        path = f"$.activities[{index}]"
        activity = _require_mapping(value, path, errors)
        _required(
            activity,
            {"id", "sequence", "type", "adaptive", "software", "parameters", "fit_scope", "input_entities", "output_entities", "channel_effect", "evidence_ids"},
            path,
            errors,
        )
        activity_id = activity.get("id")
        if not isinstance(activity_id, str) or not activity_id:
            errors.append(f"{path}.id: expected non-empty string")
        elif activity_id in activity_ids:
            errors.append(f"{path}.id: duplicate ID {activity_id!r}")
        else:
            activity_ids.add(activity_id)
        sequence = activity.get("sequence")
        if not isinstance(sequence, int) or isinstance(sequence, bool) or sequence < 1:
            errors.append(f"{path}.sequence: expected positive integer")
        else:
            sequences.append(sequence)
        for input_id in _require_list(activity.get("input_entities"), f"{path}.input_entities", errors):
            if input_id not in entity_ids and input_id not in output_entity_ids:
                errors.append(f"{path}.input_entities: {input_id!r} is not available before this activity")
        for output_id in _require_list(activity.get("output_entities"), f"{path}.output_entities", errors):
            if output_id in entity_ids or output_id in output_entity_ids:
                errors.append(f"{path}.output_entities: duplicate entity ID {output_id!r}")
            elif isinstance(output_id, str) and output_id:
                output_entity_ids.add(output_id)
        effect = activity.get("channel_effect")
        if effect in RANK_EFFECTS:
            rank = activity.get("rank")
            if not isinstance(rank, dict) or not {"before", "after", "method"} <= rank.keys():
                errors.append(f"{path}.rank: required for channel effect {effect!r}")
        if evaluation_mode == "predictive" and activity.get("adaptive") is True:
            if activity.get("fit_scope") not in TRAINING_SCOPES:
                errors.append(f"{path}.fit_scope: adaptive predictive activity must be training-only")
        _check_evidence_ids(activity.get("evidence_ids"), f"{path}.evidence_ids", errors, registered_evidence)

    if len(sequences) != len(set(sequences)):
        errors.append("$.activities[*].sequence: sequence values must be unique")
    if sequences != sorted(sequences):
        errors.append("$.activities[*].sequence: activities must be listed in sequence order")

    output_ids: set[str] = set()
    for index, value in enumerate(_require_list(ledger.get("outputs"), "$.outputs", errors)):
        path = f"$.outputs[{index}]"
        output = _require_mapping(value, path, errors)
        _required(output, {"id", "path", "media_type", "bytes", "checksum", "source_entity", "generating_activity"}, path, errors)
        output_id = output.get("id")
        if not isinstance(output_id, str) or not output_id:
            errors.append(f"{path}.id: expected non-empty string")
        elif output_id in output_ids:
            errors.append(f"{path}.id: duplicate ID {output_id!r}")
        else:
            output_ids.add(output_id)
        output_path = output.get("path")
        if source_root and isinstance(output_path, str) and _is_within(output_path, source_root):
            errors.append(f"{path}.path: derivative output is inside source_root")
        if output.get("source_entity") not in entity_ids:
            errors.append(f"{path}.source_entity: unknown source input entity")
        if output.get("generating_activity") not in activity_ids:
            errors.append(f"{path}.generating_activity: unknown activity")

    for index, value in enumerate(_require_list(ledger.get("limitations"), "$.limitations", errors)):
        limitation = _require_mapping(value, f"$.limitations[{index}]", errors)
        _required(limitation, {"issue", "affected_inference", "mitigation", "severity", "evidence_ids"}, f"$.limitations[{index}]", errors)
        _check_evidence_ids(
            limitation.get("evidence_ids"),
            f"$.limitations[{index}].evidence_ids",
            errors,
            registered_evidence,
        )

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    args = parser.parse_args(argv)
    try:
        data = json.loads(args.ledger.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    errors = validate_ledger(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Ledger invalid: {len(errors)} error(s)", file=sys.stderr)
        return 1
    print(f"Ledger valid: {args.ledger}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
