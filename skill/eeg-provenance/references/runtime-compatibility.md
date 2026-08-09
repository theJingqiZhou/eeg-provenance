# Python runtime compatibility

Use this reference when the execution host has a pre-provisioned or pinned Python stack, when a package import/signature differs from a recipe, or before creating any environment. The matrix is a routing aid checked on 2026-08-09, not a universal lock file. [[S58]](evidence-register.md#s58)

The active execution window is **CPython `>=3.10,<3.15`**. Python 3.15 is pre-release and 3.16 is the feature-development branch on the check date; do not put either into an EEG task even when a dependency declares only an open-ended lower bound. Revisit the upper bound only after a final CPython release and the complete selected stack have target-platform wheels and operation-level tests. [[S58]](evidence-register.md#s58)

## Read the existing runtime before resolving

Do not install, upgrade, or import a large framework merely to discover the environment. Inventory the interpreter, virtual-environment boundary, platform/libc/architecture, installed distribution versions, and available environment managers with the standard-library probe. (Evidence: S58, S61; local environment policy)

```bash
python scripts/probe_toolchain.py --intent runtime-compat --compact
```

Run it in the actual login node, batch image, container, notebook kernel, or
remote worker that will execute the phase. `Requires-Python`, classifiers, and
a successful dependency resolution are not proof that compatible wheels,
system libraries, accelerators, plugins, or the required API behavior exist on
that host. Perform a harmless operation-level smoke test before selection.
[[S24]](evidence-register.md#s24) [[S50]](evidence-register.md#s50)
[[S58]](evidence-register.md#s58)

## Support legend and matrix

`E` means exercised by this repository on the named lane; `M` means package
metadata permits a candidate resolution but it still requires a resolver and
smoke test; `X` means package metadata excludes the lane; `?` means the
available metadata is insufficient. Version ceilings are compatibility
anchors, not instructions to upgrade a working environment. [[S58]](evidence-register.md#s58)
[[S59]](evidence-register.md#s59)

| CPython | Core and BIDS anchor | EEG acquisition/processing anchor | State and route |
|---|---|---|---|
| 3.10 | NumPy `<=2.2.6`; SciPy `<=1.15.3`; pandas `2.3.x`; MNE `1.12.x`; MNE-BIDS `<=0.17`; PyBIDS `0.22.x` | MOABB `1.5` and DataLad `1.6`: `M`; EEGDash `0.8.4`: `X`; Braindecode `1.7`: `X` (`1.2` is the last candidate family) | Legacy-only lane: `M`. Keep a sufficient pinned stack; do not modernize it in place. Python 3.10 is security-only and reaches EOL in 2026-10. |
| 3.11 | NumPy `<=2.4.2`; SciPy `<=1.17.1`; pandas `3.0.x`; MNE `1.12.x`; MNE-BIDS `0.19`; PyBIDS `0.22.x` | EEGDash `0.8.4`, MOABB `1.5`, Braindecode `1.7`, DataLad `1.6`: `M`; TorchEEG `1.1.3` with SciPy `1.10.1` and pandas `<3`: `E` only in a separate lane | Broad current candidate: `M`; isolate TorchEEG from the modern MNE/SciPy stack. |
| 3.12 | NumPy `2.0.2`; SciPy `1.18.0`; pandas `3.0.5`; MNE `1.12.1`; MNE-BIDS `0.19.0`; PyBIDS `0.22.0`: `E` | EEGDash `0.8.4`, MOABB `1.5.0`, Braindecode `1.7.0`: `E`; PyHealth `2.0.1`: `E` only in its own tightly pinned environment | Repository reference lane. Reproduce the exact lock for validation; do not force it onto a sufficient server image. |
| 3.13 | Current NumPy/SciPy/pandas/MNE/MNE-BIDS/PyBIDS metadata: `M` | EEGDash `0.8.4`, MOABB `1.5`, Braindecode `1.7`, PyHealth `2.0.1`: `M` | Candidate lane: resolve and exercise the exact CPU/GPU wheels and selected operation. |
| 3.14 | Current core/BIDS metadata: `M`; PyEDFlib `0.1.42`: `?` because it declares no Python floor | MOABB `1.5` and Braindecode `1.7`: `M`; PyHealth `2.0.1`: `X`; EEGDash `0.8.4`: `M` with classifier/wheel coverage requiring verification | Do not default to this lane until every selected binary and adapter passes on the target platform. |

Evidence: S31, S44–S46, S52–S53, S58–S60; local exercised-version record.

## Weak lifecycle preference

After every hard gate passes and an existing sufficient stack has been considered, weakly prefer the newest in-window CPython release whose bugfix period has ended but which is still security-supported. It is a stability tie-breaker, not a compatibility rule: package constraints, target wheels/ABI, accelerator and vendor support, security policy, measured behavior, and the cost of replacing a provisioned environment can override it. On 2026-08-09 this points to Python 3.12; 3.13 and 3.14 remain in bugfix status. Recheck the lifecycle page rather than freezing that choice when 3.13 changes phase. (Evidence: S58; local environment policy)

The package floor is a second gate; it does not replace the per-interpreter
closure above:

| Distribution family | Checked release and Python declaration | Decision consequence |
|---|---|---|
| MNE | `1.12.1`, `>=3.10` | Core readers/processors still admit 3.10, subject to NumPy/SciPy ceilings. |
| MNE-BIDS | `0.19.0`, `>=3.11`; `0.17.0`, `>=3.10` | Keep 0.17 as the 3.10 candidate; do not backport a 0.19 recipe by assumption. |
| PyBIDS | `0.22.0`, `>=3.10` | Python admission does not make it the official BIDS Validator. |
| h5py / pymatreader | `3.16.0` / `1.2.3`, both `>=3.10` | Verify the MAT v7.3 variable/layout operation and binary wheel. |
| PyEDFlib | `0.1.42`, no `Requires-Python` | Treat support as `?` until a wheel/import and bounded native-header read pass. |
| AutoReject / MNE-ICALabel | `0.4.4` / `0.9.0`, both `>=3.10` | Import success does not validate learned thresholds, ICA prerequisites, or model fit scope. |
| DataLad / MOABB | `1.6.1` / `1.5.0`, both `>=3.10` | Probe git-annex and transport separately; verify wrapper release/event semantics. |
| EEGDash / Braindecode | `0.8.4` / `1.7.0`, both `>=3.11` | Exclude their current families from 3.10. |
| PyHealth | `2.0.1`, `>=3.12,<3.14` | Use only 3.12–3.13 and isolate its exact dependency closure. |
| TorchEEG | `1.1.3`, broadly declares `>=3.7` | Ignore the apparent breadth; its old SciPy ceiling and adapter/cache behavior are the effective gates. |

Evidence: S24, S31, S37, S44–S49, S52–S53, S58–S59.

Python 3.9 and older are outside this active matrix because CPython 3.9 is EOL. Preserve an older appliance only for a bounded operation that is already verified; otherwise request a maintained isolated runtime. [[S58]](evidence-register.md#s58)

## Breaking boundaries that affect EEG work

| Boundary | What can break or silently change | Required check |
|---|---|---|
| NumPy 1.x to 2.x | C-ABI compatibility, removed Python/C APIs, and type-promotion behavior; extensions built against 1.x may fail under 2.x | Import every compiled reader/transform and compare dtype plus representative numeric output. [[S60]](evidence-register.md#s60) |
| pandas 2.x to 3.x | Default string inference and Copy-on-Write mutation semantics; adapter metadata/cache code may fail or stop mutating its parent | Exercise dataset discovery, metadata transforms, and cache reopen; avoid chained mutation assumptions. [[S60]](evidence-register.md#s60) |
| MNE-BIDS 0.17 to 0.18+ | Python floor rises from 3.10 to 3.11; installed MNE and BIDS behaviors remain version-coupled | Verify the exact reader/writer signature, inheritance result, and BIDS Validator separately. [[S58]](evidence-register.md#s58) |
| MOABB 1.1 to 1.4+ | The old family constrained NumPy/pandas below 2 and MNE-BIDS below 0.15; the current family requires NumPy 2 and newer MNE/MNE-BIDS | Treat them as different environments and recheck dataset/paradigm event-window semantics. [[S59]](evidence-register.md#s59) |
| Braindecode 0.8 to 1.x | Dataset/preprocessing/window/model APIs and Python/MNE floors changed; even same-named model arguments can drift | Inspect the installed signature/source and test mutation, window end behavior, targets, and save/reload. [[S52]](evidence-register.md#s52) [[S59]](evidence-register.md#s59) |
| PyHealth 1.x to 2.x | Task/processor/cache architecture changed and 2.x tightly pins Python, MNE, NumPy, pandas, and Torch | Never upgrade an existing PyHealth cache in place; isolate 2.x and rebuild a bounded cache from source identity. [[S53]](evidence-register.md#s53) [[S59]](evidence-register.md#s59) |
| EEGDash 0.6/0.8 and backend changes | Python/MNE/MNE-BIDS floors and fetchability/cache behavior differ by release | Recheck provider identity, exact query, backend, cache root, and one-record retrieval. [[S31]](evidence-register.md#s31) [[S59]](evidence-register.md#s59) |
| TorchEEG 1.1.3 | Broad Python metadata hides an old SciPy ceiling and pandas-3-sensitive transitive code | Use a separate reviewed lane and exercise the exact adapter; do not infer archive compatibility from import success. [[S44]](evidence-register.md#s44) [[S59]](evidence-register.md#s59) |
| Binary readers and external tools | PyEDFlib lacks a `Requires-Python` declaration; DataLad metadata does not provide git-annex, network, credentials, or filesystem support | Verify a matching wheel/native header read, and probe external commands and one bounded retrieval independently. [[S37]](evidence-register.md#s37) [[S46]](evidence-register.md#s46) [[S58]](evidence-register.md#s58) |

## Environment decision

1. If the installed stack performs the bounded operation correctly, keep it and record exact versions; a light inspection does not justify an environment rebuild.
2. Prefer an already provisioned module, Conda environment, container, or virtual environment. Create a new lane only for an actual incompatibility.
3. Use the site's approved manager. `uv` is optional, not a prerequisite. If `pip` is selected, invoke it as `python -m pip` inside an authorized isolated environment; never use bare `pip`, mutate a shared base, run an unrequested bulk upgrade, or override `EXTERNALLY-MANAGED`. [[S61]](evidence-register.md#s61)
4. If no writable isolated lane or compatible binary exists, stop the affected execution phase and request a provisioned module/image. Continue any metadata-only work that the existing tools can perform safely.
5. Record the interpreter path, platform/libc/architecture, environment manager or image digest, exact package versions, resolution artifact, smoke test, and operation result in provenance. [[S05]](evidence-register.md#s05)
