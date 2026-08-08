# Provenance ledger

The ledger records an auditable processing graph using W3C PROV’s Entity–Activity–Agent pattern. The JSON schema is project-specific and does not claim PROV-O, BIDS Derivatives, or proposed BIDS-Prov conformance. [[S05]](evidence-register.md#s05) [[S23]](evidence-register.md#s23)

## Identity and source entities

Assign a stable `ledger_id` and timestamp. Record dataset/recording identifiers, version/commit, source URI, immutable relative paths, checksums or annex keys, BIDS version, and whether acquisition history is `known`, `partial`, or `unknown`. Persistent identities, rich metadata, and source relations support reuse and change detection. [[S05]](evidence-register.md#s05) [[S06]](evidence-register.md#s06)

Do not hash only a mutable path or use the derivative’s hash as proof of acquisition history. A checksum identifies bytes, while acquisition and prior processing require separate metadata evidence. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03)

## Objective and contract

Record the analysis goal, endpoint, required band, timing precision, spatial support, generalization unit, split policy, invariants, and every harmonization decision. This connects preprocessing choices to the question they are intended to support and exposes conditional alternatives. [[S03]](evidence-register.md#s03) [[S19]](evidence-register.md#s19) [[S20]](evidence-register.md#s20)

Each decision includes `classification`, `rationale`, `evidence_ids`, `information_loss`, and `validation`. Use evidence-register IDs rather than free-floating URLs so claims remain auditable. [[S03]](evidence-register.md#s03) [[S06]](evidence-register.md#s06)

## Activities

Create one ordered activity per intervention, including inspection steps that generated authoritative derived metadata. Record start/end time, code/command, executing agent, software versions, parameters, random seed, fit scope, input/output entity IDs, channel-state changes, sampling rate, shape, units, reference, and rank before/after. PROV distinguishes used and generated entities; COBIDAS requires software and processing details. [[S03]](evidence-register.md#s03) [[S05]](evidence-register.md#s05)

Use `fit_scope="none"` for fixed transforms with no estimated state, `training_only` for adaptive operations in predictive evaluation, and an explicit descriptive scope for non-predictive analyses. Adaptive artifact thresholds and decompositions are fitted procedures and must follow the evaluation split when estimating generalization. [[S12]](evidence-register.md#s12) [[S17]](evidence-register.md#s17) [[S20]](evidence-register.md#s20)

When an activity changes channel representation, include every state transition and rank estimate. Rereferencing, virtual-channel construction, dropping, and interpolation can alter dependence and spatial meaning. [[S07]](evidence-register.md#s07) [[S08]](evidence-register.md#s08)

## QC and outputs

Record retained duration/epochs, rejected spans, bad/interpolated/dropped channels, event count/sample changes, sampling-rate changes, filter-response evidence, component/reconstruction diagnostics, rank changes, and sensitivity branches appropriate to the contract. Reporting both intervention and consequence supports evaluation; plausible choices can change results. [[S03]](evidence-register.md#s03) [[S19]](evidence-register.md#s19)

For every output, record path/URI, media type, bytes, checksum, source entity, generating activity, and BIDS-derivative identifiers when used. Keep the output root outside the source tree. [[S05]](evidence-register.md#s05) [[S23]](evidence-register.md#s23)

## Limitations

List unresolved metadata, assumption, affected inference, mitigation/sensitivity test, and severity. Unknown hardware filtering, acquisition reference, event meaning, or unrecoverable channels must remain limitations rather than being rewritten as completed harmonization. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03)

## Validation

Run `python scripts/validate_ledger.py ledger.json`. The validator checks project invariants beyond JSON shape, including unique IDs, source/derivative separation, evidence-ID syntax, channel-state vocabulary, activity links/order, mandatory rank accounting for spatial transforms, and training-only fit scope for adaptive predictive processing. These are local safeguards motivated by provenance, reference/rank, and leakage evidence. [[S05]](evidence-register.md#s05) [[S08]](evidence-register.md#s08) [[S20]](evidence-register.md#s20)
