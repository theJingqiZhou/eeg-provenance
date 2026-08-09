from __future__ import annotations

import json
from pathlib import Path

from tools.score_eval_responses import load_cases, main, score_responses


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_repository_eval_cases_are_well_formed() -> None:
    cases = load_cases()
    assert len(cases) == len({case["id"] for case in cases})
    assert {"light-edf-inspection", "operation-window-semantics"} <= {
        case["id"] for case in cases
    }


def test_scorer_is_case_insensitive_and_reports_forbidden_terms() -> None:
    cases = [
        {
            "id": "example",
            "prompt": "prompt",
            "must_include": ["Inspection Finding", "native_header"],
            "must_not_include": ["Provenance Ledger"],
        }
    ]
    passed = score_responses(
        cases, {"example": "INSPECTION FINDING at native_header scope"}
    )
    failed = score_responses(
        cases, {"example": "Inspection Finding and a Provenance Ledger"}
    )
    assert passed["summary"] == {"passed": 1, "failed": 0, "total": 1}
    assert failed["results"][0]["missing_terms"] == ["native_header"]
    assert failed["results"][0]["forbidden_terms"] == ["Provenance Ledger"]


def test_cli_scores_a_selected_saved_response(tmp_path, capsys) -> None:
    response = {
        "light-edf-inspection": (
            "Inspection Finding: native_header read scope; declared units unknown."
        )
    }
    path = tmp_path / "responses.json"
    path.write_text(json.dumps(response), encoding="utf-8")

    assert main([str(path), "--case", "light-edf-inspection"]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["summary"] == {"passed": 1, "failed": 0, "total": 1}
