# EEGLAB and MATLAB recipes

These recipes target EEGLAB’s documented `EEG` structure and function layers. Record MATLAB, EEGLAB, and plugin versions plus the executed command history; `pop_` functions and `EEG.history` support reproducible scripting but do not replace a provenance ledger. [[S03]](evidence-register.md#s03) [[S24]](evidence-register.md#s24)

## Start without GUI and verify plugins

```matlab
addpath(eeglabRoot)
[ALLEEG, EEG, CURRENTSET, ALLCOM] = eeglab("nogui"); %#ok<ASGLU>
assert(~isempty(which("pop_loadset")))
assert(~isempty(which("eeg_checkset")))
assert(~isempty(which("pop_importbids")))
```

`eeglab("nogui")` is appropriate for automation, while function availability and behavior depend on the installed EEGLAB/plugin versions. Capture `eeg_getversion`, `version`, `which`, and plugin commit/release identifiers. [[S24]](evidence-register.md#s24) [[S25]](evidence-register.md#s25)

## Load a SET dataset read-only

```matlab
EEG = pop_loadset("filename", setName, "filepath", setFolder, "loadmode", "info");
EEG = eeg_checkset(EEG);
```

Use `loadmode="info"` for intake when sample access is not yet needed, then confirm channel count, sampling rate, points, trials, units/reference metadata, events, channel locations, and external `.fdt` dependencies. EEGLAB consistency checks validate structure, not acquisition history or scientific suitability. [[S03]](evidence-register.md#s03) [[S24]](evidence-register.md#s24)

## Import BIDS outside the source tree

```matlab
sourceRoot = string(java.io.File(bidsRoot).getCanonicalPath());
outputRoot = string(java.io.File(derivativeRoot).getCanonicalPath());
assert(~startsWith(outputRoot, sourceRoot + filesep), ...
    "Derivative output must be outside the BIDS source tree")

[STUDY, ALLEEG] = pop_importbids(bidsRoot, ...
    "outputdir", derivativeRoot);
```

Never place `outputdir` inside the BIDS archive: the EEG-BIDS documentation warns that importer-generated STUDY files can break the archive’s BIDS conformance. Treat imports as derivatives and retain source identifiers. [[S23]](evidence-register.md#s23) [[S25]](evidence-register.md#s25)

## Apply explicit filters and reference

```matlab
EEG = pop_eegfiltnew(EEG, 1.0, 40.0, [], 0, [], 0);
EEG = pop_reref(EEG, []);  % Example only: average reference.
EEG = eeg_checkset(EEG);
```

Replace example cutoffs/reference with the contract. Record complete arguments, actual filter design/version, original and new reference, excluded/bad channels, channel support, and rank because these transformations affect temporal/spatial representation. [[S08]](evidence-register.md#s08) [[S09]](evidence-register.md#s09) [[S24]](evidence-register.md#s24)

## Interpolate with channel-location provenance

```matlab
originalChanlocs = EEG.chanlocs;
badIdx = find(ismember({EEG.chanlocs.labels}, badLabels));
EEG = pop_select(EEG, "nochannel", badIdx);
EEG = pop_interp(EEG, originalChanlocs, "spherical");
EEG = eeg_checkset(EEG);
```

Retain original channel locations and bad labels, record the exact removed support and method, and mark reconstructed outputs as `interpolated`. Spherical interpolation estimates scalp potentials under geometry-dependent assumptions. [[S07]](evidence-register.md#s07) [[S24]](evidence-register.md#s24)

## ICA and ICLabel

```matlab
EEG = pop_runica(EEG, "icatype", "runica", "extended", 1, ...
    "randomseed", 97);
EEG = pop_iclabel(EEG, "default");
```

Record ICA training filters, reference, channels/order, rank, component count, algorithm, seed, convergence, ICLabel plugin/version, class probabilities, reviewer decisions, and removed components. ICLabel is probabilistic and its applicability depends on compatible decomposition/preprocessing. [[S12]](evidence-register.md#s12) [[S13]](evidence-register.md#s13) [[S15]](evidence-register.md#s15)

Do not remove components solely because a label wins the argmax; declare thresholds/rules and evaluate signal preservation against the endpoint. Artifact removal has not shown consistent decoding benefit across evaluated settings. [[S13]](evidence-register.md#s13) [[S18]](evidence-register.md#s18)

## Verify the execution environment

Before accessing data through an available MATLAB integration, perform a harmless version query and confirm that the required EEGLAB and plugin functions resolve. Treat a missing or unverified integration as a design-only path rather than claiming that EEGLAB execution occurred. [[S24]](evidence-register.md#s24) [[S25]](evidence-register.md#s25) [[S30]](evidence-register.md#s30)

Record the integration/server version, exposed tool names, MATLAB version, EEGLAB and plugin versions, session mode, and telemetry setting when available. These are versioned software facts, not properties of the EEG data. [[S24]](evidence-register.md#s24) [[S30]](evidence-register.md#s30)
