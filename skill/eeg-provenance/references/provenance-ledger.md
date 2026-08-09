# Provenance ledger

Use the ledger only for **execute** mode. Inspect mode returns a bounded finding; design mode returns a planned contract. The ledger records an auditable processing graph using W3C PROV's Entity–Activity–Agent pattern, but its JSON schema is project-specific and does not claim PROV-O conformance. BIDS derivatives must independently satisfy the applicable BIDS requirements. (Evidence: S05, S23; local workflow policy)

## Identity and contract

Record stable dataset, recording, and input-entity IDs; release/commit and source URI; protected source root; immutable relative paths; checksums or annex keys; BIDS version when applicable; and whether acquisition history is known, partial, or unknown. A checksum identifies bytes, not acquisition or prior-processing history. (Evidence: S01, S03, S05, S06)

Record the endpoint, required band and timing/spatial support, generalization unit, split policy, invariants, applicable harmonization decisions, and only the toolchain phases actually reached. Leave harmonization decisions empty when no alignment was proposed rather than inventing one. Each tool decision needs a stable `id`, status, observation level, hard constraints, preferences, candidates, and an explicit `failure_policy`. Use `fallback_condition=null` when the policy is `stop`. (Evidence: S03, S05, S20, S24; local provenance policy)

## Decisions and activities

Give each candidate a stable `id`, exact tool/version, availability, capability, read/write scope, status, reason, and evidence IDs. Use decision status `selected` only with a verified selected candidate, `planned` for an unexecuted route, and `stopped` when no route passes. Do not create an activity for a planned or stopped decision. (Evidence: S05, S24, S47, S53; local provenance policy)

Every activity must reference the exact `toolchain_decision_id` and `tool_candidate_id` it executed. Its recorded software name/version must match that selected candidate. Also record order, parameters, fit scope, input/output entities, channel effect, sampling rate, shape, units, reference, rank where relevant, and evidence. This closes the link between a phase-level choice and the operation that actually ran. (Evidence: S03, S05, S08, S20; local provenance policy)

Use `fit_scope="none"` only for fixed operations with no estimated state. In predictive work, adaptive artifact handling, decomposition, normalization, and learned transforms must use `training_only` or `within_train_fold`. Record channel-state transitions and rank for dropping, interpolation, rereferencing, and virtual-channel construction. (Evidence: S07, S08, S12, S17, S20)

## QC, outputs, and limitations

Record consequences appropriate to the contract: retained duration/epochs, rejected spans, channel states, event counts, sampling/filter behavior, fitted-model diagnostics, rank, and sensitivity branches. For every output, record its external path/URI, media type, bytes, checksum, source entity, and generating activity. Keep outputs outside the protected source tree. (Evidence: S03, S05, S19, S23)

Keep unresolved acquisition reference, hardware filtering, event meaning, geometry, or missing channels as limitations with affected inference, mitigation, and severity. Do not rewrite unknowns as completed harmonization. (Evidence: S01, S03)

## Validation

Run:

```bash
python scripts/validate_ledger.py ledger.json
```

The CLI first validates the complete document against canonical Draft 2020-12 schema `1.2.0`, including types, enums, required fields, unexpected fields, decision-state conditions, and date-time format. Only schema-valid documents proceed to semantic checks for registered evidence, unique graph IDs, decision/candidate/activity links, exact executed software, source/output separation, activity ordering, rank accounting, and adaptive fit scope. A successful check establishes these local invariants, not scientific validity. (Evidence: S03, S05, S08, S20, S47; local validation policy)
