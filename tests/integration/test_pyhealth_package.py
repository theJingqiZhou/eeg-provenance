from __future__ import annotations

import inspect
from importlib import metadata

import pytest

pytestmark = pytest.mark.pyhealth


def test_pyhealth_201_eeg_task_and_decoder_layer_contract() -> None:
    pytest.importorskip("pyhealth")
    import numpy as np
    import torch
    from pyhealth.models import CNNLayer
    from pyhealth.tasks import EEGAbnormalTUAB

    assert metadata.version("pyhealth") == "2.0.1"

    channel_names = [
        "EEG FP1-REF",
        "EEG F7-REF",
        "EEG T3-REF",
        "EEG T5-REF",
        "EEG O1-REF",
        "EEG FP2-REF",
        "EEG F8-REF",
        "EEG T4-REF",
        "EEG T6-REF",
        "EEG O2-REF",
        "EEG F3-REF",
        "EEG C3-REF",
        "EEG P3-REF",
        "EEG F4-REF",
        "EEG C4-REF",
        "EEG P4-REF",
    ]
    samples = np.arange(len(channel_names) * 200, dtype=float).reshape(
        len(channel_names), 200
    )
    task = EEGAbnormalTUAB(compute_stft=False)
    bipolar = task.convert_to_bipolar(samples, channel_names)
    sequence, pooled = CNNLayer(input_size=16, hidden_size=8, num_layers=2)(
        torch.zeros(2, 16, 20)
    )

    assert task.task_name == "EEG_abnormal"
    assert task.input_schema == {"signal": "tensor"}
    assert task.output_schema == {"label": "binary"}
    assert bipolar.shape == (16, 200)
    assert bipolar[0, 0] == -200
    assert tuple(sequence.shape) == (2, 8, 20)
    assert tuple(pooled.shape) == (2, 8)


def test_pyhealth_201_cache_and_source_write_contract_is_visible() -> None:
    pytest.importorskip("pyhealth")
    from pyhealth.datasets import BaseDataset, TUABDataset

    assert metadata.version("pyhealth") == "2.0.1"
    assert "cache_dir" in inspect.signature(BaseDataset).parameters
    set_task_parameters = inspect.signature(BaseDataset.set_task).parameters
    assert "input_processors" in set_task_parameters
    assert "output_processors" in set_task_parameters

    source = inspect.getsource(TUABDataset)
    assert "self.prepare_metadata()" in source
    assert "Path.home() / \".cache\" / \"pyhealth\" / \"tuab\"" in source
    assert "df.to_csv(csv_shared" in source
    assert "df.to_csv(csv_cache" in source
