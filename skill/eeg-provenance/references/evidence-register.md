# Evidence register

This register is the only source namespace used by the skill. “Supports” describes the narrow claim for which a source may be cited; it is not a summary of every conclusion in the source. “Limits” prevents a citation from being generalized beyond its design. URLs and identifiers were checked on 2026-08-08.

## Contents

- [Search and selection protocol](#search-and-selection-protocol)
- [Evidence classes](#evidence-classes)
- [Standards, reporting, and provenance (S01–S06)](#s01)
- [Signal processing and artifacts (S07–S19)](#s07)
- [Validation and leakage (S20–S22)](#s20)
- [Software and dataset contracts (S23–S33)](#s23)

## Search and selection protocol

This is a targeted scoping review for EEG intake, preprocessing decisions, channel/montage harmonization, leakage control, software behavior, dataset-specific provenance, and reproducibility. Searches covered PubMed, Crossref/DOI resolution, BIDS, W3C, MNE, MNE-BIDS, EEGLAB, EEGDash, OpenNeuro, NeMAR, and official project documentation. Representative queries included `EEG-BIDS specification reference electrodes channels`, `COBIDAS MEEG preprocessing reporting`, `EEG filter design artifacts`, `EEG interpolation spherical splines`, `EEG reference rank`, `EEG ICA high-pass`, `EEG preprocessing multiverse decoding`, `EEG cross-validation leakage`, `EEGDash metadata lazy cache`, `OpenNeuro ds003061`, and `NeMAR nm000166 M3CV`.

Include primary methods/results papers, standards, consensus reports, and versioned official software documentation that directly support an in-scope statement. Exclude reviews used only as citation proxies, unversioned tutorials when a stable API/specification is available, clinical interpretation, source localization, model-selection advice, and uncited rules inherited from ClaudeEEG. Deduplicate by DOI or canonical specification URL. Prefer a primary paper for empirical effects and official documentation for current software contracts. Record proposal status explicitly.

Searches were run on 2026-08-08. Dynamic result counts were not used as an eligibility criterion; each retained item was resolved to its DOI or canonical official page, screened against the claim it supports, and deduplicated before receiving one source ID.

| Search group | Sources searched | Exact query or route | Retained IDs |
|---|---|---|---|
| Data model/reporting | BIDS, PubMed, DOI resolver | `EEG-BIDS specification reference electrodes channels`; `COBIDAS MEEG preprocessing reporting` | S01–S03, S23 |
| Provenance/reuse | W3C, DOI resolver | `W3C PROV-O Entity Activity Agent`; `FAIR scientific data provenance` | S05–S06 |
| Reference/geometry | PubMed, DOI resolver | `EEG interpolation spherical splines`; `EEG reference montage rank` | S07–S08 |
| Temporal transforms | PubMed, DOI resolver | `EEG digital filter design artifacts`; `ERP baseline correction regression` | S09–S12 |
| Artifact procedures | PubMed, DOI resolver | `PREP EEG pipeline`; `ICLabel EEG component classifier`; `artifact subspace reconstruction EEG`; `autoreject EEG` | S04, S13, S16–S18 |
| Pipeline sensitivity | PubMed, DOI resolver | `EEG preprocessing multiverse robustness` | S19 |
| Evaluation leakage | PubMed, DOI resolver | `neuroimaging cross-validation caveats`; `EEG temporal autocorrelation cross-validation leakage`; `structured data blocked cross-validation` | S20–S22 |
| Software contracts | MNE, MNE-BIDS, EEGLAB, MathWorks official documentation | Stable API pages and installed-tool routes for the named functions/servers | S14–S15, S24–S30 |
| Dataset access | EEGDash, OpenNeuro, NeMAR, version-pinned source | `EEGDash metadata lazy cache`; dataset pages and source-backend implementation | S31–S33 |

### Evidence classes

| Class | Meaning |
|---|---|
| `HARD_INVARIANT` | Mathematical, physical, or data-model constraint. |
| `CONSENSUS_REPORTING` | Community reporting or interoperability recommendation. |
| `CONDITIONAL_EVIDENCE` | Empirical result whose transfer depends on task, data, or estimator. |
| `EMPIRICAL_BASELINE` | Published procedure useful as a starting point that requires local validation. |
| `SOFTWARE_CONTRACT` | Behavior documented for the named software/specification version. |
| `LOCAL_POLICY` | Conservative project safeguard motivated by cited risk; not external consensus. |

<a id="s01"></a>
## S01 — BIDS EEG specification

- **Type / class:** Standard specification; `HARD_INVARIANT`, `SOFTWARE_CONTRACT`.
- **Source:** BIDS Contributors. *Brain Imaging Data Structure 1.11.1 — Electroencephalography*. [Stable specification](https://bids-specification.readthedocs.io/en/stable/modality-specific-files/electroencephalography.html).
- **Supports:** EEG sidecar requirements; separation of channels from electrodes; channel status, units, reference and filter metadata; electrode coordinates and coordinate-system metadata.
- **Limits:** BIDS describes representation and required/recommended metadata, not the scientific validity of a preprocessing choice. “Stable” can advance; record the dataset and validator versions.

<a id="s02"></a>
## S02 — EEG-BIDS extension paper

- **Type / class:** Consensus data standard paper; `CONSENSUS_REPORTING`.
- **Source:** Pernet CR, et al. EEG-BIDS, an extension to the brain imaging data structure for electroencephalography. *Scientific Data*. 2019;6:103. [doi:10.1038/s41597-019-0104-8](https://doi.org/10.1038/s41597-019-0104-8).
- **Supports:** Standardized organization and metadata improve EEG data sharing and machine readability; EEG-BIDS represents acquisition metadata and events alongside signal files.
- **Limits:** The paper does not prescribe a scientifically optimal preprocessing pipeline.

<a id="s03"></a>
## S03 — COBIDAS-MEEG

- **Type / class:** Community consensus/reporting recommendations; `CONSENSUS_REPORTING`.
- **Source:** Pernet CR, et al. Best practices in data analysis and sharing in neuroimaging using MEEG. *Nature Neuroscience*. 2020;23:1173–1183. [doi:10.1038/s41593-020-00709-0](https://doi.org/10.1038/s41593-020-00709-0).
- **Supports:** Report acquisition, preprocessing, artifact handling, software, parameters, exclusions, and data-sharing details sufficiently for evaluation and reuse; choices depend on the scientific question and data.
- **Limits:** Consensus guidance is not proof that one method is superior for every endpoint.

<a id="s04"></a>
## S04 — PREP pipeline

- **Type / class:** Methods paper; `EMPIRICAL_BASELINE`.
- **Source:** Bigdely-Shamlo N, et al. The PREP pipeline: standardized preprocessing for large-scale EEG analysis. *Frontiers in Neuroinformatics*. 2015;9:16. [doi:10.3389/fninf.2015.00016](https://doi.org/10.3389/fninf.2015.00016).
- **Supports:** A documented robust-reference, line-noise, and bad-channel workflow can serve as a reproducible baseline for large heterogeneous collections.
- **Limits:** PREP’s goals and assumptions do not make it a universal pipeline; validate compatibility with the endpoint, montage, reference, and bandwidth.

<a id="s05"></a>
## S05 — W3C PROV-O

- **Type / class:** W3C Recommendation; `HARD_INVARIANT`, `CONSENSUS_REPORTING`.
- **Source:** Lebo T, Sahoo S, McGuinness D, eds. *PROV-O: The PROV Ontology*. W3C Recommendation, 30 April 2013. [W3C PROV-O](https://www.w3.org/TR/prov-o/).
- **Supports:** Model provenance with entities, activities, and agents and relations such as `used`, `wasGeneratedBy`, and `wasDerivedFrom`.
- **Limits:** The local JSON ledger borrows the conceptual model but is not automatically RDF or PROV-O conformant.

<a id="s06"></a>
## S06 — FAIR principles

- **Type / class:** Principles paper; `CONSENSUS_REPORTING`.
- **Source:** Wilkinson MD, et al. The FAIR Guiding Principles for scientific data management and stewardship. *Scientific Data*. 2016;3:160018. [doi:10.1038/sdata.2016.18](https://doi.org/10.1038/sdata.2016.18).
- **Supports:** Persistent identifiers, rich metadata, provenance, and standard representations improve findability, accessibility, interoperability, and reuse.
- **Limits:** FAIR does not by itself guarantee data quality, reproducibility, openness, or valid scientific inference.

<a id="s07"></a>
## S07 — Spherical-spline interpolation

- **Type / class:** Primary methods paper; `HARD_INVARIANT`, `CONDITIONAL_EVIDENCE`.
- **Source:** Perrin F, Pernier J, Bertrand O, Echallier JF. Spherical splines for scalp potential and current density mapping. *Electroencephalography and Clinical Neurophysiology*. 1989;72(2):184–187. [doi:10.1016/0013-4694(89)90180-6](https://doi.org/10.1016/0013-4694(89)90180-6).
- **Supports:** Spherical-spline scalp interpolation estimates a channel from potentials at other electrode positions under a spatial model.
- **Limits:** Accuracy depends on geometry, spatial sampling, model assumptions, and the unavailable signal; an interpolated channel is not a recovered native measurement.

<a id="s08"></a>
## S08 — EEG reference and rank

- **Type / class:** Methods/theory paper; `HARD_INVARIANT`.
- **Source:** Hu S, et al. How do reference montage and electrodes setup affect the measured scalp EEG potentials? *Brain Topography*. 2019;32:110–128. [doi:10.1007/s10548-019-00706-y](https://doi.org/10.1007/s10548-019-00706-y).
- **Supports:** EEG potentials are reference-dependent; rereferencing is a linear transformation that affects representation and can affect rank and downstream estimates.
- **Limits:** The paper does not make one reference universally optimal; conclusions depend on electrode configuration and analysis target.

<a id="s09"></a>
## S09 — Digital filter design for electrophysiology

- **Type / class:** Methods review/tutorial with simulations; `CONDITIONAL_EVIDENCE`.
- **Source:** Widmann A, Schröger E, Maess B. Digital filter design for electrophysiological data — a practical approach. *Journal of Neuroscience Methods*. 2015;250:34–46. [doi:10.1016/j.jneumeth.2014.08.002](https://doi.org/10.1016/j.jneumeth.2014.08.002).
- **Supports:** Report filter type, cutoff definition, transition bandwidth, order/length, direction/phase, and edge handling; filter design must consider the signal and endpoint.
- **Limits:** Recommended design heuristics are conditional, not guarantees against distortion.

<a id="s10"></a>
## S10 — Filter-induced ERP distortion

- **Type / class:** Simulation/empirical methods paper; `CONDITIONAL_EVIDENCE`.
- **Source:** Acunzo DJ, Mackenzie G, van Rossum MCW. Systematic biases in early ERP and ERF components as a result of high-pass filtering. *Journal of Neuroscience Methods*. 2012;209(1):212–218. [doi:10.1016/j.jneumeth.2012.06.011](https://doi.org/10.1016/j.jneumeth.2012.06.011).
- **Supports:** High-pass filtering can distort transient waveforms and bias component amplitude/latency under some filter and signal conditions.
- **Limits:** The magnitude and direction depend on waveform, cutoff, filter design, and analysis; do not generalize a single safe cutoff.

<a id="s11"></a>
## S11 — Baseline correction as modeling

- **Type / class:** Statistical methods paper; `CONDITIONAL_EVIDENCE`.
- **Source:** Alday PM. How much baseline correction do we need in ERP research? Extended GLM model can replace baseline correction while lifting its limits. *Psychophysiology*. 2019;56(12):e13451. [doi:10.1111/psyp.13451](https://doi.org/10.1111/psyp.13451).
- **Supports:** Conventional baseline subtraction imposes a fixed relationship; regression-based alternatives can model baseline effects more flexibly.
- **Limits:** The alternative still requires design assumptions and validation; it is not always required or superior.

<a id="s12"></a>
## S12 — High-pass filtering and ICA decomposition

- **Type / class:** Empirical methods paper; `CONDITIONAL_EVIDENCE`.
- **Source:** Winkler I, Debener S, Müller KR, Tangermann M. On the influence of high-pass filtering on ICA-based artifact reduction in EEG-ERP. *EMBC 2015*. [doi:10.1109/EMBC.2015.7319296](https://doi.org/10.1109/EMBC.2015.7319296).
- **Supports:** High-pass filtering of ICA training data can improve decomposition/artifact-reduction behavior in the evaluated ERP settings.
- **Limits:** Results do not establish a universal cutoff or justify transferring components across differently transformed channel spaces without checks.

<a id="s13"></a>
## S13 — ICLabel

- **Type / class:** Primary classifier paper; `EMPIRICAL_BASELINE`, `CONDITIONAL_EVIDENCE`.
- **Source:** Pion-Tonachini L, Kreutz-Delgado K, Makeig S. ICLabel: an automated electroencephalographic independent component classifier, dataset, and website. *NeuroImage*. 2019;198:181–197. [doi:10.1016/j.neuroimage.2019.05.026](https://doi.org/10.1016/j.neuroimage.2019.05.026).
- **Supports:** ICLabel provides probabilistic labels for ICA components trained/evaluated on specified data and label classes.
- **Limits:** Labels are model outputs, not ground truth or automatic removal decisions; applicability depends on preprocessing and decomposition compatibility.

<a id="s14"></a>
## S14 — MNE ICA API

- **Type / class:** Official software documentation, MNE 1.12; `SOFTWARE_CONTRACT`.
- **Source:** MNE Developers. `mne.preprocessing.ICA`. [MNE stable API](https://mne.tools/stable/generated/mne.preprocessing.ICA.html).
- **Supports:** Current constructor defaults and fit/apply behavior; MNE documents that high-pass filtering, commonly at 1 Hz, is recommended before ICA fitting and warns about baseline-corrected epochs.
- **Limits:** Documentation describes software behavior and practical guidance, not a universal scientific optimum; record the installed MNE version and actual arguments.

<a id="s15"></a>
## S15 — MNE-ICALabel conditions

- **Type / class:** Official software documentation, MNE-ICALabel 0.8; `SOFTWARE_CONTRACT`.
- **Source:** MNE-ICALabel Developers. `mne_icalabel.iclabel_label_components`. [Stable API](https://mne.tools/mne-icalabel/stable/api/iclabel.html).
- **Supports:** The implementation documents expected compatibility with extended-infomax ICA, average reference, and 1–100 Hz filtering and warns that mismatch can reduce label reliability.
- **Limits:** The documented conditions do not validate component removal for a given endpoint; the documentation notes that preprocessing effects were not systematically tested in the ICLabel paper.

<a id="s16"></a>
## S16 — Artifact Subspace Reconstruction

- **Type / class:** Empirical validation paper; `EMPIRICAL_BASELINE`, `CONDITIONAL_EVIDENCE`.
- **Source:** Chang CY, Hsu SH, Pion-Tonachini L, Jung TP. Evaluation of artifact subspace reconstruction for automatic artifact components removal in multi-channel EEG recordings. *IEEE Transactions on Biomedical Engineering*. 2020;67(4):1114–1121. [doi:10.1109/TBME.2019.2930186](https://doi.org/10.1109/TBME.2019.2930186).
- **Supports:** ASR is a data-adaptive reconstruction method with performance dependent on calibration and threshold settings.
- **Limits:** Evaluated datasets/metrics do not establish a universally safe threshold or preservation of every scientific signal.

<a id="s17"></a>
## S17 — AutoReject

- **Type / class:** Primary methods paper; `EMPIRICAL_BASELINE`, `CONDITIONAL_EVIDENCE`.
- **Source:** Jas M, et al. Autoreject: automated artifact rejection for MEG and EEG data. *NeuroImage*. 2017;159:417–429. [doi:10.1016/j.neuroimage.2017.06.030](https://doi.org/10.1016/j.neuroimage.2017.06.030).
- **Supports:** Cross-validated local/global peak-to-peak thresholds can automate epoch rejection and channel interpolation decisions.
- **Limits:** It optimizes its defined objective; thresholds and interpolation counts remain data- and endpoint-dependent and adaptive fitting must respect evaluation splits.

<a id="s18"></a>
## S18 — Artifact removal and EEG decoding

- **Type / class:** Comparative empirical study; `CONDITIONAL_EVIDENCE`.
- **Source:** Kang T, et al. Impact of artifact removal on EEG decoding performance. *Journal of Neural Engineering*. 2024;21. [doi:10.1088/1741-2552/ad788e](https://doi.org/10.1088/1741-2552/ad788e).
- **Supports:** Artifact-removal methods did not produce a consistent decoding benefit across the evaluated tasks and pipelines; evaluate removal against the intended endpoint.
- **Limits:** The result is bounded to the studied datasets, artifacts, features, and classifiers and does not show artifacts should be retained generally.

<a id="s19"></a>
## S19 — EEG preprocessing multiverse

- **Type / class:** Large comparative empirical study; `CONDITIONAL_EVIDENCE`.
- **Source:** Kessler K, et al. The multiverse of EEG preprocessing and its impact on the robustness of findings. *Communications Biology*. 2025. [doi:10.1038/s42003-025-08464-3](https://doi.org/10.1038/s42003-025-08464-3).
- **Supports:** Plausible preprocessing choices can materially change EEG outcomes, motivating declared pipelines and sensitivity analyses for consequential choices.
- **Limits:** Effect sizes and rankings depend on studied datasets and endpoints; a multiverse does not identify a universal winner.

<a id="s20"></a>
## S20 — Cross-validation in neuroimaging

- **Type / class:** Empirical/methodological study; `HARD_INVARIANT`, `CONDITIONAL_EVIDENCE`.
- **Source:** Varoquaux G, et al. Assessing and tuning brain decoders: cross-validation, caveats, and guidelines. *NeuroImage*. 2017;145:166–179. [doi:10.1016/j.neuroimage.2016.10.038](https://doi.org/10.1016/j.neuroimage.2016.10.038).
- **Supports:** Small-sample cross-validation estimates are variable; tuning and evaluation require separation, and split design must reflect the generalization target.
- **Limits:** Quantitative results are specific to evaluated neuroimaging settings; the independence requirement is broader than any one recommended splitter.

<a id="s21"></a>
## S21 — EEG temporal leakage

- **Type / class:** EEG methods paper; `HARD_INVARIANT`, `CONDITIONAL_EVIDENCE`.
- **Source:** Brookshire G, et al. Cross-validation pitfalls in EEG decoding: temporal autocorrelation can inflate performance. *Frontiers in Neuroscience*. 2024;18:1373515. [doi:10.3389/fnins.2024.1373515](https://doi.org/10.3389/fnins.2024.1373515).
- **Supports:** Randomly splitting temporally dependent EEG samples can leak autocorrelated information and inflate decoding estimates; group splits by the independent acquisition unit when that matches the estimand.
- **Limits:** Leakage magnitude depends on sampling, task, labels, windows, and split design.

<a id="s22"></a>
## S22 — Cross-validation with structured dependence

- **Type / class:** Methodological review; `HARD_INVARIANT`, `CONDITIONAL_EVIDENCE`.
- **Source:** Roberts DR, et al. Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. *Ecography*. 2017;40:913–929. [doi:10.1111/ecog.02881](https://doi.org/10.1111/ecog.02881).
- **Supports:** Resampling should preserve the dependence structure relevant to deployment; blocked/grouped strategies may be needed when observations are not independent.
- **Limits:** Domain examples are broader than EEG and block choice remains estimand-specific.

<a id="s23"></a>
## S23 — BIDS derivatives and provenance

- **Type / class:** Official specification guidance; `CONSENSUS_REPORTING`, `SOFTWARE_CONTRACT`.
- **Source:** BIDS Contributors. *Derivatives*. [BIDS derivatives guidance](https://bids.neuroimaging.io/getting_started/folders_and_files/derivatives.html); *BEP028 Provenance* [proposal specification](https://bids-specification.readthedocs.io/en/bep028/modality-agnostic-files/provenance.html).
- **Supports:** Keep derivatives distinct from raw data and record generated-by/source relationships. BEP028 supplies a useful emerging vocabulary for activities and inputs.
- **Limits:** BEP028 is a proposal, not part of stable BIDS; this skill does not claim BIDS-Prov conformance.

<a id="s24"></a>
## S24 — EEGLAB functions and data structures

- **Type / class:** Official software documentation; `SOFTWARE_CONTRACT`.
- **Source:** SCCN. *EEGLAB functions* and *EEGLAB data structures*. [Functions](https://eeglab.org/tutorials/ConceptsGuide/EEGLAB_functions.html), [data structures](https://eeglab.org/tutorials/ConceptsGuide/Data_Structures.html).
- **Supports:** `pop_` functions expose history-oriented user operations, lower-level functions perform computation, `EEG` stores dataset state, and consistency checks should follow structural changes.
- **Limits:** Documentation describes EEGLAB conventions; plugin/version behavior can change and must be recorded.

<a id="s25"></a>
## S25 — EEGLAB EEG-BIDS plugin

- **Type / class:** Official plugin documentation; `SOFTWARE_CONTRACT`.
- **Source:** SCCN. *EEG-BIDS EEGLAB plugin*. [Plugin documentation](https://eeglab.org/plugins/EEG-BIDS/).
- **Supports:** `pop_importbids`/`pop_exportbids` workflows and the warning that an import output folder must not be inside the BIDS archive because added STUDY files can invalidate it.
- **Limits:** Function signatures and supported BIDS features depend on plugin version; validate on the installed release.

<a id="s26"></a>
## S26 — MNE-BIDS read contract

- **Type / class:** Official software documentation, MNE-BIDS 0.19; `SOFTWARE_CONTRACT`.
- **Source:** MNE-BIDS Developers. `mne_bids.read_raw_bids`. [Stable API](https://mne.tools/mne-bids/stable/generated/mne_bids.read_raw_bids.html).
- **Supports:** Read BIDS recordings with sidecar metadata applied to an MNE Raw object; documented flags govern annotation and coordinate handling.
- **Limits:** Successful parsing is not scientific validation; unsupported or inconsistent metadata still requires an intake decision.

<a id="s27"></a>
## S27 — MNE Raw, filtering, and resampling

- **Type / class:** Official software documentation, MNE 1.12; `SOFTWARE_CONTRACT`.
- **Source:** MNE Developers. `mne.io.Raw`, filtering and resampling methods. [Raw API](https://mne.tools/stable/generated/mne.io.Raw.html).
- **Supports:** MNE records filtering and resampling parameters; resampling applies anti-alias filtering and can jointly resample events, while documentation warns of event-timing jitter and recommends epoching first when feasible.
- **Limits:** API defaults are not universal scientific defaults; verify exact installed-version behavior and downstream latency tolerance.

<a id="s28"></a>
## S28 — MNE EEG reference and interpolation

- **Type / class:** Official software documentation, MNE 1.12; `SOFTWARE_CONTRACT`.
- **Source:** MNE Developers. `mne.set_eeg_reference` and EEG reference tutorial; Raw interpolation methods. [Reference API](https://mne.tools/stable/generated/mne.set_eeg_reference.html), [reference tutorial](https://mne.tools/stable/auto_tutorials/preprocessing/55_setting_eeg_reference.html), [Raw API](https://mne.tools/stable/generated/mne.io.Raw.html).
- **Supports:** Reference can be applied immediately or as a projection; bad-channel interpolation requires marked bads and appropriate sensor locations and exposes method/origin choices.
- **Limits:** Software availability does not establish appropriateness; record channel support and rank before and after.

<a id="s29"></a>
## S29 — MNE annotations to events

- **Type / class:** Official software documentation, MNE 1.12; `SOFTWARE_CONTRACT`.
- **Source:** MNE Developers. `mne.events_from_annotations`. [Stable API](https://mne.tools/stable/generated/mne.events_from_annotations.html).
- **Supports:** Annotation onset/duration/description can be converted into discrete event samples under a documented mapping and rounding behavior.
- **Limits:** The function cannot determine experimental meaning; event semantics must come from dataset metadata/protocol.

<a id="s30"></a>
## S30 — MATLAB MCP Server and Agentic Toolkit

- **Type / class:** Official software documentation; `SOFTWARE_CONTRACT`.
- **Source:** MathWorks. *MATLAB MCP Server* and *MATLAB Agentic Toolkit*. [MCP server](https://github.com/matlab/matlab-mcp-server), [agentic toolkit](https://github.com/matlab/matlab-agentic-toolkit).
- **Supports:** The server exposes MATLAB code evaluation, code checking, toolbox detection, file execution, and test execution over MCP; launch flags select the MATLAB root, display/session mode, initial folder, and telemetry behavior. The toolkit documents Codex MCP configuration and Windows environment considerations.
- **Limits:** Tools and flags are version-specific; verify the installed binary, MATLAB release/license, configuration, and an actual evaluation in the target agent environment.

<a id="s31"></a>
## S31 — EEGDash 0.8.4 access and cache contract

- **Type / class:** Official software documentation and version-pinned source; `SOFTWARE_CONTRACT`.
- **Source:** EEGDash Developers. *EEGDash objects* and *Download an EEGDash dataset in advance and validate the local cache*. [Objects and lazy cache](https://eegdash.org/concepts/eegdash_objects.html), [bounded download and offline validation](https://eegdash.org/generated/auto_examples/how_to/how_to_download_a_dataset.html), [EEGDash v0.8.4 source](https://github.com/eegdash/EEGDash/tree/v0.8.4), [PyPI release](https://pypi.org/project/eegdash/0.8.4/).
- **Supports:** `EEGDash` returns metadata records without samples; `EEGDashDataset` resolves records lazily and writes BIDS-shaped caches; `download=False` bypasses the catalogue for local BIDS; filters should be applied before sample retrieval. Version 0.8.4 routes OpenNeuro IDs to anonymous S3 and marks NeMAR storage as a non-fetchable backend requiring an existing cache or repository-specific retrieval.
- **Limits:** This is a version-specific software contract, not evidence that catalogue metadata are correct or that a recording is scientifically suitable. Public documentation and deployed catalogue services can drift; record the package version, raw record, retrieval time, source identity, and observed errors.

<a id="s32"></a>
## S32 — OpenNeuro ds003061 auditory oddball dataset

- **Type / class:** Primary dataset record and official dataset documentation; `CONSENSUS_REPORTING`, `SOFTWARE_CONTRACT`.
- **Source:** Delorme A. *EEG data from an auditory oddball task*, OpenNeuro ds003061. [OpenNeuro snapshot 1.1.2](https://openneuro.org/datasets/ds003061/versions/1.1.2), [EEGDash dataset brief](https://eegdash.org/api/dataset/eegdash.dataset.DS003061.html).
- **Supports:** Dataset identity, CC0 license, BIDS representation, 13 participants, three approximately 13-minute runs per participant, 79 recorded channels at 256 Hz, and the standard/oddball/noise auditory-stimulus protocol and response instruction.
- **Limits:** The EEGDash brief advertises an older persistent identifier than the current OpenNeuro object tested locally; preserve rather than silently reconcile snapshot, catalogue, and embedded `DatasetDOI` values. The dataset record does not validate a preprocessing choice or event contrast.

<a id="s33"></a>
## S33 — M3CV / NeMAR nm000166 dataset and conversion provenance

- **Type / class:** Primary dataset paper and official dataset documentation; `CONSENSUS_REPORTING`, `CONDITIONAL_EVIDENCE`.
- **Source:** Huang G, et al. M3CV: A multi-subject, multi-session, and multi-task database for EEG-based biometrics challenge. *NeuroImage*. 2022;264:119666. [doi:10.1016/j.neuroimage.2022.119666](https://doi.org/10.1016/j.neuroimage.2022.119666), [PubMed 36206939](https://pubmed.ncbi.nlm.nih.gov/36206939/), [EEGDash/NeMAR dataset brief](https://eegdash.org/api/dataset/eegdash.dataset.NM000166.html).
- **Supports:** The study contains 95 distributed participants with repeated sessions and multiple tasks for cross-subject, cross-session, and cross-task analysis. The NeMAR BIDS conversion concatenates distributed four-second pre-epoched files into pseudo-continuous task recordings; original continuous data are unavailable. The distributed signals had already undergone manual bad-channel interpolation, filtering/notching, linked-mastoid rereferencing, visually guided ICA artifact removal, and downsampling to 250 Hz.
- **Limits:** The BIDS descriptor labels the converted tree `DatasetType: raw`, but `GeneratedBy`, recording sidecars, and the dataset documentation establish prior transformations; consumers must not interpret `raw` as untouched acquisition. Concatenation does not restore original temporal adjacency, discarded channels/epochs, 1000 Hz samples, or pre-cleaning signals.
