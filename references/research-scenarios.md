# Research-scenario preprocessing contracts

Start from the endpoint and deployment unit, not from a reusable list of filters. Plausible preprocessing choices can change EEG results, and adaptive steps can leak information unless their fit scope follows the intended generalization split. [[S18]](evidence-register.md#s18) [[S19]](evidence-register.md#s19) [[S20]](evidence-register.md#s20)

## ds003061: auditory oddball ERP estimation

The dataset contains three auditory oddball runs per participant with standard, oddball, noise, and response-related event labels; the protocol and BIDS event sidecars, not the string `P300` alone, define the contrasts. [[S01]](evidence-register.md#s01) [[S32]](evidence-register.md#s32)

**Objective and invariants.** Predeclare the condition contrast, response inclusion rule, epoch window, latency tolerance, channels or regions of interest, participant-level estimand, and inferential unit. Preserve event onsets, condition semantics, low-frequency support needed by the waveform, and participant/run identity. [[S03]](evidence-register.md#s03) [[S09]](evidence-register.md#s09) [[S10]](evidence-register.md#s10)

**Contract.** `must_harmonize` event coding and channel units within the analyzed runs; `may_harmonize` reference, bad-channel disposition, and a fully specified fixed filter with a declared no-filter or lower-cutoff sensitivity branch; `cannot_harmonize` undocumented acquisition facts or signal removed before the archived bytes. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03) [[S08]](evidence-register.md#s08) [[S10]](evidence-register.md#s10)

**Ordered design.** Validate event counts/bounds and channel geometry; declare bad spans/channels; test the filter impulse/frequency response and edge handling; epoch from the validated mapping; choose conventional or regression-based baseline treatment explicitly; compute participant/run QC before aggregation. High-pass filtering and baseline subtraction can alter ERP amplitude or latency under condition-dependent circumstances. [[S09]](evidence-register.md#s09) [[S10]](evidence-register.md#s10) [[S11]](evidence-register.md#s11)

**Stop conditions.** Stop if `stimulus/oddball`, `stimulus/oddball_with_reponse`, and misspelled source labels such as `reponse` cannot be mapped without changing the intended contrast, or if timing/units/geometry conflicts remain unresolved. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03) [[S32]](evidence-register.md#s32)

## ds003061: single-trial BCI decoding

The independent unit must match deployment: use participant grouping for a participant-independent claim and retain run grouping when neighboring trials or run-specific conditions would otherwise cross folds. Random trial/window splits can exploit temporal dependence rather than the intended generalization. [[S20]](evidence-register.md#s20) [[S21]](evidence-register.md#s21) [[S22]](evidence-register.md#s22)

Fit bad-channel thresholds, ICA/ASR/AutoReject state, normalization, feature scaling, and any preprocessing choice selected by validation performance inside the training partition; apply only the resulting state to validation/test data. [[S16]](evidence-register.md#s16) [[S17]](evidence-register.md#s17) [[S20]](evidence-register.md#s20)

Evaluate a no-removal branch and at least one justified artifact-handling branch because removal does not consistently improve decoding across tasks and pipelines. Record retained trials, class/response distribution by split, channel/rank changes, and endpoint sensitivity. [[S18]](evidence-register.md#s18) [[S19]](evidence-register.md#s19)

Do not use response-contaminated labels or post-stimulus intervals unless motor-response information is part of the declared BCI estimand; event semantics and temporal support must be explicit. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03) [[S32]](evidence-register.md#s32)

## nm000166: cross-session biometrics

The distributed nm000166 signals are not untouched continuous acquisition: four-second preprocessed epochs were concatenated by task, and filtering, notch filtering, bad-channel interpolation, linked-mastoid rereferencing, visually guided ICA cleaning, and downsampling had already occurred. [[S33]](evidence-register.md#s33)

For a same-person cross-session identification or verification claim, keep enrollment and testing sessions separate and preserve subject identity across those partitions; for a claim about generalization to unseen people, group the outer split by subject instead. The split is determined by the claimed deployment, not by a generic cross-validation default. [[S20]](evidence-register.md#s20) [[S22]](evidence-register.md#s22) [[S33]](evidence-register.md#s33)

Treat recorded epoch boundaries as discontinuities when filtering, windowing, or estimating temporal dependence; do not let a window span a concatenation boundary or interpret adjacent distributed epochs as originally adjacent time. [[S09]](evidence-register.md#s09) [[S21]](evidence-register.md#s21) [[S33]](evidence-register.md#s33)

Bind boundary identity to the conversion provenance and recording-level events/sidecars, and verify the expected boundary/epoch count before any segment-wise operation. Stop if those artifacts disagree or cannot establish the mapping; do not derive boundaries from waveform appearance. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03) [[S33]](evidence-register.md#s33)

`must_harmonize` task code, epoch-boundary interpretation, channel order, units, and session meaning; `may_harmonize` additional fixed transforms whose retained bandwidth and boundary handling are justified; `cannot_harmonize` original 1000 Hz samples, removed IO channel, discarded P300 nontarget epochs, pre-interpolation channels, pre-ICA signals, or original continuous ordering. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03) [[S33]](evidence-register.md#s33)

Do not label another ICA pass, rereference, or interpolation as restoration of the original acquisition. Any additional adaptive cleaning is a new intervention fitted within the training partition and evaluated against a no-additional-cleaning branch. [[S08]](evidence-register.md#s08) [[S18]](evidence-register.md#s18) [[S20]](evidence-register.md#s20) [[S33]](evidence-register.md#s33)

## nm000166: cross-task or state generalization

Define whether the model should generalize across tasks for known people, across people for known tasks, or across both; use nested subject/session/task grouping that withholds the intended axis and keeps adaptive preprocessing inside its training scope. [[S20]](evidence-register.md#s20) [[S22]](evidence-register.md#s22) [[S33]](evidence-register.md#s33)

Task blocks differ in stimulus, motor, steady-state, transient, and rest structure, so identical window length or spectral support is not automatically a harmonized estimand. Declare which physiological or engineering quantity is comparable and report task-specific retention/QC. [[S03]](evidence-register.md#s03) [[S19]](evidence-register.md#s19) [[S33]](evidence-register.md#s33)

When the withheld task requires frequencies or latencies removed by a proposed transform, classify the transform as incompatible rather than tuning it on held-out task performance. [[S09]](evidence-register.md#s09) [[S20]](evidence-register.md#s20)

## Cross-dataset use of ds003061 and nm000166

Do not merge recordings merely because both expose a `P300` task name: ds003061 is an auditory standard/oddball/noise paradigm, whereas the distributed nm000166 P300 subset contains stored visual target epochs and omits the nontarget epochs. The task labels therefore do not define the same contrast or class distribution. [[S01]](evidence-register.md#s01) [[S32]](evidence-register.md#s32) [[S33]](evidence-register.md#s33)

| Dimension | Classification | Required handling |
|---|---|---|
| Dataset and recording identity | `must_harmonize` | Bind every row/window to dataset, snapshot/commit, subject, session, task, run, payload hash, and source record. [[S05]](evidence-register.md#s05) [[S31]](evidence-register.md#s31) |
| Channel units/types and chosen common native subset | `must_harmonize` for joint features | Preserve native/missing/interpolated states; never call an estimate native. [[S01]](evidence-register.md#s01) [[S07]](evidence-register.md#s07) |
| Reference representation | `may_harmonize` | State target, rank effect, and sensitivity branch; do not assume rereferencing reconstructs a never-recorded reference. [[S08]](evidence-register.md#s08) |
| Sampling rate | `may_harmonize` | Choose from retained bandwidth/timing needs and record anti-alias/event timing behavior. [[S09]](evidence-register.md#s09) [[S27]](evidence-register.md#s27) |
| Event/class semantics | `cannot_harmonize` for a direct P300 class merge without a new defensible estimand | Preserve each protocol and narrow the comparison or analyze datasets separately. [[S01]](evidence-register.md#s01) [[S32]](evidence-register.md#s32) [[S33]](evidence-register.md#s33) |
| Prior cleaning and original temporal continuity | `cannot_harmonize` | Expose nm000166 as a converted, preprocessed derivative and do not simulate missing acquisition history for ds003061. [[S03]](evidence-register.md#s03) [[S33]](evidence-register.md#s33) |

## QC evidence for every scenario

Report payload and sidecar hashes, parse/load warnings, record-versus-loaded-object conflicts, shapes/rates/types, units, geometry coverage, non-finite samples, flat channels, annotations/event bounds, bad-channel/span decisions, retained data, and any intervention-specific diagnostics. Parsing success and a scalar quality score are not scientific acceptance. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03) [[S17]](evidence-register.md#s17)

Separate observations from decisions: the intake profiler supplies descriptive bounded-window summaries, while thresholds, exclusions, sensitivity branches, and stop conditions belong to the scenario’s Preprocessing Contract. [[S03]](evidence-register.md#s03) [[S19]](evidence-register.md#s19) [[S31]](evidence-register.md#s31)
