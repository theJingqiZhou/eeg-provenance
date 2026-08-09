# EEGLAB ecosystem implementations

Use this reference only after the active pipeline stage requires an EEGLAB
`EEG`/`STUDY` representation or a verified extension. Treat core EEGLAB,
EEG-BIDS, format importers, and processing plugins as separate versioned
capabilities. [[S24]](evidence-register.md#s24)
[[S56]](evidence-register.md#s56) [[S62]](evidence-register.md#s62)
[[S63]](evidence-register.md#s63) [[S64]](evidence-register.md#s64)

## Contents

- [Select EEGLAB for the operation](#select-eeglab-for-the-operation)
- [Distinguish EEG, STUDY, and BIDS](#distinguish-eeg-study-and-bids)
- [Build a STUDY from SET files](#build-a-study-from-set-files)
- [Create a STUDY from EEG-BIDS](#create-a-study-from-eeg-bids)
- [Respect metadata-only format limits](#respect-metadata-only-format-limits)
- [Run core EEGLAB headlessly](#run-core-eeglab-headlessly)
- [Core operation calls](#core-operation-calls)
- [Execution and provenance checks](#execution-and-provenance-checks)

## Select EEGLAB for the operation

| Need | Select EEGLAB when | Do not infer |
|---|---|---|
| Existing SET/STUDY workflow | The release can load the exact representation and downstream work remains in EEGLAB | A STUDY is BIDS or preserves every source sidecar. |
| BIDS-to-EEGLAB conversion | A bounded EEG-BIDS import is required for `EEG`/`STUDY` processing | Import is BIDS validation or a byte-faithful metadata copy. |
| Native-format intake | The required importer extension and exact entry point are verified | Core EEGLAB reads every advertised format or can always avoid sample access. |
| Processing method | A pinned core function or extension matches the operation semantics and license | Plugin publication or installation is scientific validation. |
| Evidence | S24, S56, S62–S65 | S03, S23, S64–S65 |

Prefer a native tree/header tool for a metadata-only question when EEGLAB's
format route would load samples. Prefer MNE when its normalized representation
is the direct downstream interchange and no EEGLAB-only method is required.
Changing ecosystems adds a representation activity that must preserve or
explicitly mark channel, event, unit, reference, geometry, and prior-processing
semantics. [[S03]](evidence-register.md#s03)
[[S23]](evidence-register.md#s23) [[S27]](evidence-register.md#s27)
[[S63]](evidence-register.md#s63)

## Distinguish EEG, STUDY, and BIDS

`EEG` is an EEGLAB dataset structure. `STUDY` is EEGLAB's group/multi-dataset
structure containing dataset descriptions and links plus study-level designs
and results. It can be assembled from SET files with `std_editset`, or generated
as an EEGLAB derivative while EEG-BIDS imports a BIDS dataset. Neither route
makes `STUDY` a BIDS data structure. [[S24]](evidence-register.md#s24)
[[S62]](evidence-register.md#s62) [[S63]](evidence-register.md#s63)

Keep three identities in provenance: the immutable source recording and
sidecars, each imported/saved `EEG` representation, and the `STUDY` that points
to its datasets. Do not use a `.study` file as the only metadata archive or as
evidence of BIDS conformance. [[S05]](evidence-register.md#s05)
[[S23]](evidence-register.md#s23) [[S62]](evidence-register.md#s62)
[[S63]](evidence-register.md#s63)

## Build a STUDY from SET files

Build commands explicitly so dataset identity is not inferred from load order
or filenames. `std_editset` supports dataset index/load plus subject, condition,
session, group, task, and run fields, and synchronizes the `STUDY.datasetinfo`
records with loaded EEGLAB datasets. [[S62]](evidence-register.md#s62)

```matlab
commands = { ...
    {'index', 1, 'load', char(setPath1), 'subject', 'sub-01', ...
     'session', 1, 'run', 1, 'condition', 'target', 'task', 'oddball'}, ...
    {'index', 2, 'load', char(setPath2), 'subject', 'sub-02', ...
     'session', 1, 'run', 1, 'condition', 'target', 'task', 'oddball'} };
[STUDY, ALLEEG] = std_editset([], [], 'commands', commands, ...
    'filename', char(studyPath), 'task', 'oddball');
```

Before saving, assert unique source identities and inspect `datasetinfo`,
`ALLEEG`, dataset paths, subject/session/run/task/condition values, and write
destinations. A STUDY entry describes an EEGLAB dataset; it does not prove the
publisher's subject or event semantics. [[S03]](evidence-register.md#s03)
[[S05]](evidence-register.md#s05) [[S62]](evidence-register.md#s62)

## Create a STUDY from EEG-BIDS

Use `pop_importbids` only when the EEGLAB representation is required. Supply
bounded subject/session/task/run selectors and an `outputdir` outside the BIDS
source. Validate the source with the BIDS Validator independently and compare
the imported channel, event, coordinate, and recording identities with the
resolved sidecars. [[S23]](evidence-register.md#s23)
[[S25]](evidence-register.md#s25) [[S47]](evidence-register.md#s47)
[[S63]](evidence-register.md#s63)

Before import, capture `which('fileread')` and smoke-read a temporary text file
with the same path type the installed EEG-BIDS code will pass. The exercised
10.5/R2026a Update 4 clean-path combination rejected a character-vector JSON
path. Treat that as a compatibility stop: select a compatible release or an
upstream fix, and do not insert a shadowing file-I/O shim.
[[S30]](evidence-register.md#s30) [[S63]](evidence-register.md#s63)

EEG-BIDS 10.5 does not byte-copy only the required BIDS metadata into the
STUDY. Its pinned source translates source information into the EEGLAB
representation. [[S63]](evidence-register.md#s63)

- `EEG.subject`, `session`, `run`, `task`, optional `recording`, and
  `EEG.etc.datatype` receive selected identity fields.
- `EEG.BIDS` contains `gInfo`, `pInfo`, `pInfoDesc`, `eInfo`, `eInfoDesc`,
  `tInfo`, `bidsstats`, `scannedElectrodes`, and `behavioral`.
- `std_editset` commands add subject/session/task/run, participant columns, and
  the first imported behavioral record to `STUDY.datasetinfo`; the STUDY also
  receives import statistics and optional HED-derived tags.

Evidence: S63.

This is a lossy/normalized mapping contract, not a sidecar preservation
contract. Preserve the original BIDS tree, resolved inherited metadata, source
checksums, importer selectors/version, warnings, and the imported EEGLAB files
as distinct entities. In the bounded exercise, full import wrote SET/FDT/STUDY
products rather than byte-for-byte JSON/TSV copies. [[S05]](evidence-register.md#s05)
[[S23]](evidence-register.md#s23) [[S63]](evidence-register.md#s63)

## Respect metadata-only format limits

The EEG-BIDS 10.5 `metadata='on'` option suppresses output saving/STUDY
creation; it is not a universal source-metadata-only reader. The selected
recording importer still runs, and only some branches expose a reduced-payload
route. [[S63]](evidence-register.md#s63)

| Format branch | Pinned metadata behavior | Required edge check |
|---|---|---|
| EEGLAB SET | `pop_loadset(..., 'loadmode', 'info')` | Modern SET may return a data sentinel/path; legacy layout or unresolved relative FDT can fall back to loading. Test `EEG.data` and I/O from the actual working directory. |
| BrainVision EEG/VHDR | `pop_loadbv(..., true)` | Requires the bva-io extension; confirm installed signature, text types, and companion resolution. |
| EDF/BDF | `pop_biosig(...)` | The EEG-BIDS source explicitly says this route cannot read metadata only because events are in a channel; expect sample access. |
| FIF/GZ/DS/MEFD | Same full importer used in normal mode | No metadata-only branch in the pinned importer; extension availability is separate. |
| Other plugin formats | Installed wrapper/source decides | Do not generalize SET or BrainVision behavior. |
| Evidence | S63 | S24, S64 |

For SET, do not run `eeg_checkset` merely to prove metadata-only access until
the active release is tested: consistency checks or companion resolution can
materialize samples. Measure file reads where important and report
`metadata_only: false` whenever the route accessed signal payload.
[[S24]](evidence-register.md#s24) [[S63]](evidence-register.md#s63)

Format plugins can expose lower-level native headers that the EEG-BIDS import
path does not use. For example, BIOSIG `sopen` returns a plugin-native header,
not an EEGLAB `EEG` metadata view; select and verify it as a separate operation.
Use the [extension reference](tools-eeglab-extensions.md) to resolve installation
assets and entry points. [[S46]](evidence-register.md#s46)
[[S63]](evidence-register.md#s63) [[S64]](evidence-register.md#s64)

## Run core EEGLAB headlessly

```matlab
addpath(char(eeglabRoot))
[ALLEEG, EEG, CURRENTSET, ALLCOM] = eeglab('nogui'); %#ok<ASGLU>
assert(~isempty(which('eeg_getversion')))
assert(~isempty(which('eeg_checkset')))
```

Supply every selector, option, and output path required by a `pop_` wrapper. If
a wrapper still opens `inputgui`, inspect the installed wrapper and its menu
callback, then follow the extension reference before selecting a delegated
computational API. [[S24]](evidence-register.md#s24)
[[S55]](evidence-register.md#s55) [[S56]](evidence-register.md#s56)

Use installed help, official tutorials, and `eegh`/`EEG.history` to recover
release-correct calls. Verify text types per function and release; do not apply
one character-vector or string-scalar workaround ecosystem-wide. Community
snippets are discovery leads, not universal thresholds or ordering.
[[S24]](evidence-register.md#s24)
[[S55]](evidence-register.md#s55) [[S56]](evidence-register.md#s56)

## Core operation calls

| Operation | Fully parameterized route | Record and verify |
|---|---|---|
| SET intake | `pop_loadset(...)` with tested `loadmode` | Payload access, companion resolution, fields, warnings, events, locations, reference. [[S24]](evidence-register.md#s24) [[S63]](evidence-register.md#s63) |
| Filter | `pop_eegfiltnew(EEG, low, high, ...)` | Complete effective design, version, boundaries, response, shape. [[S09]](evidence-register.md#s09) [[S24]](evidence-register.md#s24) |
| Reference | `pop_reref(EEG, refspec, ...)` | Acquisition/offline reference, support/bads, formula, rank. [[S08]](evidence-register.md#s08) [[S24]](evidence-register.md#s24) |
| Interpolate | retain original `chanlocs`; `pop_select`; `pop_interp(...)` | Removed support, geometry, donors/method, channel-state and rank changes. [[S07]](evidence-register.md#s07) [[S24]](evidence-register.md#s24) |
| Epoch | `pop_epoch(...)` plus explicit baseline/rejection calls | Events, latency convention, baseline, retained/rejected entities and parents. [[S24]](evidence-register.md#s24) |

Run `eeg_checkset` after authorized structural changes and retain exact
`EEG.history` plus the operation record. History records calls but does not
establish source identity, fit scope, or scientific validity.
[[S03]](evidence-register.md#s03) [[S05]](evidence-register.md#s05)
[[S24]](evidence-register.md#s24)

## Execution and provenance checks

Before claiming execution, capture MATLAB/EEGLAB versions and resolved function
paths. For any non-core function, also load the extension reference and record
its distribution asset, version/commit/hash, license, dependencies, and smoke
result. [[S03]](evidence-register.md#s03) [[S24]](evidence-register.md#s24)
[[S30]](evidence-register.md#s30) [[S64]](evidence-register.md#s64)

Afterward compare source/output inventories, shape/rate/events, channel states,
reference/rank, fitted-state scope, expected numerical consequences, and all
warnings. For STUDY/BIDS work, additionally record whether the STUDY came from
SET commands or EEG-BIDS, the exact imported/missing metadata mapping, selectors,
write tree, and independent BIDS validation result. [[S03]](evidence-register.md#s03)
[[S05]](evidence-register.md#s05) [[S23]](evidence-register.md#s23)
[[S62]](evidence-register.md#s62) [[S63]](evidence-register.md#s63)
