from pathlib import Path

from tools.audit_citations import audit


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = REPO_ROOT / "skill" / "eeg-provenance"


def test_scientific_claims_have_resolving_citations() -> None:
    assert audit(SKILL_ROOT) == []
