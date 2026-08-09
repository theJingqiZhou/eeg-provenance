# Intent-aware toolchain selection

Choose an implementation for the current phase, not one ecosystem for the whole dataset. Discovery, acquisition, conformance, inspection, signal reading, processing, export, and QC have different contracts. (Evidence: S05, S31, S47, S48)

## Decision algorithm

1. Name one `phase` and `intent` that the next tool call must satisfy.
2. Choose the least sufficient observation level.
3. Reject candidates that fail any hard gate; do not score them against user preferences.
4. Rank survivors by semantic preservation, explicit side effects, verified runtime support, and downstream fit.
5. Probe only availability or behavior that remains decision-relevant.
6. Record the selected, planned, or stopped outcome before executing that phase.

Evidence: S03, S05, S23, S24, S50.

Preferences rank only candidates that pass every hard constraint. Do not score a candidate that fails one. Preferences never override source identity, required semantics, protected writes, evaluation fit scope, or missing executable capability. (Evidence: S03, S20, S23, S24)

## Progressive decision record

Create records only for phases reached by the request. Do not predeclare acquisition, export, or QC for a one-header inspection. (Evidence: S05, S57; local workflow policy)

Record:

- decision `id`, `phase`, `intent`, `status`, and `observation_level`;
- hard constraints and preferences;
- each candidate's stable `id`, exact tool/version, availability, capability, read scope, write scope, status, reason, and evidence IDs;
- `failure_policy`: `stop` or `fallback`;
- `fallback_condition`: `null` for `stop`, otherwise the exact activation condition.

Evidence: S05, S24, S50; local provenance policy.

Use decision status `selected` only when at least one candidate is verified and selected, `planned` when execution has not been verified, and `stopped` when no candidate passes. A stopped phase does not need a fictional fallback. (Evidence: S05, S24, S50; local provenance policy)

## Observation ladder

| Level | Permitted observation | Typical route |
|---|---|---|
| `catalogue` | Provider records, accessions, releases, selectors; no payload | Provider API/page, EEGDash catalogue |
| `tree_and_sidecars` | Repository tree, README, TSV/JSON, annex availability | Provider CLI, Git/DataLad, PyBIDS, Validator |
| `native_header` | Container header and bounded companion metadata | PyEDFlib, SciPy `whosmat`, native reader |
| `lazy_signal` | Normalized lazy recording and annotations | MNE, MNE-BIDS, verified EEGLAB info load |
| `bounded_samples` | Explicit channels and time span for verification/QC | MNE, EEGLAB, native sliced reader |
| `full_execution` | Authorized transforms, windows, caches, and export | MNE, EEGLAB, Braindecode, PyHealth, TorchEEG |

Evidence: S23, S31, S42, S46, S52, S53.

Do not escalate merely because a higher-access tool is installed. EEG-BIDS 10.5 `metadata='on'`, for example, still loads the selected SET payload and is not a native-header route. (Evidence: S23, S31, S42, S46, S56)

## Hard gates

| Gate | Required proof |
|---|---|
| Source/release | Exact provider, release, access terms, selectors, and desired files |
| Semantics | Required events, units, reference, channel/coordinate metadata, and hierarchy survive or remain separately available |
| Side effects | Network, sample reads, indexes, caches, conversions, source mutations, and all writes are known and allowed |
| Execution | Runtime, version, signature, plugin/adapter entry points, and a harmless smoke test are verified |
| Scale/transport | Selected bytes, expansion, durable space, authentication, resumability, and restart behavior are acceptable |
| Evaluation | Baked transforms, fitting, windowing, labels, and partitions match the declared generalization split |

Evidence: S03, S20, S23, S37, S44, S50, S53, S58–S61.

For a pinned or unfamiliar Python host, inventory the active interpreter and apply [runtime compatibility](runtime-compatibility.md) before changing it. A package declaration or successful resolution does not pass the execution gate. (Evidence: S58–S61; local environment policy)

Reject the route at the first failed gate. Prefer the surviving route with the least access and fewest untracked representation changes. (Evidence: S03, S20, S23, S37, S44, S50, S53)

## Phase routing

| Intent | Primary route | Pair or switch when |
|---|---|---|
| Resolve `ds*`, `nm*`, `on*` | Provider record; EEGDash only as a covered catalogue | Preserve provider, DOI, catalogue, and cross-provider IDs separately |
| Acquire public selected content | Provider CLI/direct path or DataLad/git-annex | Use EEGDash only when its verified backend and cache representation fit |
| Acquire a supported benchmark | MOABB only after its provider, release, selectors, and cache contract are verified | Switch to the provider route when wrapper coverage or identity is insufficient |
| Acquire controlled data | Current authenticated provider route and smallest test transfer | Add a framework only after staging a protected source/work view |
| Validate BIDS conformance | Official BIDS Validator | Pair with PyBIDS for queries and MNE-BIDS or EEGLAB/EEG-BIDS for semantic reads |
| Query BIDS metadata | PyBIDS in-memory index | Add direct sidecar inspection; use MNE-BIDS only for a Raw view |
| Preserve native EDF/BDF header | PyEDFlib | Pair with MNE for the signal-read and processing representation |
| Inspect GDF/MAT | Lazy MNE GDF; SciPy MAT directory/version probe | Use pymatreader/HDF5 for v7.3 or verified MATLAB/EEGLAB for MATLAB semantics |
| Execute signal preprocessing | MNE or verified EEGLAB, selected by operation semantics | Add Braindecode only for dataset/window/model integration |
| Build model-ready cache/export | Braindecode, PyHealth, or TorchEEG after split and cache audit | Keep an MNE/EEGLAB derivative when coupling adds no value |
| Run QC | Tool matching the representation plus independent summaries | Switch when the producer cannot expose the required consequence |

Evidence: S24–S27, S31, S37, S42–S53, S56.

## Operation and environment probes

After phase routing, use [operation-semantics.md](operation-semantics.md) to choose the processing primitive. Load only the selected tool recipe afterward.

Probe only unresolved candidates:

```bash
python scripts/probe_toolchain.py --intent bids-query --compact
python scripts/probe_toolchain.py --tools mne,pyedflib --compact
```

For a pinned host, use `--intent runtime-compat`. The probe reads only standard-library metadata; it does not import or change packages. `uv` is optional; use the site's approved manager only when isolation is needed. (Evidence: S58–S61; local environment policy)
For MATLAB, run `scripts/probe_eeglab.m` in the active session; a MATLAB executable does not establish EEGLAB/plugin availability. Fully parameterize `pop_` calls. When no complete non-GUI wrapper path exists, inspect the installed wrapper/menu callback, verify its public delegated API, and test it on disposable input. (Evidence: S24, S25, S55, S56)

## Stop and fallback

For `failure_policy=stop`, set `fallback_condition=null` and report the narrow missing capability. For `failure_policy=fallback`, activate the recorded route only on its stated condition, repeat every hard gate, and update the decision before execution. A failed tool never authorizes guessed metadata, unsafe writes, weaker identity, unreported transforms, or leakage. (Evidence: S03, S20, S23, S50)
