# Non-BIDS EEG intake

Use this workflow for EDF/EDF+, GDF, MAT, CNT, EEGLAB, or project-specific layouts that do not satisfy a BIDS contract. A non-BIDS source is usable when the evidence bundle is sufficient for the intended endpoint; format readability alone is not that evidence. [[S03]](evidence-register.md#s03) [[S42]](evidence-register.md#s42) [[S43]](evidence-register.md#s43)

## Contents

- [Documentation recovery is required](#documentation-recovery-is-required)
- [Sufficiency gate](#sufficiency-gate)
- [Established-tool inspection](#established-tool-inspection)
- [Generic adaptation record](#generic-adaptation-record)
- [TorchEEG as a discovery lead](#torcheeg-as-a-discovery-lead)
- [Braindecode and PyHealth as executable pipelines](#braindecode-and-pyhealth-as-executable-pipelines)
- [BCI Competition IV 2a](#bci-competition-iv-2a)
- [SEED](#seed)
- [TUH EEG Corpus](#tuh-eeg-corpus)
- [TUH Abnormal EEG Corpus](#tuh-abnormal-eeg-corpus)
- [Endpoint-specific decisions](#endpoint-specific-decisions)
- [Stop and continue rules](#stop-and-continue-rules)

## Documentation recovery is required

Do not require the user to attach a manual before beginning intake. Search actively for the dataset publisher's official landing page, versioned release notes or README, data descriptor, primary acquisition paper, errata, label dictionary, conversion code, and the applicable container specification. Prefer official/versioned records and primary papers; use a secondary source only as a labeled lead or when no primary record survives. [[S03]](evidence-register.md#s03) [[S06]](evidence-register.md#s06)

Search by dataset name plus version, identifier, filename token, and unresolved field. Resolve papers to DOI/PubMed or the publisher record, preserve the accessed version/date, and record contradictory sources instead of choosing the most convenient value. [[S03]](evidence-register.md#s03) [[S06]](evidence-register.md#s06)

Inspect local `README`, release notes, spreadsheets, codebooks, scripts, and paper supplements even when no attachment was supplied. Treat those files as release artifacts, record their paths and hashes when practical, and distinguish them from facts inferred by a software reader. [[S05]](evidence-register.md#s05) [[S06]](evidence-register.md#s06)

If documentation remains incomplete, continue with bounded container inspection and produce an evidence-gap report. Stop only the transformations or interpretations that depend on the missing fact; do not turn “no attachment” into “no work.” [[S03]](evidence-register.md#s03) [[S42]](evidence-register.md#s42) [[S43]](evidence-register.md#s43)

Record at least these search fields in the Data Intake Report:

- `query_or_route`, `service_or_site`, `accessed_at`, and `result_url`; these make the evidence search auditable. [[S05]](evidence-register.md#s05) [[S06]](evidence-register.md#s06)
- `dataset_version_supported`, `claim_supported`, and `limits`; a relevant paper can describe another release and must not silently override the selected archive. [[S03]](evidence-register.md#s03) [[S40]](evidence-register.md#s40)
- `conflicts` and `unresolved_fields`; missing or contradictory acquisition facts remain explicit rather than becoming defaults. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03)

## Sufficiency gate

Build an evidence bundle from three separately labeled layers: `container_observation`, `release_artifact`, and `external_protocol`. A reader-generated type or name belongs to the first layer and cannot replace a documented role or event meaning from the other two. [[S03]](evidence-register.md#s03) [[S42]](evidence-register.md#s42) [[S43]](evidence-register.md#s43)

For every selected recording, require or mark unknown: [[S03]](evidence-register.md#s03)

- stable dataset version, subject/session/recording identity, and partition membership; identity ambiguity blocks grouping and leakage control. [[S20]](evidence-register.md#s20) [[S22]](evidence-register.md#s22)
- product stage (`acquisition`, `preprocessed samples`, `epoched/segmented samples`, or `features`) and known transformations; later products cannot recover discarded source information. [[S03]](evidence-register.md#s03) [[S33]](evidence-register.md#s33) [[S39]](evidence-register.md#s39)
- array axes, per-signal sampling, physical units, channel roles, reference, filters, and geometry source; these define amplitude, time, and spatial interpretation. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03) [[S42]](evidence-register.md#s42)
- event or label dictionary, alignment rule, missing-value/boundary encoding, artifact annotations, and trial exclusions; a numeric code without the protocol is not an experimental condition. [[S03]](evidence-register.md#s03) [[S29]](evidence-register.md#s29) [[S38]](evidence-register.md#s38)
- generalization unit and publisher partition contract; adaptive processing stays inside the training side of the intended evaluation. [[S20]](evidence-register.md#s20) [[S21]](evidence-register.md#s21) [[S22]](evidence-register.md#s22)

Declare the bundle `sufficient_for:<endpoint>` rather than globally sufficient. Unknown physical units can block amplitude comparisons while still allowing a carefully defined within-recording scale-invariant analysis; absent geometry blocks spatial interpolation/source modeling without necessarily blocking temporal inspection. [[S03]](evidence-register.md#s03) [[S07]](evidence-register.md#s07) [[S34]](evidence-register.md#s34)

## Established-tool inspection

Do not create a catch-all parser that embeds known datasets. Select a maintained tool by container and ecosystem, then constrain it to one explicit recording and exact companion files; avoid recursive enumeration, sample preloading, whole-payload hashing, or source writes during the first pass. These safeguards are especially important for archives such as the 1,643 GB TUH v2.0.1 release. [[S23]](evidence-register.md#s23) [[S40]](evidence-register.md#s40)

Build a candidate set with [toolchain-selection.md](toolchain-selection.md); the following are conditional routes, not a fixed order or a requirement to invoke every framework. Stop at the least observation level that resolves the current field. [[S03]](evidence-register.md#s03) [[S23]](evidence-register.md#s23) [[S44]](evidence-register.md#s44)

- Choose EEGDash when the dataset is indexed and catalogue metadata or its supported cache route serves the current intent; verify any local cache and embedded BIDS metadata rather than trusting catalogue fields alone. [[S31]](evidence-register.md#s31)
- Check MOABB, TorchEEG, Braindecode, and PyHealth registries for versioned dataset adapters; inspect their source as implementation evidence and compare every baked-in assumption with official documentation and local artifacts. Do not construct a training-framework dataset during this read-only pass because construction may retrieve samples, preprocess them, or write metadata and caches. [[S23]](evidence-register.md#s23) [[S44]](evidence-register.md#s44) [[S45]](evidence-register.md#s45) [[S52]](evidence-register.md#s52) [[S53]](evidence-register.md#s53)
- Use MNE-Python with `preload=False` for a selected EDF/GDF/EEGLAB recording and raw annotation inventory; reader types and names remain observations rather than final dataset semantics. [[S26]](evidence-register.md#s26) [[S27]](evidence-register.md#s27) [[S43]](evidence-register.md#s43)
- Use PyEDFlib for the selected EDF when per-signal labels, physical dimensions, prefilter strings, or sampling frequencies must be checked without MNE's normalized representation. [[S42]](evidence-register.md#s42) [[S46]](evidence-register.md#s46)
- Use `scipy.io.whosmat` or MATLAB `whos -file` for a selected MAT file before loading arrays; bind axes, units, labels, and processing stage only from the release contract. [[S03]](evidence-register.md#s03) [[S43]](evidence-register.md#s43)
- Use EEGLAB/BIOSIG when that importer is the release-supported route, and record plugin/toolbox versions plus generated history before any transform. [[S24]](evidence-register.md#s24) [[S25]](evidence-register.md#s25)

The resulting headers, annotations, and array directories intentionally leave semantic blockers because software output does not by itself prove identity, axes, roles, units, label meanings, or processing history. Resolve those fields in the separately cited adaptation record. [[S03]](evidence-register.md#s03) [[S42]](evidence-register.md#s42) [[S43]](evidence-register.md#s43)

Record the script version or repository commit, selected relative path, source size and modification time, exact companion files, and every warning/blocker in the ledger. Run any later sample-level QC on an explicitly selected derivative work area, never inside the source archive. [[S05]](evidence-register.md#s05) [[S23]](evidence-register.md#s23)

## Generic adaptation record

For every unfamiliar release, write a small declarative adaptation record or cited reference page containing: [[S03]](evidence-register.md#s03) [[S06]](evidence-register.md#s06)

- recognized filename/path grammar and the exact subject, session, run, token, and partition fields it carries. [[S20]](evidence-register.md#s20) [[S22]](evidence-register.md#s22)
- expected containers and companion files, plus whether absence is legal, version-specific, or a blocker. [[S03]](evidence-register.md#s03) [[S06]](evidence-register.md#s06)
- channel-label source, role rules, coordinate source, unit source, reference, acquisition filters, and per-signal rate behavior. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03) [[S42]](evidence-register.md#s42)
- event/label source, code dictionary, alignment key, boundary encoding, artifact/exclusion status, and any publisher split. [[S20]](evidence-register.md#s20) [[S29]](evidence-register.md#s29)
- released product stage and transformations already applied, including whether original continuous or raw acquisition data remain available. [[S03]](evidence-register.md#s03) [[S33]](evidence-register.md#s33) [[S39]](evidence-register.md#s39)
- citations, version limits, observed conflicts, and tests against a bounded real recording plus synthetic failure cases. [[S03]](evidence-register.md#s03) [[S06]](evidence-register.md#s06)

Keep parsing and semantics separate. Established libraries can expose an EDF physical dimension, GDF annotation, or MAT shape, while the adaptation record supplies documented meaning and the agent reports a blocker when observation and contract differ. Do not hard-code one dataset's assumptions into a generic tool. [[S03]](evidence-register.md#s03) [[S42]](evidence-register.md#s42) [[S43]](evidence-register.md#s43)

## TorchEEG as a discovery lead

Check the versioned TorchEEG dataset registry when a non-BIDS/apply-to-access dataset may already have an adapter. Its source can reveal concrete hypotheses about expected filenames, array keys, label files, channel counts, windowing, and cache behavior, and its generic folder/CSV/MNE routes can inform a later implementation. [[S44]](evidence-register.md#s44)

Do not treat TorchEEG's baked-in values as primary dataset documentation or transplant them into general tool guidance. Compare every adapter assumption with the selected release's official page, paper, release artifacts, and observed format inventory; record code version and discrepancies. [[S03]](evidence-register.md#s03) [[S44]](evidence-register.md#s44)

Inspect adapter source before instantiation. Dataset construction can load complete arrays, segment samples, transform labels, apply offline transforms, and create an IO cache, so it belongs after read-only intake and must target an authorized derivative/cache directory outside the source archive. [[S23]](evidence-register.md#s23) [[S44]](evidence-register.md#s44)

Use [tool-recipes-torcheeg.md](tool-recipes-torcheeg.md) for the version check, adapter audit, and guarded execution pattern. [[S44]](evidence-register.md#s44)

## Braindecode and PyHealth as executable pipelines

Use Braindecode after intake when an MNE-native dataset needs a maintained MOABB/BIDS wrapper, explicit preprocessing, event- or fixed-window construction, augmentation, or an EEG decoder interface. Use PyHealth after intake when a supported healthcare-signal dataset/task contract and its `BaseDataset` → task → `SampleDataset` cache are appropriate. In both cases, record the exact release and inspect adapter/task source before execution. [[S45]](evidence-register.md#s45) [[S52]](evidence-register.md#s52) [[S53]](evidence-register.md#s53)

Do not treat either framework's preprocessing as neutral loading. Braindecode preprocessors and window builders change the analysis representation; PyHealth EEG tasks can preload EDF, filter, notch, resample, derive bipolar channels, window, normalize, or compute STFT, while `set_task()` fits processors and writes a persistent cache. Declare and validate those operations under the same preprocessing and leakage rules as hand-written code. [[S03]](evidence-register.md#s03) [[S20]](evidence-register.md#s20) [[S52]](evidence-register.md#s52) [[S53]](evidence-register.md#s53)

Do not instantiate PyHealth 2.0.1 TUAB/TUEV adapters against a protected archive for discovery: their version-pinned metadata preparation can attempt writes under the supplied root before using a user-cache fallback. For approved processing, work from a bounded derivative view or copy-on-write mount and declare all explicit and implicit cache locations. [[S23]](evidence-register.md#s23) [[S40]](evidence-register.md#s40) [[S53]](evidence-register.md#s53)

Use [tool-recipes-braindecode-pyhealth.md](tool-recipes-braindecode-pyhealth.md) for environment isolation, forward tests, cache controls, split-sensitive processor fitting, and decoder-interface limits. [[S20]](evidence-register.md#s20) [[S52]](evidence-register.md#s52) [[S53]](evidence-register.md#s53)

## BCI Competition IV 2a

Bind identity from `A<subject><T|E>.gdf`, preserve the training/evaluation role, and expect one GDF file per subject/session. The documented session contains 288 trials, 22 EEG channels followed by three EOG channels, all sampled at 250 Hz. [[S38]](evidence-register.md#s38)

Do not trust the reader's generic names or types for the final role map. Use the documented first-22/last-three channel contract, and obtain electrode positions from a verified montage mapping before interpolation, topography, connectivity over named sites, or source analysis. [[S07]](evidence-register.md#s07) [[S38]](evidence-register.md#s38) [[S43]](evidence-register.md#s43)

Preserve event codes `768` trial start, `769`–`772` class cues, `783` unknown cue, `1023` rejected trial, and `32766` run start. Preserve the 100-missing-sample run boundaries rather than filtering or epoching across them unknowingly. [[S38]](evidence-register.md#s38)

When an official companion `classlabel` vector is present, bind it one-to-one and in order to the 288 trial starts, verify allowed values 1–4, and keep embedded cue events and companion labels as separate source fields. A count mismatch blocks condition analysis. [[S03]](evidence-register.md#s03) [[S38]](evidence-register.md#s38)

Treat the original prohibition on using EOG for classification and the causal-output requirement as benchmark rules when reproducing the competition. For other research endpoints, declare EOG inclusion and causality from the new estimand rather than presenting the competition rule as universal science. [[S03]](evidence-register.md#s03) [[S38]](evidence-register.md#s38)

## SEED

Classify `Preprocessed_EEG` as released, segmented sample data—not raw acquisition. The publisher states that it is already downsampled to 200 Hz, filtered from 0–75 Hz, and split into 15 movie-duration arrays with 62 channel rows. [[S39]](evidence-register.md#s39)

Classify `ExtractedFeatures` as a derivative feature product. Do not apply sample-level filtering, rereferencing, ICA, epoch rejection, or timing analyses to those matrices as though they were continuous EEG samples. [[S03]](evidence-register.md#s03) [[S39]](evidence-register.md#s39)

Read the MAT variable directory before any array. Validate the expected array count and first dimension without loading the large signal matrices, then bind the separately supplied channel-order workbook; MAT shape alone does not name channels. [[S39]](evidence-register.md#s39) [[S43]](evidence-register.md#s43)

Treat 200 Hz, the released passband, channel order, stimulus order, and emotion encoding as external release metadata. If the official page's -1/0/+1 encoding conflicts with a local workbook such as 0/1/2, retain both sources and require an explicit recorded conversion table. [[S03]](evidence-register.md#s03) [[S39]](evidence-register.md#s39)

Do not infer the physical amplitude unit from array magnitude. Until a version-matched source establishes it, block absolute-amplitude thresholds, cross-dataset amplitude comparison, and physical-unit reporting; document whether a scale-invariant endpoint remains defensible. [[S03]](evidence-register.md#s03) [[S39]](evidence-register.md#s39)

## TUH EEG Corpus

Do not assume a local corpus volume. For a new server, use the provider's approved SSH-key/`rsync` route and exact release path after access is granted, preferably as a resumable staging job with a frozen selection manifest and durable completion record. Begin header inspection or preprocessing only after the selected files and release metadata are verified in the protected server-side source root. [[S05]](evidence-register.md#s05) [[S40]](evidence-register.md#s40) [[S50]](evidence-register.md#s50) [[S54]](evidence-register.md#s54)

Never inventory the complete archive merely to inspect one recording. Require an explicit EDF path, read its header only, and use the root versioned README for release identity; TUH v2.0.1 is approximately 1,643 GB and 69.7k EDF files, with an internal README conflict of 69,670 versus 69,672 that must remain visible. [[S03]](evidence-register.md#s03) [[S40]](evidence-register.md#s40)

Parse subject, session directory, configuration directory, and token separately. Do not assume token numbers form a safe continuous recording or reconstruct material pruned before EDF export; treat each EDF independently unless a stronger version-matched contract proves ordering and boundary semantics. [[S40]](evidence-register.md#s40)

Resolve every signal by its label rather than absolute index. Preserve the EDF physical dimension, prefilter text, and samples-per-record for each signal because institutional configurations and per-signal rates vary; auxiliary EKG/ECG, EOG, EMG, respiration, photic, IBI, burst, and suppression streams are not scalp EEG merely because a reader labels them `eeg`. [[S40]](evidence-register.md#s40) [[S42]](evidence-register.md#s42) [[S43]](evidence-register.md#s43)

Interpret `01_tcp_ar`, `02_tcp_le`, `03_tcp_ar_a`, or `04_tcp_le_a` as configuration compatibility. The stored EDF streams are referential; record any later bipolar montage as a new derived transform with its channel equations and rank/channel-state consequences. [[S05]](evidence-register.md#s05) [[S08]](evidence-register.md#s08) [[S40]](evidence-register.md#s40)

Pin the local release even when the public catalogue advances. Do not silently combine counts, headers, labels, or errata from another TUEG version. [[S05]](evidence-register.md#s05) [[S40]](evidence-register.md#s40)

## TUH Abnormal EEG Corpus

Preserve `train`/`eval` and `normal`/`abnormal` from the path as publisher assignments, not new clinical interpretations. TUAB v3.0.1 contains 2,993 selected files, one file per selected session, and does not represent every token or all longitudinal material from TUEG. [[S41]](evidence-register.md#s41)

Keep the official evaluation subjects held out. Within training, split by subject rather than file/session because subjects can have multiple sessions and some training subjects occur under both normal and abnormal release labels. [[S20]](evidence-register.md#s20) [[S22]](evidence-register.md#s22) [[S41]](evidence-register.md#s41)

Fit filtering choices selected from data, normalization, artifact models, feature selection, and model hyperparameters only inside the training side of every evaluation. A fixed causal filter can be applied consistently, but choosing its parameters from held-out outcomes is still adaptive leakage. [[S20]](evidence-register.md#s20) [[S21]](evidence-register.md#s21) [[S22]](evidence-register.md#s22)

Do not generalize the normal/abnormal label beyond the selected released record. The source report can summarize a larger clinical session, while the released annotation and signal segment have their own selection context. [[S03]](evidence-register.md#s03) [[S41]](evidence-register.md#s41)

## Endpoint-specific decisions

For within-dataset BCI decoding, verify trial/label alignment, run/session grouping, artifact policy, causal versus offline endpoint, and train-only fitting before selecting preprocessing. [[S20]](evidence-register.md#s20) [[S21]](evidence-register.md#s21) [[S38]](evidence-register.md#s38)

For cross-session emotion analysis, keep subject and session identities, released preprocessing stage, stimulus order, label conversion, and time-window construction explicit; group evaluation by the intended new-subject or new-session deployment unit. [[S22]](evidence-register.md#s22) [[S39]](evidence-register.md#s39)

For clinical-record classification, preserve subject-level grouping, release selection, per-file channel/rate inventory, auxiliary-channel policy, montage equations, and held-out publisher partitions. Do not treat classification output as clinical interpretation. [[S20]](evidence-register.md#s20) [[S40]](evidence-register.md#s40) [[S41]](evidence-register.md#s41)

For cross-dataset harmonization, compare product stage before signal parameters. Raw acquisition, already filtered/segmented samples, and feature derivatives do not become equivalent through a common resampling or normalization call. [[S03]](evidence-register.md#s03) [[S19]](evidence-register.md#s19) [[S39]](evidence-register.md#s39)

## Stop and continue rules

Continue metadata intake when attachments are absent, a payload is too large, or the source is read-only. Search external documentation, inspect exact local metadata, and read only the selected container header or MAT directory. [[S03]](evidence-register.md#s03) [[S40]](evidence-register.md#s40) [[S43]](evidence-register.md#s43)

Stop event-locked or supervised analysis when condition meaning or label alignment remains unresolved; stop unit-sensitive operations when physical units remain unresolved; stop spatial operations when role/reference/geometry is unresolved; and stop adaptive evaluation when subject/partition grouping is unresolved. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03) [[S20]](evidence-register.md#s20)

Do not stop unrelated work. Return the observed facts, documentation-search log, remaining conflicts, the exact blocked decision, and any narrower endpoint still supported by the evidence bundle. [[S03]](evidence-register.md#s03) [[S05]](evidence-register.md#s05)
