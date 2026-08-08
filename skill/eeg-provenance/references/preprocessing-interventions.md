# Preprocessing interventions

Select the smallest set of transformations needed by the stated endpoint. Record “none” as an evaluated option where admissible, because artifact removal and other plausible preprocessing choices do not improve all EEG endpoints consistently. [[S18]](evidence-register.md#s18) [[S19]](evidence-register.md#s19)

## Filtering

State the signal or nuisance targeted, required retained band, filter family, passband/stopband or cutoff definition, transition bandwidth, order/length, phase/direction, padding, segment boundaries, and edge exclusion. These details determine the actual response and are required for interpretation and reproduction. [[S03]](evidence-register.md#s03) [[S09]](evidence-register.md#s09)

Inspect the effective response and time-domain effect on representative signals. High-pass filters can distort transient waveforms and bias ERP amplitude/latency depending on signal and design, so never present a cutoff alone as sufficient specification. [[S09]](evidence-register.md#s09) [[S10]](evidence-register.md#s10)

Fit or choose any data-adaptive filter parameters within the training partition for predictive evaluation. A fixed, predeclared linear filter may be applied identically to all partitions, but choosing it from held-out performance is tuning and must be nested. [[S20]](evidence-register.md#s20) [[S21]](evidence-register.md#s21)

## Line-noise handling

Record the observed mains frequency, nominal acquisition metadata, harmonics, method, bandwidth/model, affected channels/spans, and before/after spectral diagnostics. EEG-BIDS carries power-line and filter metadata, while PREP provides one reproducible baseline rather than a universal mandate. [[S01]](evidence-register.md#s01) [[S04]](evidence-register.md#s04)

Do not assume 50 or 60 Hz from geographic location when recording metadata or spectra conflict; preserve the conflict and stop if it affects the retained band. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03)

## Resampling

Resample only after declaring required bandwidth and timing precision. Record old/new sample rates, anti-alias method, event resampling mode, rounding, and observed event-sample changes. MNE applies anti-alias filtering and warns that resampling can jitter event timing. [[S27]](evidence-register.md#s27)

When analysis is epoch-based and memory permits, consider epoching before resampling to reduce event-timing ambiguity; validate this against boundary handling and the actual software contract. [[S27]](evidence-register.md#s27)

## Baseline and detrending

Record the baseline interval, estimator, per-epoch/per-channel scope, order relative to filtering, and treatment in the statistical model. Conventional subtraction fixes the baseline coefficient, while regression alternatives expose a different assumption. [[S11]](evidence-register.md#s11)

Do not baseline-correct ICA training epochs without checking the decomposition assumptions and installed MNE warning; fit ICA on a compatible continuous or appropriately high-pass-filtered copy when justified, then document how the learned unmixing is transferred. [[S12]](evidence-register.md#s12) [[S14]](evidence-register.md#s14)

## Bad channels and spans

Separate detection from disposition. Record metric, window, threshold, calibration subset, channel type, reviewer, bad span, and whether data were retained, dropped, or interpolated. COBIDAS requires artifact/exclusion reporting, and adaptive threshold methods optimize specific objectives. [[S03]](evidence-register.md#s03) [[S17]](evidence-register.md#s17)

Treat thresholds learned from the dataset as fitted state. For predictive evaluation, learn them within training folds and apply the resulting rule to validation/test data without using held-out outcomes or distribution summaries. [[S17]](evidence-register.md#s17) [[S20]](evidence-register.md#s20)

## ICA

Record the exact training data, filters, reference, channel set/order, bad channels, rank, algorithm, number of components, convergence, random seed, excluded components, labeling evidence, and application target. ICA behavior depends on preprocessing and channel representation. [[S12]](evidence-register.md#s12) [[S14]](evidence-register.md#s14)

Transfer an ICA solution only to data with the same channel identity/order and compatible linear preprocessing/reference; otherwise refit or document why the linear mapping remains valid. Reference and channel transformations change the representation on which the decomposition was fit. [[S08]](evidence-register.md#s08) [[S12]](evidence-register.md#s12)

Treat ICLabel outputs as probabilities/advisory evidence, not automatic truth. Verify compatibility with the documented training conditions, inspect components, declare decision thresholds, and evaluate the endpoint after removal. [[S13]](evidence-register.md#s13) [[S15]](evidence-register.md#s15) [[S18]](evidence-register.md#s18)

## ASR and automated epoch repair/rejection

Record calibration data, thresholds, windowing, maximum repaired channels/components, output data fraction, and diagnostics. ASR and AutoReject are adaptive procedures whose results depend on calibration and objectives. [[S16]](evidence-register.md#s16) [[S17]](evidence-register.md#s17)

Fit calibration and thresholds inside the training partition for predictive evaluation; never let held-out trials determine repairs, rejection thresholds, or component decisions. [[S17]](evidence-register.md#s17) [[S20]](evidence-register.md#s20) [[S21]](evidence-register.md#s21)

## Sensitivity and QC

For each consequential conditional intervention, compare at least the declared primary choice with a defensible alternative on retention, channel/rank transitions, event timing, spectral/temporal distortion, and endpoint stability. Comparative EEG studies show neither a single cleaning method nor a single plausible pipeline dominates across settings. [[S18]](evidence-register.md#s18) [[S19]](evidence-register.md#s19)
