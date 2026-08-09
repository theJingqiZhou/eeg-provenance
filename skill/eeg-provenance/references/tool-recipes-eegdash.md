# EEGDash metadata, bounded acquisition, and QC

Use EEGDash as a catalogue and access layer, not as the owner of OpenNeuro or NeMAR datasets and not as evidence that catalogue fields are correct or that one preprocessing pipeline fits every endpoint. Record the package version, exact query, returned record, provider accession, source dataset identity, cache location, and any disagreement with the loaded object. [[S03]](evidence-register.md#s03) [[S31]](evidence-register.md#s31) [[S51]](evidence-register.md#s51)

## Contents

- [Route the accession before selecting a tool](#route-the-accession-before-selecting-a-tool)
- [Runtime contract](#runtime-contract)
- [Metadata first](#metadata-first)
- [One OpenNeuro recording](#one-openneuro-recording)
- [One NeMAR recording](#one-nemar-recording)
- [Offline QC](#offline-qc)
- [Verified bounded exercise](#verified-bounded-exercise)
- [Stop conditions](#stop-conditions)

## Route the accession before selecting a tool

Recognize `dsNNNNNN` as an OpenNeuro accession and `nmNNNNNN` or `onNNNNNN` as NeMAR accessions. Preserve the supplied string exactly; an `on*` prefix does not authorize guessing or substituting a `ds*` accession, even when the NeMAR record later supplies an OpenNeuro relation. [[S51]](evidence-register.md#s51)

Query provider and EEGDash metadata first, compare version/snapshot, license, source URI, related identifiers, storage backend, and available download methods, then select transport. OpenNeuro can expose browser/S3 or EEGDash retrieval and provider-published Git/DataLad/git-annex routes; NeMAR dataset pages can expose NeMAR CLI, DataLad, git-annex, archive, or manifest/direct-file routes, while EEGDash support depends on the installed release and backend. [[S31]](evidence-register.md#s31) [[S37]](evidence-register.md#s37) [[S51]](evidence-register.md#s51)

Do not construct a repository URL solely from the accession. Use the provider-published URL and pin the declared snapshot, tag, commit, or release before bounded retrieval. [[S05]](evidence-register.md#s05) [[S51]](evidence-register.md#s51)

## Runtime contract

The repository exercised EEGDash 0.8.4 in a dedicated Python 3.12 environment because catalogue, backend, and cache behavior are version-specific software contracts. On a target host, first apply the [runtime compatibility matrix](runtime-compatibility.md): keep a sufficient installed stack, and create a separate site-approved environment only when the selected operation is incompatible. `uv` is not required. [[S31]](evidence-register.md#s31) [[S58]](evidence-register.md#s58) [[S61]](evidence-register.md#s61)

```bash
python -c "import eegdash; print(eegdash.__version__)"
```

## Metadata first

`EEGDash.find()` transfers metadata records but no sample arrays; query those records before constructing a signal-bearing dataset, and retain the raw record rather than copying only selected fields. [[S05]](evidence-register.md#s05) [[S31]](evidence-register.md#s31)

```bash
python scripts/eegdash_intake.py \
  --dataset ds003061 --subject 001 --task P300 --run 1 \
  --catalogue-only
```

The intake command requests at most two records so zero matches and ambiguous filters remain visible. A catalogue outage or schema error is an acquisition failure; do not substitute metadata inferred from filenames or signal samples. [[S03]](evidence-register.md#s03) [[S31]](evidence-register.md#s31)

## One OpenNeuro recording

When EEGDash is selected for an OpenNeuro `ds*` accession, the script constructs the lazy dataset, verifies that the exact subject/task/session/run selectors resolve to one recording, and only then accesses `.raw`; EEGDash stores the BIDS-shaped result under `cache_dir/<dataset_id>`. [[S31]](evidence-register.md#s31)

```bash
python scripts/eegdash_intake.py \
  --dataset ds003061 --subject 001 --task P300 --run 1 \
  --cache-dir .workbench/eegdash-cache --download-one
```

Never set the cache to a source archive, and pass every known source tree through `--protected-source`. Path names, drive letters, and mount points do not prove that a location is protected, writable, durable, or local; establish those properties in the execution preflight. [[S23]](evidence-register.md#s23) [[S31]](evidence-register.md#s31) [[S50]](evidence-register.md#s50)

If provider Git/DataLad access is better suited to partial or remote execution, clone the exact published repository URL and retrieve only the selected recording bundle; a metadata clone alone does not transfer annexed objects. [[S37]](evidence-register.md#s37) [[S51]](evidence-register.md#s51)

```bash
datalad clone "$PUBLISHED_REPOSITORY_URL" .workbench/datasets/dsNNNNNN
datalad get -d .workbench/datasets/dsNNNNNN -- path/to/selected-recording-bundle
```

## One NeMAR recording

The pinned EEGDash 0.8.4 contract identifies both `nm*` and `on*` NeMAR storage as non-fetchable; acquire exact objects into a separate cache through a provider-published NeMAR CLI, DataLad, git-annex, or direct-file route, then use EEGDash offline. Recheck this branch when the installed EEGDash version changes because newer catalogue/backend behavior may differ. [[S31]](evidence-register.md#s31) [[S51]](evidence-register.md#s51)

```bash
git clone https://github.com/nemarDatasets/nm000166.git \
  .workbench/eegdash-cache/nm000166
git -C .workbench/eegdash-cache/nm000166 annex init
git -C .workbench/eegdash-cache/nm000166 annex enableremote nemar-s3
git -C .workbench/eegdash-cache/nm000166 annex get --from nemar-s3 \
  sub-001/ses-01/eeg/sub-001_ses-01_task-aep_eeg.eeg \
  sub-001/ses-01/eeg/sub-001_ses-01_task-aep_eeg.vhdr
```

The `nm000166` commands are a verified worked example, not a URL template for every `nm*` or `on*` accession. Resolve the selected dataset's download methods from its NeMAR record before execution. [[S31]](evidence-register.md#s31) [[S51]](evidence-register.md#s51)

The metadata clone contains BIDS sidecars but annex links do not prove content availability; record `git annex whereis`, the repository commit, the annex key, the content hash, and the exact paths retrieved. [[S05]](evidence-register.md#s05) [[S23]](evidence-register.md#s23) [[S31]](evidence-register.md#s31)

Do not initialize or fetch annex content inside a protected archive during intake. Clone to an authorized cache or ask the archive manager to stage content. [[S23]](evidence-register.md#s23)

## Offline QC

Offline mode bypasses the catalogue, selects one local BIDS recording, hashes its payload and sidecars, and profiles only bounded signal windows. It reports structure, channel types, geometry coverage, annotations, non-finite values, robust amplitude summaries, a sampled numerical rank, and a descriptive line-to-neighbor power ratio without applying pass/fail thresholds. [[S03]](evidence-register.md#s03) [[S17]](evidence-register.md#s17) [[S31]](evidence-register.md#s31)

```bash
python scripts/eegdash_intake.py \
  --dataset ds003061 --subject 001 --task P300 --run 1 \
  --cache-dir .workbench/eegdash-cache --offline-qc

python scripts/eegdash_intake.py \
  --dataset nm000166 --subject 001 --session 01 --task aep \
  --cache-dir .workbench/eegdash-cache --offline-qc
```

Treat the sampled numeric rank and spectral ratio as diagnostics, not claims about covariance rank, source-model rank, artifact status, or scientific acceptability. Endpoint-specific thresholds and adaptive QC rules belong in the Preprocessing Contract and, for prediction, must be fitted within the training partition. [[S03]](evidence-register.md#s03) [[S17]](evidence-register.md#s17) [[S20]](evidence-register.md#s20)

## Verified bounded exercise

These observations were reproduced on 2026-08-08 with EEGDash 0.8.4, MNE 1.12.1, and MNE-BIDS 0.19.0; dataset interpretation comes from the primary dataset records, while numeric values below are local file/QC observations rather than population claims. [[S31]](evidence-register.md#s31) [[S32]](evidence-register.md#s32) [[S33]](evidence-register.md#s33)

| Observation | ds003061 / sub-001 / P300 / run-1 | nm000166 / sub-001 / ses-01 / aep |
|---|---|---|
| Acquisition path | EEGDash anonymous OpenNeuro S3 | NeMAR `nemar-s3` git-annex remote, then EEGDash offline |
| Primary payload | SET, 63,516,912 bytes | BrainVision EEG, 15,104,000 bytes; VHDR, 1,796 bytes |
| SHA-256 | `e07138cd7f7509fe40655691f61df29324f89d40141dae701407fc6cbca8646c` | EEG `b6b3675f6fb43ecbf6579ee6e35f7a5bfada2620dcbcf6c1b1475a99c1021752`; VHDR `2ae20e94c31f194b4cf0262c947c414897868f97f562a9dc1a1261d7705733d3` |
| Loaded shape | 79 channels × 194,048 samples at 256 Hz | 64 channels × 59,000 samples at 250 Hz |
| Channel types | 64 EEG, 2 GSR, 11 misc, 1 respiration, 1 temperature | 64 EEG |
| Events/annotations | 860 annotations across response and auditory-stimulus labels | 59 `stimulus/aep` annotations |
| Geometry | 64/64 EEG channels had finite non-zero positions | 64/64 EEG channels had finite non-zero positions |
| Local metadata conflict | discovery record `nchans=75`, loaded object 79; record channel-name list length 79 | discovery record `ntimes=58,999`, loaded object 59,000 |
| Sampled numeric EEG rank | 64 | 63 |

Evidence: S31–S33.

A 2026-08-09 cross-view with EEGLAB 2026.0.0 and EEG-BIDS 10.5 imported the same ds003061 object as 79 channels × 194,048 samples and preserved all 863 `events.tsv` rows, including three rows whose value was `ignore`; the MNE view above exposed 860 annotations. Treat this as a representation difference to reconcile from the BIDS event table and each reader's mapping, not as evidence that either count is universally correct. The fully parameterized import wrote a SET/FDT/STUDY only to a temporary derivative tree and left the bounded cache inventory unchanged. [[S25]](evidence-register.md#s25) [[S31]](evidence-register.md#s31) [[S32]](evidence-register.md#s32) [[S56]](evidence-register.md#s56)

Preserve the ds003061 identifier disagreement: the tested current S3 `dataset_description.json` embedded `v1.1.2`, while the EEGDash brief displayed `v1.1.0`; bind results to file hashes and retrieval time instead of silently choosing one identifier. [[S05]](evidence-register.md#s05) [[S31]](evidence-register.md#s31) [[S32]](evidence-register.md#s32)

For nm000166, the BIDS field `DatasetType: raw` does not erase the recorded `GeneratedBy` history: the tested tree is a pseudo-continuous conversion of already preprocessed four-second epochs. [[S23]](evidence-register.md#s23) [[S33]](evidence-register.md#s33)

## Stop conditions

Stop before sample retrieval when filters select zero or multiple recordings, the cache overlaps a protected source, the source backend cannot satisfy the requested object, or dataset/catalogue identities conflict without a recorded resolution policy. [[S03]](evidence-register.md#s03) [[S23]](evidence-register.md#s23) [[S31]](evidence-register.md#s31)

Stop before preprocessing when units, channel types, event semantics, prior processing, or temporal adjacency are unresolved in ways that affect the endpoint. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03) [[S33]](evidence-register.md#s33)
