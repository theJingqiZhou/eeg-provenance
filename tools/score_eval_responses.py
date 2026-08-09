#!/usr/bin/env python3
"""Score saved agent responses against eeg-provenance forward-test cases."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


DEFAULT_CASES = Path(__file__).resolve().parents[1] / "evals" / "cases.json"


def load_cases(path: Path = DEFAULT_CASES) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    cases = data.get("cases")
    if not isinstance(cases, list):
        raise ValueError("cases file must contain a 'cases' array")
    seen: set[str] = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            raise ValueError(f"cases[{index}] must be an object")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            raise ValueError(f"cases[{index}].id must be a non-empty string")
        if case_id in seen:
            raise ValueError(f"duplicate case id: {case_id}")
        seen.add(case_id)
        for field in ("prompt", "must_include", "must_not_include"):
            if field not in case:
                raise ValueError(f"{case_id}: missing {field}")
        if not isinstance(case["prompt"], str):
            raise ValueError(f"{case_id}.prompt must be a string")
        for field in ("must_include", "must_not_include"):
            if not isinstance(case[field], list) or not all(
                isinstance(term, str) and term for term in case[field]
            ):
                raise ValueError(f"{case_id}.{field} must contain strings")
    return cases


def score_responses(
    cases: list[dict[str, Any]],
    responses: dict[str, str],
    selected_ids: set[str] | None = None,
) -> dict[str, Any]:
    known = {case["id"] for case in cases}
    selected = selected_ids or known
    unknown = sorted(selected - known)
    if unknown:
        raise ValueError(f"unknown case id(s): {', '.join(unknown)}")
    unknown_responses = sorted(set(responses) - known)
    if unknown_responses:
        raise ValueError(
            f"response has unknown case id(s): {', '.join(unknown_responses)}"
        )
    for case_id, response in responses.items():
        if not isinstance(response, str):
            raise ValueError(f"response for {case_id} must be a string")

    results: list[dict[str, Any]] = []
    for case in cases:
        case_id = case["id"]
        if case_id not in selected:
            continue
        response = responses.get(case_id)
        folded = response.casefold() if response is not None else ""
        missing = [
            term for term in case["must_include"] if term.casefold() not in folded
        ]
        forbidden = [
            term for term in case["must_not_include"] if term.casefold() in folded
        ]
        results.append(
            {
                "id": case_id,
                "passed": response is not None and not missing and not forbidden,
                "response_missing": response is None,
                "missing_terms": missing,
                "forbidden_terms": forbidden,
            }
        )
    passed = sum(result["passed"] for result in results)
    return {
        "summary": {
            "passed": passed,
            "failed": len(results) - passed,
            "total": len(results),
        },
        "results": results,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("responses", type=Path, help="JSON object mapping case IDs to responses")
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--case", action="append", default=[], dest="case_ids")
    args = parser.parse_args(argv)
    try:
        cases = load_cases(args.cases)
        responses = json.loads(args.responses.read_text(encoding="utf-8"))
        if not isinstance(responses, dict):
            raise ValueError("responses file must be a JSON object")
        report = score_responses(cases, responses, set(args.case_ids) or None)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2))
    return 0 if report["summary"]["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
