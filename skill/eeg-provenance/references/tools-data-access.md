# Data access and metadata implementations

Use this reference for Resolve/Acquire and catalogue, tree, sidecar, conformance,
or native-header inspection. It describes implementation differences; obtain
the active operation and gates from `pipeline.md` before choosing a tool.
[[S03]](evidence-register.md#s03) [[S23]](evidence-register.md#s23)

## Contents

- [Choose by observation](#choose-by-observation)
- [Provider identity and transport](#provider-identity-and-transport)
- [EEGDash](#eegdash)
- [BIDS conformance and metadata](#bids-conformance-and-metadata)
- [Native EDF, GDF, and MAT headers](#native-edf-gdf-and-mat-headers)
- [Dataset adapters as acquisition routes](#dataset-adapters-as-acquisition-routes)
- [Access decision record](#access-decision-record)

## Choose by observation

| Need | Prefer | Do not substitute |
|---|---|---|
| Provider/release/access route | Official provider record and versioned release metadata | Filename inference or framework catalogue identity |
| Indexed catalogue metadata | EEGDash `find()` when the installed release covers the source | Signal loading or cache construction |
| Selected public objects | Provider CLI/direct path or published DataLad/git-annex route | A URL synthesized from an accession |
| BIDS conformance | Official BIDS Validator with recorded schema/version | PyBIDS, MNE-BIDS, or EEGLAB reader success |
| BIDS entities/inheritance | PyBIDS plus retained applicable sidecar paths | Validator output alone |
| Exact EDF/BDF per-signal header | PyEDFlib or an equivalent format-native reader | MNE-normalized channel fields |
| MAT directory/version | SciPy `whosmat` for v4–v7.2; HDF5 inventory for v7.3 | Loading arbitrary arrays or assuming `.mat` semantics |
| Evidence | S31, S42, S43, S46–S48 | S26, S49 |

These tools expose different contracts and are complementary, not a quality
ranking. [[S26]](evidence-register.md#s26) [[S31]](evidence-register.md#s31)
[[S42]](evidence-register.md#s42) [[S43]](evidence-register.md#s43)
[[S46]](evidence-register.md#s46) [[S47]](evidence-register.md#s47)
[[S48]](evidence-register.md#s48)

## Provider identity and transport

Treat `dsNNNNNN` as an OpenNeuro routing clue and `nmNNNNNN` or `onNNNNNN` as
NeMAR routing clues. Preserve the supplied ID and resolve the official record,
snapshot/release, DOI, related identifiers, license/access terms, desired
objects, and published download methods before selecting transport. Prefixes do
not establish repository URLs or cross-provider mappings. [[S51]](evidence-register.md#s51)

OpenNeuro can publish CLI, Git, DataLad, git-annex, and object-storage routes;
NeMAR records can expose NeMAR CLI, DataLad, git-annex, archive, manifest, or
direct-file routes. Select the route that passes identity, byte-selection,
authentication, resumability, filesystem, and durability gates on the actual
host. [[S37]](evidence-register.md#s37) [[S50]](evidence-register.md#s50)
[[S51]](evidence-register.md#s51)

For a provider-published DataLad repository, a metadata clone and content
retrieval are separate operations:

```bash
datalad clone "$PUBLISHED_REPOSITORY_URL" /authorized/cache/dataset
datalad get -d /authorized/cache/dataset -- path/to/selected-recording-bundle
```

Record repository commit, annex key/availability, selected paths, content hash,
remote, and retrieval result. Do not fetch, unlock, drop, initialize, or write
indexes in a protected source archive. [[S05]](evidence-register.md#s05)
[[S23]](evidence-register.md#s23) [[S37]](evidence-register.md#s37)

For controlled TUH data, use the current authenticated provider route and its
small test path before a large synchronized transfer. Provider support for
rsync-over-SSH does not prove that a remote host has egress, credentials,
durable storage, or successful restart behavior. Never place credentials in
commands captured by the ledger. [[S50]](evidence-register.md#s50)
[[S54]](evidence-register.md#s54)

## EEGDash

Use EEGDash as a versioned catalogue/cache layer, not the owner of OpenNeuro or
NeMAR datasets. Record package version, raw query/record, provider accession,
cache root, backend, retrieval time, and conflicts with loaded metadata.
`EEGDash.find()` returns metadata records without sample arrays; dataset object
construction and `.raw` access can resolve/download samples into a BIDS-shaped
cache. [[S31]](evidence-register.md#s31) [[S51]](evidence-register.md#s51)

Use the bundled bounded route instead of an unfiltered dataset construction:

```bash
python scripts/eegdash_intake.py \
  --dataset dsNNNNNN --subject LABEL --task TASK --run RUN \
  --catalogue-only

python scripts/eegdash_intake.py \
  --dataset dsNNNNNN --subject LABEL --task TASK --run RUN \
  --cache-dir /authorized/cache --download-one
```

The selectors must resolve exactly one recording before sample access, and the
cache must not overlap any protected source. In EEGDash 0.8.4, OpenNeuro used an
anonymous S3 path while NeMAR backends were marked non-fetchable; for `nm*` or
`on*`, use a provider-published transport into the cache and then the verified
offline route. Re-probe this behavior on another release. [[S23]](evidence-register.md#s23)
[[S31]](evidence-register.md#s31) [[S51]](evidence-register.md#s51)

For a locally complete selected recording, the bundled offline route inventories
payload/sidecar hashes and profiles bounded signal windows without changing the
cache:

```bash
python scripts/eegdash_intake.py \
  --dataset ACCESSION --subject LABEL --task TASK --run RUN \
  --cache-dir /authorized/cache --offline-qc
```

Its non-finite, amplitude, sampled-rank, geometry, annotation, and spectral
summaries are descriptive observations. Set endpoint-specific thresholds in the
operation contract. In predictive work, fit adaptive QC only from the declared
population available before prediction; default to the training fold unless the
deployment protocol explicitly provides calibration or unlabeled record data.
[[S17]](evidence-register.md#s17) [[S20]](evidence-register.md#s20)
[[S31]](evidence-register.md#s31)

Catalogue fields are discovery evidence. Reconcile them with the selected
provider snapshot and embedded files; preserve version, channel-count, or sample
count disagreements rather than silently choosing one. [[S03]](evidence-register.md#s03)
[[S31]](evidence-register.md#s31) [[S32]](evidence-register.md#s32)

## BIDS conformance and metadata

Run the official Validator for conformance, PyBIDS for entity/inheritance
queries, and a BIDS-aware signal reader only when a normalized EEG view is
needed. No reader replaces validator output or establishes historical truth or
scientific suitability. [[S01]](evidence-register.md#s01)
[[S26]](evidence-register.md#s26) [[S47]](evidence-register.md#s47)
[[S48]](evidence-register.md#s48)

In the pinned validation lane, the official 2.2.9 wheel exposed
`bids-validator-deno`; pin the dereferenced BIDS 1.11.1 schema URL/hash because
that binary treated bare `1.11.1` as an invalid schema URL. Inspect `--help`
before copying newer options, and preserve warnings in the report.
[[S47]](evidence-register.md#s47)

```bash
bids-validator-deno --version
bids-validator-deno /path/to/dataset \
  --schema https://raw.githubusercontent.com/bids-standard/bids-schema/34d59276aa8f34d3e3b2f17723183b5c7ecc1efb/versions/1.11.1/schema.json \
  --format json_pp
```

Keep PyBIDS indexes in memory for read-only intake; place any persistent
`database_path` outside the source. Select recordings by explicit entities, not
list position, and retain the paths/override chain when field-source provenance
matters. [[S01]](evidence-register.md#s01) [[S23]](evidence-register.md#s23)
[[S48]](evidence-register.md#s48)

```python
from bids import BIDSLayout

layout = BIDSLayout(dataset_root, validate=False, config="bids-schema")
matches = layout.get(datatype="eeg", suffix="eeg", subject=subject,
                     task=task, run=run, return_type="filename", scope="raw")
if len(matches) != 1:
    raise RuntimeError(f"Expected one recording, found {len(matches)}")
entities = layout.parse_file_entities(matches[0])
effective_metadata = layout.get_metadata(matches[0])
```

Use the scoped [BIDS EEG contract](bids-eeg-1.11.1.md) to interpret the files,
requirements, inheritance, coordinates, and derivative boundary.
[[S01]](evidence-register.md#s01) [[S23]](evidence-register.md#s23)

## Native EDF, GDF, and MAT headers

Use PyEDFlib when exact EDF/BDF header fields such as per-signal labels,
physical dimensions, physical/digital extrema, prefilter strings, and sampling
frequencies must remain visible. MNE's normalized Raw view is a later operation.
Do not recursively inspect a large corpus when one selected token answers the
question. [[S40]](evidence-register.md#s40) [[S42]](evidence-register.md#s42)
[[S46]](evidence-register.md#s46)

For GDF, use a verified lazy format reader and preserve warnings; for MAT v4
through v7.2, use `scipy.io.whosmat` before `loadmat`. SciPy does not implement
MAT v7.3/HDF5, so inventory groups, datasets, shapes, dtypes, and attributes with
`h5py` without indexing values, then use bounded `pymatreader` variable
selection after the release contract identifies variables. An HDF5 hierarchy
does not establish EEG axes, units, labels, or product stage. [[S03]](evidence-register.md#s03)
[[S43]](evidence-register.md#s43) [[S49]](evidence-register.md#s49)

The `mne[hdf5]` extra supplies the supported HDF5-related dependencies for the
pinned MNE lane but does not turn an arbitrary MAT structure into an MNE or
EEGLAB dataset. Apply the runtime matrix before resolving it on a shared host.
[[S49]](evidence-register.md#s49) [[S58]](evidence-register.md#s58)
[[S61]](evidence-register.md#s61)

## Dataset adapters as acquisition routes

MOABB, TorchEEG, Braindecode, and PyHealth can expose datasets or retrieval
helpers, but adapters may encode release assumptions, load samples, transform
signals, fit processors, or create caches during construction. First inspect
the version-pinned adapter source and compare provider, release, selectors,
paths, labels, channels, axes, partitions, and cache behavior with primary
records. Use [framework integrations](tools-frameworks.md) only after this
read-only audit. [[S23]](evidence-register.md#s23)
[[S44]](evidence-register.md#s44) [[S45]](evidence-register.md#s45)
[[S52]](evidence-register.md#s52) [[S53]](evidence-register.md#s53)

## Access decision record

For a non-obvious choice, record candidate tool/version, exact intent and
observation level, source identity, selectors, read/network/write/cache scope,
availability probe, hard-gate result, selected/fallback status, and evidence
IDs. For a one-header request with one safe available reader, the same facts may
be reported in a compact Inspection Finding rather than a multi-candidate
matrix. [[S05]](evidence-register.md#s05) [[S57]](evidence-register.md#s57)
