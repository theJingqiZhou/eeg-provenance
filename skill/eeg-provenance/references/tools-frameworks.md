# Dataset and training-framework integrations

Use this reference only when an adapter, window/task abstraction, or model-ready
cache is part of the requested endpoint. MOABB, Braindecode, PyHealth, and
TorchEEG add different coupled semantics; none is a metadata-only default or a
substitute for the publisher contract. [[S44]](evidence-register.md#s44)
[[S45]](evidence-register.md#s45) [[S52]](evidence-register.md#s52)
[[S53]](evidence-register.md#s53)

## Contents

- [Choose the smallest coupling](#choose-the-smallest-coupling)
- [Shared adapter preflight](#shared-adapter-preflight)
- [MOABB](#moabb)
- [Braindecode](#braindecode)
- [PyHealth](#pyhealth)
- [TorchEEG](#torcheeg)
- [Fit and cache safeguards](#fit-and-cache-safeguards)

## Choose the smallest coupling

| Needed capability | Candidate | Added semantics and side effects |
|---|---|---|
| Maintained BCI dataset/paradigm/evaluation adapter | MOABB | Provider/release assumptions, retrieval/cache, MNE Raw hierarchy, event/paradigm conventions |
| MNE-backed dataset orchestration, preprocessing, windows, augmentation, decoder integration | Braindecode | Dataset descriptions/targets, object mutation or replacement, optional derivative writes, example metadata |
| Patient/record tree, typed task, processors, LitData sample cache | PyHealth | Adapter metadata preparation, task materialization, processor fitting, schema/state cache, sample serialization |
| Versioned non-BIDS adapter or offline/online transform cache | TorchEEG | Path/key/channel/window/label assumptions and `io_path` cache construction |
| Evidence | S45, S52–S53 | S44–S45, S52–S53 |

Prefer direct MNE/EEGLAB operations when this coupling adds no capability needed
by the downstream consumer. Framework adapters and defaults are executable
assumptions, not primary evidence for dataset identity or a universal processing
choice. [[S03]](evidence-register.md#s03) [[S44]](evidence-register.md#s44)
[[S45]](evidence-register.md#s45) [[S52]](evidence-register.md#s52)
[[S53]](evidence-register.md#s53)

## Shared adapter preflight

Before construction, bind the installed version to matching source and inspect:

- provider, dataset release, download URL/method, selectors, and cache root;
- record discovery and silent filtering/order behavior;
- full-array reads, normalization, windowing, transforms, label maps, and axis/
  channel/unit assumptions;
- subject/session/run/trial identity, publisher partitions, and split helpers;
- constructor-time network, metadata/index writes, sample/cache writes, reuse,
  overwrite, worker behavior, and partial-build recovery;
- fit/apply boundaries for processors, normalizers, artifact rules, vocabulary,
  and any data-dependent transform. [[S20]](evidence-register.md#s20)
  [[S23]](evidence-register.md#s23) [[S44]](evidence-register.md#s44)
  [[S52]](evidence-register.md#s52) [[S53]](evidence-register.md#s53)

Compare each assumption with official release documentation and bounded local
artifacts. Mark it confirmed, conflicting, or unresolved; reject or patch the
adapter in derivative code rather than coercing the protected source to match.
[[S03]](evidence-register.md#s03) [[S05]](evidence-register.md#s05)
[[S20]](evidence-register.md#s20) [[S23]](evidence-register.md#s23)
[[S44]](evidence-register.md#s44) [[S52]](evidence-register.md#s52)
[[S53]](evidence-register.md#s53)

Apply the [runtime compatibility matrix](runtime-compatibility.md) before
resolving a framework. Keep a sufficient provisioned environment unchanged;
isolate incompatible generations using the site's approved manager. Package
metadata is a candidate boundary, not an import or operation-level proof.
[[S58]](evidence-register.md#s58) [[S59]](evidence-register.md#s59)
[[S60]](evidence-register.md#s60) [[S61]](evidence-register.md#s61)

## MOABB

Use MOABB when its versioned dataset adapter and the desired BCI endpoint match
the selected release. Treat the dataset object, paradigm, and evaluation as
separate choices: an adapter can return MNE Raw recordings without validating a
paradigm's event map, interval, preprocessing, subject/session split, or local
archive equivalence. [[S38]](evidence-register.md#s38)
[[S45]](evidence-register.md#s45)

Before a download, inspect the class's provider URL, subject list, event map,
interval, cache/update flags, and recording hierarchy. For a separately acquired
archive, compare hashes/paths and protocol details rather than assuming the
MOABB class consumes that representation. MOABB 1.5.0's exercised
`BNCI2014_001` metadata declared nine subjects, four motor-imagery events, and a
2–6 s interval; those values still require comparison with the official release
for the intended reproduction. [[S38]](evidence-register.md#s38)
[[S45]](evidence-register.md#s45)

Keep MOABB generations isolated when required: 1.1.1 constrained NumPy/pandas
below 2 and MNE-BIDS below 0.15, whereas 1.5 required NumPy 2 and newer
MNE/MNE-BIDS in the checked metadata. [[S59]](evidence-register.md#s59)

## Braindecode

`RawDataset` adds description and target plumbing around MNE; it does not add
native-header fidelity or BIDS conformance. `preprocess()` applies each
`Preprocessor` to the wrapped MNE datasets. In exercised 1.7.0 behavior, serial
processing changed wrapped objects in place, parallel processing could replace
subdatasets with worker results, and `save_dir` wrote then reloaded derivatives.
Record worker/copy policy, input-to-dataset index, exact preprocessors, and every
write/reload. [[S52]](evidence-register.md#s52)

Use event windows only after declaring annotation-to-target `mapping`, offsets,
size, stride, overlap, bad-window policy, and parent IDs. Event windows carry
target/start/stop metadata. For fixed windows, `drop_last_window=False` added a
full end-aligned overlapping window when a remainder existed; it did not create
a short padded window. With `drop_last_window=True`, that extra window was
omitted. [[S20]](evidence-register.md#s20) [[S52]](evidence-register.md#s52)

Fixed-window targets come from the wrapped dataset's declared `target_name`; the
exercised 1.7.0 route produced `-1` when none was declared. Validate target
source, example count, start/stop bounds, overlap, and split grouping before
training. A `Preprocessor` wrapper does not make adaptive code stateless: split
fit from apply when state is learned. [[S20]](evidence-register.md#s20)
[[S21]](evidence-register.md#s21) [[S52]](evidence-register.md#s52)

Stable web documentation and installed code can differ. Bind calls to the
installed/tagged release and smoke-test exact signatures; in the exercised
1.7.0 wheel, an `EEGNet` warning suggested a keyword the constructor rejected.
[[S52]](evidence-register.md#s52)

## PyHealth

In PyHealth 2.0.1, `BaseDataset` represents a provider/adapter-defined
patient-record tree; it is not MNE Raw or a read-only header view. Dataset
construction can prepare metadata and attempt writes beneath the supplied root
before falling back to a user cache. Audit the adapter and destination before
construction. [[S23]](evidence-register.md#s23)
[[S53]](evidence-register.md#s53)

A `BaseTask` declares input/output schemas and patient-to-sample extraction.
`set_task()` materializes the task dataset, keys cache paths from serialized
task/schema/processor configuration, fits `SampleBuilder` processors on the
supplied dataset unless pre-fitted processors are passed, stores schema/state,
writes LitData samples, and returns a cache-backed `SampleDataset`; split
identity is separate from that call. Constructing it on pooled train,
validation, and test entities leaks any data-dependent processor state.
[[S20]](evidence-register.md#s20) [[S21]](evidence-register.md#s21)
[[S53]](evidence-register.md#s53)

Version-pinned TUAB/TUEV tasks bundle EDF loading, temporal transforms, bipolar
derivations, window/label construction, optional normalization, and optional
STFT. Select such a task only when every coupled operation matches the endpoint,
channel equations, fit scope, and release contract; otherwise implement lighter
explicit operations. Generic PyHealth models are not automatically validated
EEG decoders. [[S40]](evidence-register.md#s40)
[[S41]](evidence-register.md#s41) [[S53]](evidence-register.md#s53)

PyHealth 2.0.1 admitted only Python 3.12–3.13 and tightly constrained the checked
MNE/NumPy/pandas/Torch stack, so keep it in a separately verified lane when the
main environment differs. [[S59]](evidence-register.md#s59)

## TorchEEG

Treat a TorchEEG adapter as a versioned implementation lead. Before
instantiation inspect `set_records`, `process_record`, constructor defaults,
path/key filtering, array reads and axes, labels, chunk size/overlap, channels,
transforms, workers, `io_mode`, `io_path`, and split helpers. Its source can
suggest hypotheses but cannot replace the publisher protocol. [[S03]](evidence-register.md#s03)
[[S44]](evidence-register.md#s44)

Construction can load complete arrays, segment examples, transform labels, and
write an IO cache. After the adaptation record authorizes execution, use a cache
outside the source, start with no transforms and one worker, verify generated
IDs/shapes/labels/counts against the release, and use a fresh cache identity for
each changed offline configuration. [[S05]](evidence-register.md#s05)
[[S23]](evidence-register.md#s23) [[S44]](evidence-register.md#s44)

```python
dataset = VerifiedAdapter(
    root_path=str(protected_source),
    io_path=str(authorized_cache),
    offline_transform=None,
    online_transform=None,
    label_transform=None,
    num_worker=0,
)
```

For unsupported data, prefer a reviewed folder/CSV/MNE/custom adapter whose
metadata explicitly carries source path, subject, session, trial, label, and
partition. Keep dataset-specific parsing/semantics in that tested adapter, not
in a generic inspection script. [[S20]](evidence-register.md#s20)
[[S22]](evidence-register.md#s22) [[S44]](evidence-register.md#s44)

The exercised TorchEEG 1.1.3 lane used Python 3.11, SciPy 1.10.1, and pandas
below 3; unconstrained pandas 3 failed through a dependency. Source inspection
also showed that the SEED adapter loaded MAT arrays and built window/cache
outputs, while its BCI IV 2a adapter expected a MAT representation rather than
the archived GDF bundle. These are version-specific compatibility and adapter
facts, not dataset defaults. [[S38]](evidence-register.md#s38)
[[S39]](evidence-register.md#s39) [[S44]](evidence-register.md#s44)
[[S59]](evidence-register.md#s59)

## Fit and cache safeguards

For every framework output, record source/release and split entity IDs, adapter
version/source commit, constructor and operation arguments, fitted processor or
transform state, axes/channel order/units, example bounds/targets/groups,
cache schema/version, shard/index inventory, completion marker, destination,
reuse/overwrite policy, and parent entities. Never infer split membership or
safe fitted state from cache reuse. [[S05]](evidence-register.md#s05)
[[S20]](evidence-register.md#s20) [[S23]](evidence-register.md#s23)
[[S44]](evidence-register.md#s44) [[S52]](evidence-register.md#s52)
[[S53]](evidence-register.md#s53)
