# Channels, electrodes, montages, and reference

## Keep four concepts separate

- A **channel** is a recorded or derived signal stream with a type, unit, reference, and status; an **electrode** is a physical contact with a position. BIDS represents them in different files because they need not map one-to-one. [[S01]](evidence-register.md#s01)
- A **montage** in software associates names with locations and coordinate information; it does not prove the recording used those exact positions. Label template coordinates as template-derived and preserve measured coordinates separately. [[S01]](evidence-register.md#s01) [[S28]](evidence-register.md#s28)
- A **reference** defines potential differences and changes the channel representation. Do not compare amplitudes or spatial features across incompatible references without an explicit transformation or limitation. [[S08]](evidence-register.md#s08)
- A **virtual channel** is algebraically constructed; an **interpolated channel** is spatially estimated from other channels. Neither is a native measurement. [[S07]](evidence-register.md#s07) [[S08]](evidence-register.md#s08)

## Channel-state machine

Assign each output channel exactly one primary state and retain its history so native measurements remain distinguishable from annotations, omissions, exclusions, estimates, and algebraic derivatives. [[S01]](evidence-register.md#s01) [[S05]](evidence-register.md#s05) [[S07]](evidence-register.md#s07) [[S08]](evidence-register.md#s08)

| State | Meaning | Required provenance |
|---|---|---|
| `native` | Present as a source signal and retained without spatial reconstruction. | Source file, source name/type/unit/reference, any rename or unit conversion. [[S01]](evidence-register.md#s01) |
| `bad` | Present but marked unsuitable for some or all analyses. | Detection basis, affected span, reviewer/algorithm, thresholds, disposition. [[S03]](evidence-register.md#s03) |
| `missing` | Expected by the target support but absent from the source. | Target definition and evidence that absence is structural. [[S01]](evidence-register.md#s01) |
| `dropped` | Present in the input but deliberately excluded. | Reason, step, and downstream support. [[S03]](evidence-register.md#s03) |
| `interpolated` | Estimated from other sensors under a spatial method. | Method, geometry source/frame, donor channels, bad list, parameters, rank before/after. [[S07]](evidence-register.md#s07) [[S28]](evidence-register.md#s28) |
| `virtual` | Constructed algebraically, including bipolar or reference channels. | Formula/weights, source channels, units, reference, rank before/after. [[S08]](evidence-register.md#s08) |

Do not erase prior states: a channel may transition `native → bad → interpolated`, and the ledger must preserve every activity rather than only the final label. This follows the provenance distinction between input entities and generated entities. [[S05]](evidence-register.md#s05)

## Reference decisions

Record the acquisition/online reference separately from every offline rereference. If the acquisition reference is unknown, offline average reference does not recover that history. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03)

Before rereferencing, state the intended common representation, included/excluded channel types, treatment of bad channels, and whether the reference is applied immediately or represented as a projection. MNE exposes both application modes and excludes bad channels from average-reference computation. [[S28]](evidence-register.md#s28)

Record numerical rank before and after rereferencing with the estimator and tolerance used. Reference transforms can introduce dependencies, while delayed projections may cause software-reported and effective rank to differ until applied. [[S08]](evidence-register.md#s08) [[S28]](evidence-register.md#s28)

## Interpolation decisions

Interpolate only when the analysis requires a common spatial support or a limited bad sensor would otherwise invalidate a spatial quantity, and only when usable geometry and sufficient neighboring information exist. Spherical-spline interpolation is a spatial estimate whose assumptions and error depend on sensor geometry and sampling. [[S07]](evidence-register.md#s07)

Never interpolate a channel merely to make a matrix rectangular when the downstream method can use an explicit channel mask or native support. Plausible preprocessing alternatives can change results, so treat the choice as conditional and test sensitivity when consequential. [[S07]](evidence-register.md#s07) [[S19]](evidence-register.md#s19)

After interpolation, report the number and identity of estimated channels, their donor support/method, location provenance, data rank, and whether interpolated channels were reset from the bad list. MNE’s API makes bad marking, method, origin, and reset behavior explicit. [[S28]](evidence-register.md#s28)

## Cross-dataset montage harmonization

Prefer channel intersections when the scientific quantity remains defined on that support. Prefer a declared target montage plus interpolation only when spatial comparability is required and the geometry supports the estimate. Keep native and estimated channels distinguishable in both cases. [[S01]](evidence-register.md#s01) [[S07]](evidence-register.md#s07)

Do not call coordinate templates “measured locations,” convert bipolar channels into monopolar channels without the original signals, reconstruct channels outside observed spatial support as if native, or claim that rereferencing reverses an unknown online reference. These operations lack the acquisition information required for such claims. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03) [[S08]](evidence-register.md#s08)
