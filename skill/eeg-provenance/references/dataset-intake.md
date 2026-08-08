# Dataset intake

Use this checklist before opening the signal payload. BIDS metadata is evidence about acquisition and representation, but missing metadata remains unknown and parsing success does not establish scientific validity. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03) [[S26]](evidence-register.md#s26)

## Read-only boundary

- Resolve and record the dataset root, dataset identifier, version/commit, source URL or archive location, recording entities, and source-file hashes when available. Rich identifiers and provenance make reuse and change detection more reliable. [[S05]](evidence-register.md#s05) [[S06]](evidence-register.md#s06)
- Treat a raw BIDS tree or data archive as immutable. Put derivatives, EEGLAB STUDY files, reports, caches, and temporary files elsewhere. [[S23]](evidence-register.md#s23) [[S25]](evidence-register.md#s25)
- Do not run `git annex get`, `unlock`, `drop`, `sync`, or `adjust` during intake. Object availability is an archive-management fact, not permission to change annex state; this prohibition is local policy protecting the source/derivative boundary. [[S05]](evidence-register.md#s05) [[S23]](evidence-register.md#s23)

## Dataset-level facts

Record `Name`, `BIDSVersion`, `DatasetType`, `License`, `Authors`, `DatasetDOI`, `GeneratedBy`, `SourceDatasets`, and `DatasetLinks` when present. `GeneratedBy` and `SourceDatasets` may show that the dataset is already a derivative, but absence of those fields cannot prove that no prior processing occurred. [[S01]](evidence-register.md#s01) [[S23]](evidence-register.md#s23)

Classify acquisition history as `known`, `partial`, or `unknown`, and cite the files supporting that classification. Do not reverse-engineer amplifier, online reference, hardware filters, or previous cleaning from the samples. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03)

## Recording-level facts

For each recording, record the raw format and associated files, sampling frequency, duration, channel count, EEG reference, power-line frequency, hardware/software filters, recording type, and manufacturer metadata when present. These fields are part of the EEG-BIDS sidecar model and are necessary context for later transforms. [[S01]](evidence-register.md#s01) [[S02]](evidence-register.md#s02)

From `channels.tsv`, retain channel name, type, unit, sampling frequency, low/high cutoff, reference, status, and status description. Do not replace a missing unit, type, cutoff, or reference with a tool default without labeling the substitution as a new assumption. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03)

From `electrodes.tsv` and `coordsystem.json`, retain electrode identity, coordinates, units, coordinate system, fiducials, and coordinate provenance. Channels are signal streams and electrodes are physical contacts, so do not assume a one-to-one mapping for bipolar or derived channels. [[S01]](evidence-register.md#s01)

From `events.tsv`/JSON and annotations, retain onset, duration, trial type, response, stimulus identifiers, value mappings, and missing-value encodings. Software can map annotations to sample indices, but experimental meaning must be supplied by the dataset protocol. [[S01]](evidence-register.md#s01) [[S29]](evidence-register.md#s29)

## Conflict handling

Use this precedence only as a reporting strategy, not as a claim that one file is true: preserve every conflicting value, identify its source and inheritance level, select the value used by the contract, and explain why. BIDS inheritance and sidecars organize metadata, while COBIDAS requires transparent reporting of analysis inputs and deviations. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03)

Stop if a conflict affects units, channel type, sampling frequency, reference, coordinate frame, or event semantics and no defensible resolution is available. Those quantities define the interpretation of amplitudes, topology, timing, or conditions. [[S01]](evidence-register.md#s01) [[S08]](evidence-register.md#s08)

## Read-only inspector

Run the inspector against a BIDS dataset root. It reads JSON/TSV metadata and prints JSON to stdout; it never follows annex links or writes into the dataset. [[S01]](evidence-register.md#s01) [[S23]](evidence-register.md#s23)

```bash
python scripts/inspect_bids_metadata.py /path/to/dataset
python scripts/inspect_bids_metadata.py /path/to/dataset --recording sub-001/eeg/sub-001_task-P300_run-1_eeg
```

Record the inspector version or repository commit in the ledger. A metadata inventory is only the first intake pass; inspect the acquisition paper/protocol and any transformation code when the endpoint depends on facts not represented in BIDS. [[S03]](evidence-register.md#s03) [[S06]](evidence-register.md#s06)
