# BIDS inspection with maintained tools

Use the official Validator, PyBIDS, MNE-BIDS, and EEG-BIDS as complementary contracts. No one tool establishes both conformance and scientific sufficiency. [[S01]](evidence-register.md#s01) [[S25]](evidence-register.md#s25) [[S26]](evidence-register.md#s26) [[S47]](evidence-register.md#s47) [[S48]](evidence-register.md#s48)

## 1. Pin and run the official Validator

```bash
bids-validator-deno --version
bids-validator-deno /path/to/dataset \
  --schema https://raw.githubusercontent.com/bids-standard/bids-schema/34d59276aa8f34d3e3b2f17723183b5c7ecc1efb/versions/1.11.1/schema.json \
  --format json_pp
```

The pinned validation environment installs the official 2.2.9 wheel as `bids-validator-deno`; a direct Deno/JSR installation may use `bids-validator`. Pin the dereferenced official 1.11.1 schema by immutable commit URL because the binary release predates the pinned specification PDF and treats a bare `1.11.1` value as an invalid URL despite its help text. Capture stdout outside the source dataset together with the command, validator version, `--help` capability set, schema URL/hash, dataset commit or snapshot, and any severity configuration. Do not suppress warnings in the durable intake record. [[S01]](evidence-register.md#s01) [[S05]](evidence-register.md#s05) [[S47]](evidence-register.md#s47)

For a configured annex repository, first establish work-tree/object availability with native git-annex commands. The exercised 2.2.9 binary accepts experimental `--preferredRemote` but does not expose the newer `--git-ref` option shown by latest documentation; inspect the actual CLI before using version-dependent examples. [[S37]](evidence-register.md#s37) [[S47]](evidence-register.md#s47)

Do not reinterpret `.lnk`, a filesystem placeholder, or a network-mount convention as a BIDS or git-annex standard. If the validator runtime cannot read the selected mount under its filesystem permissions, use a verified supported staging/view route and record that environment limitation; do not copy source data merely to hide unavailable annex objects. [[S37]](evidence-register.md#s37) [[S47]](evidence-register.md#s47)

Validator success is the conformance result for the selected tool/schema, not evidence that acquisition metadata are historically true or preprocessing is appropriate. Carry all warnings and scientific unknowns into the Data Intake Report. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03) [[S47]](evidence-register.md#s47)

## 2. Query entities and inherited metadata with PyBIDS

```python
from bids import BIDSLayout

layout = BIDSLayout(
    dataset_root,
    validate=False,          # official Validator already ran
    config="bids-schema",
    derivatives=True,
)

eeg_files = layout.get(
    datatype="eeg",
    suffix="eeg",
    return_type="filename",
    scope="raw",
)
selected = eeg_files[0]      # replace with explicit entities
effective_metadata = layout.get_metadata(selected)
entities = layout.parse_file_entities(selected)
```

Select a recording by explicit subject/session/task/acquisition/run entities rather than list position. `get_metadata` supplies effective inherited JSON; separately retain the applicable sidecar paths and overrides when field-source provenance matters. [[S01]](evidence-register.md#s01) [[S05]](evidence-register.md#s05) [[S48]](evidence-register.md#s48)

Keep the PyBIDS index in memory during read-only intake. If a persistent `database_path` is needed for scale, put it in a cache/derivative location outside the immutable dataset. [[S23]](evidence-register.md#s23) [[S48]](evidence-register.md#s48)

Query candidate raw anatomy by the same subject/session identity:

```python
t1w = layout.get(
    subject=entities.get("subject"),
    session=entities.get("session"),
    suffix="T1w",
    extension=["nii", "nii.gz"],
    return_type="filename",
    scope="raw",
)
```

Query derivative scopes separately and inspect each derivative `dataset_description.json`. A T1w path, FreeSurfer subject tree, transform, surfaces, and BEM/FEM solution remain distinct readiness facts; follow [anatomy-forward-model.md](anatomy-forward-model.md). [[S23]](evidence-register.md#s23) [[S34]](evidence-register.md#s34) [[S35]](evidence-register.md#s35) [[S48]](evidence-register.md#s48)

## 3. Read one EEG recording with MNE-BIDS

```python
from mne_bids import get_bids_path_from_fname, read_raw_bids

bids_path = get_bids_path_from_fname(selected, check=True)
raw = read_raw_bids(
    bids_path,
    extra_params={"preload": False},
    on_ch_mismatch="raise",
    verbose=False,
)
```

Record warnings and compare `raw.info`, bad channels, coordinates, and annotations with the PyBIDS metadata and source TSV/JSON files. MNE-BIDS maps supported BIDS fields into MNE but does not preserve every custom column or validate experimental meaning. [[S01]](evidence-register.md#s01) [[S26]](evidence-register.md#s26) [[S29]](evidence-register.md#s29)

Do not call `load_data`, plotting that forces samples, filtering, resampling, or export during metadata-only intake. Authorize sample reads only after the Preprocessing Contract defines the endpoint and derivative destination. [[S03]](evidence-register.md#s03) [[S23]](evidence-register.md#s23) [[S27]](evidence-register.md#s27)

## 4. Cross-check the MATLAB/EEGLAB view

Use EEG-BIDS `pop_importbids` when the MATLAB/EEGLAB representation is required. Select an output directory outside the BIDS source tree, record EEGLAB and plugin versions, and compare imported events/channel locations with the Python view before processing. [[S24]](evidence-register.md#s24) [[S25]](evidence-register.md#s25)

Do not use agreement between two readers as proof of historical truth: both may consume the same incomplete sidecars. Return unresolved acquisition or conversion history as a limitation and inspect the dataset paper/conversion code. [[S03]](evidence-register.md#s03) [[S06]](evidence-register.md#s06)
