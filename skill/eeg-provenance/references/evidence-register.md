# Evidence register

This register is the only source namespace used by the skill. “Supports” describes the narrow claim for which a source may be cited; it is not a summary of every conclusion in the source. “Limits” prevents a citation from being generalized beyond its design. URLs and identifiers were checked on 2026-08-09.

## Contents

- [Search and selection protocol](#search-and-selection-protocol)
- [Evidence classes](#evidence-classes)
- [Standards, reporting, and provenance (S01–S06)](#s01)
- [Signal processing and artifacts (S07–S19)](#s07)
- [Validation and leakage (S20–S22)](#s20)
- [Software, dataset, and archive contracts (S23–S35, S37–S61)](#s23)
- [Forward-model methods (S36)](#s36)

## Search and selection protocol

This is a targeted scoping review for EEG intake, preprocessing decisions, channel/montage harmonization, leakage control, software behavior, dataset-specific provenance, reproducibility, remote cache execution, and the minimum anatomy/head-model readiness needed for EEG forward solutions. Searches covered PubMed, Crossref/DOI resolution, BIDS, the BIDS Validator, PyBIDS, W3C, MNE, MNE-BIDS, SciPy, pymatreader, FreeSurfer, EEGLAB, EEGDash, TorchEEG, MOABB, Braindecode, PyHealth, PyEDFlib, DataLad, git-annex, Google Colab, OpenNeuro, NeMAR, BCI Competition IV, SEED, and TUH/NEDC official documentation. Representative queries included `EEG-BIDS specification reference electrodes channels`, `COBIDAS MEEG preprocessing reporting`, `EEG filter design artifacts`, `EEG interpolation spherical splines`, `EEG reference rank`, `EEG ICA high-pass`, `EEG preprocessing multiverse decoding`, `EEG cross-validation leakage`, `EEG BEM FEM head volume conductor`, `MNE MRI head transform`, `FreeSurfer recon-all SUBJECTS_DIR`, `MNE hdf5 pymatreader MATLAB 7.3`, `SciPy loadmat HDF5 7.3`, `remote EEG cache Colab git-annex standalone`, `DataLad get drop`, `EEGDash metadata lazy cache`, `TorchEEG datasets SEED BCICIV2a`, `MOABB dataset MNE Raw`, `Braindecode datasets preprocessing windows models`, `PyHealth TUAB TUEV set_task processors cache models`, `PyBIDS BIDSLayout get_metadata`, `BIDS Validator JSON git annex`, `OpenNeuro ds003061`, `NeMAR nm000166 M3CV`, `BCI Competition IV 2a GDF events`, `SEED Preprocessed_EEG`, `TUH EEG channel labels TUAB split`, `TUH EEG SSH key rsync access`, and `EEGLAB official tutorials history Makoto useful code`.

Include primary methods/results papers, standards, consensus reports, and versioned official software documentation that directly support an in-scope statement. Exclude reviews used only as citation proxies, unversioned tutorials when a stable API/specification is available, clinical interpretation, inverse-method or source-estimator selection advice, and uncited rules inherited from ClaudeEEG. Source imaging is limited to anatomy discovery, coordinate alignment, forward-model readiness, and provenance. Deduplicate by DOI or canonical specification URL. Prefer a primary paper for empirical effects and official documentation for current software contracts. Record proposal status explicitly.

Searches were run on 2026-08-08 and updated on 2026-08-09. Dynamic result counts were not used as an eligibility criterion; each retained item was resolved to its DOI or canonical official page, screened against the claim it supports, and deduplicated before receiving one source ID.

| Search group | Sources searched | Exact query or route | Retained IDs |
|---|---|---|---|
| Data model/reporting | BIDS, PubMed, DOI resolver | `EEG-BIDS specification reference electrodes channels`; `COBIDAS MEEG preprocessing reporting` | S01–S03, S23 |
| Provenance/reuse | W3C, DOI resolver | `W3C PROV-O Entity Activity Agent`; `FAIR scientific data provenance` | S05–S06 |
| Reference/geometry | PubMed, DOI resolver | `EEG interpolation spherical splines`; `EEG reference montage rank` | S07–S08 |
| Temporal transforms | PubMed, DOI resolver | `EEG digital filter design artifacts`; `ERP baseline correction regression` | S09–S12 |
| Artifact procedures | PubMed, DOI resolver | `PREP EEG pipeline`; `ICLabel EEG component classifier`; `artifact subspace reconstruction EEG`; `autoreject EEG` | S04, S13, S16–S18 |
| Pipeline sensitivity | PubMed, DOI resolver | `EEG preprocessing multiverse robustness` | S19 |
| Evaluation leakage | PubMed, DOI resolver | `neuroimaging cross-validation caveats`; `EEG temporal autocorrelation cross-validation leakage`; `structured data blocked cross-validation` | S20–S22 |
| Software contracts | Python, PyPA, PyPI metadata, NumPy, pandas, MNE, MNE-BIDS, PyBIDS, EEGLAB, MathWorks, and OpenAI official documentation | Stable API pages and installed-tool routes for the named functions/servers; Python lifecycle and packaging-environment rules; current and historical Python/dependency floors; NumPy 2 and pandas 3 migration boundaries; EEGLAB tutorial/history, version-pinned wrapper source, community-recipe boundary; and skill progressive-disclosure contract | S14–S15, S24–S30, S55–S61 |
| Dataset access | EEGDash, OpenNeuro, NeMAR, BCI Competition IV, SEED, TUH/NEDC, git-annex, version-pinned source | `EEGDash metadata lazy cache`; `OpenNeuro ds accession DataLad git-annex`; `NeMAR nm on accession download`; dataset pages and source-backend implementation; `BCI Competition IV 2a event codes GDF`; `SEED preprocessed EEG 200 Hz`; `TUH EEG channel labels configuration`; `TUAB subject disjoint`; `TUH EEG SSH key rsync access`; `git-annex content availability crippled filesystem` | S31–S33, S37–S41, S51, S54 |
| Non-BIDS containers and adapters | EDF+ specification, MNE, SciPy, TorchEEG, MOABB, PyEDFlib | `EDF fixed header per-signal samples`; `MNE read_raw_gdf preload`; `scipy whosmat variables shape class`; `TorchEEG built-in custom dataset cache`; `MOABB datasets MNE Raw`; `PyEDFlib signal headers` | S42–S46 |
| Dataset-to-model frameworks | Braindecode, PyHealth, EEGDash, MOABB, TorchEEG, version-pinned package/source | `Braindecode datasets preprocessing windows models`; `PyHealth TUAB TUEV set_task processors cache models`; historical and current package dependency metadata | S52–S53, S59 |
| BIDS validation and queries | BIDS Validator, PyBIDS | `BIDS Validator JSON git-ref annex`; `PyBIDS BIDSLayout get_metadata derivatives` | S47–S48 |
| MATLAB HDF5 route | MNE, SciPy, pymatreader, MathWorks | `MNE hdf5 extra pymatreader`; `SciPy loadmat MATLAB 7.3 HDF5` | S49 |
| Remote acquisition and cache | inspected project commit, DataLad, git-annex, Google Colab | `remote EEG cache`; `DataLad get drop`; `git-annex Linux standalone verify`; `Colab VM persistence Drive I/O` | S50 |
| Anatomy and forward readiness | BIDS, MNE, FreeSurfer, PubMed | `T1w anatomical landmarks`; `MNE head MRI trans BEM`; `recon-all SUBJECTS_DIR`; `EEG BEM FEM volume conductor` | S01, S23, S34–S36 |

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
- **Source:** BIDS Contributors. *Brain Imaging Data Structure 1.11.1*, PDF release `2b3e7e3`, 2026-02-19: common principles and file formats (PDF pp. 47–60), dataset-level metadata and events (pp. 65–89), and Electroencephalography (pp. 185–203). [Official 1.11.1 EEG specification](https://bids-specification.readthedocs.io/en/stable/modality-specific-files/electroencephalography.html).
- **Supports:** Requirement levels; source/raw/derived distinctions; filename and TSV/JSON rules; inheritance resolution; dataset description, participants, sessions, scans, and events; EEG storage formats and sidecar requirements; channels versus electrodes; channel status, units, reference and filter metadata; electrode coordinates and coordinate-system metadata.
- **Limits:** BIDS describes representation and required/recommended metadata, not the scientific validity of a preprocessing choice. The `stable` URL can advance; pin decisions to 1.11.1 and record the validator version.

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
- **Source:** BIDS Contributors. *Brain Imaging Data Structure 1.11.1*: storage and derived dataset description (PDF pp. 51–53, 65–70) and BIDS Derivatives (pp. 365–372). [Official BIDS Derivatives specification](https://bids-specification.readthedocs.io/en/stable/derivatives/introduction.html).
- **Supports:** Keep derivatives distinct from raw data; require a derivative dataset description and `GeneratedBy`; name outputs from source entities without raw-name collisions; propagate still-valid required metadata; record dataset sources and immediate file inputs with `SourceDatasets`, `DatasetLinks`, and `Sources`; treat `RawSources` as deprecated.
- **Limits:** BIDS Derivatives standardizes dataset/file representation but does not encode every activity parameter, fit scope, random seed, channel/rank transition, QC result, or scientific limitation. This project ledger supplements those gaps and does not by itself establish BIDS conformance.

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
## S27 — MNE Raw, Epochs, filtering, and resampling

- **Type / class:** Official software documentation, MNE 1.12; `SOFTWARE_CONTRACT`.
- **Source:** MNE Developers. `mne.io.Raw`, `mne.Epochs`, memory-efficient I/O, and filtering/resampling guidance. [Raw API](https://mne.tools/stable/generated/mne.io.Raw.html), [Epochs API](https://mne.tools/stable/generated/mne.Epochs.html), [implementation notes](https://mne.tools/stable/documentation/implementation.html), [resampling FAQ](https://mne.tools/stable/help/faq.html).
- **Supports:** MNE readers can keep supported recordings lazy until data access or preload; `Epochs` creates an event-bounded representation without replacing Raw and can defer data loading/rejection; Raw transforms document in-place behavior and preload requirements. Resampling applies anti-alias filtering and can jointly resample events, while the FAQ warns of event-timing jitter and recommends epoching first when feasible.
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

<a id="s34"></a>
## S34 — MNE forward and coregistration contract

- **Type / class:** Official software documentation, MNE 1.12; `SOFTWARE_CONTRACT`.
- **Source:** MNE Developers. *Forward models and source spaces*, *Head model and forward computation*, and MRI processing API. [Forward tutorials](https://mne.tools/stable/auto_tutorials/forward/index.html), [head model and forward computation](https://mne.tools/stable/auto_tutorials/forward/30_forward.html), [MRI processing API](https://mne.tools/stable/api/mri.html).
- **Supports:** MNE treats source space, head model, sensor information, and the head-to-MRI transform as distinct forward-model inputs; coregistration places MRI/head geometry and sensors in a common coordinate system, and the transform can be stored in a `-trans.fif` file. MNE documents subject-MRI and template-MRI branches separately.
- **Limits:** This is an MNE 1.12 software contract, not a validation of a dataset's geometry or a universal source-imaging workflow. Record the installed version, selected files, transform, conductivities, source space, and QC.

<a id="s35"></a>
## S35 — FreeSurfer reconstruction contract

- **Type / class:** Official software documentation; `SOFTWARE_CONTRACT`.
- **Source:** FreeSurfer Developers. *recon-all* and *FreeSurfer and BIDS*. [recon-all documentation](https://surfer.nmr.mgh.harvard.edu/fswiki/recon-all), [FreeSurfer BIDS notes](https://surfer.nmr.mgh.harvard.edu/fswiki/BIDS).
- **Supports:** `recon-all -subject <id> -i <volume> -all` creates a subject reconstruction beneath `SUBJECTS_DIR`; the subject directory contains MRI and surface outputs plus logs/status. A conventional FreeSurfer subject tree is not, by default, a BIDS-compatible derivative representation.
- **Limits:** Flags, outputs, and BIDS export behavior are version-specific. Presence of a subject directory does not establish successful reconstruction or scientific usability; inspect completion state, logs, version/build stamp, manual edits, and surface/segmentation QC.

<a id="s36"></a>
## S36 — EEG/MEG volume-conductor modeling

- **Type / class:** Simulation-based methods guideline; `CONDITIONAL_EVIDENCE`.
- **Source:** Vorwerk J, Cho JH, Rampp S, Hamer H, Knösche TR, Wolters CH. A guideline for head volume conductor modeling in EEG and MEG. *NeuroImage*. 2014;100:590–607. [doi:10.1016/j.neuroimage.2014.06.040](https://doi.org/10.1016/j.neuroimage.2014.06.040), [PubMed 24971512](https://pubmed.ncbi.nlm.nih.gov/24971512/).
- **Supports:** An EEG/MEG volume-conductor model combines anatomical compartment geometry with electrical conductivity assumptions; compartment selection can materially change simulated forward fields, and BEM/FEM choices must be reported with the represented tissues and conductivities.
- **Limits:** The quantitative comparisons are simulations under particular geometries, sources, conductivities, and numerical methods. They do not establish one universally optimal head model or make every tissue refinement necessary for every endpoint.

<a id="s37"></a>
## S37 — git-annex availability boundary

- **Type / class:** Official software documentation and local compatibility policy; `SOFTWARE_CONTRACT`, `LOCAL_POLICY`.
- **Source:** git-annex Developers. *git-annex* configuration and repository documentation. [Official manual](https://git-annex.branchable.com/git-annex/), [crippled-filesystem design note](https://git-annex.branchable.com/design/assistant/blog/day_188__crippled_filesystem_support/).
- **Supports:** Available annexed content resides in `.git/annex/objects/`, while filesystems without symlink, hard-link, or Unix-permission support require special handling. Metadata-only intake must keep work-tree representation separate from verified content availability.
- **Limits:** git-annex does not define the `.lnk` filename convention used by the tested Windows archives. The inspector's `.lnk` recognition is a conservative local compatibility shim for a logical recognized extension and does not replace `git annex whereis`, `find --not --in here`, or content verification in a configured git-annex environment.

<a id="s38"></a>
## S38 — BCI Competition IV dataset 2a contract

- **Type / class:** Official dataset protocol; `HARD_INVARIANT`, `SOFTWARE_CONTRACT`.
- **Source:** Brunner C, Leeb R, Müller-Putz GR, Schlögl A, Pfurtscheller G. *BCI Competition 2008 — Graz data set A*. [Official BCI Competition IV dataset 2a description](https://www.bbci.de/competition/IV/desc_2a.pdf).
- **Supports:** Nine subjects with one training and one evaluation GDF session; 288 four-class motor-imagery trials per session; 22 monopolar EEG plus three EOG channels sampled at 250 Hz; acquisition reference, ground, passband and notch; event-code meanings, rejected-trial markers, run boundaries represented by missing samples, channel order, and the original competition's evaluation constraints.
- **Limits:** The original evaluation files withheld class cues during the competition, but later release bundles can include separate official label files. The competition's causal-classifier and EOG-use rules apply when reproducing that benchmark and do not establish universal constraints for every secondary analysis.

<a id="s39"></a>
## S39 — SEED release contract

- **Type / class:** Official dataset documentation and primary methods paper; `CONSENSUS_REPORTING`, `SOFTWARE_CONTRACT`.
- **Source:** BCMI Laboratory. *SEED Dataset*. [Official SEED description](https://bcmi.sjtu.edu.cn/home/seed/seed.html). Zheng WL, Lu BL. Investigating critical frequency bands and channels for EEG-based emotion recognition with deep neural networks. *IEEE Transactions on Autonomous Mental Development*. 2015;7(3):162–175. [doi:10.1109/TAMD.2015.2431497](https://doi.org/10.1109/TAMD.2015.2431497).
- **Supports:** Fifteen participants, three sessions approximately one week apart, 15 film trials per session, and a 62-channel acquisition; the distributed `Preprocessed_EEG` product contains movie-segmented arrays already downsampled to 200 Hz and filtered from 0–75 Hz, while `ExtractedFeatures` contains feature derivatives. The official page documents negative/neutral/positive as -1/0/+1 and states that channel order is supplied separately.
- **Limits:** MAT arrays do not inherently prove axis meanings, units, channel order, label encoding, or preprocessing history. Different local release workbooks may use another numeric code; preserve the exact source and declare any translation rather than silently reconciling it.

<a id="s40"></a>
## S40 — TUH EEG Corpus organization and channel contract

- **Type / class:** Primary corpus paper, versioned release record, and official technical report; `CONSENSUS_REPORTING`, `SOFTWARE_CONTRACT`.
- **Source:** Obeid I, Picone J. The Temple University Hospital EEG Data Corpus. *Frontiers in Neuroscience*. 2016;10:196. [doi:10.3389/fnins.2016.00196](https://doi.org/10.3389/fnins.2016.00196). NEDC. *TUH EEG Corpus v2.0.1 AAREADME*. [Official v2.0.1 release record](https://isip.piconepress.com/projects/nedc/data/tuh_eeg/tuh_eeg/v2.0.1/AAREADME.txt). Ferrell S, et al. *The Temple University Hospital EEG Corpus: Electrode Location and Channel Labels*. [Official technical-report directory](https://isip.piconepress.com/publications/reports/2020/tuh_eeg/electrodes/).
- **Supports:** The versioned subject/session/configuration/token path contract; a 1,643 GB v2.0.1 corpus whose README internally reports 69,670 EDF files in prose but 69,672 in its command/output lines; more than 40 channel configurations and recording rates ranging from 250–1024 Hz; randomized subject identity; institutional label variability; lookup by label rather than absolute index; stored referential signals versus compatible display montage; auxiliary physiologic channels; pruned clinical source material; and independent treatment of EDF tokens.
- **Limits:** Counts and paths are release-specific, and the official catalogue can publish newer versions. A configuration directory describes compatibility rather than proving that a bipolar montage has been applied to stored samples; channel role still requires label-level inspection.

<a id="s41"></a>
## S41 — TUH Abnormal EEG Corpus v3.0.1 contract

- **Type / class:** Versioned official subset documentation and thesis; `HARD_INVARIANT`, `SOFTWARE_CONTRACT`.
- **Source:** NEDC. *TUH Abnormal EEG Corpus v3.0.1 AAREADME*. [Official v3.0.1 release record](https://isip.piconepress.com/projects/nedc/data/tuh_eeg/tuh_eeg_abnormal/v3.0.1/AAREADME.txt). Lopez S. *Automated Identification of Abnormal EEGs*. Temple University, 2017. [Official thesis directory](https://isip.piconepress.com/publications/ms_theses/2017/abnormal/).
- **Supports:** TUAB v3.0.1 contains 2,993 selected EDF recordings organized by publisher `train`/`eval`, `normal`/`abnormal`, and `01_tcp_ar`; train and evaluation subjects are disjoint; training can contain multiple sessions and 54 subjects represented under both class labels; one pruned EDF was selected per session; and the folder label is a release annotation for the chosen record.
- **Limits:** The release label is not a new clinical judgment by the skill, and TUAB is not the complete longitudinal TUEG record. The official evaluation partition must remain untouched by training or adaptive preprocessing when reproducing the benchmark; internal validation within training remains subject-grouped.

<a id="s42"></a>
## S42 — EDF/EDF+ container header contract

- **Type / class:** Official format specification; `HARD_INVARIANT`, `SOFTWARE_CONTRACT`.
- **Source:** European Data Format developers. *EDF and EDF+ specifications*. [Official EDF specification](https://www.edfplus.info/specs/edf.html), [official EDF+ specification](https://www.edfplus.info/specs/edfplus.html).
- **Supports:** The fixed EDF header and per-signal header fields encode signal labels, physical dimensions and extrema, digital extrema, prefilter text, data-record duration, and samples per data record; per-signal sampling frequency is derived from samples per data record divided by record duration.
- **Limits:** A syntactically readable header does not establish experimental semantics, label ontology, montage history, diagnostic meaning, or data quality. EDF+ annotations and vendor conventions require their applicable release contract.

<a id="s43"></a>
## S43 — Metadata-only GDF and MAT software contracts

- **Type / class:** Official software documentation; `SOFTWARE_CONTRACT`.
- **Source:** MNE Developers. `mne.io.read_raw_gdf`. [MNE stable API](https://mne.tools/stable/generated/mne.io.read_raw_gdf.html). SciPy Developers. `scipy.io.whosmat`. [SciPy stable API](https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.whosmat.html).
- **Supports:** MNE can construct a lazy Raw object from GDF with `preload=False`, exposing header-derived channel information and annotations without preloading the sample matrix; SciPy `whosmat` lists MAT variable names, shapes, and data classes without loading those arrays as analysis data.
- **Limits:** Reader types and generated channel names are software interpretations, not dataset semantics. GDF event meaning, MAT axis meaning, unit, channel order, label mapping, and prior transformations require a separate protocol or release contract; small non-signal companion metadata can be read explicitly when bounded and recorded.

<a id="s44"></a>
## S44 — TorchEEG dataset adapters

- **Type / class:** Official software documentation and version-pinned source, TorchEEG 1.1.3; `SOFTWARE_CONTRACT`.
- **Source:** TorchEEG Developers. *torcheeg.datasets* and *Introduction to the datasets Module*. [Dataset API](https://torcheeg.readthedocs.io/en/stable/torcheeg.datasets.html), [dataset tutorial](https://torcheeg.readthedocs.io/en/stable/auto_examples/examples_datasets.html), [TorchEEG v1.1.3 source](https://github.com/torcheeg/torcheeg/tree/v1.1.3/torcheeg/datasets).
- **Supports:** TorchEEG includes versioned adapters for multiple non-BIDS/apply-to-access EEG datasets and generic `FolderDataset`, `CSVFolderDataset`, and `MNERawDataset` routes. Built-in adapters encode filename, array, label, windowing, and channel-count assumptions; dataset construction can read samples, segment them, apply offline transforms, and create an IO cache at `io_path`.
- **Limits:** An adapter is executable software behavior, not primary evidence that a local archive matches the assumed release. Adapter defaults can transform samples, labels, axes, and partitions and can write caches; inspect version-pinned source and compare every assumption with official documentation and local metadata before execution. Do not instantiate a built-in adapter merely to perform read-only intake.

<a id="s45"></a>
## S45 — MOABB dataset abstraction

- **Type / class:** Official software documentation and methods paper; `SOFTWARE_CONTRACT`.
- **Source:** MOABB Developers. *API and Main Concepts*. [Official dataset API](https://moabb.neurotechx.com/docs/api.html). Jayaram V, Barachant A. MOABB: trustworthy algorithm benchmarking for BCIs. *Journal of Neural Engineering*. 2018;15(6):066011. [doi:10.1088/1741-2552/aadea0](https://doi.org/10.1088/1741-2552/aadea0).
- **Supports:** MOABB supplies dataset classes that obtain supported BCI releases and expose recordings as MNE Raw objects, while paradigms, evaluations, and pipelines define later processing and measurement. Dataset/session pooling and evaluation design are explicit software choices.
- **Limits:** MOABB's downloaded representation and adapter behavior remain version-specific. A supported class is not evidence that a separately obtained archive has identical files, labels, release version, or preprocessing; inspect source and compare with primary dataset documentation before reuse.

<a id="s46"></a>
## S46 — PyEDFlib header reader

- **Type / class:** Official software documentation; `SOFTWARE_CONTRACT`.
- **Source:** PyEDFlib Developers. *PyEDFlib EDF/BDF reader*. [Official documentation](https://pyedflib.readthedocs.io/en/latest/ref/edfreader.html), [documented reader source](https://pyedflib.readthedocs.io/en/latest/_modules/pyedflib/edfreader.html).
- **Supports:** `EdfReader.getSignalHeaders()` exposes per-signal label, physical dimension, sample frequency, physical/digital extrema, prefilter, and transducer fields; these calls read the container header without requiring `readSignal` sample access.
- **Limits:** Header fields and labels are source observations, not a channel ontology, montage interpretation, diagnostic label, or guarantee of correct units. Do not call sample-reading methods during metadata-only intake, and record the installed PyEDFlib version.

<a id="s47"></a>
## S47 — Official BIDS Validator

- **Type / class:** Official standard-validation software documentation and exercised validator 2.2.9; `SOFTWARE_CONTRACT`.
- **Source:** BIDS Validator Developers. *The BIDS Validator* and *Using the command line*. [Official documentation](https://bids-validator.readthedocs.io/en/latest/), [command-line reference](https://bids-validator.readthedocs.io/en/latest/user_guide/command-line.html). BIDS Contributors. [Official historical 1.11.1 schema at reviewed commit `34d5927`](https://github.com/bids-standard/bids-schema/tree/34d59276aa8f34d3e3b2f17723183b5c7ecc1efb/versions/1.11.1).
- **Supports:** The schema-based validator assesses BIDS compliance, emits text or JSON issue reports, accepts issue-severity configuration, and can validate raw/derivative/study datasets. The latest documentation describes Git-ref validation and an experimental preferred git-annex remote, while the web validator performs local browser-side validation without transferring selected data to a server.
- **Limits:** CLI options are release-specific: the exercised 2.2.9 PyPI binary exposes `--preferredRemote` but not the newer documented `--git-ref`. Validator success establishes conformance to the selected schema/software contract, not scientific validity, acquisition truth, preprocessing appropriateness, object availability at every annex remote, or endpoint sufficiency. Pin the validator and BIDS versions, inspect `--help`, and preserve warnings/configuration.

<a id="s48"></a>
## S48 — PyBIDS layout and inheritance queries

- **Type / class:** Official software documentation, PyBIDS 0.22.0; `SOFTWARE_CONTRACT`.
- **Source:** PyBIDS Developers. `bids.layout.BIDSLayout`. [Official 0.22.0 API](https://bids-standard.github.io/pybids/generated/bids.layout.BIDSLayout.html), [PyBIDS API reference](https://bids-standard.github.io/pybids/api.html).
- **Supports:** `BIDSLayout` indexes BIDS entities in memory or a database, can use the official BIDS schema configuration, queries raw and derivative scopes, exposes dataset descriptions and file/entity tables, resolves inherited JSON through `get_metadata`, and finds associated or nearest files.
- **Limits:** `validate=True` filters indexing through PyBIDS' own validation layer and is not a replacement for the official Validator. Effective metadata do not by themselves preserve every contributing sidecar path or prove historical truth; record relevant source files and conflicts separately, and avoid persistent database paths inside an immutable source archive.

<a id="s49"></a>
## S49 — MNE HDF5 and MATLAB v7.3 route

- **Type / class:** Official software documentation and exercised MNE 1.12.1 environment; `SOFTWARE_CONTRACT`.
- **Source:** MNE Developers. *Installing MNE-Python with HDF5 support* and *Frequently Asked Questions*. [MNE 1.12.1 installation documentation](https://mne.tools/stable/install/manual_install.html), [MNE persistence guidance](https://mne.tools/stable/help/faq.html). pymatreader Developers. `pymatreader.read_mat`. [Official pymatreader documentation](https://pymatreader.readthedocs.io/en/latest/). SciPy Developers. `scipy.io.loadmat`. [SciPy stable API](https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.matlab.loadmat.html). MathWorks. *MAT-File Versions*. [Official MATLAB documentation](https://www.mathworks.com/help/matlab/import_export/mat-file-versions.html).
- **Supports:** MNE 1.12.1 documents `mne[hdf5]` as the pip extra for functions requiring HDF5 and names h5io and pymatreader as its added packages; pymatreader provides one interface for MAT files older than 7.3 and HDF5-based v7.3 files with optional variable selection; SciPy `loadmat` supports v4, v6, and v7 through v7.2 but not the HDF5/v7.3 interface; MATLAB documents v7.3 as HDF5-based. The locked exercise resolved MNE 1.12.1, h5io 0.2.5, h5py 3.16.0, and pymatreader 1.2.3 and round-tripped selected numeric variables from a temporary v7.3 fixture without MATLAB.
- **Limits:** HDF5 readability does not supply dataset-specific MATLAB semantics. Pymatreader converts MATLAB containers to Python types, while h5io serves HDF5 serialization used by MNE and other Python data; neither proves EEG axes, units, channel labels, event meaning, acquisition history, or that an arbitrary MAT structure is an EEGLAB/MNE object. Inspect hierarchy metadata first and load only documented variables needed by the endpoint.

<a id="s50"></a>
## S50 — Remote acquisition and durable cache execution

- **Type / class:** Version-pinned project case study and official runtime/data-management documentation; `SOFTWARE_CONTRACT`, `LOCAL_POLICY`.
- **Source:** Zhou J. *brainprint-rseeg-data*, inspected read-only at commit `cd4adb9d2b72f9f3953302892f6050b921821173`: [repository snapshot](https://github.com/theJingqiZhou/brainprint-rseeg-data/tree/cd4adb9d2b72f9f3953302892f6050b921821173), [README](https://github.com/theJingqiZhou/brainprint-rseeg-data/blob/cd4adb9d2b72f9f3953302892f6050b921821173/README.md), [git-annex bootstrap](https://github.com/theJingqiZhou/brainprint-rseeg-data/blob/cd4adb9d2b72f9f3953302892f6050b921821173/src/brainprint_rseeg_data/builder/utils/datalad.py), [bounded fetcher](https://github.com/theJingqiZhou/brainprint-rseeg-data/blob/cd4adb9d2b72f9f3953302892f6050b921821173/src/brainprint_rseeg_data/builder/fetchers.py), and [cache verification](https://github.com/theJingqiZhou/brainprint-rseeg-data/blob/cd4adb9d2b72f9f3953302892f6050b921821173/src/brainprint_rseeg_data/builder/utils/cache.py). DataLad Developers. [Basic `get` behavior](https://docs.datalad.org/en/master/basics.html) and [`drop` reference](https://docs.datalad.org/en/latest/generated/man/datalad-drop.html). git-annex Developers. [Linux standalone installation](https://git-annex.branchable.com/install/Linux_standalone/) and [download verification](https://git-annex.branchable.com/install/verifying_downloads/). Google. [Colab FAQ](https://research.google.com/colaboratory/faq.html).
- **Supports:** The inspected project demonstrates direct compute-side metadata checkout, selected annex-object retrieval, bounded fetch/process/drop batches, separate ephemeral source/staging roots, resumable shard state, persistent Drive-backed cache output, record metadata, and SHA-256 manifests. Its Colab bootstrap detects a missing TCP/UDP protocol database and installs `netbase`, and it can install a standalone git-annex bundle when the image lacks a packaged binary. DataLad documents path-scoped `get`, safe-by-default `drop`, and the safety checks disabled by reckless availability mode; git-annex publishes self-contained Linux bundles and signed-download verification; Colab documents ephemeral VM lifetimes plus Drive mount, quota, item-count, and small-I/O limitations.
- **Limits:** The Colab paths, Google Drive backend, `netbase` repair, current standalone bundle, source remotes, TFRecord format, and reckless drop decision are project- and runtime-specific. The reviewed notebook disables bundle-signature verification even though its helper can verify signatures; do not copy that exception without an independently verified artifact policy. Other legacy VMs may lack a compatible architecture/kernel, package manager, privileges, GPG, DNS, outbound HTTPS, protocol database, persistent mount, or remote credentials. A preflight and explicit fallback are required before bulk retrieval, and remote acquisition does not relax dataset access terms or scientific preprocessing/evaluation constraints.

<a id="s51"></a>
## S51 — OpenNeuro and NeMAR accession routing

- **Type / class:** Official provider and software documentation; `SOFTWARE_CONTRACT`.
- **Source:** OpenNeuro Developers. *Git access to OpenNeuro datasets* and *OpenNeuro command line interface*. [Official Git/DataLad/git-annex access](https://docs.openneuro.org/git), [official CLI download documentation](https://docs.openneuro.org/packages/openneuro-cli.html). NeMAR. *Download this dataset*, represented by provider records for [`nm000245`](https://ww2.nemar.org/dataset/nm000245) and [`on004840`](https://ww2.nemar.org/dataset/on004840). EEGDash Developers. `EEGDash` and `EEGDashDataset`. [Official dataset API](https://eegdash.org/api/dataset/eegdash.html), [dataset classes](https://eegdash.org/api/dataset/eegdash.dataset.html).
- **Supports:** `dsNNNNNN` is an OpenNeuro accession in this workflow, while NeMAR publishes both `nmNNNNNN` and `onNNNNNN` accessions. OpenNeuro documents CLI, direct Git, DataLad, and git-annex access in addition to exported object storage; NeMAR dataset records expose multiple resumable routes that can include NeMAR CLI, DataLad, git-annex, archive, and manifest/direct-file download. EEGDash accepts dataset identifiers for metadata queries and provides a separate dataset/cache access layer. These are alternative transports or catalogue views of provider datasets, not competing ownership identities.
- **Limits:** Prefix recognition is routing, not complete identity resolution. Do not derive a repository URL, snapshot, version, DOI, or cross-provider mapping from the prefix alone; use the provider record and preserve related identifiers explicitly. Available routes, authentication, mirrors, snapshots, and EEGDash backend behavior can differ by dataset and software version. The cited NeMAR records demonstrate both accession families and platform download options but do not guarantee that every option is present for every dataset.

<a id="s52"></a>
## S52 — Braindecode dataset-to-decoder contract

- **Type / class:** Official software documentation, version-pinned source, and bounded execution, Braindecode 1.7.0; `SOFTWARE_CONTRACT`.
- **Source:** Braindecode Developers. *Braindecode — Decode raw EEG, ECoG and MEG with deep learning* and API reference. [Official stable overview](https://braindecode.org/stable/index.html), [official dataset/preprocessing API](https://braindecode.org/stable/api.html), [Braindecode v1.7.0 source](https://github.com/braindecode/braindecode/tree/v1.7.0), [PyPI 1.7.0 release](https://pypi.org/project/braindecode/1.7.0/).
- **Supports:** Braindecode provides MNE-backed datasets, preprocessing, event/fixed windows, augmentation, models, and sklearn/skorch-style training. In exercised 1.7.0 behavior, serial `preprocess()` changes the wrapped MNE object in place, parallel execution may replace subdatasets with worker results, and `save_dir` writes then reloads derivatives. Event windows carry explicit target/start/stop metadata. Fixed windows with `drop_last_window=False` add a full end-aligned overlapping window for a remainder rather than a short padded window; fixed-window targets come from the declared `RawDataset.target_name`, otherwise the exercised route returned `-1`.
- **Limits:** Dataset wrappers can delegate retrieval and encode release assumptions, but do not replace publisher documentation or prove local-release equivalence. Preprocessing, windowing, augmentation, samplers, model architecture, pretrained weights, and evaluation remain separate scientific choices. On 2026-08-08 the official stable pages were labeled 1.5.1 while the installed/pinned release was 1.7.0; copy API names only from the exercised runtime or matching source tag. In the exercised 1.7.0 wheel, the `EEGNet` warning recommends `final_layer_linear` even though the constructor rejects that keyword, so warnings also require runtime verification.

<a id="s53"></a>
## S53 — PyHealth signal dataset, task, cache, and model contract

- **Type / class:** Official software documentation, version-pinned source, and bounded source inspection, PyHealth 2.0.1; `SOFTWARE_CONTRACT`.
- **Source:** PyHealth Developers. *Architecture Overview*, *Datasets*, *Tasks*, *Processors*, and *Models*. [Architecture](https://pyhealth.readthedocs.io/en/latest/api/overview.html), [datasets and cache](https://pyhealth.readthedocs.io/en/latest/api/datasets.html), [tasks and `set_task`](https://pyhealth.readthedocs.io/en/latest/api/tasks.html), [processors](https://pyhealth.readthedocs.io/en/latest/api/processors.html), [models](https://pyhealth.readthedocs.io/en/latest/api/models.html), [PyHealth v2.0.1 source](https://github.com/sunlabuiuc/PyHealth/tree/v2.0.1), [PyPI 2.0.1 release](https://pypi.org/project/pyhealth/2.0.1/).
- **Supports:** PyHealth 2.0.1 represents source data through `BaseDataset` and turns a task into an indexable `SampleDataset`. `set_task()` keys task and sample caches from serialized task/schema and processor configuration, materializes the task dataset, fits a `SampleBuilder` on that supplied dataset unless pre-fitted processors are passed, saves processor/schema state, writes LitData samples, and returns the cache-backed dataset; split identity is not part of that call. Its TUAB/TUEV tasks bundle EDF loading, temporal transforms, bipolar derivations, window/label construction, optional normalization, and optional STFT. Version-pinned dataset source prepares metadata CSVs and can attempt writes below the supplied root before falling back to a user cache.
- **Limits:** These adapters and task defaults are executable implementation assumptions, not primary dataset evidence or universally valid preprocessing. Dataset construction and `set_task()` are not read-only inspection operations; cache and metadata destinations must be audited. Because processors are fit during `set_task()`, any data-adaptive processor must respect the declared training partition. PyHealth's generic healthcare models are not automatically validated EEG decoders, and the exact 2.0.1 dependency stack should be isolated from incompatible project environments.

<a id="s54"></a>
## S54 — TUH EEG authorized rsync access

- **Type / class:** Official current provider access documentation; `SOFTWARE_CONTRACT`.
- **Source:** Neural Engineering Data Consortium. *Temple University EEG Corpus — Downloads*. [Official access and rsync instructions](https://isip.piconepress.com/projects/nedc/html/tuh_eeg/index.shtml), [official access-request form](https://isip.piconepress.com/projects/nedc/forms/tuh_eeg.pdf).
- **Supports:** As of January 2026, the provider requires an accepted access request, supplies account/credential instructions separately, registers an SSH key, and distributes released TUH EEG corpora through `rsync` over SSH. The provider publishes a small test path, recommends testing it before a full corpus transfer, requires link following because corpus subsets link back to TUEG, and publishes versioned rsync paths for TUEG and subsets including TUAB and TUEV.
- **Limits:** Approval, credentials, hostnames, release paths, and transfer instructions can change; re-check the provider record at execution time. Provider support for `rsync` does not prove that a compute environment permits outbound SSH, has adequate durable storage, or completed a background transfer. Never expose a private key or credential in a repository, command log, provenance ledger, cache, or generated report.

<a id="s55"></a>
## S55 — EEGLAB official tutorial and community recipe boundary

- **Type / class:** Official software tutorials plus a maintained SCCN community recipe page; `SOFTWARE_CONTRACT`, `LOCAL_POLICY`.
- **Source:** SCCN. *Welcome to the EEGLAB tutorial*, *Using EEGLAB history*, and *Makoto's useful EEGLAB code*. [Official tutorial index](https://eeglab.org/tutorials/), [official history/scripting tutorial](https://eeglab.org/tutorials/11_Scripting/Using_EEGLAB_history.html), [SCCN community recipe collection](https://eeglab.ucsd.edu/wiki/Makoto%27s_useful_EEGLAB_code).
- **Supports:** The official tutorial routes importing, preprocessing, artifact handling, scripting, data structures, and function documentation, and documents `EEG.history` plus `eegh` for recovering version-specific GUI-issued calls. Makoto's SCCN page is a dated collection of practical snippets and explicitly invites error reports; it includes code for history inspection, channels/reference, filtering, events, ICA/rank, and batch processing.
- **Limits:** The community page mixes personal recommendations, hard-coded paths/channel indices, dataset-specific assumptions, evolving snippets, and scientific heuristics. It is a recipe-discovery source, not independent evidence for a universal parameter, threshold, processing order, or scientific optimum. Reconcile a candidate snippet with the current official tutorial/help, installed EEGLAB/plugin versions and signatures, the dataset contract, and a disposable or bounded test before use.

<a id="s56"></a>
## S56 — EEGLAB 2026.0.0 headless wrapper contracts

- **Type / class:** Official version-pinned source plus bounded execution on MATLAB R2026a Update 4; `SOFTWARE_CONTRACT`.
- **Source:** SCCN. *EEGLAB 2026.0.0* and its release-pinned plugins. [EEGLAB tag `2026.0.0`](https://github.com/sccn/eeglab/tree/bcc710a8edd712738e48879b6846958a2be7be1d), [`pop_runica` wrapper](https://github.com/sccn/eeglab/blob/bcc710a8edd712738e48879b6846958a2be7be1d/functions/popfunc/pop_runica.m), [`runica` options and RNG initialization](https://github.com/sccn/eeglab/blob/bcc710a8edd712738e48879b6846958a2be7be1d/functions/sigprocfunc/runica.m), and [legacy STUDY save path](https://github.com/sccn/eeglab/blob/bcc710a8edd712738e48879b6846958a2be7be1d/functions/studyfunc/pop_savestudy.m). SCCN. *EEG-BIDS 10.5 source pinned by that release*: [`pop_importbids`](https://github.com/sccn/EEG-BIDS/blob/8486b1dde369079578452e632ee1aac29fe86db8/pop_importbids.m), [`bids_matlab_tools_ver`](https://github.com/sccn/EEG-BIDS/blob/8486b1dde369079578452e632ee1aac29fe86db8/bids_matlab_tools_ver.m).
- **Supports:** The installed wrappers can run without input dialogs when complete arguments are supplied. In these pinned sources, `pop_importbids` documents numeric or cell run selectors but later applies text `contains` matching; its `'metadata','on'` branch still loads the selected recording while skipping output saving; and its STUDY save path ultimately uses character-vector indexing. `pop_runica` forwards unrecognized name-value pairs to the selected ICA algorithm, while `runica` documents `rndreset` rather than `randomseed` and uses a fixed initialization when reset is off. The bounded exercise started all release-pinned plugins, round-tripped a synthetic SET, filtered/rereferenced/interpolated sample data, ran a deliberately truncated ICA wrapper smoke test, obtained normalized ICLabel probabilities, and imported one explicitly selected EEG-BIDS recording into a temporary derivative tree without changing the source inventory.
- **Limits:** These are executable contracts and local verification results for the exact commits, MATLAB release, and bounded inputs—not scientific validation of the example filter, reference, interpolation, ICA, ICLabel, event interpretation, or any preprocessing order. GUI callbacks, accepted text types, selectors, RNG behavior, payload access, and plugin output can change; inspect and re-run the active release before use. A temporary derivative and unchanged file inventory do not by themselves prove bitwise source immutability or BIDS/scientific validity.

<a id="s57"></a>
## S57 — Skill progressive-disclosure contract

- **Type / class:** Official OpenAI product documentation; `SOFTWARE_CONTRACT`, `LOCAL_POLICY`.
- **Source:** OpenAI. *Build skills*. [Official skill authoring documentation](https://learn.chatgpt.com/docs/build-skills).
- **Supports:** Skills package instructions, references, assets, and optional scripts. ChatGPT and Codex initially use skill metadata, then read the full `SKILL.md` after activation; references and scripts provide the next disclosure level. The description should state a concise scope and clear triggers because it controls implicit matching and may itself be shortened when many skills compete for the initial context budget.
- **Limits:** The documentation supports progressive disclosure and concise routing, not this repository's numeric context limits, preferred count of simultaneously loaded references, or exact file organization. Those are local engineering budgets that require eval-based revision rather than presentation as platform guarantees.

<a id="s58"></a>
## S58 — Python lifecycle and scientific-stack metadata

- **Type / class:** Official Python lifecycle plus current and historical package metadata, checked 2026-08-09; `SOFTWARE_CONTRACT`.
- **Source:** Python Core Developers. [Supported Python versions](https://devguide.python.org/versions/). Python Package Index release metadata: [NumPy 2.5.1](https://pypi.org/project/numpy/2.5.1/), [NumPy 2.4.2](https://pypi.org/project/numpy/2.4.2/), [NumPy 2.2.6](https://pypi.org/project/numpy/2.2.6/), [NumPy 1.26.4](https://pypi.org/project/numpy/1.26.4/), [SciPy 1.18.0](https://pypi.org/project/scipy/1.18.0/), [SciPy 1.17.1](https://pypi.org/project/scipy/1.17.1/), [SciPy 1.15.3](https://pypi.org/project/scipy/1.15.3/), [pandas 3.0.5](https://pypi.org/project/pandas/3.0.5/), [pandas 2.3.3](https://pypi.org/project/pandas/2.3.3/), [MNE 1.12.1](https://pypi.org/project/mne/1.12.1/), [MNE-BIDS 0.17.0](https://pypi.org/project/mne-bids/0.17.0/), [MNE-BIDS 0.18.0](https://pypi.org/project/mne-bids/0.18.0/), [MNE-BIDS 0.19.0](https://pypi.org/project/mne-bids/0.19.0/), [PyBIDS 0.22.0](https://pypi.org/project/pybids/0.22.0/), [h5py 3.16.0](https://pypi.org/project/h5py/3.16.0/), [PyEDFlib 0.1.42](https://pypi.org/project/pyedflib/0.1.42/), [pymatreader 1.2.3](https://pypi.org/project/pymatreader/1.2.3/), and [DataLad 1.6.1](https://pypi.org/project/datalad/1.6.1/).
- **Supports:** CPython 3.10–3.14 lifecycle status on the check date; declared `Requires-Python` floors and dependency constraints used as the compatibility-matrix anchors; the lack of a `Requires-Python` field for PyEDFlib 0.1.42. Python 3.9 reached EOL in 2025, while 3.10 remains security-supported until 2026-10.
- **Limits:** Package metadata and classifiers are declarations, not proof that a resolver closes, a wheel exists for the target libc/architecture, an extension has the required ABI, or the operation behaves correctly. PyPI metadata can be corrected after release. The matrix therefore separates metadata-permitted from locally exercised combinations and must be rechecked after its stated date.

<a id="s59"></a>
## S59 — EEG framework dependency-generation boundaries

- **Type / class:** Official current and historical PyPI release metadata plus version-pinned local exercises; `SOFTWARE_CONTRACT`.
- **Source:** Python Package Index releases: EEGDash [0.8.4](https://pypi.org/project/eegdash/0.8.4/); MOABB [1.1.1](https://pypi.org/project/moabb/1.1.1/) and [1.5.0](https://pypi.org/project/moabb/1.5.0/); Braindecode [0.8.1](https://pypi.org/project/braindecode/0.8.1/), [1.2.0](https://pypi.org/project/braindecode/1.2.0/), and [1.7.0](https://pypi.org/project/braindecode/1.7.0/); PyHealth [1.1.6](https://pypi.org/project/pyhealth/1.1.6/) and [2.0.1](https://pypi.org/project/pyhealth/2.0.1/); [TorchEEG 1.1.3](https://pypi.org/project/torcheeg/1.1.3/); [AutoReject 0.4.4](https://pypi.org/project/autoreject/0.4.4/); and [MNE-ICALabel 0.9.0](https://pypi.org/project/mne-icalabel/0.9.0/). See also the pinned behavior records in S31, S44–S45, and S52–S53.
- **Supports:** EEGDash 0.8.4 and Braindecode 1.7 require Python 3.11 or newer; PyHealth 2.0.1 requires Python 3.12–3.13 and tightly constrains MNE, NumPy, pandas, and Torch; MOABB 1.1.1 constrains NumPy and pandas below 2 plus MNE-BIDS below 0.15, whereas MOABB 1.5 requires NumPy 2 and newer MNE/MNE-BIDS; Braindecode and PyHealth generation changes carry different Python/dependency floors. The repository separately exercised TorchEEG 1.1.3 on Python 3.11 with SciPy 1.10.1 and pandas below 3, the modern core/EEG framework lane on Python 3.12, and PyHealth 2.0.1 in an isolated environment.
- **Limits:** Dependency metadata does not establish API equivalence, dataset-release identity, cache compatibility, numerical equivalence, accelerator support, or scientific validity. TorchEEG's broad Python declaration and sparse dependency constraints are especially insufficient without source inspection and an adapter smoke test. “Last candidate family” means the last checked release family whose Python declaration admits that lane, not a maintenance or security recommendation.

<a id="s60"></a>
## S60 — NumPy 2 and pandas 3 migration contracts

- **Type / class:** Official migration guides and release documentation; `SOFTWARE_CONTRACT`.
- **Source:** NumPy Developers. [NumPy 2.0 migration guide](https://numpy.org/doc/2.0/numpy_2_0_migration_guide.html) and [2.0 release notes](https://numpy.org/devdocs/release/2.0.0-notes.html). pandas Developers. [Migration guide for the new string data type](https://pandas.pydata.org/docs/user_guide/migration-3-strings.html) and [Copy-on-Write behavior](https://pandas.pydata.org/pandas-docs/stable/user_guide/copy_on_write.html).
- **Supports:** NumPy 2.0 introduced an ABI break for binaries built against NumPy 1.x, removed or changed APIs, and changed type-promotion behavior. pandas 3 uses the new string dtype by default and makes Copy-on-Write the only mutation mode, affecting code that relied on chained assignment or mutation propagating through derived objects.
- **Limits:** These documents identify migration boundaries, not every affected EEG package or the direction/magnitude of a numerical difference. Import and operation-level regression tests remain necessary for the exact readers, transforms, metadata adapters, and compiled wheels selected by a workflow.

<a id="s61"></a>
## S61 — Isolated and externally managed Python environments

- **Type / class:** Python Packaging Authority guide and interoperability specification; `SOFTWARE_CONTRACT`, `LOCAL_POLICY`.
- **Source:** Python Packaging Authority. [Install packages in a virtual environment using pip and venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) and [Externally Managed Environments](https://packaging.python.org/en/latest/specifications/externally-managed-environments/).
- **Supports:** A virtual environment isolates a project interpreter and installed distributions. The `EXTERNALLY-MANAGED` marker tells Python-specific installers not to modify the interpreter's default environment and to guide users to an isolated environment; `sys.prefix == sys.base_prefix` identifies execution outside a virtual environment for that check. Conda-managed environments are handled separately by Conda.
- **Limits:** PyPA does not require this skill to choose `venv`, `pip`, Conda, modules, containers, or `uv` in every environment. Manager preference, refusal to mutate a shared base, and choosing the already provisioned sufficient stack are conservative local policies. Some legacy images omit `pip`, the `venv` module, compilers, indexes, or outbound network, so environment creation itself requires a capability and authorization check.
