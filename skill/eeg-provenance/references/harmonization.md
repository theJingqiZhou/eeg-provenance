# Harmonization contract

Harmonization is a decision about the estimand, not a cosmetic request for identical matrices. For every dimension, state the target, classify the action, cite the evidence, and record information loss or assumptions. Plausible pipelines can yield materially different EEG results. [[S03]](evidence-register.md#s03) [[S19]](evidence-register.md#s19)

## Classification test

1. Classify as `must_harmonize` only when incompatible representations make the specified comparison undefined or the software contract cannot operate. Examples include reconciling physical units before combining amplitudes, using compatible event semantics for the same condition, and bringing reference representations into a declared common space when comparing reference-dependent quantities. [[S01]](evidence-register.md#s01) [[S08]](evidence-register.md#s08)
2. Classify as `may_harmonize` when an intervention could improve comparability but changes, discards, or models information. Filtering to a common passband, resampling, channel intersection, montage interpolation, and common artifact handling usually belong here until the objective makes them necessary. [[S07]](evidence-register.md#s07) [[S09]](evidence-register.md#s09) [[S19]](evidence-register.md#s19)
3. Classify as `cannot_harmonize` when acquisition information is absent or irreversible information loss prevents a defensible transformation. Unknown hardware filters, missing electrodes outside recoverable support, clipped samples, and incompatible/undefined event meanings cannot be repaired by relabeling. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03)

## Required dimensions

| Dimension | Questions the contract must answer |
|---|---|
| Identity/version | Are datasets and recordings immutable and traceable to source commits, versions, or hashes? [[S05]](evidence-register.md#s05) [[S06]](evidence-register.md#s06) |
| Units/scaling | Are physical units known and convertible without guessing? [[S01]](evidence-register.md#s01) |
| Temporal support | What bandwidth, sample rate, latency precision, and segment boundaries does the endpoint require? [[S09]](evidence-register.md#s09) [[S27]](evidence-register.md#s27) |
| Events | Do labels, onsets, durations, clocks, and condition meanings denote comparable phenomena? [[S01]](evidence-register.md#s01) [[S29]](evidence-register.md#s29) |
| Channels/electrodes | Is comparison defined on native intersection, target montage, regions, or channel-independent features? [[S01]](evidence-register.md#s01) [[S07]](evidence-register.md#s07) |
| Reference/rank | Are data in a declared compatible representation and are dependencies tracked? [[S08]](evidence-register.md#s08) |
| Artifact policy | Does cleaning preserve the endpoint, and will alternatives be checked where evidence is conditional? [[S18]](evidence-register.md#s18) [[S19]](evidence-register.md#s19) |
| Evaluation split | What independent unit—sample, trial, run, session, participant, or site—matches deployment, and where is adaptive fitting allowed? [[S20]](evidence-register.md#s20) [[S21]](evidence-register.md#s21) [[S22]](evidence-register.md#s22) |

## Contract record

For each row in `harmonization_decisions`, include `dimension`, `classification`, `observed_state`, `target_state`, `decision`, `rationale`, `information_loss`, `alternatives`, `evidence_ids`, and `validation`. Provenance needs explicit entities and activities; COBIDAS requires parameters and deviations sufficient to evaluate the processing. [[S03]](evidence-register.md#s03) [[S05]](evidence-register.md#s05)

When a `may_harmonize` choice could affect the conclusion, predeclare at least one sensitivity branch or provide a justified reason it is out of scope. Multiverse evidence shows that seemingly reasonable preprocessing variants can alter outcomes. [[S19]](evidence-register.md#s19)

When a dimension is `cannot_harmonize`, narrow the comparison, model dataset/site as part of the design, stratify results, or stop. Do not convert an unrecoverable difference into an undocumented batch effect. [[S03]](evidence-register.md#s03) [[S19]](evidence-register.md#s19)
