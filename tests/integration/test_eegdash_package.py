import inspect

import pytest

from scripts.eegdash_intake import IntakeError, _load_one


pytestmark = pytest.mark.eegdash


def test_pinned_eegdash_surface_and_storage_contract() -> None:
    import eegdash
    from eegdash import EEGDash, EEGDashDataset
    from eegdash.dataset import DS003061, NM000166
    from eegdash.dataset._source_inference import expected_backend

    assert eegdash.__version__ == "0.8.4"
    assert "download" in inspect.signature(EEGDashDataset).parameters
    assert "limit" not in inspect.signature(EEGDash.find).parameters
    assert DS003061.__name__ == "DS003061"
    assert NM000166.__name__ == "NM000166"
    assert expected_backend("ds003061") == "s3"
    assert expected_backend("nm000166") == "nemar"
    assert expected_backend("on002724") == "nemar"


def test_ambiguous_online_query_never_accesses_raw(monkeypatch, tmp_path) -> None:
    import eegdash

    raw_accessed = False

    class Recording:
        @property
        def raw(self):
            nonlocal raw_accessed
            raw_accessed = True
            raise AssertionError("raw must remain lazy for an ambiguous query")

    class AmbiguousDataset:
        def __init__(self, **kwargs):
            self.datasets = [Recording(), Recording()]

    monkeypatch.setattr(eegdash, "EEGDashDataset", AmbiguousDataset)
    with pytest.raises(IntakeError, match="selected 2"):
        _load_one(
            tmp_path,
            {"dataset": "ds003061", "subject": "001", "task": "P300"},
            download=True,
            sample_seconds=1.0,
        )
    assert raw_accessed is False


@pytest.mark.parametrize("dataset", ["nm000166", "on002724"])
def test_nemar_online_download_is_refused_before_dataset_construction(
    monkeypatch, tmp_path, dataset
) -> None:
    import eegdash

    class MustNotConstruct:
        def __init__(self, **kwargs):
            raise AssertionError("NeMAR download should be refused before construction")

    monkeypatch.setattr(eegdash, "EEGDashDataset", MustNotConstruct)
    with pytest.raises(IntakeError, match="non-fetchable"):
        _load_one(
            tmp_path,
            {
                "dataset": dataset,
                "subject": "001",
                "session": "01",
                "task": "aep",
            },
            download=True,
            sample_seconds=1.0,
        )
