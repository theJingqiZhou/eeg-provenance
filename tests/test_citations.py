from pathlib import Path

from scripts.audit_citations import audit


ROOT = Path(__file__).resolve().parents[1]


def test_scientific_claims_have_resolving_citations() -> None:
    assert audit(ROOT) == []
