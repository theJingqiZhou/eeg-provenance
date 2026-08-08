#!/usr/bin/env python3
"""Exercise the documented MNE recipes on deterministic synthetic EEG."""

from __future__ import annotations

import importlib.metadata as metadata
import json

import mne
import numpy as np
from mne.preprocessing import ICA


def _rank(raw: mne.io.BaseRaw) -> int:
    return int(mne.compute_rank(raw, rank=None, verbose=False).get("eeg", 0))


def run_verification() -> dict[str, object]:
    rng = np.random.default_rng(97)
    sfreq = 256.0
    duration = 12.0
    times = np.arange(int(sfreq * duration)) / sfreq
    eeg_names = [
        "Fp1", "Fp2", "F7", "F3", "Fz", "F4", "F8", "T7", "C3", "Cz",
        "C4", "T8", "P7", "P3", "Pz", "P4", "P8", "O1", "Oz", "O2",
    ]
    channel_names = [*eeg_names, "EOG"]
    channel_types = ["eeg"] * len(eeg_names) + ["eog"]
    data = np.vstack(
        [
            8e-6 * np.sin(2 * np.pi * (8.0 + index / 10) * times)
            + 2e-6 * rng.standard_normal(times.size)
            for index in range(len(eeg_names))
        ]
        + [
            20e-6 * np.sin(2 * np.pi * 1.2 * times)
            + 3e-6 * rng.standard_normal(times.size)
        ]
    )
    info = mne.create_info(channel_names, sfreq, channel_types)
    raw = mne.io.RawArray(data, info, verbose=False)
    raw.set_montage("standard_1020", on_missing="raise", verbose=False)
    raw.set_annotations(
        mne.Annotations(
            onset=[2.0, 5.0, 8.0],
            duration=[0.0, 0.0, 0.0],
            description=["target", "standard", "target"],
        )
    )
    events, event_id = mne.events_from_annotations(raw, event_id="auto", use_rounding=True, verbose=False)

    rank_native = _rank(raw)
    reref, _ = mne.set_eeg_reference(
        raw.copy(), ref_channels="average", projection=False, copy=False, verbose=False
    )
    rank_reref = _rank(reref)
    reref.info["bads"] = ["P4"]
    rank_pre_interp = _rank(reref)
    interpolated = reref.copy().interpolate_bads(
        reset_bads=False,
        mode="accurate",
        method={"eeg": "spline"},
        verbose=False,
    )
    rank_post_interp = _rank(interpolated)
    if interpolated.info["bads"] != ["P4"]:
        raise AssertionError("interpolated channel state was reset unexpectedly")

    filtered = interpolated.copy().filter(
        l_freq=1.0,
        h_freq=40.0,
        method="fir",
        phase="zero",
        fir_design="firwin",
        pad="reflect_limited",
        verbose=False,
    )
    resampled, resampled_events = filtered.copy().resample(
        128.0,
        events=events,
        method="polyphase",
        verbose=False,
    )
    original_seconds = events[:, 0] / sfreq
    resampled_seconds = resampled_events[:, 0] / resampled.info["sfreq"]
    max_event_delta_s = float(np.max(np.abs(original_seconds - resampled_seconds)))
    if max_event_delta_s > 0.5 / resampled.info["sfreq"] + np.finfo(float).eps:
        raise AssertionError("event timing changed by more than half a target sample")

    ica_training = reref.copy().filter(l_freq=1.0, h_freq=None, verbose=False)
    ica_training.info["bads"] = []
    ica = ICA(
        n_components=5,
        method="infomax",
        fit_params={"extended": True},
        random_state=97,
        max_iter=1000,
    )
    ica.fit(ica_training, picks="eeg", verbose=False)
    sources = ica.get_sources(ica_training)
    if sources.n_times != raw.n_times or len(sources.ch_names) != 5:
        raise AssertionError("ICA source shape does not match the declared contract")

    return {
        "versions": {
            package: metadata.version(package)
            for package in ("mne", "mne-bids", "mne-icalabel", "autoreject")
        },
        "input_shape": list(raw.get_data().shape),
        "input_sfreq_hz": sfreq,
        "event_id": event_id,
        "event_count": int(len(events)),
        "rank": {
            "native": rank_native,
            "average_reference": rank_reref,
            "before_interpolation": rank_pre_interp,
            "after_interpolation": rank_post_interp,
        },
        "channel_state_transition": "P4:native->bad->interpolated",
        "interpolated_channel_retained_in_bads": interpolated.info["bads"],
        "output_sfreq_hz": float(resampled.info["sfreq"]),
        "max_event_delta_s": max_event_delta_s,
        "ica_components": int(ica.n_components_),
        "ica_method": ica.method,
        "random_seed": 97,
    }


def main() -> int:
    print(json.dumps(run_verification(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
