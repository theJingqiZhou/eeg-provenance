#!/usr/bin/env python3
"""Validate an EEG provenance ledger: JSON Schema, then project invariants."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

try:
    import rfc3339_validator
    from jsonschema import Draft202012Validator, FormatChecker
except ModuleNotFoundError:  # pragma: no cover - exercised only outside validation env
    rfc3339_validator = None  # type: ignore[assignment]
    Draft202012Validator = None  # type: ignore[assignment,misc]
    FormatChecker = None  # type: ignore[assignment,misc]


SCHEMA_VERSION = "1.2.0"
SKILL_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = SKILL_ROOT / "assets" / "provenance-ledger.schema.json"
EVIDENCE_REGISTER = SKILL_ROOT / "references" / "evidence-register.md"
EVIDENCE_ANCHOR_RE = re.compile(r'<a id="(s\d{2})"></a>', re.IGNORECASE)
RANK_EFFECTS = {"drop", "interpolate", "rereference", "virtual"}
TRAINING_SCOPES = {"training_only", "within_train_fold"}


def _json_path(parts: Iterable[Any]) -> str:
    path = "$"
    for part in parts:
        path += f"[{part}]" if isinstance(part, int) else f".{part}"
    return path


def validate_schema(data: Any) -> list[str]:
    """Run the canonical Draft 2020-12 schema before semantic checks."""

    if (
        Draft202012Validator is None
        or FormatChecker is None
        or rfc3339_validator is None
    ):
        return [
            "schema validation unavailable: install jsonschema>=4.25 and "
            "rfc3339-validator>=0.1.4 before running validate_ledger.py"
        ]
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"schema load failed: {exc}"]
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:  # jsonschema raises a detailed SchemaError
        return [f"schema definition invalid: {exc}"]
    format_checker = FormatChecker()
    format_checker.checks("date-time", raises=Exception)(
        rfc3339_validator.validate_rfc3339
    )
    validator = Draft202012Validator(schema, format_checker=format_checker)
    errors = sorted(
        validator.iter_errors(data),
        key=lambda error: tuple(str(part) for part in error.path),
    )
    return [f"schema {_json_path(error.path)}: {error.message}" for error in errors]


def _normalize_path(value: str) -> PurePosixPath:
    return PurePosixPath(value.replace("\\", "/").rstrip("/").casefold())


def _is_within(child: str, parent: str) -> bool:
    child_path = _normalize_path(child)
    parent_path = _normalize_path(parent)
    return child_path == parent_path or parent_path in child_path.parents


def _registered_evidence_ids() -> set[str]:
    try:
        text = EVIDENCE_REGISTER.read_text(encoding="utf-8")
    except OSError:
        return set()
    return {match.upper() for match in EVIDENCE_ANCHOR_RE.findall(text)}


def _check_registered_evidence(
    value: list[str], path: str, registered: set[str], errors: list[str]
) -> None:
    for index, source_id in enumerate(value):
        if source_id not in registered:
            errors.append(f"{path}[{index}]: evidence ID {source_id} is not registered")


def _record_unique(
    value: str, seen: set[str], path: str, label: str, errors: list[str]
) -> None:
    key = value.casefold()
    if key in seen:
        errors.append(f"{path}: duplicate {label} {value!r}")
    else:
        seen.add(key)


def validate_semantics(ledger: dict[str, Any]) -> list[str]:
    """Check graph, archive, evidence, rank, and evaluation invariants."""

    errors: list[str] = []
    registered = _registered_evidence_ids()
    if not registered:
        errors.append("references/evidence-register.md: no registered evidence IDs found")

    dataset = ledger["dataset"]
    source_root = dataset["source_root"]
    recording_ids: set[str] = set()
    for index, recording in enumerate(dataset["recordings"]):
        _record_unique(
            recording["id"],
            recording_ids,
            f"$.dataset.recordings[{index}].id",
            "recording ID",
            errors,
        )

    entity_ids: set[str] = set()
    for index, entity in enumerate(ledger["inputs"]["entities"]):
        _record_unique(
            entity["id"],
            entity_ids,
            f"$.inputs.entities[{index}].id",
            "entity ID",
            errors,
        )
        if entity["recording_id"].casefold() not in recording_ids:
            errors.append(f"$.inputs.entities[{index}].recording_id: unknown recording")

    channel_names: set[str] = set()
    for index, channel in enumerate(ledger["inputs"]["channel_support"]):
        _record_unique(
            channel["name"],
            channel_names,
            f"$.inputs.channel_support[{index}].name",
            "channel",
            errors,
        )

    decisions: dict[str, dict[str, Any]] = {}
    candidates: dict[str, tuple[str, dict[str, Any]]] = {}
    phases: set[str] = set()
    for decision_index, decision in enumerate(
        ledger["contract"]["toolchain_decisions"]
    ):
        decision_path = f"$.contract.toolchain_decisions[{decision_index}]"
        decision_key = decision["id"].casefold()
        if decision_key in decisions:
            errors.append(f"{decision_path}.id: duplicate decision ID {decision['id']!r}")
        else:
            decisions[decision_key] = decision
        _record_unique(
            decision["phase"], phases, f"{decision_path}.phase", "phase", errors
        )
        for candidate_index, candidate in enumerate(decision["candidates"]):
            candidate_path = f"{decision_path}.candidates[{candidate_index}]"
            candidate_key = candidate["id"].casefold()
            if candidate_key in candidates:
                errors.append(
                    f"{candidate_path}.id: duplicate candidate ID {candidate['id']!r}"
                )
            else:
                candidates[candidate_key] = (decision_key, candidate)
            if candidate["status"] == "selected":
                if candidate["availability"] != "verified":
                    errors.append(
                        f"{candidate_path}.availability: selected tool must be verified"
                    )
                if not candidate["version"]:
                    errors.append(
                        f"{candidate_path}.version: selected tool requires a verified version"
                    )
            if candidate["status"] == "planned" and candidate["availability"] == "unavailable":
                errors.append(
                    f"{candidate_path}.availability: planned tool cannot be unavailable"
                )
            _check_registered_evidence(
                candidate["evidence_ids"],
                f"{candidate_path}.evidence_ids",
                registered,
                errors,
            )

    for index, decision in enumerate(ledger["contract"]["harmonization_decisions"]):
        _check_registered_evidence(
            decision["evidence_ids"],
            f"$.contract.harmonization_decisions[{index}].evidence_ids",
            registered,
            errors,
        )

    activity_ids: set[str] = set()
    generated_entities: set[str] = set()
    sequences: list[int] = []
    evaluation_mode = ledger["contract"]["evaluation_mode"]
    for index, activity in enumerate(ledger["activities"]):
        path = f"$.activities[{index}]"
        _record_unique(
            activity["id"], activity_ids, f"{path}.id", "activity ID", errors
        )
        sequences.append(activity["sequence"])

        decision_key = activity["toolchain_decision_id"].casefold()
        candidate_key = activity["tool_candidate_id"].casefold()
        decision = decisions.get(decision_key)
        candidate_entry = candidates.get(candidate_key)
        if decision is None:
            errors.append(f"{path}.toolchain_decision_id: unknown decision")
        if candidate_entry is None:
            errors.append(f"{path}.tool_candidate_id: unknown candidate")
        elif candidate_entry[0] != decision_key:
            errors.append(f"{path}.tool_candidate_id: candidate belongs to another decision")
        else:
            candidate = candidate_entry[1]
            if decision is not None and decision["status"] != "selected":
                errors.append(f"{path}.toolchain_decision_id: activity requires a selected decision")
            if candidate["status"] != "selected":
                errors.append(f"{path}.tool_candidate_id: activity requires a selected candidate")
            if activity["software"]["name"].casefold() != candidate["tool"].casefold():
                errors.append(f"{path}.software.name: does not match selected candidate tool")
            if activity["software"]["version"] != candidate["version"]:
                errors.append(f"{path}.software.version: does not match selected candidate version")

        available_entities = entity_ids | generated_entities
        for entity_id in activity["input_entities"]:
            if entity_id.casefold() not in available_entities:
                errors.append(
                    f"{path}.input_entities: {entity_id!r} is not available before this activity"
                )
        for entity_id in activity["output_entities"]:
            entity_key = entity_id.casefold()
            if entity_key in available_entities:
                errors.append(f"{path}.output_entities: duplicate entity ID {entity_id!r}")
            else:
                generated_entities.add(entity_key)

        if activity["channel_effect"] in RANK_EFFECTS and activity.get("rank") is None:
            errors.append(
                f"{path}.rank: required for channel effect {activity['channel_effect']!r}"
            )
        if evaluation_mode == "predictive" and activity["adaptive"]:
            if activity["fit_scope"] not in TRAINING_SCOPES:
                errors.append(
                    f"{path}.fit_scope: adaptive predictive activity must be training-only"
                )
        _check_registered_evidence(
            activity["evidence_ids"], f"{path}.evidence_ids", registered, errors
        )

    if len(sequences) != len(set(sequences)):
        errors.append("$.activities[*].sequence: sequence values must be unique")
    if sequences != sorted(sequences):
        errors.append("$.activities[*].sequence: activities must be listed in sequence order")

    output_ids: set[str] = set()
    for index, output in enumerate(ledger["outputs"]):
        path = f"$.outputs[{index}]"
        _record_unique(output["id"], output_ids, f"{path}.id", "output ID", errors)
        if _is_within(output["path"], source_root):
            errors.append(f"{path}.path: derivative output is inside source_root")
        if output["source_entity"].casefold() not in entity_ids:
            errors.append(f"{path}.source_entity: unknown source input entity")
        if output["generating_activity"].casefold() not in activity_ids:
            errors.append(f"{path}.generating_activity: unknown activity")

    for index, limitation in enumerate(ledger["limitations"]):
        _check_registered_evidence(
            limitation["evidence_ids"],
            f"$.limitations[{index}].evidence_ids",
            registered,
            errors,
        )
    return errors


def validate_ledger(data: Any) -> list[str]:
    """Validate shape first; run semantic invariants only on schema-valid data."""

    schema_errors = validate_schema(data)
    if schema_errors:
        return schema_errors
    return validate_semantics(data)


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
