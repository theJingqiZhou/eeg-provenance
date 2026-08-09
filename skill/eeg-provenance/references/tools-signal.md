# MNE signal representation and processing

Use this reference after the active pipeline stage selects MNE-Python. It maps
normalized signal, temporal, spatial, epoch, adaptive, and derivative semantics
to MNE APIs without turning the ecosystem into a fixed pipeline. Select the
[EEGLAB ecosystem reference](tools-eeglab.md) instead when a MATLAB-native
`EEG`/`STUDY` representation or verified plugin is required.
[[S03]](evidence-register.md#s03) [[S27]](evidence-register.md#s27)

## Contents

- [When MNE is the matching representation](#when-mne-is-the-matching-representation)
- [MNE read and normalization calls](#mne-read-and-normalization-calls)
- [MNE operation calls](#mne-operation-calls)
- [MNE adaptive and derivative calls](#mne-adaptive-and-derivative-calls)
- [MNE execution and provenance checks](#mne-execution-and-provenance-checks)

## When MNE is the matching representation

| Condition | MNE route | Boundary |
|---|---|---|
| Supported native/BIDS file needs a lazy Python processing view | `Raw` or MNE-BIDS with `preload=False` | A normalized view is not a byte-faithful native header. |
| Operation must integrate with Braindecode or Python QC | Keep an MNE object as the direct interchange | Audit framework mutation, materialization, and cache behavior separately. |
| A documented MNE implementation meets the operation semantics | Use a copy when input preservation is required | Defaults and successful execution do not justify the scientific choice. |
| A required algorithm or representation is EEGLAB-only | Do not force an approximate round trip | Select the EEGLAB implementation reference and verify its extension contract. |
| Evidence | S26–S27 | S03, S23, S52 |

Select by semantic preservation, side effects, fitted-state exposure, runtime,
and downstream representation. Reader success does not validate acquisition
history or processing suitability. [[S03]](evidence-register.md#s03)
[[S23]](evidence-register.md#s23) [[S26]](evidence-register.md#s26)
[[S27]](evidence-register.md#s27) [[S52]](evidence-register.md#s52)

## MNE read and normalization calls

These are API routes, not parameter defaults. Record installed versions,
warnings, source files, preload state, normalized/omitted fields, annotations,
channel order/types/units/reference, and montage source. [[S26]](evidence-register.md#s26)
[[S27]](evidence-register.md#s27)

| Input | Call contract | Important boundary |
|---|---|---|
| BIDS recording | `mne_bids.read_raw_bids(path, extra_params={"preload": False}, on_ch_mismatch="raise")` | Applies supported sidecars to `Raw`; compare with source TSV/JSON and preserve warnings. [[S26]](evidence-register.md#s26) |
| EDF/EDF+ | `mne.io.read_raw_edf(path, preload=False, infer_types=False)` | Normalized view; use PyEDFlib when exact per-signal header fidelity is the operation. [[S27]](evidence-register.md#s27) [[S42]](evidence-register.md#s42) [[S46]](evidence-register.md#s46) |
| GDF | `mne.io.read_raw_gdf(path, preload=False)` | Preserve discontinuity/event warnings and reconcile roles with the format/release contract. [[S27]](evidence-register.md#s27) [[S43]](evidence-register.md#s43) |
| EEGLAB SET | `mne.io.read_raw_eeglab(path, preload=False)` | Valid only for the EEGLAB SET contract and may depend on companion FDT data. [[S27]](evidence-register.md#s27) |
| Annotations | `mne.events_from_annotations(raw, event_id=..., use_rounding=True)` | Save original annotations, event map, sample array, and rounding; mapping does not establish experimental meaning. [[S29]](evidence-register.md#s29) |

Do not call `load_data()`, a transform, or a plot that materializes samples for
a metadata-only question. A lazy Raw view is not a lossless native-header view.
[[S23]](evidence-register.md#s23) [[S27]](evidence-register.md#s27)

For MAT files, follow the native version/directory route in the data-access
reference. `mne.io.read_raw_eeglab()` is not a generic MAT reader, `h5io` is not
a generic MATLAB semantic parser, and the `mne[hdf5]` extra does not infer axes
or dataset meaning. [[S43]](evidence-register.md#s43)
[[S49]](evidence-register.md#s49)

## MNE operation calls

Use copies when the contract requires input preservation: Raw methods commonly
mutate the receiving object and sample transforms require loaded data. Capture
object identity/copy policy and actual logged designs. [[S27]](evidence-register.md#s27)

| Operation | API shape | Record and verify |
|---|---|---|
| Filter/notch | `raw.copy().load_data().filter(...)` / `.notch_filter(...)` | Complete family, cutoffs/stopbands, transitions, order/length, phase, padding, boundaries, effective response, and shape. [[S09]](evidence-register.md#s09) [[S10]](evidence-register.md#s10) [[S27]](evidence-register.md#s27) |
| Resample | `raw.copy().resample(new_sfreq, events=events, method=...)` | Anti-alias route, old/new rate, old/new event samples, maximum timing change, and epoch-first alternative. [[S27]](evidence-register.md#s27) |
| Reference | `mne.set_eeg_reference(copy, ref_channels=..., projection=...)` | Included/excluded channels, bads, acquisition versus offline reference, application/projection mode, returned reference data, and rank. [[S08]](evidence-register.md#s08) [[S28]](evidence-register.md#s28) |
| Interpolate | mark `info["bads"]`, then `interpolate_bads(reset_bads=False, method={"eeg": ...})` | Geometry/frame, donor support, origin/method, bad-state transition, reset policy, and rank before/after. [[S07]](evidence-register.md#s07) [[S28]](evidence-register.md#s28) |
| Epoch | `mne.Epochs(raw, events, event_id, tmin, tmax, baseline=..., preload=...)` | Boundary source, sample convention, event map, baseline, picks, rejection, parent IDs, and deferred data/rejection behavior. [[S27]](evidence-register.md#s27) |

Compute rank with the same estimator/tolerance before and after reference,
channel removal, interpolation, or projection application. Software-reported
rank can differ from effective rank while projections remain unapplied.
[[S08]](evidence-register.md#s08) [[S28]](evidence-register.md#s28)

## MNE adaptive and derivative calls

Fit ICA on a declared training representation and apply the fitted object only
to compatible channel order/reference/linear preprocessing. Record training
entities, filters, rank, algorithm, component count, convergence, seed,
selection evidence, exclusions, and target. A 1 Hz high-pass training copy is a
conditional practical example, not a universal cutoff. [[S12]](evidence-register.md#s12)
[[S14]](evidence-register.md#s14)

```python
from mne.preprocessing import ICA

training = train_raw.copy().load_data().filter(l_freq=contract_l_freq,
                                                h_freq=None)
ica = ICA(n_components=contract_components, method=contract_method,
          random_state=contract_seed, max_iter="auto")
ica.fit(training, picks="eeg")
ica.exclude = reviewed_components
cleaned = ica.apply(target_raw.copy())
```

For MNE-ICALabel, verify its documented decomposition, average-reference, and
band assumptions before interpreting probabilities; keep them advisory and
record the human/rule decision. AutoReject and other learned rejection or repair
thresholds are fitted state and must be trained inside the evaluation partition.
[[S13]](evidence-register.md#s13) [[S15]](evidence-register.md#s15)
[[S17]](evidence-register.md#s17) [[S20]](evidence-register.md#s20)

Before writing, resolve source and derivative roots and reject equality or a
derivative nested under the protected source. Claim BIDS Derivatives only with
the required dataset description, collision-safe filename/entities, still-valid
metadata, and immediate inputs in `Sources`; otherwise label a project
derivative. [[S23]](evidence-register.md#s23)

## MNE execution and provenance checks

Before claiming execution, capture exact runtime and entry points, run a harmless
smoke test, and verify the selected operation on disposable or bounded data.
Afterward compare source inventory, output inventory, object shape/rate/events,
channel states/rank, fitted-state scope, and expected numerical consequences.
Record APIs and accepted arguments rather than describing only a GUI action.
[[S03]](evidence-register.md#s03) [[S05]](evidence-register.md#s05)
[[S27]](evidence-register.md#s27) [[S30]](evidence-register.md#s30)
