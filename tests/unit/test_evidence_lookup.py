from __future__ import annotations

import json

from scripts import evidence_lookup


def test_lookup_returns_only_requested_sections(capsys) -> None:
    assert evidence_lookup.main(["S03", "S52"]) == 0
    output = capsys.readouterr().out
    assert 'id="s03"' in output
    assert 'id="s52"' in output
    assert 'id="s04"' not in output
    assert "## S53" not in output


def test_lookup_json_preserves_source_support_and_limits(capsys) -> None:
    assert evidence_lookup.main(["s53", "--format", "json"]) == 0
    records = json.loads(capsys.readouterr().out)
    assert [record["id"] for record in records] == ["S53"]
    assert {"source", "supports", "limits"} <= records[0].keys()


def test_lookup_rejects_unknown_ids(capsys) -> None:
    assert evidence_lookup.main(["S99"]) == 2
    assert "unknown evidence" in capsys.readouterr().err
