# BIDS 1.11.1 EEG contract

Use this reference when interpreting, validating, or writing BIDS EEG metadata. It is a scoped operational map of the supplied 805-page BIDS 1.11.1 PDF, not a substitute for the full specification or the official BIDS validator. Apply only rules relevant to core dataset structure, EEG, events, coordinates, and derivatives. [[S01]](evidence-register.md#s01) [[S23]](evidence-register.md#s23)

PDF page numbers below are one-based file pages. In the normative chapters, the printed page number is generally one lower.

## Contents

- [Requirement discipline](#requirement-discipline)
- [Source, raw, and derivative boundaries](#source-raw-and-derivative-boundaries)
- [File and metadata encoding](#file-and-metadata-encoding)
- [Inheritance resolution](#inheritance-resolution)
- [Dataset-level intake](#dataset-level-intake)
- [EEG recording bundle](#eeg-recording-bundle)
- [Effective EEG sidecar](#effective-eeg-sidecar)
- [Channels](#channels)
- [Events](#events)
- [Electrodes and coordinates](#electrodes-and-coordinates)
- [Anatomy linkage for EEG source work](#anatomy-linkage-for-eeg-source-work)
- [Derivative outputs](#derivative-outputs)
- [Validation boundary](#validation-boundary)
- [PDF source map](#pdf-source-map)

## Requirement discipline

Preserve the specification’s requirement level in every finding. Report `REQUIRED` failures separately from `RECOMMENDED` omissions and `OPTIONAL` absences; do not promote a recommendation into a conformance requirement or dismiss a required field as “best practice.” [[S01]](evidence-register.md#s01)

Treat BIDS as a representation contract. A conforming filename or sidecar describes how data and metadata are organized; it does not establish that acquisition or preprocessing was scientifically suitable for the intended endpoint. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03)

Record the declared `BIDSVersion`, the validator name/version when one is run, and the version of any library used to resolve inheritance. Never silently interpret a 1.11.1 dataset with rules from an unspecified or moving version. [[S01]](evidence-register.md#s01)

## Source, raw, and derivative boundaries

Distinguish three layers:

- `sourcedata/` contains material before harmonization, reconstruction, or format conversion. Retain it when allowed because conversion can omit acquisition-specific metadata. [[S01]](evidence-register.md#s01)
- Raw BIDS contains unprocessed data or data minimally processed for format conversion. A `DatasetType` of `raw` does not prove that the samples are untouched; inspect `GeneratedBy`, `SourceDatasets`, documentation, and conversion history. [[S01]](evidence-register.md#s01) [[S33]](evidence-register.md#s33)
- Derivatives contain processing outputs and must remain distinguishable from raw data. Protect the source tree and write new outputs to a dedicated derivative dataset or a separate external output root. [[S23]](evidence-register.md#s23)

Do not treat the presence of a `derivatives/` directory as proof that each child is BIDS-compliant. BIDS permits a heterogeneous mixture of standardized and non-compliant derivatives; inspect each derivative dataset’s own root metadata. [[S23]](evidence-register.md#s23)

## File and metadata encoding

Require entity order and entity uniqueness in filenames, preserve case, and reject case-insensitive label collisions. Identify a recording by its complete relative path and entities rather than by basename alone. [[S01]](evidence-register.md#s01)

For plain TSV files, require UTF-8 text, true tab delimiters, a header, non-empty unique column names, dot decimal separators, and `n/a` for missing or non-applicable values. Do not interpret spaces as tabs or empty cells as an undocumented missing-value convention. [[S01]](evidence-register.md#s01)

For `.tsv.gz`, apply it only where the specification permits compressed tabular data, require gzip compression, omit the header row, and obtain column names from the associated JSON `Columns` field. Plain TSV and compressed TSV are not interchangeable. [[S01]](evidence-register.md#s01)

Require JSON key-value files to decode as UTF-8 JSON objects. Preserve exact TSV column spelling when a JSON data dictionary describes a column; otherwise prefer the BIDS CamelCase convention for metadata keys. [[S01]](evidence-register.md#s01)

When a TSV data dictionary is present, use `Description`, `Levels`, `Units`, `Delimiter`, `TermURL`, `HED`, `Minimum`, and `Maximum` according to the represented column. Do not assume that both `Levels` and `Units` apply to the same variable. [[S01]](evidence-register.md#s01)

## Inheritance resolution

Resolve inheritance against a specific target recording before deciding that metadata are missing. A metadata file applies only when it is at the recording’s directory level or above, has the applicable suffix, and contains no entity that is absent or mismatched in the target. [[S01]](evidence-register.md#s01)

At any one directory level, reject multiple metadata files that are simultaneously applicable to the target. For a simple metadata file such as TSV, use only the applicable file lowest in the hierarchy. For JSON, merge applicable objects from the dataset root downward and let a lower value override the same key from above. [[S01]](evidence-register.md#s01)

Record the source path for every effective JSON field and retain each override transition. Absence of a key at a lower level does not unset an inherited key, and a legal override is not evidence that either value describes the original acquisition more accurately. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03)

Keep participant- or session-specific metadata at or below its corresponding directory, and keep metadata intended for multiple participants or sessions outside any single participant/session subtree. Prefer shared metadata over duplication when values are genuinely identical. [[S01]](evidence-register.md#s01)

## Dataset-level intake

Require `dataset_description.json` at every BIDS dataset root. Record at least `Name` and `BIDSVersion`; interpret an omitted `DatasetType` as the backwards-compatible `raw` default, while preserving whether it was explicit or inferred. [[S01]](evidence-register.md#s01)

Record `DatasetLinks`, `License`, `Authors` or `CITATION.cff`, `Keywords`, `EthicsApprovals`, `ReferencesAndLinks`, `DatasetDOI`, `HEDVersion`, `GeneratedBy`, and `SourceDatasets` when present. If `DatasetLinks` is used, reject an empty dataset-name key. [[S01]](evidence-register.md#s01)

Require exactly one root `README`, allowing no extension or `.md`, `.rst`, or `.txt`. Treat `participants.tsv` as recommended; when present, require `participant_id` first, exactly one unique row per participant, and coverage of every subject directory. [[S01]](evidence-register.md#s01)

For multi-session data, inspect each subject’s optional sessions table and require `session_id` first when the file exists. Inspect scans tables for acquisition time and file-level facts without using timestamps to infer missing experimental semantics. [[S01]](evidence-register.md#s01)

## EEG recording bundle

Require the raw EEG recording under `sub-<label>/[ses-<label>/]eeg/` with a `task-<label>` entity and `_eeg` suffix. Accept only these primary storage contracts: EDF (`.edf`), BrainVision (`.vhdr`, `.vmrk`, `.eeg` triplet), EEGLAB (`.set` with optional `.fdt`), or BioSemi (`.bdf`). Reject uppercase `.EDF` and `.BDF`. [[S01]](evidence-register.md#s01)

Do not duplicate one recording across multiple permitted formats under the same BIDS identity. Treat EDF and BrainVision as the specification’s recommended interchange choices, not as evidence that a conversion is lossless. [[S01]](evidence-register.md#s01)

Classify `RecordingType` from the stored stream: `continuous` is one uninterrupted segment, `epoched` contains equal-length segments separated by gaps, and `discontinuous` contains unequal-length segments. If `epoched`, retain `EpochLength`; never relabel concatenated epochs as original continuous acquisition. [[S01]](evidence-register.md#s01) [[S33]](evidence-register.md#s33)

Keep electrode and channel concepts separate. An electrode is a physical contact; a channel is a digitized signal stream and may be differential, auxiliary, or derived from more than one contact. Reference and ground electrodes commonly are not recorded channels. [[S01]](evidence-register.md#s01)

## Effective EEG sidecar

After inheritance, require these recording metadata fields. [[S01]](evidence-register.md#s01)

- `TaskName` identifies the task represented by `task-<label>`. [[S01]](evidence-register.md#s01)
- `EEGReference` describes the acquisition reference generally; put channel-specific references in `channels.tsv`. [[S01]](evidence-register.md#s01)
- `SamplingFrequency` is the main positive sampling rate in hertz; record per-channel deviations in `channels.tsv`. [[S01]](evidence-register.md#s01)
- `PowerLineFrequency` is the local grid frequency or `n/a`. Do not substitute a geographically likely value. [[S01]](evidence-register.md#s01)
- `SoftwareFilters` is an object describing applied temporal software filters or `n/a` when unavailable. Do not convert absence into “no filtering.” [[S01]](evidence-register.md#s01)

Retain the recommended acquisition context when present: cap manufacturer/model, channel counts by type, recording duration/type, ground, head circumference, placement scheme, hardware filters, subject artifact description, device manufacturer/model/software/serial pseudonym, task description/instructions, and institution fields. [[S01]](evidence-register.md#s01)

Use `HardwareFilters: "n/a"` when unavailable and a structured filter object when known. Distinguish unknown filter history from an explicitly documented absence of an optional filter; neither state can be reconstructed from the samples alone. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03)

## Channels

Treat `channels.tsv` as recommended but high-value intake evidence. Require its first three columns to be `name`, `type`, and `units`; require unique names and the uppercase controlled channel-type vocabulary. Preserve row order because it should match the signal-file channel order. [[S01]](evidence-register.md#s01)

Retain `sampling_frequency`, `reference`, `low_cutoff`, `high_cutoff`, `notch`, `status`, and `status_description` when present. Interpret `status` as observed data quality, not as authorization to drop a channel; retain the reason for each `bad` state. [[S01]](evidence-register.md#s01)

Put sensor positions in `electrodes.tsv`, not `channels.tsv`. Do not require one-to-one equality between channel and electrode rows, especially for bipolar EOG/EMG channels, reference/ground contacts, and auxiliary devices. [[S01]](evidence-register.md#s01)

## Events

When `events.tsv` exists, require at least one corresponding data file and one row per event. Require `onset` first and `duration` second; measure both in seconds relative to the first stored sample, allow negative onsets, allow `n/a` for unknown values, and reject negative durations. [[S01]](evidence-register.md#s01)

Preserve overlapping events and long-duration blocks. Sort rows by onset as recommended and retain enough decimal precision for the acquisition rate rather than rounding high-rate EEG timing prematurely. [[S01]](evidence-register.md#s01)

Document `trial_type` and arbitrary additional columns in `events.json`. If one event refers to multiple channels, require the JSON description of `channel` to declare its `Delimiter`; do not split a channel name on an undeclared character. [[S01]](evidence-register.md#s01)

Treat event codes, annotations, HED tags, and stimulus paths as representations requiring protocol interpretation. A valid `onset` and `duration` do not establish the scientific meaning of a condition or response. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03)

## Electrodes and coordinates

When `electrodes.tsv` exists, require `name`, `x`, `y`, and `z` as the first four columns with unique electrode names. Interpret coordinates only through an applicable `coordsystem.json`; the latter is required whenever electrodes are supplied. [[S01]](evidence-register.md#s01)

Require `EEGCoordinateSystem` and `EEGCoordinateUnits`, limiting units to `m`, `mm`, `cm`, or `n/a`. If the system is `Other`, require `EEGCoordinateSystemDescription`. Retain fiducial and anatomical-landmark coordinates, units, systems, and descriptions separately. [[S01]](evidence-register.md#s01)

Use inheritance rather than duplicating electrode/coordinate files for each run. If electrodes were repositioned, prefer separate sessions; when multiple `space-<label>` representations exist, preserve them as distinct candidates and require the analysis contract to select one explicitly. [[S01]](evidence-register.md#s01)

Treat landmark photos as potentially identifying. Do not copy them into reports or derivatives without checking consent and deidentification requirements. [[S01]](evidence-register.md#s01)

## Anatomy linkage for EEG source work

For an individualized forward-model plan, inventory the applicable `sub-<label>/[ses-<label>/]anat/*_T1w.nii[.gz]` candidates and their JSON sidecars. Select among session, acquisition, reconstruction, run, and echo variants explicitly; BIDS-valid anatomy is not automatically the anatomy appropriate to a particular EEG session or head model. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03)

Retain `AnatomicalLandmarkCoordinates` from a T1w sidecar and interpret them as voxel indices in that image, starting at `[0, 0, 0]`. Keep those MRI landmarks distinct from EEG electrode coordinates and from the fitted head-to-MRI transform used by analysis software. [[S01]](evidence-register.md#s01) [[S34]](evidence-register.md#s34)

Record defacing or other deidentification metadata and inspect an optional defacing mask when published. Do not assume that a defaced T1w remains suitable for every scalp-surface or coregistration method; make usability a documented QC result for the selected tool and anatomy rather than a BIDS conformance claim. [[S01]](evidence-register.md#s01) [[S34]](evidence-register.md#s34)

Search each derivative dataset independently for released reconstructions, surfaces, segmentations, transforms, BEM solutions, or volumetric meshes. A FreeSurfer-style `subjects/sub-*/mri` and `surf` tree is useful tool input but is not automatically a standardized BIDS derivative. Use [anatomy-forward-model.md](anatomy-forward-model.md) for the complete readiness and provenance checklist. [[S23]](evidence-register.md#s23) [[S35]](evidence-register.md#s35)

## Derivative outputs

Claim BIDS Derivatives compatibility only when the derivative root has its own `dataset_description.json`, `DatasetType` is `derivative`, and `GeneratedBy` is a non-empty array whose entries contain `Name`. Record `SourceDatasets` and `DatasetLinks` when linking source datasets through BIDS URIs. [[S23]](evidence-register.md#s23)

Name a derivative from the complete relevant source entities, omit the source suffix/extension, and add entities such as `desc-<label>` so a processed output cannot collide with a permissible raw filename. A time-domain filtered EEG output can retain the `_eeg` suffix when the data type remains EEG. [[S23]](evidence-register.md#s23)

For every derivative sidecar, propagate required source metadata that remain valid after processing and remove fields made invalid by the transform. Record direct inputs in `Sources` using BIDS URIs; do not use the deprecated `RawSources` field for new outputs. [[S23]](evidence-register.md#s23)

Use `Sources` for immediate inputs rather than flattening the entire ancestry: in an A→B→C chain, C names B and B names A unless A also directly contributes to C. Keep the project provenance ledger for activity parameters, fit scope, seeds, channel/rank transitions, QC, hashes, and limitations that BIDS file-level metadata does not fully represent. [[S05]](evidence-register.md#s05) [[S23]](evidence-register.md#s23)

## Validation boundary

Run the official BIDS Validator for conformance and record its version, schema target, configuration, warnings, and complete result. Use PyBIDS for entity/inheritance queries, MNE-BIDS for a lazy EEG-aware view, and EEG-BIDS for a MATLAB/EEGLAB cross-check when needed; none replaces the others or establishes scientific validity. [[S01]](evidence-register.md#s01) [[S25]](evidence-register.md#s25) [[S26]](evidence-register.md#s26) [[S47]](evidence-register.md#s47) [[S48]](evidence-register.md#s48)

Preserve validator failures and warnings in the Data Intake Report. Do not “repair” a protected source tree during intake; plan corrections as a new curated dataset or derivative with explicit source identities. [[S01]](evidence-register.md#s01) [[S23]](evidence-register.md#s23)

## PDF source map

| Topic | BIDS 1.11.1 PDF pages |
|---|---:|
| Definitions, filesystem, filenames, source/raw/derived | 47–53 |
| TSV, JSON, and inheritance | 54–60 |
| Dataset description and derivative root provenance | 65–70 |
| Participants, sessions, scans, and events | 72–89 |
| MRI anatomy, landmarks, T1w, and defacing | 110–120 |
| EEG recording formats and EEG JSON | 185–192 |
| Channels | 193–196 |
| Electrodes, coordinates, and landmark photos | 197–203 |
| Stable BIDS Derivatives conventions | 365–372 |
