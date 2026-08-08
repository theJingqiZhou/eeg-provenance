# Braindecode and PyHealth dataset-to-model routes

Use these frameworks only after the source identity and release contract are established. Their dataset classes, preprocessing tasks, window builders, processors, and caches are executable transformations; a supported dataset name or model class is not evidence that its defaults match the intended endpoint. [[S03]](evidence-register.md#s03) [[S20]](evidence-register.md#s20) [[S52]](evidence-register.md#s52) [[S53]](evidence-register.md#s53)

## Choose the route

| Need | Preferred route | Boundary |
|---|---|---|
| MNE-native EEG/ECoG/MEG, MOABB, local BIDS, event/fixed windows, EEG-specific augmentations, or an EEG architecture interface | Braindecode | Keep acquisition, preprocessing, windowing, augmentation, and evaluation as separate ledger activities. [[S52]](evidence-register.md#s52) |
| PyHealth-supported sleep, TUAB/TUEV, or other healthcare signal task represented through `BaseDataset` → task → `SampleDataset` | PyHealth | Audit dataset/task source and cache writes before construction; do not interpret a generic healthcare model as an EEG-validated decoder. [[S53]](evidence-register.md#s53) |
| Read-only header or metadata intake | MNE, PyEDFlib, PyBIDS, MNE-BIDS, or the provider tool | Do not instantiate a training framework merely to inspect a protected or very large archive. [[S23]](evidence-register.md#s23) [[S42]](evidence-register.md#s42) [[S43]](evidence-register.md#s43) |

## Braindecode

The repository pins Braindecode 1.7.0 in a dedicated group. The official stable documentation was still labeled 1.5.1 during the 2026-08-08 review, so record the runtime version and test imports instead of copying names from a different documentation release. In the exercised 1.7.0 wheel, `RawDataset` and `EEGNet` replace examples that import the no-longer-exported `BaseDataset` or `EEGNetv4`; its `EEGNet` deprecation message also recommends `final_layer_linear`, although that constructor rejects the argument. Treat warnings and signatures as testable versioned behavior, not instructions to apply blindly. [[S52]](evidence-register.md#s52)

```bash
uv sync --group validation --group braindecode --locked
uv run --group validation --group braindecode \
  pytest tests/integration/test_braindecode_package.py -q
```

Before data retrieval, inspect the named `MOABBDataset`, `BIDSDataset`, or other adapter's versioned source, upstream data provider, release identifier, selectors, cache location, and access terms. A Braindecode wrapper can delegate acquisition to MOABB or read a local BIDS tree, but it does not replace primary dataset documentation. [[S06]](evidence-register.md#s06) [[S45]](evidence-register.md#s45) [[S52]](evidence-register.md#s52)

Write the ordered `Preprocessor` calls, MNE functions and parameters, copy/in-place behavior, save directory, event mapping, offsets, window size/stride, rejection rules, and output metadata into the preprocessing contract before calling `preprocess`, `create_windows_from_events`, or `create_fixed_length_windows`. Treat windowing and augmentation as interventions, and fit any data-adaptive transform only inside the training partition. [[S03]](evidence-register.md#s03) [[S20]](evidence-register.md#s20) [[S52]](evidence-register.md#s52)

Use a model construction and one synthetic forward pass to verify tensor shape and software compatibility. Selecting an architecture, pretrained checkpoint, loss, sampler, or evaluation protocol is a separate evidence task; presence in the model zoo is not a scientific endorsement for the dataset or endpoint. [[S19]](evidence-register.md#s19) [[S20]](evidence-register.md#s20) [[S52]](evidence-register.md#s52)

## PyHealth

Keep PyHealth 2.0.1 in an isolated uv environment because it pins a large healthcare/deep-learning stack, including older MNE, NumPy, and PyTorch minor lines than this repository's core validation environment. Exercise the exact wheel without installing it into the main environment: [[S53]](evidence-register.md#s53)

```bash
uv run --no-project --python 3.12 \
  --with pyhealth==2.0.1 --with pytest==8.4.2 \
  python -m pytest tests/integration/test_pyhealth_package.py -q
```

Inspect the dataset class, task class, and processors before construction. Record source-root reads, metadata generation, filter/notch/resample values, unit conversion, montage derivation, windowing, label construction, STFT generation, normalization, cache directory, and software versions. These are implementation assumptions to accept, override, or reject in the preprocessing contract—not defaults supplied by the dataset itself. [[S03]](evidence-register.md#s03) [[S08]](evidence-register.md#s08) [[S09]](evidence-register.md#s09) [[S53]](evidence-register.md#s53)

Do not assume TUH data are locally mounted, and do not point PyHealth 2.0.1's TUAB or TUEV dataset constructor at a protected source archive for inspection. Stage the authorized selection through the provider's current access route when needed. The version-pinned implementation prepares metadata CSVs and may attempt a write under the supplied root before falling back to a user cache. Use established read-only readers first; for approved execution, create a bounded derivative work view or copy-on-write mount, pass an explicit task-cache root, and inventory every additional cache path. [[S23]](evidence-register.md#s23) [[S40]](evidence-register.md#s40) [[S53]](evidence-register.md#s53) [[S54]](evidence-register.md#s54)

`set_task()` turns a `BaseDataset` into a model-ready `SampleDataset`, fits configured processors, and serializes LitData caches. Freeze the generalization split first. If any processor learns data-dependent state, fit it on training data and reuse that fitted processor for validation/test rather than fitting on the pooled cohort. Preserve patient, record, session, site, publisher split, task parameters, processor state, and cache identity. [[S20]](evidence-register.md#s20) [[S21]](evidence-register.md#s21) [[S22]](evidence-register.md#s22) [[S53]](evidence-register.md#s53)

PyHealth's generic `CNN`, `RNN`, and `Transformer` consume the processed `SampleDataset`; reusable layers can also be shape-tested independently. Do not call these classes validated EEG decoders unless the exact architecture, input representation, training procedure, endpoint, and evaluation have suitable evidence. [[S19]](evidence-register.md#s19) [[S20]](evidence-register.md#s20) [[S53]](evidence-register.md#s53)

## Ledger additions

For either framework, record `framework`, `version`, adapter/task class and source revision, acquisition delegate, source selection, preprocessing/window/processor configuration, cache roots and hashes, split membership, fit scope, tensor shape/unit/channel order, model class or checkpoint identity, synthetic compatibility result, and all warnings or documentation/runtime disagreements. [[S03]](evidence-register.md#s03) [[S05]](evidence-register.md#s05) [[S20]](evidence-register.md#s20) [[S52]](evidence-register.md#s52) [[S53]](evidence-register.md#s53)
