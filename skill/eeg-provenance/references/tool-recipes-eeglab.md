# EEGLAB and MATLAB recipes

These recipes target EEGLAB’s documented `EEG` structure and function layers. Record MATLAB, EEGLAB, and plugin versions plus the executed command history; `pop_` functions and `EEG.history` support reproducible scripting but do not replace a provenance ledger. [[S03]](evidence-register.md#s03) [[S24]](evidence-register.md#s24)

## Contents

- [Derive calls from the active EEGLAB release](#derive-calls-from-the-active-eeglab-release)
- [Resolve a non-GUI API](#resolve-a-non-gui-api)
- [Start without GUI and verify plugins](#start-without-gui-and-verify-plugins)
- [Load a SET dataset read-only](#load-a-set-dataset-read-only)
- [Import BIDS outside the source tree](#import-bids-outside-the-source-tree)
- [Apply explicit filters and reference](#apply-explicit-filters-and-reference)
- [Interpolate with channel-location provenance](#interpolate-with-channel-location-provenance)
- [ICA and ICLabel](#ica-and-iclabel)
- [Verify the execution environment](#verify-the-execution-environment)

## Derive calls from the active EEGLAB release

Use the [official EEGLAB tutorials](https://eeglab.org/tutorials/), installed `help`, function signatures, and GUI-generated `eegh`/`EEG.history` as the primary route to version-correct calls. The history tutorial distinguishes session history from dataset history and exposes the actual `pop_` calls issued by the active release. [[S24]](evidence-register.md#s24) [[S55]](evidence-register.md#s55)

[Makoto's useful EEGLAB code](https://eeglab.ucsd.edu/wiki/Makoto%27s_useful_EEGLAB_code) is a practical recipe index, not a parameter authority. For a candidate snippet, record its retrieval/update date, remove machine-specific paths and channel indices, compare the function with installed help/source, replace every heuristic with the preprocessing contract, and exercise it on a disposable or bounded recording before use. Do not inherit its thresholds, reference construction, filter settings, ICA/rank remedies, or recommended step order without endpoint-specific evidence and QC. [[S19]](evidence-register.md#s19) [[S55]](evidence-register.md#s55)

## Resolve a non-GUI API

Supply every selector, option, and output path required by a `pop_` function so omission does not open an input dialog. When a wrapper has no complete non-GUI path, inspect the installed wrapper and its menu callback to identify the public function it delegates to; verify that function's installed help and signature, call it on a disposable input, and record the representation handoff. Do not copy a private helper or bypass consistency checks merely to suppress a GUI. [[S24]](evidence-register.md#s24) [[S55]](evidence-register.md#s55) [[S56]](evidence-register.md#s56)

Treat EEGLAB's text interface as release-specific. Prefer character vectors for legacy `pop_` keys, filenames, and option values unless the installed function is verified with MATLAB string scalars. EEGLAB 2026.0.0 and EEG-BIDS 10.5 accepted a fully parameterized headless route, but exposed string-versus-character and run-selector mismatches described below; do not project those details onto another release without re-running the probe. [[S24]](evidence-register.md#s24) [[S25]](evidence-register.md#s25) [[S56]](evidence-register.md#s56)

## Start without GUI and verify plugins

```matlab
addpath(char(eeglabRoot))
[ALLEEG, EEG, CURRENTSET, ALLCOM] = eeglab('nogui'); %#ok<ASGLU>
assert(~isempty(which('pop_loadset')))
assert(~isempty(which('eeg_checkset')))
assert(~isempty(which('pop_importbids')))
assert(~isempty(which('eegh')))
```

`eeglab('nogui')` is appropriate for automation, while function availability and behavior depend on the installed EEGLAB/plugin versions. A source checkout whose plugin folder has no version suffix can be displayed as `v?` in no-GUI startup even when its entry points work; obtain versions from a verified plugin API, a normal plugin initialization, and the pinned source commit rather than inferring them from that display alone. Capture `eeg_getversion`, `version`, `which`, and plugin commit/release identifiers. [[S24]](evidence-register.md#s24) [[S25]](evidence-register.md#s25) [[S56]](evidence-register.md#s56)

## Load a SET dataset read-only

```matlab
EEG = pop_loadset('filename', char(setName), ...
    'filepath', char(setFolder), 'loadmode', 'info');
EEG = eeg_checkset(EEG);
```

Use `loadmode='info'` for intake when sample access is not yet needed, then confirm channel count, sampling rate, points, trials, units/reference metadata, events, channel locations, and external `.fdt` dependencies. EEGLAB consistency checks validate structure, not acquisition history or scientific suitability. [[S03]](evidence-register.md#s03) [[S24]](evidence-register.md#s24)

## Import BIDS outside the source tree

```matlab
sourceRoot = string(bidsRoot);       % Resolve to an absolute path first.
outputRoot = string(derivativeRoot); % Resolve to an absolute path first.
assert(isfolder(sourceRoot) && isfolder(outputRoot), ...
    'Resolve source and output folders first')
assert(~startsWith(lower(outputRoot), lower(sourceRoot + filesep)), ...
    'Derivative output must be outside the BIDS source tree')

selectorArgs = { ...
    'subjects', {char(subjectLabel)}, ...
    'runs', {char(runLabel)}, ...
    'bidstask', char(taskLabel), ...
    'bidsevent', 'on', ...
    'bidschanloc', 'on' ...
};
[STUDY, ALLEEG] = pop_importbids(char(bidsRoot), ...
    selectorArgs{:}, ...
    'metadata', 'off', ...
    'outputdir', char(derivativeRoot), ...
    'studyName', char(studyName));
assert(numel(ALLEEG) == 1, 'The bounded selector must resolve once')
```

Never place `outputdir` inside the BIDS archive: the EEG-BIDS documentation warns that importer-generated STUDY files can break the archive’s BIDS conformance. Treat imports as derivatives and retain source identifiers. [[S23]](evidence-register.md#s23) [[S25]](evidence-register.md#s25)

In the exercised EEG-BIDS 10.5 source, a numeric `runs` value passed its documented input check but later failed in a text `contains` call; a text cell such as `{'1'}` completed the same selection. A MATLAB string-scalar `studyName` later failed in legacy STUDY filename indexing, while a character vector completed the save. These are pinned-release workarounds, not general semantics. Inspect the active source/help and retain the exact accepted call in the ledger. [[S25]](evidence-register.md#s25) [[S56]](evidence-register.md#s56)

Do not interpret EEG-BIDS 10.5 `'metadata','on'` as header-only access. The bounded SET exercise showed that this mode still called `pop_loadset` on the selected payload; it suppressed derivative/STUDY saving but did not preserve the `native_header` observation level. Use catalogue, BIDS query, or format-native header tools when samples must remain inaccessible. [[S25]](evidence-register.md#s25) [[S31]](evidence-register.md#s31) [[S56]](evidence-register.md#s56)

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
EEG = pop_select(EEG, 'nochannel', badIdx);
EEG = pop_interp(EEG, originalChanlocs, 'spherical');
EEG = eeg_checkset(EEG);
```

Retain original channel locations and bad labels, record the exact removed support and method, and mark reconstructed outputs as `interpolated`. Spherical interpolation estimates scalp potentials under geometry-dependent assumptions. [[S07]](evidence-register.md#s07) [[S24]](evidence-register.md#s24)

## ICA and ICLabel

```matlab
EEG = pop_runica(EEG, 'icatype', 'runica', 'extended', 1, ...
    'rndreset', 'off', 'interrupt', 'off');
EEG = pop_iclabel(EEG, 'default');
```

EEGLAB 2026.0.0 `runica` does not expose the previously shown `randomseed` key. Its documented `rndreset='off'` path resets to the same built-in initialization, while `'on'` seeds from the clock; verify a different release or algorithm separately if an arbitrary seed is required. Record the complete RNG control, ICA training filters, reference, channels/order, rank, component count, algorithm, convergence, ICLabel plugin/version, class probabilities, reviewer decisions, and removed components. ICLabel is probabilistic and its applicability depends on compatible decomposition/preprocessing. [[S12]](evidence-register.md#s12) [[S13]](evidence-register.md#s13) [[S15]](evidence-register.md#s15) [[S56]](evidence-register.md#s56)

Do not remove components solely because a label wins the argmax; declare thresholds/rules and evaluate signal preservation against the endpoint. Artifact removal has not shown consistent decoding benefit across evaluated settings. [[S13]](evidence-register.md#s13) [[S18]](evidence-register.md#s18)

## Verify the execution environment

Before accessing data through an available MATLAB integration, perform a harmless version query and confirm that the required EEGLAB and plugin functions resolve. Treat a missing or unverified integration as a design-only path rather than claiming that EEGLAB execution occurred. [[S24]](evidence-register.md#s24) [[S25]](evidence-register.md#s25) [[S30]](evidence-register.md#s30)

Record the integration/server version, exposed tool names, MATLAB version, EEGLAB and plugin versions, session mode, and telemetry setting when available. These are versioned software facts, not properties of the EEG data. [[S24]](evidence-register.md#s24) [[S30]](evidence-register.md#s30)
