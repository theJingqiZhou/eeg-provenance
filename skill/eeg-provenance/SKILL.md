---
name: eeg-provenance
description: Provenance-aware EEG dataset intake for BIDS and sufficiently documented non-BIDS releases and containers including EDF/GDF/MAT/CNT/SET, active dataset-documentation recovery, accession-first OpenNeuro and NeMAR acquisition via EEGDash, provider tools, DataLad, or git-annex, remote compute-side acquisition and durable cache builds, preprocessing design, channel and montage harmonization, MNE or EEGLAB execution, and QC. Use when onboarding or comparing EEG datasets, receiving OpenNeuro dsNNNNNN or NeMAR nmNNNNNN/onNNNNNN identifiers, resolving BIDS inheritance or legacy release contracts, auditing preprocessing, converting BIDS/EEGLAB/MNE data, handling MATLAB v7.3 without MATLAB, preparing data on an ephemeral server, deciding filters, reference, interpolation, resampling, or artifact handling, and producing reproducible preprocessing ledgers. Do not use for clinical interpretation or model selection.
---

# EEG Provenance

Build an auditable EEG preprocessing decision before changing samples. Treat every transform as an evidence-bounded intervention with explicit inputs, parameters, fit scope, channel effect, rank effect, outputs, and limitations. [[S03]](references/evidence-register.md#s03) [[S05]](references/evidence-register.md#s05)

## Non-negotiable rules

1. Preserve source bytes. Write derivatives, caches, reports, and temporary files outside the source dataset. BIDS derivatives are distinct from raw source data, and the EEG-BIDS importer warns that writing its generated STUDY files into a BIDS archive breaks conformance. [[S23]](references/evidence-register.md#s23) [[S25]](references/evidence-register.md#s25)
2. Keep unknown acquisition or preprocessing history unknown. Do not infer it from current samples or filenames; record the missing evidence and its consequences. COBIDAS-MEEG and EEG-BIDS require acquisition and processing metadata because signal arrays alone do not preserve that history. [[S01]](references/evidence-register.md#s01) [[S03]](references/evidence-register.md#s03)
3. Complete the Data Intake Report and Preprocessing Contract before executing interventions. Report parameters and deviations at the level needed to reproduce the derivative. [[S03]](references/evidence-register.md#s03) [[S05]](references/evidence-register.md#s05)
4. For predictive evaluation, fit learned or data-adaptive preprocessing only on the training partition, nested within resampling when tuning it. Leakage and non-independent cross-validation can inflate estimated generalization. [[S20]](references/evidence-register.md#s20) [[S21]](references/evidence-register.md#s21) [[S22]](references/evidence-register.md#s22)
5. Preserve channel identity. Label every channel as `native`, `bad`, `missing`, `dropped`, `interpolated`, or `virtual`; never present an estimate or algebraic channel as a native measurement. Spatial interpolation estimates signals from other sensors and referencing changes the representation and rank. [[S07]](references/evidence-register.md#s07) [[S08]](references/evidence-register.md#s08)
6. Reject a universal “gold-standard pipeline.” Choose interventions from the analysis objective, acquisition facts, retained bandwidth, geometry, reference, and validation design; EEG outcomes can vary materially across plausible preprocessing choices. [[S18]](references/evidence-register.md#s18) [[S19]](references/evidence-register.md#s19)
7. Search for missing dataset evidence. An absent attachment is not a reason to abandon intake: inspect exact local release artifacts and actively search official dataset pages, versioned README/release notes, primary papers, codebooks, and conversion code; record unsuccessful routes and block only the decisions that remain unsupported. [[S03]](references/evidence-register.md#s03) [[S06]](references/evidence-register.md#s06)

## Required workflow

### 1. Produce a Data Intake Report

Inventory the immutable source, dataset and recording identifiers, data format, sidecars, sampling rate, units, channel types, reference, line frequency, hardware/software filters, event semantics, electrode coordinates and coordinate frame, existing bad-channel annotations, and known prior processing. Preserve conflicts and unknowns instead of silently resolving them. [[S01]](references/evidence-register.md#s01) [[S02]](references/evidence-register.md#s02)

Use [references/dataset-intake.md](references/dataset-intake.md) for the common checklist and source-contract routing. For a BIDS source or derivative, apply the pinned core, inheritance, EEG, events, coordinates, and derivative rules in [references/bids-eeg-1.11.1.md](references/bids-eeg-1.11.1.md), then use the maintained validator/PyBIDS/MNE-BIDS/EEG-BIDS stack in [references/tool-recipes-bids.md](references/tool-recipes-bids.md). For non-BIDS layouts, use the documentation-recovery, endpoint sufficiency, established-tool routing, and adaptation-record rules in [references/non-bids-intake.md](references/non-bids-intake.md). [[S01]](references/evidence-register.md#s01) [[S03]](references/evidence-register.md#s03) [[S23]](references/evidence-register.md#s23) [[S47]](references/evidence-register.md#s47) [[S48]](references/evidence-register.md#s48)

When the endpoint includes EEG source imaging, a forward solution, or head modeling, use [references/anatomy-forward-model.md](references/anatomy-forward-model.md) to locate raw T1w anatomy, released reconstructions, surfaces, segmentations, sensor-to-MRI transforms, and BEM/FEM assets. Keep this as a separate readiness gate: sensor geometry or a structural MRI alone is not a complete forward-model input set. [[S34]](references/evidence-register.md#s34) [[S36]](references/evidence-register.md#s36)

Treat OpenNeuro `dsNNNNNN` and NeMAR `nmNNNNNN` or `onNNNNNN` strings as provider accessions. EEGDash is a catalogue/access option rather than the provenance owner. Preserve the supplied accession, resolve provider metadata and version or snapshot, then choose among EEGDash, provider CLI/direct transfer, or DataLad/git-annex according to the verified backend and execution environment. Do not infer an OpenNeuro `ds*` cross-reference from a NeMAR `on*` prefix without provider metadata. [[S31]](references/evidence-register.md#s31) [[S37]](references/evidence-register.md#s37) [[S51]](references/evidence-register.md#s51)

When preprocessing will run on a remote server, hosted notebook, or ephemeral VM, use [references/remote-cache-execution.md](references/remote-cache-execution.md) to preflight network, tooling, disk, quota, and persistence; acquire selected source objects directly on the compute side when authorized; publish verified resumable cache shards to durable storage; and preserve failure states. Do not assume that a repository clone, scheduler submission, or notebook start implies data content, git-annex, outbound networking, or persistent storage is available. [[S37]](references/evidence-register.md#s37) [[S50]](references/evidence-register.md#s50)

### 2. State the objective and invariants

Specify the scientific endpoint, required temporal and spectral support, epoch definition, acceptable latency error, spatial quantities, native information that must survive, generalization unit, and allowed derivative outputs. These constraints determine whether filtering, resampling, referencing, interpolation, or artifact correction is admissible. [[S03]](references/evidence-register.md#s03) [[S09]](references/evidence-register.md#s09)

### 3. Produce a Preprocessing Contract

For each dataset dimension, classify the proposed alignment as:

- `must_harmonize`: incompatible representations would make the intended comparison undefined or invalid; document the target and evidence. [[S01]](references/evidence-register.md#s01) [[S08]](references/evidence-register.md#s08)
- `may_harmonize`: the intervention may improve comparability but discards or models information; predeclare alternatives or sensitivity analyses. [[S07]](references/evidence-register.md#s07) [[S19]](references/evidence-register.md#s19)
- `cannot_harmonize`: the relevant acquisition fact or information is absent and cannot be recovered by preprocessing; expose the limitation or narrow the estimand. [[S03]](references/evidence-register.md#s03) [[S19]](references/evidence-register.md#s19)

Use [references/harmonization.md](references/harmonization.md), [references/channels-montages.md](references/channels-montages.md), and [references/preprocessing-interventions.md](references/preprocessing-interventions.md). Include an explicit “no intervention” option whenever it is scientifically admissible. [[S18]](references/evidence-register.md#s18) [[S19]](references/evidence-register.md#s19)

Use [references/research-scenarios.md](references/research-scenarios.md) for ERP, single-trial BCI, cross-session biometrics, cross-task generalization, and the ds003061/nm000166 comparison; its branches remain conditional on the declared endpoint. [[S19]](references/evidence-register.md#s19) [[S20]](references/evidence-register.md#s20)

### 4. Execute with a ledger

Create the ledger from [assets/provenance-ledger.template.json](assets/provenance-ledger.template.json). Record source entities, activities in order, executing software and versions, exact parameters, random seeds, fit scope, input/output shapes, sample rate, units, channel states, reference, bad spans, rank estimates, QC, output hashes, and unresolved limitations. Use W3C PROV’s Entity–Activity–Agent relations as the conceptual model without claiming full PROV-O conformance. Treat BIDS Derivatives conformance as a separate file, naming, metadata, and provenance contract; the ledger alone does not confer it. [[S05]](references/evidence-register.md#s05) [[S23]](references/evidence-register.md#s23)

Validate the ledger:

```bash
python scripts/validate_ledger.py path/to/ledger.json
```

Use [references/provenance-ledger.md](references/provenance-ledger.md) for field semantics.

### 5. Produce QC and limitations

Compare before/after summaries appropriate to the declared objective; at minimum report data loss, channel-state transitions, event changes, sampling-rate changes, reference, rank, and intervention-specific diagnostics. Keep algorithm scores separate from scientific acceptability, and report sensitivity to consequential conditional choices. [[S03]](references/evidence-register.md#s03) [[S17]](references/evidence-register.md#s17) [[S19]](references/evidence-register.md#s19)

Return exactly three named artifacts:

1. **Data Intake Report** — observed facts, conflicts, unknowns, and source identities.
2. **Preprocessing Contract** — objectives, invariants, harmonization classes, ordered interventions, fit scope, alternatives, and stop conditions.
3. **Provenance Ledger and QC** — executed activities, versioned parameters, channel/rank/shape transitions, diagnostics, outputs, and limitations. [[S03]](references/evidence-register.md#s03) [[S05]](references/evidence-register.md#s05)

If a stop condition is reached or the request is design-only, still return all three names, but mark execution in **Provenance Ledger and QC** as `not_executed`; record the refusal/stop evidence and never invent transforms, outputs, or post-transform QC. [[S03]](references/evidence-register.md#s03) [[S05]](references/evidence-register.md#s05)

## Evidence discipline

Tag important decisions with one of these evidence classes and cite an evidence-register ID:

- `HARD_INVARIANT`: a mathematical, physical, or data-model constraint. [[S01]](references/evidence-register.md#s01) [[S08]](references/evidence-register.md#s08)
- `CONSENSUS_REPORTING`: a community reporting or interoperability recommendation. [[S02]](references/evidence-register.md#s02) [[S03]](references/evidence-register.md#s03)
- `CONDITIONAL_EVIDENCE`: empirical evidence whose applicability depends on task, data, or estimator. [[S12]](references/evidence-register.md#s12) [[S18]](references/evidence-register.md#s18)
- `EMPIRICAL_BASELINE`: a documented starting point to validate locally, not a universal default. [[S04]](references/evidence-register.md#s04) [[S17]](references/evidence-register.md#s17)
- `SOFTWARE_CONTRACT`: behavior documented for a named software version; record the actual version used. [[S14]](references/evidence-register.md#s14) [[S24]](references/evidence-register.md#s24)
- `LOCAL_POLICY`: a conservative project safeguard; label it as policy and cite the risk it controls. [[S20]](references/evidence-register.md#s20) [[S23]](references/evidence-register.md#s23)

Use [references/evidence-register.md](references/evidence-register.md) as the sole claim-source registry. If a necessary claim is absent, report the evidence gap and stop short of presenting the claim as supported; do not invent a source or silently extend the registry. [[S03]](references/evidence-register.md#s03)

## Tool routing

- Use [references/tool-recipes-mne.md](references/tool-recipes-mne.md) for MNE-Python and MNE-BIDS.
- Use [references/anatomy-forward-model.md](references/anatomy-forward-model.md) for subject-anatomy discovery, FreeSurfer derivative checks, coregistration inputs, and BEM/FEM readiness.
- Use [references/tool-recipes-eeglab.md](references/tool-recipes-eeglab.md) for MATLAB, EEGLAB, and the EEG-BIDS plugin.
- Use [references/tool-recipes-eegdash.md](references/tool-recipes-eegdash.md) for accession-first `ds*`/`nm*`/`on*` route selection, EEGDash metadata queries and supported downloads, provider/DataLad/git-annex alternatives, offline loading, and descriptive QC. [[S31]](references/evidence-register.md#s31) [[S51]](references/evidence-register.md#s51)
- Use [references/tool-recipes-torcheeg.md](references/tool-recipes-torcheeg.md) to inspect a versioned built-in adapter as a hypothesis source or to stage an authorized derivative cache only after the local release contract is verified. [[S44]](references/evidence-register.md#s44)
- Use [references/tool-recipes-braindecode-pyhealth.md](references/tool-recipes-braindecode-pyhealth.md) when Braindecode or PyHealth may supply acquisition adapters, preprocessing/window/task machinery, persistent model-ready caches, or reusable decoder interfaces. Treat every baked-in transform and processor fit as an auditable intervention; model availability is not model-selection evidence. [[S20]](references/evidence-register.md#s20) [[S52]](references/evidence-register.md#s52) [[S53]](references/evidence-register.md#s53)
- Use [references/tool-recipes-bids.md](references/tool-recipes-bids.md) for official validation, inherited metadata queries, BIDS-aware lazy reads, derivative/anatomy discovery, and annex-backed validation. [[S26]](references/evidence-register.md#s26) [[S47]](references/evidence-register.md#s47) [[S48]](references/evidence-register.md#s48)
- Use [references/remote-cache-execution.md](references/remote-cache-execution.md) for compute-side acquisition, runtime preflight, verified standalone git-annex fallback, bounded fetch/process/release loops, durable cache publication, and restart-safe failure handling. [[S37]](references/evidence-register.md#s37) [[S50]](references/evidence-register.md#s50)
- Run `scripts/eegdash_intake.py --help` for guarded catalogue, one-recording download, and offline-QC modes. [[S31]](references/evidence-register.md#s31)

## Stop conditions

Stop before transformation when the source location is writable but no derivative destination is defined, the recording identity is ambiguous, channel units or types are unresolved, required geometry/reference information is missing for a spatial operation, event meaning is unresolved for event-locked analysis, or the evaluation split cannot contain adaptive fitting. Search and report available evidence first; absence of a user attachment alone is not a stop condition. These are decision blockers, not invitations to guess. [[S01]](references/evidence-register.md#s01) [[S03]](references/evidence-register.md#s03) [[S06]](references/evidence-register.md#s06) [[S20]](references/evidence-register.md#s20)
