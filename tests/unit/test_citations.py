from pathlib import Path

from tools.audit_citations import _declared_ids, audit


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = REPO_ROOT / "skill" / "eeg-provenance"


def test_scientific_claims_have_resolving_citations() -> None:
    assert audit(SKILL_ROOT) == []


def test_compact_evidence_syntax_expands_ranges() -> None:
    assert _declared_ids("Claim. (Evidence: S03, S20–S22; local policy)") == {
        "S03",
        "S20",
        "S21",
        "S22",
    }
    assert _declared_ids("| Evidence | S52–S53 |") == {"S52", "S53"}
