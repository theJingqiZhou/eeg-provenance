# Dataset intake

Use this checklist before opening the signal payload. BIDS metadata is evidence about acquisition and representation, but missing metadata remains unknown and parsing success does not establish scientific validity. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03) [[S26]](evidence-register.md#s26)

For exact BIDS 1.11.1 requirement levels, inheritance behavior, EEG field contracts, event timing, coordinates, and derivative naming/provenance, use [bids-eeg-1.11.1.md](bids-eeg-1.11.1.md). [[S01]](evidence-register.md#s01) [[S23]](evidence-register.md#s23)

For non-BIDS EDF/GDF/MAT releases, use [non-bids-intake.md](non-bids-intake.md). It requires active documentation recovery, separates format observations from release/protocol evidence, defines a generic adaptation record, and uses BCI Competition IV 2a, SEED, TUEG, and TUAB only as worked evidence cases. [[S03]](evidence-register.md#s03) [[S38]](evidence-register.md#s38) [[S39]](evidence-register.md#s39) [[S40]](evidence-register.md#s40) [[S41]](evidence-register.md#s41)

## Route by source contract

Apply [toolchain-selection.md](toolchain-selection.md) before turning these source routes into commands. Choose separately for discovery, acquisition, conformance, metadata/native-header inspection, lazy signal representation, and later processing; user preferences rank only candidates that preserve the required source semantics and read/write boundary. [[S03]](evidence-register.md#s03) [[S05]](evidence-register.md#s05) [[S23]](evidence-register.md#s23)

- Route a conforming BIDS dataset to the pinned BIDS workflow and resolve inheritance before judging recording-level fields. [[S01]](evidence-register.md#s01)
- Route a documented legacy/project layout to the non-BIDS sufficiency gate; do not demand conversion to BIDS before learning the original release semantics. [[S03]](evidence-register.md#s03) [[S42]](evidence-register.md#s42)
- If the layout is unfamiliar, search official portals, versioned release records, primary papers, codebooks, and conversion code, then use a generic header/array-directory inventory while semantic gaps remain explicit. Missing attachments do not excuse skipping this evidence search. [[S03]](evidence-register.md#s03) [[S06]](evidence-register.md#s06) [[S43]](evidence-register.md#s43)
- Route a supplied `dsNNNNNN`, `nmNNNNNN`, or `onNNNNNN` accession through provider metadata before choosing transport. `ds*` denotes OpenNeuro here; `nm*` and `on*` denote NeMAR accessions, and EEGDash is one catalogue/access layer rather than the owner of those datasets. [[S31]](evidence-register.md#s31) [[S51]](evidence-register.md#s51)
- If preprocessing will run on remote compute, record data locality, access terms, expected transfer size, available source endpoints, content identities, and the persistent cache destination before sample retrieval; use [remote-cache-execution.md](remote-cache-execution.md) for capability gates and resumable execution. [[S05]](evidence-register.md#s05) [[S50]](evidence-register.md#s50)

## Read-only boundary

- Resolve and record the dataset root, dataset identifier, version/commit, source URL or archive location, recording entities, and source-file hashes when available. Rich identifiers and provenance make reuse and change detection more reliable. [[S05]](evidence-register.md#s05) [[S06]](evidence-register.md#s06)
- Treat a raw BIDS tree or data archive as immutable. Put derivatives, EEGLAB STUDY files, reports, caches, and temporary files elsewhere. [[S23]](evidence-register.md#s23) [[S25]](evidence-register.md#s25)
- Do not run `git annex get`, `unlock`, `drop`, `sync`, or `adjust` during intake. Object availability is an archive-management fact, not permission to change annex state; this prohibition is local policy protecting the source/derivative boundary. [[S05]](evidence-register.md#s05) [[S23]](evidence-register.md#s23)

## Dataset-level facts

Require `Name`, `BIDSVersion`, and exactly one root `README`. Record `DatasetType`, `License`, `Authors` or `CITATION.cff`, `DatasetDOI`, `HEDVersion`, `GeneratedBy`, `SourceDatasets`, and `DatasetLinks` when present. `GeneratedBy` and `SourceDatasets` may show that a nominally raw dataset has conversion or processing history, but their absence cannot prove that no prior processing occurred. [[S01]](evidence-register.md#s01) [[S23]](evidence-register.md#s23)

Classify acquisition history as `known`, `partial`, or `unknown`, and cite the files supporting that classification. Do not reverse-engineer amplifier, online reference, hardware filters, or previous cleaning from the samples. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03)

## Recording-level facts

For each recording, record the complete entity path and accepted EEG format bundle. Resolve applicable JSON from the root downward before checking `TaskName`, `EEGReference`, `SamplingFrequency`, `PowerLineFrequency`, and `SoftwareFilters`; retain field-level sources and overrides. Then record duration, channel counts, hardware filters, recording type, and manufacturer metadata when present. [[S01]](evidence-register.md#s01) [[S02]](evidence-register.md#s02)

From `channels.tsv`, retain channel name, type, unit, sampling frequency, low/high cutoff, reference, status, and status description. Do not replace a missing unit, type, cutoff, or reference with a tool default without labeling the substitution as a new assumption. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03)

From `electrodes.tsv` and `coordsystem.json`, retain electrode identity, coordinates, units, coordinate system, fiducials, and coordinate provenance. Channels are signal streams and electrodes are physical contacts, so do not assume a one-to-one mapping for bipolar or derived channels. [[S01]](evidence-register.md#s01)

For source imaging only, also inventory candidate T1w images and sidecars, defacing state, anatomical landmarks, released reconstruction/surface/segmentation roots, and existing head-to-MRI transforms or head-model assets. Do not treat any single one of those as a complete forward model. [[S01]](evidence-register.md#s01) [[S34]](evidence-register.md#s34)

From `events.tsv`/JSON and annotations, retain onset, duration, trial type, response, stimulus identifiers, value mappings, and missing-value encodings. Software can map annotations to sample indices, but experimental meaning must be supplied by the dataset protocol. [[S01]](evidence-register.md#s01) [[S29]](evidence-register.md#s29)

## Conflict handling

Apply BIDS inheritance mechanically: select the applicable simple metadata file lowest in the hierarchy, merge JSON from the root downward, and let lower keys override upper keys. Preserve every override with its source path; legal precedence determines the effective representation, not which value is historically true. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03)

Stop if a conflict affects units, channel type, sampling frequency, reference, coordinate frame, or event semantics and no defensible resolution is available. Those quantities define the interpretation of amplitudes, topology, timing, or conditions. [[S01]](evidence-register.md#s01) [[S08]](evidence-register.md#s08)

## BIDS established-tool inspection

When BIDS conformance is part of the current phase, select the official BIDS Validator and preserve its version, schema/specification target, command, configuration, JSON result, and dataset commit or snapshot. Use its Git-ref/annex options when the active release exposes them instead of teaching local placeholder conventions as BIDS behavior. [[S01]](evidence-register.md#s01) [[S37]](evidence-register.md#s37) [[S47]](evidence-register.md#s47)

Use PyBIDS for in-memory indexing, entity queries, inherited JSON metadata, raw/derivative scopes, and subject-matched anatomy discovery. Use MNE-BIDS for the selected EEG recording with `preload=False`, then compare applied channel/event/coordinate metadata and warnings with the source sidecars. [[S01]](evidence-register.md#s01) [[S26]](evidence-register.md#s26) [[S48]](evidence-register.md#s48)

Use EEG-BIDS for the MATLAB/EEGLAB view and write its generated STUDY outside the source archive. Use native git-annex commands in a configured repository to establish object availability; neither a work-tree suffix nor parser success proves that content is materialized. [[S25]](evidence-register.md#s25) [[S37]](evidence-register.md#s37)

Follow [tool-recipes-bids.md](tool-recipes-bids.md) for commands and role boundaries. No project-specific BIDS parser replaces these maintained tools. A metadata inventory remains only the first intake pass; inspect the acquisition paper/protocol and transformation code when the endpoint depends on facts not represented in BIDS. [[S03]](evidence-register.md#s03) [[S06]](evidence-register.md#s06) [[S47]](evidence-register.md#s47) [[S48]](evidence-register.md#s48)

## Non-BIDS established-tool inspection

Select established tools by phase intent, container, dataset ecosystem, required metadata fidelity, side effects, and downstream representation; constrain them to one explicit recording, disable preloading or sample retrieval where supported, and inspect exact companion metadata separately. A library parser supplies observations, while the adaptation record supplies version-matched meaning. [[S03]](evidence-register.md#s03) [[S42]](evidence-register.md#s42) [[S43]](evidence-register.md#s43)

Use MNE-Python for lazy EDF/GDF/EEGLAB reads and annotations, PyEDFlib when the native EDF per-signal header must be preserved, SciPy for MAT v4–v7.2, and the MNE `hdf5` extra's pymatreader route for MATLAB v7.3 when MATLAB is unavailable. Use EEGLAB for a validated MATLAB/BIOSIG import route. Consult EEGDash, MOABB, TorchEEG, Braindecode, and PyHealth before writing a new adapter, but audit their versioned assumptions and write/cache behavior against the local release before execution. Braindecode and PyHealth belong after the read-only intake gate when their preprocessing, task, windowing, processor, or model-ready cache machinery is needed. [[S24]](evidence-register.md#s24) [[S31]](evidence-register.md#s31) [[S43]](evidence-register.md#s43) [[S44]](evidence-register.md#s44) [[S45]](evidence-register.md#s45) [[S46]](evidence-register.md#s46) [[S49]](evidence-register.md#s49) [[S52]](evidence-register.md#s52) [[S53]](evidence-register.md#s53)

Never generalize one adapter's path grammar, event dictionary, channel roles, label map, or partition semantics to an arbitrary release. Resolve semantic blockers in the cited adaptation record and keep any dataset-specific code in a reviewed adapter with bounded tests. [[S03]](evidence-register.md#s03) [[S43]](evidence-register.md#s43) [[S44]](evidence-register.md#s44)
