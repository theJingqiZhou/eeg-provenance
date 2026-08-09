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
   outside the source tree. (Evidence: S23, S25)
2. Keep unknown acquisition or preprocessing history unknown while actively
   searching publisher records, release documents, papers, codebooks, and
   conversion code. (Evidence: S01, S03, S06)
3. Preserve representation identity: distinguish channels from electrodes and
   native, bad, missing, dropped, interpolated, and virtual channels. Fit every
   adaptive operation inside the declared training scope. (Evidence: S07, S08,
   S20, S21, S22)
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

1. State the current intent, endpoint, protected source, permitted writes, and
   least sufficient observation level.
2. Read exactly one intake branch: BIDS, non-BIDS, or the short common checklist
   when the source contract is still unknown. Do not preload samples to answer a
   catalogue, tree, sidecar, or native-header question. (Evidence: S01, S23,
   S31, S42, S46)
3. Use the tool selector for the current phase only. Form one or two viable
   candidates first; run a filtered capability probe only when availability or
   version uncertainty changes the choice. On a pinned or unfamiliar Python
   host, apply the runtime matrix before resolving or installing anything.
   Preferences rank candidates only after hard gates pass. (Evidence: S05,
   S24, S47, S52, S53, S58–S61)
4. Before transforming data, use the operation card and then only the selected
   implementation recipe. Record semantic input/output, hidden assumptions,
   mutation/cache behavior, fit state, parameters, and expected QC.
5. Execute within the authorized write boundary. For execute mode, link every
   activity to its selected decision and candidate, then validate the ledger
   with `python scripts/validate_ledger.py ledger.json`.

## Working-set policy

Target `SKILL.md + one intake reference + one decision or implementation
reference` for ordinary work. Do not load both BIDS and non-BIDS branches, local
and remote branches, MNE and EEGLAB recipes, or framework recipes unless the
current task genuinely crosses them. Do not load anatomy guidance without a
source/forward-model endpoint. These are engineering budgets, not scientific
thresholds; revise them through evals. Official skill guidance confirms that
the full `SKILL.md` enters context after activation and recommends progressive
disclosure. (Evidence: S57; local workflow policy)

Never read the full evidence register for a routine claim. Query only the IDs
used by the active reference. (Evidence: S57; local workflow policy)

```bash
python scripts/evidence_lookup.py S03 S20 S52
```

## Resource map

Load only a resource whose condition is true:

- Unknown source contract: [common intake](references/dataset-intake.md).
- BIDS source: [BIDS 1.11.1 EEG contract](references/bids-eeg-1.11.1.md); read
  [BIDS tool recipes](references/tool-recipes-bids.md) only for execution.
- Non-BIDS source: [non-BIDS intake](references/non-bids-intake.md).
- Tool choice: [toolchain selection](references/toolchain-selection.md).
- Pinned, legacy, or conflicting Python stack: [runtime compatibility](references/runtime-compatibility.md).
- Processing primitive choice: [operation semantics](references/operation-semantics.md).
- Channels/reference/interpolation: [channels and montages](references/channels-montages.md).
- Cross-source alignment: [harmonization](references/harmonization.md).
- Filtering/resampling/artifacts: [preprocessing interventions](references/preprocessing-interventions.md).
- MNE implementation: [MNE recipes](references/tool-recipes-mne.md).
- MATLAB/EEGLAB implementation: [EEGLAB recipes](references/tool-recipes-eeglab.md).
- Accession or EEGDash route: [EEGDash recipes](references/tool-recipes-eegdash.md).
- TorchEEG adapter/cache route: [TorchEEG recipes](references/tool-recipes-torcheeg.md).
- Remote or ephemeral compute: [remote cache execution](references/remote-cache-execution.md).
- MRI, BEM, or FEM readiness: [anatomy and forward models](references/anatomy-forward-model.md).
- Execute-mode record: [provenance ledger semantics](references/provenance-ledger.md).
- Claim source details: [evidence register](references/evidence-register.md), accessed
  through `scripts/evidence_lookup.py` rather than loaded wholesale.

Evidence: S24–S31, S37, S42–S61; local routing policy.

## Stop conditions

Stop only the affected phase when identity is ambiguous, required units/types/
reference/events/geometry are unresolved, no candidate passes the hard gates,
adaptive fitting cannot respect the evaluation split, or no safe output boundary
exists. Report what is known, the failed evidence route, and what would unblock
the phase; do not guess or weaken the source boundary. (Evidence: S01, S03, S20,
S23)
