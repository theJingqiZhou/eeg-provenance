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
        create_fixed_length_windows,
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
    wrapped_raw = dataset.datasets[0].raw

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
    assert dataset.datasets[0].raw is wrapped_raw
    assert len(windows) == 2
    assert x.shape == (2, 128)
    assert label == 0
    assert [windows[index][1] for index in range(len(windows))] == [0, 1]
    assert tuple(output.shape) == (1, 2)


def test_braindecode_audio_dependency_is_cpu_compatible() -> None:
    import torch
    import torchaudio

    assert metadata.version("torchaudio").split("+", 1)[0] == "2.11.0"
    assert torch.version.cuda is None
    assert torchaudio.__version__.split("+", 1)[0] == "2.11.0"


def test_braindecode_170_fixed_window_remainder_and_target_contract() -> None:
    pytest.importorskip("braindecode")
    import mne
    import numpy as np
    from braindecode.datasets import BaseConcatDataset, RawDataset
    from braindecode.preprocessing import create_fixed_length_windows

    assert metadata.version("braindecode") == "1.7.0"

    def make_dataset(*, target_name: str | None) -> BaseConcatDataset:
        info = mne.create_info(["Cz"], sfreq=100, ch_types="eeg")
        raw = mne.io.RawArray(np.zeros((1, 950)), info, verbose="ERROR")
        return BaseConcatDataset(
            [
                RawDataset(
                    raw,
                    description={"target": 7},
                    target_name=target_name,
                )
            ]
        )

    keep_remainder = create_fixed_length_windows(
        make_dataset(target_name="target"),
        window_size_samples=400,
        window_stride_samples=300,
        drop_last_window=False,
        preload=True,
    )
    drop_remainder = create_fixed_length_windows(
        make_dataset(target_name="target"),
        window_size_samples=400,
        window_stride_samples=300,
        drop_last_window=True,
        preload=True,
    )
    no_target = create_fixed_length_windows(
        make_dataset(target_name=None),
        window_size_samples=400,
        window_stride_samples=300,
        drop_last_window=True,
        preload=True,
    )

    metadata_frame = keep_remainder.datasets[0].metadata
    assert metadata_frame["i_start_in_trial"].tolist() == [0, 300, 550]
    assert metadata_frame["i_stop_in_trial"].tolist() == [400, 700, 950]
    assert [keep_remainder[index][1] for index in range(3)] == [7, 7, 7]
    assert len(drop_remainder) == 2
    assert [no_target[index][1] for index in range(2)] == [-1, -1]


def test_braindecode_170_exports_guard_documentation_drift() -> None:
    datasets = pytest.importorskip("braindecode.datasets")
    models = pytest.importorskip("braindecode.models")

    assert metadata.version("braindecode") == "1.7.0"
    assert hasattr(datasets, "RawDataset")
    assert not hasattr(datasets, "BaseDataset")
    assert hasattr(models, "EEGNet")
    assert not hasattr(models, "EEGNetv4")
