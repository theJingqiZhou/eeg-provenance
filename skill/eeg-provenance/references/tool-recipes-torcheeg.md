# TorchEEG and MOABB dataset-adapter recipe

Use TorchEEG as a versioned implementation lead after generic format intake, not as the authority for a dataset contract. Built-in adapters encode assumptions and can load, segment, transform, and cache signal data. [[S44]](evidence-register.md#s44)

Use MOABB as the preferred maintained BCI adapter/benchmark route when it supports the dataset and endpoint. Its dataset object exposes MNE Raw recordings, while paradigms and evaluations remain separate choices. [[S45]](evidence-register.md#s45)

## 1. Record the installed contract

```python
import importlib.metadata as metadata

version = metadata.version("torcheeg")
print(version)
```

Match the installed version to a tagged source tree and record the adapter module, class, and commit or release tag. Stable documentation can move ahead of the environment, so cite version-pinned source for behavior. [[S06]](evidence-register.md#s06) [[S44]](evidence-register.md#s44)

## 2. Audit source before construction

Inspect the class documentation and these implementation points:

- `set_records`: filename filtering, ordering, and files silently skipped. [[S44]](evidence-register.md#s44)
- `process_record`: full-array reads, axis slicing, label alignment, chunk boundaries, overlap, baseline handling, and yielded identity fields. [[S44]](evidence-register.md#s44)
- constructor defaults: `num_channel`, `chunk_size`, `overlap`, transforms, workers, `io_mode`, and `io_path`. [[S44]](evidence-register.md#s44)
- model-selection helpers used later: subject, session, trial, and group boundaries must match the declared generalization unit. [[S20]](evidence-register.md#s20) [[S22]](evidence-register.md#s22)

Copy each relevant assumption into the adaptation record with status `confirmed_by_primary_source`, `confirmed_by_local_artifact`, `conflicting`, or `unresolved`. TorchEEG source is supporting implementation evidence, not a substitute for the publisher protocol. [[S03]](evidence-register.md#s03) [[S44]](evidence-register.md#s44)

## 3. Compare without executing

Compare the adapter's expected paths and keys with established format-tool output and exact companion inventories. Do not instantiate the adapter merely to discover whether the archive matches because construction may load sample arrays and create a cache. [[S23]](evidence-register.md#s23) [[S43]](evidence-register.md#s43) [[S44]](evidence-register.md#s44)

Reject or patch the adapter outside the source archive when any identity, label, channel, axis, unit, product-stage, or split assumption conflicts with the selected release. Record the discrepancy instead of coercing files into the expected schema. [[S03]](evidence-register.md#s03) [[S44]](evidence-register.md#s44)

## 4. Guarded derivative execution

Only after the Preprocessing Contract authorizes sample reads, provide an explicit cache directory outside the source tree and start with no offline or label transform. [[S23]](evidence-register.md#s23) [[S44]](evidence-register.md#s44)

```python
from pathlib import Path

source_root = Path(source_path).resolve()
cache_root = Path(cache_path).resolve()
if cache_root == source_root or source_root in cache_root.parents:
    raise ValueError("TorchEEG io_path must be outside the source archive")

# Substitute only a verified adapter or a reviewed custom dataset.
dataset = AdapterClass(
    root_path=str(source_root),
    io_path=str(cache_root),
    offline_transform=None,
    online_transform=None,
    label_transform=None,
    num_worker=0,
    verbose=True,
)
```

Capture the generated sample metadata before adding transforms. Verify subject/session/trial grouping, source offsets, shapes, labels, and counts against the adaptation record; then create a fresh cache path for every changed offline configuration because TorchEEG caches intermediate results. [[S05]](evidence-register.md#s05) [[S20]](evidence-register.md#s20) [[S44]](evidence-register.md#s44)

## 5. New datasets

For an unsupported release, prefer a reviewed `CSVFolderDataset`, `FolderDataset`, `MNERawDataset`, or custom reader whose metadata table explicitly carries subject, session, trial, label, and source path. Folder position alone is insufficient when grouping or label semantics require more fields. [[S20]](evidence-register.md#s20) [[S22]](evidence-register.md#s22) [[S44]](evidence-register.md#s44)

Keep the established format-inspection tools free of dataset assumptions. Dataset-specific reading, windowing, and label logic belongs in a separately tested adapter plus its cited adaptation record. [[S03]](evidence-register.md#s03) [[S44]](evidence-register.md#s44)

## Exercised compatibility boundaries

The project validation environment pins Python 3.12 and modern SciPy for MNE/EEGDash. TorchEEG 1.1.3 declares SciPy at most 1.10.1, so keep it out of that environment and exercise it with an isolated Python 3.11 runtime. [[S27]](evidence-register.md#s27) [[S31]](evidence-register.md#s31) [[S44]](evidence-register.md#s44)

```bash
uv run --isolated --no-project --python 3.11 \
  --with torcheeg==1.1.3 --with 'pandas<3' python -c \
  "from torcheeg.datasets import SEEDDataset, BCICIV2aDataset; print(SEEDDataset, BCICIV2aDataset)"
```

The unconstrained 2026-08-08 exercise selected pandas 3 and failed while importing TorchEEG through its WFDB dependency; adding `pandas<3` yielded TorchEEG 1.1.3 with SciPy 1.10.1 and pandas 2.3.3. Record these as observed compatibility facts, not permanent upstream guarantees. [[S44]](evidence-register.md#s44)

Source inspection in that environment showed that `SEEDDataset.process_record` calls `loadmat` and dataset construction creates windowed/cache outputs; the `BCICIV2aDataset` adapter expects a `BCICIV_2a_mat` representation with 22 selected channels rather than the locally archived GDF bundle. Therefore neither class is a metadata-only reader for the tested archives. [[S38]](evidence-register.md#s38) [[S39]](evidence-register.md#s39) [[S44]](evidence-register.md#s44)

MOABB 1.5.0 was exercised separately under Python 3.12 without downloading data. Its `BNCI2014_001` adapter declared nine subjects, four motor-imagery events, and a 2–6 second interval; verify its download source and event/window mapping against the official BCI Competition release before using it with a separately obtained archive. [[S38]](evidence-register.md#s38) [[S45]](evidence-register.md#s45)
