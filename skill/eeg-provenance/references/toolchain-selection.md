# Intent-aware toolchain selection

Choose a toolchain per phase, not one tool for the whole dataset. Discovery, acquisition, conformance, metadata resolution, native-header inspection, signal reading, preprocessing, cache/export, and QC have different contracts; tools that complement one another must not be ranked as if they were interchangeable. [[S05]](evidence-register.md#s05) [[S31]](evidence-register.md#s31) [[S45]](evidence-register.md#s45) [[S47]](evidence-register.md#s47) [[S48]](evidence-register.md#s48)

## Contents

- [Required decision record](#required-decision-record)
- [Observation ladder](#observation-ladder)
- [Hard gates and preferences](#hard-gates-and-preferences)
- [Environment and candidate probes](#environment-and-candidate-probes)
- [Phase routing](#phase-routing)
- [Candidate boundaries](#candidate-boundaries)
- [Common intent patterns](#common-intent-patterns)
- [Stop and fallback rules](#stop-and-fallback-rules)

## Required decision record

Before invoking a candidate, add a `toolchain_decisions` entry to the Preprocessing Contract and provenance ledger with: [[S05]](evidence-register.md#s05)

1. `phase` and `intent`: the single job this decision must perform. [[S05]](evidence-register.md#s05)
2. `observation_level`: the least data access needed to answer it. [[S23]](evidence-register.md#s23) [[S31]](evidence-register.md#s31)
3. `hard_constraints`: source/release coverage, access terms, read-only boundaries, semantics that must survive, runtime/network/storage limits, allowed writes, and required output form. [[S03]](evidence-register.md#s03) [[S23]](evidence-register.md#s23) [[S50]](evidence-register.md#s50)
4. `preferences`: language, existing environment, dependency weight, memory, interactivity, cache format, and downstream framework. Preferences rank only candidates that pass every hard constraint. [[S03]](evidence-register.md#s03) [[S19]](evidence-register.md#s19)
5. `candidates`: tool/version, availability, capability, read scope, write scope, status, reason, and evidence IDs. Preserve rejected candidates when their failure explains why a less convenient route was selected. [[S05]](evidence-register.md#s05) [[S06]](evidence-register.md#s06)
6. `fallback_condition`: the exact failed probe or changed condition that activates a fallback. [[S05]](evidence-register.md#s05) [[S50]](evidence-register.md#s50)

Use `selected` only after runtime availability and the required entry points are verified. Use `planned` for a design-only route awaiting an environment probe, `fallback` for a conditional alternative, and `rejected` for a candidate that fails a hard gate. A package name in documentation, an executable on `PATH`, or a successful import alone does not establish release coverage, plugin availability, non-writing behavior, or endpoint suitability. [[S24]](evidence-register.md#s24) [[S25]](evidence-register.md#s25) [[S44]](evidence-register.md#s44) [[S53]](evidence-register.md#s53)

One decision may select multiple components when the route is genuinely composed, such as OpenNeuro CLI for the metadata checkout plus DataLad/git-annex for selected annex objects. Do not merge conformance and metadata-query candidates merely because both read a BIDS tree. [[S47]](evidence-register.md#s47) [[S48]](evidence-register.md#s48) [[S51]](evidence-register.md#s51)

## Observation ladder

Stop at the least sufficient observation level that answers the phase intent. Escalating access can trigger downloads, sample reads, transformations, memory allocation, or cache writes that are not justified by a metadata question. [[S23]](evidence-register.md#s23) [[S31]](evidence-register.md#s31) [[S44]](evidence-register.md#s44) [[S53]](evidence-register.md#s53)

| Level | What may be observed | Typical candidates |
|---|---|---|
| `catalogue` | Provider/catalogue records, accession, release, license, recording selectors; no signal bytes. [[S31]](evidence-register.md#s31) [[S51]](evidence-register.md#s51) | Provider page/API, EEGDash `EEGDash` client |
| `tree_and_sidecars` | Repository tree, README, BIDS TSV/JSON, annex keys/availability; no signal-array read. [[S01]](evidence-register.md#s01) [[S37]](evidence-register.md#s37) [[S48]](evidence-register.md#s48) | Provider CLI, Git/DataLad, PyBIDS, official Validator |
| `native_header` | Container header fields and bounded companion metadata. [[S42]](evidence-register.md#s42) [[S43]](evidence-register.md#s43) [[S46]](evidence-register.md#s46) | PyEDFlib, SciPy `whosmat`, format-native reader |
| `lazy_signal` | A normalized lazy recording object plus annotations/channel information, without preloading samples. [[S26]](evidence-register.md#s26) [[S27]](evidence-register.md#s27) [[S43]](evidence-register.md#s43) | MNE, MNE-BIDS, EEGLAB metadata/info load where supported |
| `bounded_samples` | Explicit channels/time span needed for unit, event, or QC verification. [[S03]](evidence-register.md#s03) [[S17]](evidence-register.md#s17) | MNE/EEGLAB or a native reader with an explicit slice |
| `full_execution` | Authorized preprocessing, windowing, caching, and export under the declared contract. [[S03]](evidence-register.md#s03) [[S20]](evidence-register.md#s20) [[S23]](evidence-register.md#s23) | MNE, EEGLAB, Braindecode, PyHealth, TorchEEG |

## Hard gates and preferences

Apply these gates in order. Do not score a candidate that fails one. [[S03]](evidence-register.md#s03) [[S23]](evidence-register.md#s23)

1. **Source and release gate:** confirm that the provider or adapter supports the exact accession/release, authentication terms, selectors, and desired files. A built-in dataset class does not prove equivalence to a separately obtained archive. [[S06]](evidence-register.md#s06) [[S44]](evidence-register.md#s44) [[S45]](evidence-register.md#s45) [[S51]](evidence-register.md#s51)
2. **Semantic gate:** confirm that required sidecars, native header fields, events, units, reference, channel types, coordinates, and hierarchy survive the route or remain separately accessible. A normalized MNE or framework object is not a lossless substitute for all source metadata. [[S01]](evidence-register.md#s01) [[S26]](evidence-register.md#s26) [[S42]](evidence-register.md#s42)
3. **Side-effect gate:** enumerate network reads, sample reads, source-tree writes, implicit caches, metadata indexes, conversions, and in-place mutations before invocation. Reject any route whose unavoidable writes intersect protected source data. [[S23]](evidence-register.md#s23) [[S25]](evidence-register.md#s25) [[S31]](evidence-register.md#s31) [[S53]](evidence-register.md#s53)
4. **Execution gate:** verify runtime, version, command/function signature, plugin/adapter entry points, and a harmless or synthetic smoke test. Documentation for another release is not evidence that the active runtime accepts the same call. [[S24]](evidence-register.md#s24) [[S47]](evidence-register.md#s47) [[S52]](evidence-register.md#s52) [[S55]](evidence-register.md#s55)
5. **Scale and transport gate:** estimate metadata size, selected content size, durable free space, cache expansion, network reachability, authentication, resume behavior, and restart recovery before bulk acquisition. [[S37]](evidence-register.md#s37) [[S50]](evidence-register.md#s50) [[S54]](evidence-register.md#s54)
6. **Evaluation gate:** reject framework routes whose baked-in transforms, processor fitting, windowing, or partition semantics cannot be made consistent with the declared endpoint and generalization split. [[S20]](evidence-register.md#s20) [[S21]](evidence-register.md#s21) [[S44]](evidence-register.md#s44) [[S53]](evidence-register.md#s53)

Among survivors, prefer the route that (a) uses the provider/release-native contract, (b) stops at the lowest observation level, (c) preserves the needed semantics, (d) makes writes and transforms explicit, (e) is already verified in the execution environment, and (f) produces the required downstream representation with the fewest untracked conversions. Record the tie-break instead of claiming a universal best tool. [[S03]](evidence-register.md#s03) [[S05]](evidence-register.md#s05) [[S19]](evidence-register.md#s19)

## Environment and candidate probes

Run the bundled non-network probe before choosing an implementation route:

```bash
python scripts/probe_toolchain.py > toolchain-capabilities.json
```

The probe reports Python distribution versions and command locations without opening EEG data, executing candidate commands, or testing network access. Its result is an availability inventory, not a selector; follow it with candidate-specific `--version`/`--help`, import/signature, source-adapter, write-scope, and smoke-test checks. [[S05]](evidence-register.md#s05) [[S47]](evidence-register.md#s47) [[S52]](evidence-register.md#s52)

Run the probe in the runtime that will execute the phase. Treat native Windows, WSL, a container, a scheduler job, a hosted notebook, and a remote server as separate capability domains; a tool found in one is not evidence that another has it, can reach the source, or writes to durable storage. [[S50]](evidence-register.md#s50)

For a MATLAB route, command availability and an active MATLAB integration are separate from EEGLAB/plugin availability. Run `scripts/probe_eeglab.m` in the actual session before selecting it; the equivalent core probe is: [[S24]](evidence-register.md#s24) [[S25]](evidence-register.md#s25) [[S30]](evidence-register.md#s30)

```matlab
fprintf('MATLAB=%s\n', version)
required = ["eeglab", "eeg_getversion", "eeg_checkset", ...
            "pop_loadset", "pop_importbids", "pop_eegfiltnew", "eegh"];
for name = required
    fprintf('%s=%s\n', name, string(which(name)))
end
if ~isempty(which('eeg_getversion'))
    fprintf('EEGLAB=%s\n', string(eeg_getversion))
end
```

An empty function path keeps that candidate `planned`, `fallback`, or `rejected`; it is not repaired by merely detecting MATLAB. Prefer a fully parameterized `pop_` call that never opens a dialog. If the wrapper has no complete non-GUI route, inspect its installed source/menu callback, identify the public wrapped API, verify its help/signature, and exercise the substitution on a disposable input before selection. Capture `eegh`/`EEG.history` when a GUI reproduction is useful, but do not require GUI interaction when the complete version-correct call is already known. [[S24]](evidence-register.md#s24) [[S55]](evidence-register.md#s55) [[S56]](evidence-register.md#s56)

## Phase routing

| Phase intent | Select first | Pair or switch when |
|---|---|---|
| Resolve `ds*`, `nm*`, or `on*` identity and available releases | Provider record/API; use EEGDash as a catalogue view when it covers the identifier. [[S31]](evidence-register.md#s31) [[S51]](evidence-register.md#s51) | Preserve provider, catalogue, DOI, and cross-provider identifiers separately when they disagree. [[S31]](evidence-register.md#s31) [[S51]](evidence-register.md#s51) |
| Acquire an OpenNeuro snapshot or selected files | OpenNeuro CLI/direct provider route; use DataLad/git-annex for the metadata/content split and path-scoped object retrieval. [[S37]](evidence-register.md#s37) [[S51]](evidence-register.md#s51) | Use EEGDash when its verified backend covers the recording and its BIDS-shaped cache/MNE-Braindecode representation is desired; it is not the provenance owner. [[S31]](evidence-register.md#s31) |
| Acquire an authorized or apply-to-access release | Current provider-native authenticated route and smallest official test transfer. [[S40]](evidence-register.md#s40) [[S54]](evidence-register.md#s54) | Add a framework only after data exist in a protected source/staged view and its release assumptions and writes have been accepted. [[S44]](evidence-register.md#s44) [[S53]](evidence-register.md#s53) |
| Validate BIDS conformance | Official BIDS Validator with recorded executable/schema/configuration. [[S47]](evidence-register.md#s47) | Pair with PyBIDS for queries and MNE-BIDS/EEG-BIDS for semantic reads; neither replaces official conformance. [[S25]](evidence-register.md#s25) [[S26]](evidence-register.md#s26) [[S48]](evidence-register.md#s48) |
| Query BIDS entities, inheritance, raw/derivative scopes, and anatomy candidates | PyBIDS with an in-memory index for read-only intake. [[S48]](evidence-register.md#s48) | Pair with direct TSV/JSON inspection to retain contributing sidecars/conflicts and MNE-BIDS only when a normalized Raw view is needed. [[S01]](evidence-register.md#s01) [[S26]](evidence-register.md#s26) |
| Preserve EDF/BDF per-signal header fidelity | PyEDFlib header calls. [[S42]](evidence-register.md#s42) [[S46]](evidence-register.md#s46) | Pair with MNE for a lazy processing representation; preserve native header observations separately. [[S27]](evidence-register.md#s27) [[S46]](evidence-register.md#s46) |
| Inspect GDF or MAT without loading signal arrays | MNE lazy GDF reader; SciPy `whosmat`/MAT version probe; use pymatreader/HDF5 route for documented v7.3 variables. [[S43]](evidence-register.md#s43) [[S49]](evidence-register.md#s49) | Switch to MATLAB/EEGLAB when dataset documentation or required semantics are encoded in MATLAB/EEGLAB structures and that environment is verified. [[S24]](evidence-register.md#s24) [[S49]](evidence-register.md#s49) |
| Execute a Python-native preprocessing contract | MNE/MNE-BIDS when its representation and algorithms cover the endpoint. [[S26]](evidence-register.md#s26) [[S27]](evidence-register.md#s27) | Add Braindecode only for accepted window/dataset/model integration; add MOABB only for a supported BCI release/paradigm route. [[S45]](evidence-register.md#s45) [[S52]](evidence-register.md#s52) |
| Execute a MATLAB-native or EEGLAB-plugin contract | Verified EEGLAB plus required plugins, using official tutorials/help/history to derive calls. [[S24]](evidence-register.md#s24) [[S25]](evidence-register.md#s25) [[S55]](evidence-register.md#s55) | Use MNE/Python for unsupported automation only with an explicit representation handoff and cross-view checks. [[S03]](evidence-register.md#s03) [[S24]](evidence-register.md#s24) |
| Build model-ready framework caches | Braindecode, PyHealth, or TorchEEG only when its representation, transformations, cache writes, split behavior, and downstream consumer match the contract. [[S20]](evidence-register.md#s20) [[S44]](evidence-register.md#s44) [[S52]](evidence-register.md#s52) [[S53]](evidence-register.md#s53) | Keep a simpler MNE/EEGLAB derivative when framework coupling is not required or obscures source semantics. [[S03]](evidence-register.md#s03) [[S24]](evidence-register.md#s24) [[S27]](evidence-register.md#s27) |

## Candidate boundaries

- **EEGDash:** choose its catalogue client for metadata-only search and its dataset class for a deliberately selected, supported recording/cache route. Reject it as a BIDS validator, provider identity authority, or universal `ds*`/`nm*`/`on*` downloader. [[S31]](evidence-register.md#s31) [[S51]](evidence-register.md#s51)
- **DataLad/git-annex:** choose them when the verified source is annex-backed and selective, resumable content retrieval matters. Verify repository state and object availability; a clone or work-tree path alone does not mean payload bytes are local. [[S37]](evidence-register.md#s37) [[S50]](evidence-register.md#s50) [[S51]](evidence-register.md#s51)
- **MOABB:** choose a versioned class for its supported BCI release and MNE/paradigm interface. Reject it as evidence that an arbitrary local copy matches that release or as a general non-BIDS inspector. [[S45]](evidence-register.md#s45)
- **MNE/MNE-BIDS:** choose them for lazy multi-format reads and Python preprocessing, and MNE-BIDS when BIDS sidecars must populate the Raw view. Pair with the official Validator/PyBIDS/native header tools when conformance, inheritance provenance, or container fidelity is required. [[S26]](evidence-register.md#s26) [[S27]](evidence-register.md#s27) [[S46]](evidence-register.md#s46) [[S48]](evidence-register.md#s48)
- **EEGLAB/EEG-BIDS:** choose a verified MATLAB route for EEGLAB structures, plugins, interactive review, or MATLAB-native processing. Reject it when required plugins are absent, source-safe output cannot be guaranteed, or a server has no verified MATLAB integration. [[S24]](evidence-register.md#s24) [[S25]](evidence-register.md#s25) [[S30]](evidence-register.md#s30)
- **Makoto's useful EEGLAB code:** use it to locate practical snippets and edge cases, then reconcile each snippet with the current official tutorial/help, installed signature, endpoint contract, and a bounded test. Do not import its hard-coded paths, channel indices, thresholds, filter settings, preprocessing order, or personal recommendations as dataset-independent guidance. [[S19]](evidence-register.md#s19) [[S55]](evidence-register.md#s55)
- **Braindecode:** choose it after intake for MNE-backed dataset, preprocessing, window, augmentation, and decoder integration. Record mutations/saves and keep architecture choice outside this skill's scientific scope. [[S20]](evidence-register.md#s20) [[S52]](evidence-register.md#s52)
- **PyHealth:** choose a version-isolated route only when its dataset/task representation and baked transforms match the intended healthcare EEG endpoint. Reject it for read-only archive inspection because dataset/task construction can fit processors and write metadata/caches. [[S20]](evidence-register.md#s20) [[S53]](evidence-register.md#s53)
- **TorchEEG:** choose a versioned adapter or generic cache only after release assumptions, segmentation, transforms, axes, labels, partitions, and `io_path` writes are accepted. Reject adapter availability as primary dataset documentation. [[S06]](evidence-register.md#s06) [[S44]](evidence-register.md#s44)

## Common intent patterns

### Read-only local BIDS intake in Python

Select the official Validator for conformance and PyBIDS for entity/inheritance queries. Add MNE-BIDS at `lazy_signal` only when channel, bad, annotation, or coordinate mapping in an MNE Raw object is needed; add PyEDFlib for EDF-native header fidelity. Do not select EEGDash merely because the dataset once originated from OpenNeuro or NeMAR. [[S26]](evidence-register.md#s26) [[S31]](evidence-register.md#s31) [[S46]](evidence-register.md#s46) [[S47]](evidence-register.md#s47) [[S48]](evidence-register.md#s48)

### Partial remote acquisition from an accession

Resolve provider/version first, enumerate exact recording/sidecar paths, preflight networking/tooling/durable space, then select a provider-native/DataLad/git-annex or verified EEGDash route. Fetch one representative recording and companions, verify identity and cache destination, and expand only after the bounded pipeline passes. [[S31]](evidence-register.md#s31) [[S50]](evidence-register.md#s50) [[S51]](evidence-register.md#s51)

### Authorized TUH preparation for a PyHealth experiment

Select the provider's current authenticated rsync route for acquisition and test its small official path first; use native EDF/PyEDFlib or lazy MNE intake on the staged source. Select PyHealth only after its TUAB/TUEV task transforms, predefined split, cache writes, and version-isolated dependencies match the endpoint, and never point a write-capable constructor at the protected source. [[S40]](evidence-register.md#s40) [[S46]](evidence-register.md#s46) [[S53]](evidence-register.md#s53) [[S54]](evidence-register.md#s54)

### MATLAB/EEGLAB-preferred processing

Select the official Validator separately for BIDS conformance, then verify the active MATLAB session, EEGLAB version, required import/processing plugins, `which` paths, and a disposable smoke test. Use official tutorials and generated history to form version-correct calls; consult Makoto's collection for candidate recipes only, and preserve the source/derivative boundary. [[S23]](evidence-register.md#s23) [[S24]](evidence-register.md#s24) [[S25]](evidence-register.md#s25) [[S47]](evidence-register.md#s47) [[S55]](evidence-register.md#s55)

## Stop and fallback rules

Stop the affected phase when no candidate passes every hard constraint. Report the failed probes and the narrow missing capability; do not silently substitute a catalogue for a provider, a layout indexer for a validator, a normalized reader for native-header evidence, or a training framework for read-only intake. [[S03]](evidence-register.md#s03) [[S31]](evidence-register.md#s31) [[S46]](evidence-register.md#s46) [[S47]](evidence-register.md#s47) [[S48]](evidence-register.md#s48)

Activate a fallback only on its recorded condition, repeat the hard gates for that route, and update the ledger before execution. Tool failure can narrow an implementation choice; it does not authorize weaker source identity, unsafe writes, guessed metadata, unreported transforms, or evaluation leakage. [[S03]](evidence-register.md#s03) [[S20]](evidence-register.md#s20) [[S23]](evidence-register.md#s23) [[S50]](evidence-register.md#s50)
