from __future__ import annotations

from importlib import metadata

import pytest

pytestmark = pytest.mark.braindecode


def test_braindecode_170_mne_window_and_decoder_contract() -> None:
    pytest.importorskip("braindecode")
    import mne
    import numpy as np
    import torch
    from braindecode.datasets import BaseConcatDataset, RawDataset
    from braindecode.models import EEGNet
    from braindecode.preprocessing import (
        Preprocessor,
        create_windows_from_events,
        preprocess,
    )

    assert metadata.version("braindecode") == "1.7.0"

    info = mne.create_info(["C3", "C4"], sfreq=256, ch_types="eeg")
    data = np.random.default_rng(7).normal(scale=1e-6, size=(2, 1536))
    raw = mne.io.RawArray(data, info, verbose="ERROR")
    raw.set_annotations(
        mne.Annotations(
            onset=[1.0, 3.0],
            duration=[0.0, 0.0],
            description=["left", "right"],
        )
    )
    dataset = BaseConcatDataset(
        [RawDataset(raw, description={"subject": "synthetic"})]
    )

    preprocess(
        dataset,
        [Preprocessor("resample", apply_on_array=False, sfreq=128)],
        n_jobs=1,
    )
    windows = create_windows_from_events(
        dataset,
        trial_stop_offset_samples=128,
        mapping={"left": 0, "right": 1},
        preload=True,
    )
    x, label, _ = windows[0]
    output = EEGNet(
        n_chans=2,
        n_outputs=2,
        n_times=x.shape[-1],
        final_layer_with_constraint=True,
    )(
        torch.as_tensor(x[None], dtype=torch.float32)
    )

    assert dataset.datasets[0].raw.info["sfreq"] == 128
    assert len(windows) == 2
    assert x.shape == (2, 128)
    assert label == 0
    assert [windows[index][1] for index in range(len(windows))] == [0, 1]
    assert tuple(output.shape) == (1, 2)


def test_braindecode_170_exports_guard_documentation_drift() -> None:
    datasets = pytest.importorskip("braindecode.datasets")
    models = pytest.importorskip("braindecode.models")

    assert metadata.version("braindecode") == "1.7.0"
    assert hasattr(datasets, "RawDataset")
    assert not hasattr(datasets, "BaseDataset")
    assert hasattr(models, "EEGNet")
    assert not hasattr(models, "EEGNetv4")
