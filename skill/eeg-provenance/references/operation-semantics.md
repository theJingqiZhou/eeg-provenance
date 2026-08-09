# EEG operation semantics

Choose a primitive by semantic effect, not framework name. Read one card for the
next operation, then the selected tool recipe. Parameters remain endpoint- and
dataset-specific.

## Contents

- [Read or normalize a recording](#read-or-normalize-a-recording)
- [Apply a deterministic temporal transform](#apply-a-deterministic-temporal-transform)
- [Materialize epochs or windows](#materialize-epochs-or-windows)
- [Construct tasks and labels](#construct-tasks-and-labels)
- [Fit adaptive preprocessing](#fit-adaptive-preprocessing)
- [Build a model-ready cache or handoff](#build-a-model-ready-cache-or-handoff)

## Read or normalize a recording

| Field | Semantic contract |
|---|---|
| Intent | Obtain the least normalized representation that preserves the metadata needed by the endpoint. |
| MNE/MNE-BIDS | A lazy `Raw` view normalizes supported formats and, for MNE-BIDS, applies supported sidecars. It is not a lossless native-header view. |
| Braindecode | `RawDataset` adds dataset description/target plumbing around an MNE object; it does not improve source-format or BIDS conformance evidence. |
| PyHealth | `BaseDataset` is a provider/adapter-defined patient-record tree, not an MNE Raw replacement or read-only EEG header view. Construction may prepare metadata or caches. |
| EEGLAB | Importers create an `EEG` structure whose event/channel fields reflect the active importer and plugin. Use info-only loading only when the exact route is verified not to materialize samples. |
| Side effects | Keep source opening, normalization, metadata application, cache creation, and sample loading as distinct ledger observations. |
| Prefer / avoid | Prefer native-header tools for container fidelity, MNE for a Python processing view, and EEGLAB for a verified MATLAB/plugin representation. Avoid training frameworks for bounded intake. |
| Ledger | Record source object, reader/importer, preload/materialization state, warnings, normalized fields, omitted native fields, and cache/write paths. |
| Evidence | S24–S27, S42, S46, S52, S53, S56 |

## Apply a deterministic temporal transform

| Field | Semantic contract |
|---|---|
| Intent | Apply a fully parameterized filter, notch, crop, unit conversion, or resample without learning cohort state. |
| Direct MNE | Methods such as `Raw.resample()` mutate the object and require loaded data. Resampling includes anti-alias processing; jointly transform events or justify epoch-first timing. |
| Braindecode | `preprocess()` applies each `Preprocessor` to the wrapped MNE object and mutates or replaces the supplied `BaseConcatDataset`. With `save_dir`, it writes and reloads derivatives. The wrapper adds dataset orchestration and provenance fields, not a different resampling estimand. |
| EEGLAB | Fully parameterized `pop_` calls return a changed `EEG` representation; source files remain unchanged only until an explicit save/export path is invoked. |
| PyHealth | A task may embed filtering, resampling, montage, or STFT while also creating labels and caches. Do not select that bundled route for a standalone transform unless all coupled semantics are wanted. |
| Fit state | `none` only when parameters are fixed independently of the analyzed samples. Data-chosen cutoffs, thresholds, or branches are adaptive even if the underlying function is deterministic. |
| Prefer / avoid | Prefer direct MNE/EEGLAB for one transparent operation. Prefer Braindecode when the transformed MNE datasets must continue into its window/model interface. |
| Known surprise | Braindecode 1.7.0 parallel processing can replace subdatasets with worker copies; serial processing is in-place. A save directory changes both write behavior and the object subsequently held by the concat dataset. |
| Ledger | Record object identity/copy policy, exact function and arguments, preload, event handling, shape/rate before and after, and every written derivative. |
| Evidence | S09, S24, S27, S52, S53, S56 |

## Materialize epochs or windows

| Field | Semantic contract |
|---|---|
| Intent | Convert continuous or trial-delimited data into explicit analysis examples with auditable bounds and targets. |
| MNE Epochs | Construct an event-defined `Epochs` object from Raw, events, `event_id`, time bounds, baseline, picks, and rejection policy. With lazy data, some rejection occurs only when data are accessed; Raw is not replaced. |
| Braindecode event windows | `create_windows_from_events()` returns a new concat of window datasets and stores target plus window start/stop metadata. Mapping, offsets, size, stride, overlap policy, bad-window policy, and overlapping-event behavior are part of the label/example definition. |
| Braindecode fixed windows | `create_fixed_length_windows()` uses recording bounds and description targets. With a remainder, `drop_last_window=False` adds a full end-aligned overlapping window; it does not emit a short final window. `drop_last_window=True` omits that end-aligned window. |
| EEGLAB | `pop_epoch`/related functions create an epoched `EEG`; event selection, latency bounds, baseline handling, rejected epochs, and retained event fields remain explicit operations. |
| PyHealth | Task execution creates model samples, not merely signal epochs; it can combine signal loading, windowing, representation, and labels before processors run. |
| Fit state | Window bounds and fixed event maps are stateless; data-derived rejection, normalization, or window selection is adaptive and belongs inside the training partition. |
| Prefer / avoid | Prefer MNE Epochs for conventional event-locked analysis, Braindecode windows for its dataset/model interface, and PyHealth only when its whole task/sample contract is intended. |
| Ledger | Record boundary source, event map, offsets, inclusive/exclusive sample convention, stride, final-window rule, target source, rejected windows, and parent recording IDs. |
| Evidence | S20, S21, S24, S29, S52, S53 |

## Construct tasks and labels

| Field | Semantic contract |
|---|---|
| Intent | Turn publisher events/records into an endpoint-specific target without confusing software encoding with experimental meaning. |
| MNE/EEGLAB | Event IDs or event types select observations; the scientific label policy still comes from the protocol and declared endpoint. |
| Braindecode | Event-window `mapping` converts annotation descriptions to targets. Fixed windows obtain description targets only when the wrapped dataset declares the target field; otherwise the exercised 1.7.0 route yielded `-1`. |
| PyHealth | A `BaseTask` defines `input_schema`, `output_schema`, and patient-to-sample extraction. `set_task()` applies it across the supplied `BaseDataset` before processor fitting and cache creation. |
| Hidden assumptions | Label timing, response contamination, subject/session grouping, missing events, class mapping, and publisher split semantics are not repaired by a framework. |
| Fit state | A fixed code map is stateless. Vocabulary, encoder, normalization, or selection learned from examples is fitted state and must respect the split. |
| Prefer / avoid | Prefer the lightest explicit mapping that represents the endpoint. Avoid PyHealth `set_task()` when only an annotation dictionary or MNE Epochs object is needed. |
| Ledger | Record protocol evidence, task/event mapping, excluded events, group identities, target source, processor state, and cache identity. |
| Evidence | S01, S20–S22, S29, S52, S53 |

## Fit adaptive preprocessing

| Field | Semantic contract |
|---|---|
| Intent | Learn nuisance, normalization, rejection, decomposition, or feature state from data. |
| MNE/EEGLAB | ICA and any data-driven bad-channel, rejection, or artifact model have fitted state even when their later `apply` step is deterministic. |
| Braindecode | `Preprocessor` can wrap fixed or adaptive code; the wrapper does not establish a safe fit scope. Separate fit from application when state is learned. |
| PyHealth | `set_task()` calls processor fitting on the task dataset unless pre-fitted processors are supplied. Building it on pooled train/validation/test therefore leaks any data-dependent processor state. |
| Fit state | Use `training_only` or `within_train_fold` for predictive work; tune adaptive parameters only inside the same nesting. Preserve fitted state and reuse it without refitting on validation/test. |
| Prefer / avoid | Prefer APIs that expose fit/apply state and accept a pre-fitted object. Reject a bundled task/cache route when its fit population cannot match the generalization contract. |
| Known surprise | A transform called “preprocessing” is not necessarily adaptive, and a processor called during cache construction is not necessarily stateless; inspect the implementation rather than infer from naming. |
| Ledger | Record training entity IDs, grouping/split, fitted object identity/hash, seed, hyperparameter selection scope, application entities, and ablation/QC. |
| Evidence | S12–S18, S20–S22, S52, S53 |

## Build a model-ready cache or handoff

| Field | Semantic contract |
|---|---|
| Intent | Persist a representation whose axes, units, labels, grouping, fitted state, and source lineage are sufficient for downstream training. |
| MNE/EEGLAB | FIF/SET or other derivatives preserve their framework representation but do not by themselves encode the full preprocessing contract or evaluation split. |
| Braindecode | `preprocess(..., save_dir=...)` writes per-dataset derivatives and reloads them lazily; window datasets add example metadata. Record the source-to-dataset index and preprocessing/window kwargs. |
| PyHealth | `set_task()` keys task and processor cache directories from serialized task/processor configuration, fits processors, stores schema/state, and returns `SampleDataset`. Split membership is separate provenance and must not be inferred from cache reuse. |
| TorchEEG | Its `io_path` cache is a derived representation whose adapter assumptions, axes, transforms, labels, and partition contract require explicit acceptance. |
| Side effects | Preflight destination, free space, overwrite/reuse behavior, partial-build recovery, permissions, and durable lifetime. Never target a protected archive. |
| Prefer / avoid | Build a framework cache only when the downstream consumer benefits from that representation. Keep a simpler MNE/EEGLAB derivative when coupling adds no required capability. |
| Ledger | Record cache schema/version, source and split identities, tensor shape/order/unit, transform and processor hashes, shard/index inventory, completion marker, and reusable fitted state. |
| Evidence | S05, S23, S44, S50, S52, S53 |
