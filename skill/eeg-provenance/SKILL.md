---
name: eeg-provenance
description: Provenance-aware EEG data intake, acquisition/tool selection, preprocessing, QC, and auditable handoff for BIDS and documented non-BIDS EDF/GDF/MAT/CNT/SET. Use for OpenNeuro/NeMAR ds*/nm*/on* accessions, release-metadata recovery, BIDS inheritance, source-safe local or remote caches, pinned or legacy Python compatibility, MNE/EEGLAB or dataset-framework routing, and decisions about channels, reference, filters, artifacts, resampling, epochs/windows, labels, and adaptive fit scope. Not for clinical interpretation or decoder/model selection.
---

# EEG Provenance

Build the smallest evidence-backed workflow that answers the current EEG data
question. Escalate from inspection to transformation only when the requested
endpoint needs it. (Evidence: S57; local workflow policy)

## Kernel invariants

1. Preserve source bytes. Put reports, caches, temporary files, and derivatives
   only in explicitly authorized output roots. If the source tree is protected,
   keep every write outside it; otherwise an authorized BIDS `derivatives/`
   subtree is valid. (Evidence: S23, S25; local write-boundary policy)
2. Keep unknown acquisition or preprocessing history unknown while actively
   searching publisher records, release documents, papers, codebooks, and
   conversion code. (Evidence: S01, S03, S06)
3. Preserve representation identity: distinguish channels from electrodes and
   native, bad, missing, dropped, interpolated, and virtual channels. For
   predictive evaluation, fit adaptive state only from information available
   and authorized before the corresponding prediction. For descriptive work,
   declare the fitted population and reuse scope. (Evidence: S07, S08, S20,
   S21, S22)
4. Reject universal pipelines. Tie each operation to the endpoint, input and
   output semantics, assumptions, side effects, fit state, and QC. (Evidence:
   S03, S18, S19)

## Choose the work mode

- **Inspect** — answer one bounded identity, metadata, header, event, channel,
  or capability question. Return an **Inspection Finding** with observations,
  unknowns, evidence, and the tool/read scope used. Do not create a full ledger
  or enumerate future phases unless requested.
- **Design** — return a **Preprocessing Contract** for the requested endpoint,
  current-phase tool decisions, unresolved facts, alternatives, and stop
  conditions. Mark unexecuted routes `planned`; do not invent QC or outputs.
- **Execute** — return the full **Data Intake Report**, **Preprocessing
  Contract**, and **Provenance Ledger and QC**. Add decisions progressively,
  immediately before each phase is executed.

Evidence: S03, S05; local workflow policy.

Do not silently upgrade modes. A narrow request remains narrow even when a full
dataset is available. (Evidence: S03, S05; local workflow policy)

## Workflow

1. State the current intent, endpoint, source-protection state, authorized
   output roots, and least sufficient observation level.
2. Read exactly one intake branch: BIDS, non-BIDS, or the short common checklist
   while the source contract is unknown. Do not preload samples to answer a
   catalogue, tree, sidecar, or native-header question. (Evidence: S01, S23,
   S31, S42, S46)
3. Enter the process pipeline at the first stage required by the request and
   stop after the last required stage. The stage defines semantic input/output,
   hard gates, fit state, side effects, and QC before a tool is selected. Skip
   irrelevant stages; a bounded inspection need not manufacture a full
   pipeline or candidate matrix. (Evidence: S03, S05, S57; local workflow
   policy)
4. Choose one implementation group from the active pipeline stage. Compare
   candidates only when more than one can materially satisfy the intent. Probe
   availability or behavior only when uncertainty changes the choice. On a
   pinned or unfamiliar Python host, apply the runtime matrix before resolving
   or installing anything. (Evidence: S24, S47, S52, S53, S58–S61)
5. Execute within the authorized write boundary. In Execute mode, link every
   activity to its stage decision and tool candidate, then validate the ledger
   with `python scripts/validate_ledger.py ledger.json`.

## Working-set policy

For ordinary work, target `SKILL.md + one intake branch + pipeline.md`. If the
source type is known, use the common intake page only as a router and replace it
with that branch. Add at most one primary implementation reference for the
active stage; add the EEGLAB-extension page only when that implementation needs
a non-core capability. Do not retain both BIDS and non-BIDS branches, multiple
tool groups, or special branches unless the request genuinely crosses them.
These are engineering budgets, not scientific thresholds; revise them through
evals. Official skill guidance confirms that the full `SKILL.md` enters context
after activation and recommends progressive disclosure. (Evidence: S57; local
workflow policy)

Never read the full evidence register for a routine claim. Query only the IDs
used by the active reference. (Evidence: S57; local workflow policy)

```bash
python scripts/evidence_lookup.py S03 S20 S52
```

## Resource map

Load only a resource whose condition is true:

- Source identity or acquisition: enter the [dataset intake
  router](references/dataset-intake.md), then follow only its matching leaf.
- Processing or tool choice: enter the [pipeline](references/pipeline.md), then
  follow only the active stage's semantic and implementation leaves.
- Pinned, legacy, or uncertain Python host: add [runtime
  compatibility](references/runtime-compatibility.md).
- Execute-mode record: [provenance ledger](references/provenance-ledger.md).
  Citation audit only: [evidence register](references/evidence-register.md).

Evidence: S24–S31, S37, S42–S65; local routing policy.

## Stop conditions

Stop only the affected phase when identity is ambiguous, required units/types/
reference/events/geometry are unresolved, no candidate passes the hard gates,
adaptive fitting cannot respect the evaluation split, or no safe output boundary
exists. Report what is known, the failed evidence route, and what would unblock
the phase; do not guess or weaken the source boundary. (Evidence: S01, S03, S20,
S23)
