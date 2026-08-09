# EEGLAB extensions and plugin operations

Load this page only when an EEGLAB operation needs a non-core importer or
processing extension. Resolve the distribution asset before installation, then
verify the installed entry point and operation behavior independently.
[[S24]](evidence-register.md#s24) [[S64]](evidence-register.md#s64)

## Contents

- [Preflight the capability](#preflight-the-capability)
- [Resolve the distribution asset](#resolve-the-distribution-asset)
- [Install without assuming Git](#install-without-assuming-git)
- [Verify format importers](#verify-format-importers)
- [Run plugin code headlessly](#run-plugin-code-headlessly)
- [Handle adaptive operations](#handle-adaptive-operations)
- [GEDAI extension card](#gedai-extension-card)
- [Record and close](#record-and-close)

## Preflight the capability

Run `scripts/probe_eeglab.m` after `eeglab('nogui')`. Verify the resolved
function path as well as the plugin label: capabilities are extension-defined,
multiple versions can coexist on the MATLAB path, and the registry can differ
from an upstream repository. [[S24]](evidence-register.md#s24)
[[S30]](evidence-register.md#s30) [[S64]](evidence-register.md#s64)

| Capability | Entry points | Typical boundary |
|---|---|---|
| BIDS | `pop_importbids`, `pop_exportbids` | EEG-BIDS |
| BrainVision | `pop_loadbv`, `eegplugin_bva_io` | bva-io |
| EDF/BDF and other BioSig formats | `pop_biosig`, `sopen`, `eegplugin_biosig` | BIOSIG |
| FIF and other FileIO formats | `pop_fileio` | File-IO/FieldTrip integration |
| MEF3 | `pop_MEF3` | MEF3 |
| ICA labels/cleaning/source support | `pop_iclabel`, `pop_clean_rawdata`, `pop_dipfit_settings` | ICLabel, clean_rawdata, DIPFIT |
| GEDAI | `GEDAI`, `pop_GEDAI`, `eegplugin_GEDAI` | GEDAI |
| Evidence | S24, S56, S63–S65 | S64 |

A core wrapper path is insufficient when its backend is an extension. In the
clean exercised installation, `pop_biosig` and `pop_fileio` resolved while
BIOSIG `sopen` and the corresponding plugin records did not. Require both the
wrapper and its backend/dependencies, then run the selected format operation.
[[S24]](evidence-register.md#s24) [[S64]](evidence-register.md#s64)

Stop if the selected function resolves from an unexpected folder, the required
dependency or license is unavailable, or a bounded smoke cannot establish the
operation's payload and write behavior. [[S03]](evidence-register.md#s03)
[[S23]](evidence-register.md#s23) [[S64]](evidence-register.md#s64)

## Resolve the distribution asset

Do not translate “EEGLAB plugin” into `git clone`. Select the exact asset that
the publisher supports for the required release. [[S64]](evidence-register.md#s64)

| Distribution case | Acquisition contract | Identity to record |
|---|---|---|
| EEGLAB registry release | Query the extension manager/`plugin_getweb`, or download its versioned ZIP | Registry name/version, exact URL, retrieval time, byte size, SHA-256 |
| SCCN-hosted upstream repository | Use Git only when the registry/official page identifies a repository and the needed release is represented there | Remote URL, tag/commit, submodules/LFS, tree status |
| Other publisher release | Follow that publisher's archive/package instructions; do not invent a Git remote | Publisher URL, release/archive version, hash, license |
| EEGLAB-bundled/submodule plugin | Use the commit pinned by the EEGLAB release | EEGLAB commit plus plugin submodule commit |
| Evidence | S64 | S56, S64 |

For example, bva-io has both an EEGLAB registry ZIP and an SCCN GitHub
repository; name which one supplied the tested tree. BIOSIG is distributed by
the registry as a versioned archive and by its own project, so an SCCN Git clone
must not be assumed. The official old-version directory is an archive source,
not evidence that its newest file matches the current registry record.
[[S64]](evidence-register.md#s64)

## Install without assuming Git

Use `plugin_askinstall(name, [], true)` only when network access and mutation of
that dedicated EEGLAB installation are authorized. The pinned implementation
downloads the registry ZIP and unpacks it below EEGLAB's `plugins/` directory;
it is unsuitable for a read-only or shared installation. [[S23]](evidence-register.md#s23)
[[S64]](evidence-register.md#s64)

For a headless reproducible environment, download the exact official asset to a
staging directory, compute its hash, inspect archive roots and licenses, extract
into a dedicated EEGLAB copy, restart EEGLAB, and verify the registrar plus
public functions. Never use `addpath(genpath(pluginRoot))` without inspection:
plugin trees can contain compatibility functions that shadow MATLAB/EEGLAB
APIs. Let `eegplugin_*` register intended subpaths, or add only source-reviewed
subdirectories in a disposable session. [[S24]](evidence-register.md#s24)
[[S64]](evidence-register.md#s64)

Do not silently remove or replace another version. Capture `which -all` for
public and dependency functions, then ensure the selected path is first. A
successful startup message is capability discovery, not an operation smoke or
scientific validation. [[S03]](evidence-register.md#s03)
[[S24]](evidence-register.md#s24) [[S64]](evidence-register.md#s64)

## Verify format importers

| Importer | Verification rule |
|---|---|
| bva-io | Verify VHDR/VMRK/data companion resolution, orientation/scaling, events, and whether `pop_loadbv(..., true)` leaves `EEG.data` empty for a synthetic or bounded file. |
| BIOSIG | Verify both EEGLAB `pop_biosig` and lower-level `sopen`/`sread` paths. A header returned by `sopen` is not an EEGLAB `EEG` object, and EEG-BIDS 10.5 calls the full `pop_biosig` route for EDF/BDF. |
| FileIO/other | Inspect the exact wrapper for header versus data access, normalized fields, dependencies, and temporary writes; do not inherit behavior from SET or BrainVision. |
| Evidence | S46, S63–S64 |

The bounded R2026a/bva-io 1.75 ZIP exercise created a synthetic BrainVision
triplet and confirmed that the metadata flag returned correct shape with empty
`EEG.data`. String paths succeeded while character-vector paths hit the active
MATLAB `fileread` argument validator. This is a version-specific compatibility
finding, not a general preference; test the installed release and record the
accepted call. [[S64]](evidence-register.md#s64)

## Run plugin code headlessly

Supply every selector, option, and output path that a wrapper accepts. If it
still opens `inputgui`, inspect the installed `pop_` wrapper and menu callback,
identify the documented public computational function it delegates to, verify
its help/signature, and test disposable input. Do not copy private helpers or
bypass required consistency checks. [[S24]](evidence-register.md#s24)
[[S55]](evidence-register.md#s55) [[S56]](evidence-register.md#s56)
[[S65]](evidence-register.md#s65)

Plugin registrars commonly create menus and are not themselves computational
batch entry points. Record the callable API and effective arguments rather than
a GUI action or a registrar name. [[S24]](evidence-register.md#s24)
[[S64]](evidence-register.md#s64)

## Handle adaptive operations

For the exercised EEGLAB 2026.0.0 route, `pop_runica(..., 'rndreset', 'off',
'interrupt', 'off')` used `runica`'s fixed initialization; `randomseed` was not
a supported `runica` key. Verify other algorithms/releases separately. Record
training representation, channel order/reference/rank, RNG control,
convergence, ICLabel evidence/decision, reviewer, exclusions, and target.
[[S12]](evidence-register.md#s12) [[S13]](evidence-register.md#s13)
[[S15]](evidence-register.md#s15) [[S18]](evidence-register.md#s18)
[[S56]](evidence-register.md#s56)

Treat an extension that estimates thresholds, subspaces, components,
covariances, channel/epoch exclusions, or repair parameters as fitted state.
Registry presence, installability, history, and plugin QC scores do not prove
leakage safety or endpoint superiority. [[S03]](evidence-register.md#s03)
[[S20]](evidence-register.md#s20) [[S21]](evidence-register.md#s21)
[[S64]](evidence-register.md#s64)

## GEDAI extension card

GEDAI is an optional third-party denoising plugin using generalized eigenvalue
decomposition and a theoretical/reference covariance derived from a leadfield.
The registry entry is discovery, not validation; review the primary preprint,
pinned source, dependencies, and noncommercial license.
[[S64]](evidence-register.md#s64) [[S65]](evidence-register.md#s65)

Preflight its reference mode. The exercised source offers `precomputed`
standard-location BEM, an `interpolated` route for current coordinates, a
template FieldTrip/DIPFIT `warped` route, or a custom covariance. A
head-model-informed covariance does not establish participant-specific MRI/BEM
or source-localization readiness. Verify labels, coordinates, model/reference,
support, rank, and dependencies. [[S08]](evidence-register.md#s08)
[[S34]](evidence-register.md#s34) [[S35]](evidence-register.md#s35)
[[S65]](evidence-register.md#s65)

At upstream commit `c48f7d6`, `pop_GEDAI(EEG, varargin)` parses arguments but
still calls `inputgui` unconditionally. For a headless batch, inspect the active
source and call public `GEDAI(...)` with every parameter. Disable visualization
and bound the smoke input. [[S65]](evidence-register.md#s65)

Record threshold mode/value, epoch cycles, low cutoff, reference-matrix mode or
hash, parallel/visualization flags, ENOVA epoch/channel thresholds, signal type,
smoothing window, output reference, removals, and `EEG.etc.GEDAI`. Auto
thresholding and ENOVA exclusions are adaptive; fit inside the declared training
partition for predictive work. [[S05]](evidence-register.md#s05)
[[S20]](evidence-register.md#s20) [[S21]](evidence-register.md#s21)
[[S65]](evidence-register.md#s65)

## Record and close

Capture extension name/version, distribution kind, URL or Git commit, archive
hash, resolved functions, dependencies, license, MATLAB/EEGLAB compatibility,
installed paths, complete call, fit scope, warnings, payload/write observations,
and smoke/QC results. Preserve the downloaded asset or a resolvable identity
according to project policy. [[S03]](evidence-register.md#s03)
[[S05]](evidence-register.md#s05) [[S06]](evidence-register.md#s06)
[[S64]](evidence-register.md#s64)
