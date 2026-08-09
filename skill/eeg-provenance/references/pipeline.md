# EEG processing pipeline

Use this page as the stable process architecture. Enter at the first stage
needed by the request, leave after the last needed stage, and select tools only
after the active stage's semantic contract is clear. A stage may be inspected,
designed, executed, or skipped; this is not a mandatory end-to-end pipeline.
[[S03]](evidence-register.md#s03) [[S05]](evidence-register.md#s05)
[[S57]](evidence-register.md#s57)

## Contents

- [Use one stage at a time](#use-one-stage-at-a-time)
- [Operation record](#operation-record)
- [Observation ladder](#observation-ladder)
- [Hard gates and tool choice](#hard-gates-and-tool-choice)
- [Resolve and acquire](#resolve-and-acquire)
- [Inspect](#inspect)
- [Normalize representation](#normalize-representation)
- [Temporal operations](#temporal-operations)
- [Spatial operations](#spatial-operations)
- [Segment or window](#segment-or-window)
- [Construct labels or tasks](#construct-labels-or-tasks)
- [Fit adaptive operations](#fit-adaptive-operations)
- [Cache and hand off](#cache-and-hand-off)
- [QC and close](#qc-and-close)
- [Evidence lookup](#evidence-lookup)

## Use one stage at a time

For a light Inspect request, name the intent and observation level, use the one
obvious safe tool when there is one, and report the finding. Do not create
records for acquisition, preprocessing, caching, or QC that the request never
reaches. Compare candidates only when their semantic coverage, side effects, or
verified availability could change the answer. [[S05]](evidence-register.md#s05)
[[S57]](evidence-register.md#s57)

For Design or Execute, choose one current stage and complete its operation
record before loading an implementation reference. Preserve upstream outputs as
inputs rather than silently folding several representation changes into one
framework call. [[S03]](evidence-register.md#s03)
[[S05]](evidence-register.md#s05)

## Operation record

Record only fields relevant to the active operation:

| Field | Required meaning |
|---|---|
| `intent` | The single question or transformation this operation answers. |
| `input -> output` | Entity/representation before and after; include axes, units, support, timing, labels, and product stage that change. |
| `assumptions` | Required source facts, endpoint constraints, and unresolved conflicts. |
| `read/write scope` | Network, metadata, samples, mutation, cache, temporary, and derivative effects. |
| `fit_state` | `none`, `training_only`, `within_train_fold`, or an explicitly justified alternative. |
| `implementation` | Exact tool/version/API and why its contract matches this operation. |
| `parameters` | Complete effective arguments, defaults accepted deliberately, seed, and fitted-state identity. |
| `QC/stop` | Observable consequences, comparison or tolerance, and the condition that blocks this operation. |
| Evidence | S03, S05, S20, S23 |

These fields operationalize reproducible method reporting and entity/activity
provenance; a successful function call is not itself evidence that the source
semantics or scientific choice were valid. [[S03]](evidence-register.md#s03)
[[S05]](evidence-register.md#s05)

## Observation ladder

| Level | Maximum permitted observation | Typical implementation group |
|---|---|---|
| `catalogue` | Provider records, releases, accessions, selectors; no payload | [Data access](tools-data-access.md) |
| `tree_and_sidecars` | Tree, README, TSV/JSON, manifest, annex availability | [Data access](tools-data-access.md) |
| `native_header` | One container header and bounded companions | [Data access](tools-data-access.md) |
| `lazy_signal` | Normalized lazy recording and annotations | [MNE signal](tools-signal.md) or [EEGLAB](tools-eeglab.md), after format-specific access checks |
| `bounded_samples` | Declared channels and time span for verification | [MNE signal](tools-signal.md) or [EEGLAB](tools-eeglab.md) |
| `full_execution` | Authorized transforms, examples, caches, and export | [MNE signal](tools-signal.md), [EEGLAB](tools-eeglab.md), or [framework integrations](tools-frameworks.md) |
| Evidence | S23, S27, S52, S63 | S24, S27, S31, S52–S53, S63 |

Do not escalate because a higher-access framework is installed. In particular,
dataset construction can retrieve samples, normalize a representation, fit
processors, or create caches. [[S23]](evidence-register.md#s23)
[[S31]](evidence-register.md#s31) [[S44]](evidence-register.md#s44)
[[S52]](evidence-register.md#s52) [[S53]](evidence-register.md#s53)

## Hard gates and tool choice

Reject a candidate at the first gate it cannot pass. [[S03]](evidence-register.md#s03)
[[S20]](evidence-register.md#s20) [[S23]](evidence-register.md#s23)
[[S50]](evidence-register.md#s50)

| Gate | Proof needed for the active operation |
|---|---|
| Identity | Exact provider/release/recording and input entity are resolved. |
| Semantics | Required units, axes, events, reference, geometry, hierarchy, and prior processing survive or remain separately available. |
| Side effects | Reads, network, mutation, indexes, cache, conversions, and writes are known and authorized. |
| Execution | Installed version/signature/entry points and a harmless operation-level smoke test are verified when execution is claimed. |
| Scale | Selected bytes, expansion, space, authentication, restart, and durable lifetime fit the task. |
| Evaluation | Baked transforms, learned state, labels, windows, and grouping respect the declared generalization split. |
| Evidence | S03, S20, S23, S50 |

Preferences rank only surviving candidates. Prefer the least access and fewest
untracked representation changes that meet the current intent. A stopped stage
does not need a fictional fallback; a fallback must repeat every gate.
[[S03]](evidence-register.md#s03) [[S20]](evidence-register.md#s20)
[[S23]](evidence-register.md#s23) [[S50]](evidence-register.md#s50)

## Resolve and acquire

**Input -> output:** accession, provider record, or access grant -> pinned source
identity plus a bounded content manifest in a protected source or authorized
cache. Preserve `ds*`, `nm*`, and `on*` as provider-routing clues, not ownership
or URL templates. Select transport only after version, desired objects, access
terms, resumability, and write boundary are known. Use
[data access implementations](tools-data-access.md). Fit state is `none`; QC is
identity, manifest, availability, and content verification. [[S37]](evidence-register.md#s37)
[[S50]](evidence-register.md#s50) [[S51]](evidence-register.md#s51)

## Inspect

**Input -> output:** protected source -> observations, conflicts, and unknowns at
the least sufficient level. Use provider metadata and sidecars before headers,
headers before lazy signals, and bounded samples only when the question requires
them. A reader field is a container observation until reconciled with release
documentation. Use [data access implementations](tools-data-access.md) for
catalogue/tree/header work. For a lazy processing view, select [MNE
signal](tools-signal.md), or [EEGLAB](tools-eeglab.md) only after its exact
format importer proves the required access level. Fit state is `none`; QC
compares independent metadata layers without treating reader agreement as
historical proof. [[S03]](evidence-register.md#s03)
[[S42]](evidence-register.md#s42) [[S43]](evidence-register.md#s43)
[[S63]](evidence-register.md#s63)

## Normalize representation

**Input -> output:** native container plus companion metadata -> a declared MNE
`Raw`, EEGLAB `EEG`, or other processing representation. Record native fields
omitted or normalized, applied sidecars, preload state, events/annotations,
channel order/types/units/reference, and object mutation/copy behavior. Do not
use a training framework merely to obtain a header or imply that normalized
names/types are publisher semantics. Select exactly one representation guide:
[MNE signal](tools-signal.md) or [EEGLAB EEG/STUDY](tools-eeglab.md).
[[S24]](evidence-register.md#s24) [[S26]](evidence-register.md#s26)
[[S27]](evidence-register.md#s27) [[S62]](evidence-register.md#s62)
[[S63]](evidence-register.md#s63)

## Temporal operations

**Input -> output:** declared signal representation -> cropped, unit-normalized,
filtered, notched, or resampled representation plus updated event timing. Read
[preprocessing interventions](preprocessing-interventions.md), then use
[MNE signal operations](tools-signal.md) or [EEGLAB core/plugin
operations](tools-eeglab.md), matching the current representation. Fixed,
predeclared parameters have no fit state; data-chosen bands, thresholds, or
branches are adaptive. Record the effective filter response, boundaries,
preload/mutation, old/new rate, anti-alias route, and event-sample differences.
[[S09]](evidence-register.md#s09)
[[S10]](evidence-register.md#s10) [[S20]](evidence-register.md#s20)
[[S27]](evidence-register.md#s27)

## Spatial operations

**Input -> output:** channels, reference, and geometry -> a declared channel
support/reference with every native, bad, dropped, virtual, or interpolated
state preserved. Read [channels and montages](channels-montages.md), then use
[MNE signal operations](tools-signal.md) or [EEGLAB core/plugin
operations](tools-eeglab.md). Record equations or donors, geometry source/frame,
bad-channel disposition, projection/application mode, and rank before/after.
Geometry or reference ambiguity blocks only the affected spatial operation.
[[S07]](evidence-register.md#s07) [[S08]](evidence-register.md#s08)
[[S28]](evidence-register.md#s28)

## Segment or window

**Input -> output:** continuous/trial-delimited representation plus boundary
source -> explicit examples with parent IDs, sample bounds, target source, and
rejection state. Use direct MNE/EEGLAB epochs for conventional event-locked
analysis and a framework window primitive only when its downstream dataset
contract is wanted. Record rounding, offsets, stride, overlap, final-window
rule, baseline, and deferred rejection/materialization. Use
[MNE signal](tools-signal.md), [EEGLAB](tools-eeglab.md), or [framework
integrations](tools-frameworks.md), matching the desired output representation.
Fixed bounds are stateless; data-selected examples or rejection are adaptive.
[[S20]](evidence-register.md#s20) [[S27]](evidence-register.md#s27)
[[S52]](evidence-register.md#s52) [[S53]](evidence-register.md#s53)

## Construct labels or tasks

**Input -> output:** publisher events/records plus declared endpoint -> explicit
labels and grouping fields. Software mappings encode, but do not establish,
experimental meaning. Record protocol evidence, event/task map, excluded and
missing events, response contamination policy, subject/session groups, and any
learned vocabulary or encoder. Prefer the lightest mapping that represents the
endpoint; use [framework integrations](tools-frameworks.md) only when its whole
task/sample contract is intended. [[S20]](evidence-register.md#s20)
[[S21]](evidence-register.md#s21) [[S22]](evidence-register.md#s22)
[[S29]](evidence-register.md#s29)

## Fit adaptive operations

**Input -> output:** training entities -> reusable fitted state, then unchanged
state applied to validation/test entities. This includes ICA, learned bad-channel
or rejection thresholds, artifact models, normalizers, vocabularies, and any
data-driven branch. Preserve training IDs, grouping/split, algorithm, seed,
selection scope, fitted-object identity/hash, and application compatibility.
Read [preprocessing interventions](preprocessing-interventions.md), then use
[MNE signal](tools-signal.md), [EEGLAB/plugin](tools-eeglab.md), or [framework
integrations](tools-frameworks.md). If an EEGLAB extension is selected, resolve
its distribution and computational entry point before fitting. Reject a bundled
cache/task route whose fit population cannot match the generalization contract.
[[S12]](evidence-register.md#s12)
[[S17]](evidence-register.md#s17) [[S20]](evidence-register.md#s20)
[[S21]](evidence-register.md#s21) [[S53]](evidence-register.md#s53)
[[S64]](evidence-register.md#s64) [[S65]](evidence-register.md#s65)

## Cache and hand off

**Input -> output:** processed entities and fitted state -> durable derivative or
model-ready cache with axes, units, labels, grouping, split identity, source
lineage, schema/version, and completion state. Build a framework cache only
when the downstream consumer needs that representation; otherwise keep the
simpler signal derivative. Preflight space, overwrite/reuse, partial recovery,
permissions, and lifetime. Use [framework integrations](tools-frameworks.md) or
[MNE signal](tools-signal.md)/[EEGLAB](tools-eeglab.md) export behavior.
[[S05]](evidence-register.md#s05)
[[S23]](evidence-register.md#s23) [[S44]](evidence-register.md#s44)
[[S52]](evidence-register.md#s52) [[S53]](evidence-register.md#s53)

## QC and close

QC belongs to the operation that creates a consequence, followed by an
independent handoff summary: source/output inventories, retention, channel and
rank transitions, event timing, effective temporal response, non-finite data,
fitted-state scope, cache completeness, and endpoint-sensitive alternatives.
Do not convert descriptive diagnostics into universal pass thresholds. For
cross-source work, read [harmonization](harmonization.md) before claiming a
common representation. [[S03]](evidence-register.md#s03)
[[S17]](evidence-register.md#s17) [[S18]](evidence-register.md#s18)
[[S19]](evidence-register.md#s19)

## Evidence lookup

The implementation references cite stable IDs. Query only the active IDs rather
than loading the full [evidence register](evidence-register.md):

```bash
python scripts/evidence_lookup.py S03 S20 S52
```
