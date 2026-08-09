# Provenance ledger

Use the ledger only for **execute** mode. Inspect mode returns a bounded finding; design mode returns a planned contract. The ledger records an auditable processing graph using W3C PROV's Entity–Activity–Agent pattern, but its JSON schema is project-specific and does not claim PROV-O conformance. BIDS derivatives must independently satisfy the applicable BIDS requirements. (Evidence: S05, S23; local workflow policy)

## Identity and contract

Record stable dataset, recording, and input-entity IDs; release/commit and source
URI; source root and protection state; immutable relative paths; checksums or
annex keys; BIDS version when applicable; and whether acquisition history is
known, partial, or unknown. A checksum identifies bytes, not acquisition or
prior-processing history. (Evidence: S01, S03, S05, S06)

Declare whether the source tree is protected and list narrow authorized output
roots. A protected archive admits no internal writes. When the dataset is
writable and permission is explicit, an authorized BIDS `derivatives/` subtree
may be inside the dataset root; never authorize the dataset root itself.
(Evidence: S23; local write-boundary policy)

Record the endpoint, required band and timing/spatial support, generalization unit, split policy, invariants, applicable harmonization decisions, and only the toolchain phases actually reached. Leave harmonization decisions empty when no alignment was proposed rather than inventing one. Each tool decision needs a stable `id`, status, observation level, hard constraints, preferences, candidates, and an explicit `failure_policy`. Use `fallback_condition=null` when the policy is `stop`. (Evidence: S03, S05, S20, S24; local provenance policy)

## Decisions and activities

Give each candidate a stable `id`, exact tool/version, availability, capability, read/write scope, status, reason, and evidence IDs. Use decision status `selected` only with a verified selected candidate, `planned` for an unexecuted route, and `stopped` when no route passes. Do not create an activity for a planned or stopped decision. (Evidence: S05, S24, S47, S53; local provenance policy)

Every activity must reference the exact `toolchain_decision_id` and `tool_candidate_id` it executed. Its recorded software name/version must match that selected candidate. Also record order, parameters, fit scope, input/output entities, channel effect, sampling rate, shape, units, reference, rank where relevant, and evidence. This closes the link between a phase-level choice and the operation that actually ran. (Evidence: S03, S05, S08, S20; local provenance policy)

For every activity, make `fit_scope` an explicit object: fitted `population`,
`fit_unit`, whether labels or the target distribution were observed, whether
that information was available and authorized before prediction, and where the
state was reused. Use the canonical `not_applicable`/`none` object only for a
fixed operation. Predictive work may legitimately use a training fold,
authorized calibration partition, external pretrained state, or a declared
unlabeled per-recording estimate; the record must expose the distinction rather
than collapse it into “training only.” For descriptive analysis, declare the
population even when no deployment split exists. Record channel-state
transitions and rank for dropping, interpolation, rereferencing, and
virtual-channel construction. (Evidence: S07, S08, S12, S17, S20; local
provenance policy)

## QC, outputs, and limitations

Use the common QC skeleton for machine-readable summaries: status, typed
observations, retention, shape/sampling/channel/event/rank transitions,
warnings, and an `operation_specific` object. Status is relative to the declared
contract and checks; it is not proof of scientific validity. For every output,
record its authorized path/URI, media type, bytes, checksum, source entity, and
generating activity. (Evidence: S03, S05, S19, S23; local QC policy)

Keep unresolved acquisition reference, hardware filtering, event meaning, geometry, or missing channels as limitations with affected inference, mitigation, and severity. Do not rewrite unknowns as completed harmonization. (Evidence: S01, S03)

## Validation

Run:

```bash
python scripts/validate_ledger.py ledger.json
```

The CLI first validates the complete document against canonical Draft 2020-12
schema `2.0.0`, including types, required fields, unexpected fields,
decision-state conditions, structured fit scope/QC, and date-time format. Only
schema-valid documents proceed to semantic checks for registered evidence,
unique graph IDs, decision/candidate/activity links, exact executed software,
authorized output roots, activity ordering, rank accounting, fit availability,
and QC status consistency. A successful check establishes these local
invariants, not scientific validity. (Evidence: S03, S05, S08, S20, S47; local
validation policy)
