# MNE-Python recipes

These recipes are software contracts exercised in the project validation environment against MNE 1.12.1 with its `hdf5` extra, MNE-BIDS 0.19.0, MNE-ICALabel 0.8.1, and AutoReject 0.4.4; they are not scientific defaults. Record actual versions in every ledger. [[S14]](evidence-register.md#s14) [[S15]](evidence-register.md#s15) [[S17]](evidence-register.md#s17) [[S26]](evidence-register.md#s26) [[S49]](evidence-register.md#s49)

## Contents

- [Environment and version capture](#environment-and-version-capture)
- [Read BIDS without preloading](#read-bids-without-preloading)
- [Read one non-BIDS container without preloading](#read-one-non-bids-container-without-preloading)
- [Route MATLAB MAT files by version](#route-matlab-mat-files-by-version)
- [Convert annotations to events](#convert-annotations-to-events)
- [Filter with an explicit effective design](#filter-with-an-explicit-effective-design)
- [Resample signal and events together](#resample-signal-and-events-together)
- [Reference and rank](#reference-and-rank)
- [Interpolate marked bad channels](#interpolate-marked-bad-channels)
- [Fit and apply ICA](#fit-and-apply-ica)
- [Safe derivative write](#safe-derivative-write)

## Environment and version capture

```python
import importlib.metadata as md

versions = {
    name: md.version(name)
    for name in (
        "mne",
        "mne-bids",
        "mne-icalabel",
        "autoreject",
        "h5io",
        "h5py",
        "pymatreader",
    )
}
```

Pinning a tested environment supports reproduction but does not make an intervention appropriate for a new dataset; use the contract and record version drift. [[S03]](evidence-register.md#s03) [[S06]](evidence-register.md#s06)

## Read BIDS without preloading

```python
from mne_bids import BIDSPath, read_raw_bids

bids_path = BIDSPath(
    root=dataset_root,
    subject="001",
    task="P300",
    run="1",
    datatype="eeg",
)
raw = read_raw_bids(bids_path, extra_params={"preload": False}, verbose=False)
```

`read_raw_bids` applies supported BIDS sidecar metadata to `Raw`, but still compare `raw.info`, annotations, and channel locations with the intake report and preserve warnings. [[S01]](evidence-register.md#s01) [[S26]](evidence-register.md#s26)

For annex-managed data, resolve availability through archive policy and read the immutable object only when authorized. Do not use a test recipe to fetch, unlock, drop, or rewrite annex objects; this is local policy enforcing the source/derivative separation. [[S05]](evidence-register.md#s05) [[S23]](evidence-register.md#s23)

## Read one non-BIDS container without preloading

```python
import mne

edf = mne.io.read_raw_edf(
    selected_edf,
    preload=False,
    infer_types=False,
    verbose="ERROR",
)
gdf = mne.io.read_raw_gdf(
    selected_gdf,
    preload=False,
    verbose="ERROR",
)
eeglab = mne.io.read_raw_eeglab(
    selected_set,
    preload=False,
    verbose="ERROR",
)
```

Call only the reader matching the selected file. Record `raw.info`, `raw.ch_names`, reader channel types, annotations, warnings, and `raw.preload`; do not call `load_data()` during header-level intake. [[S27]](evidence-register.md#s27) [[S43]](evidence-register.md#s43)

Treat generated names, inferred types, a recording-wide sampling rate, and annotation descriptions as reader observations. Reconcile them with the versioned dataset protocol and use PyEDFlib when native EDF per-signal header fields must remain visible. [[S03]](evidence-register.md#s03) [[S42]](evidence-register.md#s42) [[S43]](evidence-register.md#s43) [[S46]](evidence-register.md#s46)

## Route MATLAB MAT files by version

First probe whether the installed MNE/HDF5 route is sufficient. If it is absent and the operation requires MATLAB v7.3 support, resolve `mne[hdf5]==1.12.1` only in an authorized isolated environment using the site's approved manager; for a pip-managed lane, invoke `python -m pip`, never bare `pip`. In MNE 1.12.1 this extra supplies `h5io` and `pymatreader`, with `h5py` supplied transitively; the project exercise resolved h5io 0.2.5, h5py 3.16.0, and pymatreader 1.2.3. Apply the [runtime compatibility matrix](runtime-compatibility.md) before changing an environment. [[S49]](evidence-register.md#s49) [[S58]](evidence-register.md#s58) [[S61]](evidence-register.md#s61)

Use SciPy `whosmat`/`loadmat` only for MAT v4 through v7.2. SciPy explicitly does not implement the HDF5/v7.3 interface, so a v7.3 failure is a routing decision rather than evidence that MATLAB is required. [[S43]](evidence-register.md#s43) [[S49]](evidence-register.md#s49)

For a v7.3 file, inventory the HDF5 hierarchy without reading dataset values:

```python
from pathlib import Path

import h5py

mat_path = Path(selected_mat)
if not h5py.is_hdf5(mat_path):
    raise ValueError("Route this file to scipy.io.whosmat/loadmat")

inventory = []
with h5py.File(mat_path, "r") as handle:
    def note(name, obj):
        if isinstance(obj, h5py.Dataset):
            inventory.append(
                {
                    "name": name,
                    "shape": obj.shape,
                    "dtype": str(obj.dtype),
                    "attributes": sorted(obj.attrs),
                }
            )

    handle.visititems(note)
```

Do not index datasets during this metadata pass: MATLAB cells and structs can use object references, and shapes, attributes, or names do not establish EEG axes, units, labels, or prior processing. Resolve those semantics from the release contract before selecting variables. [[S03]](evidence-register.md#s03) [[S39]](evidence-register.md#s39) [[S49]](evidence-register.md#s49)

After the adaptation record identifies the required variables, use pymatreader's bounded variable selection:

```python
from pymatreader import read_mat

selected = read_mat(
    selected_mat,
    variable_names=["signal", "sampling_frequency", "channel_labels"],
)
```

Replace the example names with documented variables and record the returned types and shapes. Pymatreader converts MATLAB primitives, matrices, cells, and structs to Python representations; successful conversion does not validate the dataset-specific axis or label contract. [[S39]](evidence-register.md#s39) [[S49]](evidence-register.md#s49)

Use `mne.io.read_raw_eeglab()` only for an EEGLAB `.set` contract and MNE's format-specific readers only for their documented formats. The presence of HDF5 or a `.mat` suffix does not make an arbitrary v7.3 structure an EEGLAB or MNE object, and `h5io` is not a generic MATLAB semantic parser. [[S27]](evidence-register.md#s27) [[S43]](evidence-register.md#s43) [[S49]](evidence-register.md#s49)

## Convert annotations to events

```python
events, event_id = mne.events_from_annotations(
    raw,
    event_id="auto",
    use_rounding=True,
)
```

Save both the original annotation table and the resulting `event_id`/sample array. The function performs a documented conversion but cannot validate experimental semantics. [[S01]](evidence-register.md#s01) [[S29]](evidence-register.md#s29)

## Filter with an explicit effective design

```python
filtered = raw.copy().load_data().filter(
    l_freq=1.0,
    h_freq=40.0,
    method="fir",
    phase="zero",
    fir_design="firwin",
    pad="reflect_limited",
)
```

Replace the example cutoffs from the Preprocessing Contract; record MNE’s logged filter length and transition bands in addition to the arguments. Cutoffs alone do not specify the response, and high-pass choices can distort transient endpoints. [[S09]](evidence-register.md#s09) [[S10]](evidence-register.md#s10) [[S27]](evidence-register.md#s27)

## Resample signal and events together

```python
resampled, resampled_events = filtered.copy().resample(
    128.0,
    events=events,
    method="polyphase",
)
```

Record old/new event samples and the maximum timing difference. MNE applies anti-alias filtering and documents possible event jitter; epoch first when that better matches the endpoint and boundary policy. [[S27]](evidence-register.md#s27)

## Reference and rank

```python
import mne

rank_before = mne.compute_rank(raw, rank=None)
reref, ref_data = mne.set_eeg_reference(
    raw.copy(),
    ref_channels="average",
    projection=False,
    copy=False,
)
rank_after = mne.compute_rank(reref, rank=None)
```

Replace average reference when the contract selects another representation. Record included channels, bad-channel exclusions, projection/application mode, `ref_data` availability, and rank estimator/tolerance. [[S08]](evidence-register.md#s08) [[S28]](evidence-register.md#s28)

## Interpolate marked bad channels

```python
work = reref.copy()
work.info["bads"] = ["Pz"]
rank_pre_interp = mne.compute_rank(work, rank=None)
work.interpolate_bads(
    reset_bads=False,
    mode="accurate",
    method={"eeg": "spline"},
)
rank_post_interp = mne.compute_rank(work, rank=None)
```

Run only with defensible channel locations. Keep the channel marked bad until the ledger records the transition, and label the final channel `interpolated`; MNE’s success does not turn the estimate into native data. [[S07]](evidence-register.md#s07) [[S28]](evidence-register.md#s28)

## Fit and apply ICA

```python
from mne.preprocessing import ICA

ica_training = raw.copy().load_data().filter(l_freq=1.0, h_freq=None)
ica = ICA(
    n_components=0.99,
    method="fastica",
    random_state=97,
    max_iter="auto",
)
ica.fit(ica_training, picks="eeg")

# Inspect/label components, then declare exclusions explicitly.
ica.exclude = selected_components
cleaned = ica.apply(raw.copy())
```

Treat the 1 Hz filter as an example consistent with current MNE practical guidance and conditional ICA evidence, not a universal cutoff. Record the training copy, channel order, reference, rank, algorithm, convergence, selection evidence, and compatibility of the application target. [[S12]](evidence-register.md#s12) [[S14]](evidence-register.md#s14)

When using MNE-ICALabel, verify its documented extended-infomax, average-reference, and 1–100 Hz assumptions; otherwise label the mismatch and do not convert classifier probabilities into automatic component truth. [[S13]](evidence-register.md#s13) [[S15]](evidence-register.md#s15)

## Safe derivative write

```python
from pathlib import Path

source_root = Path(dataset_root).resolve()
derivative_root = Path(output_root).resolve()
if derivative_root == source_root or source_root in derivative_root.parents:
    raise ValueError("Derivative root must be outside the source dataset")
```

When claiming BIDS Derivatives compatibility, create the derivative dataset description, avoid a raw-filename collision with an appropriate entity such as `desc-<label>`, propagate required metadata that remain valid, and record immediate inputs in `Sources` using BIDS URIs. Otherwise label the output as a project derivative without a BIDS conformance claim. [[S23]](evidence-register.md#s23)
