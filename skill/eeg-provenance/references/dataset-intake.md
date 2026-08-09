# Common dataset intake

Use this short checklist only while the source contract is unknown or spans
multiple formats. Once identified, switch to the BIDS or non-BIDS branch rather
than accumulating both. (Evidence: S57; local workflow policy)

## Route the source

| Observation | Next branch |
|---|---|
| Valid BIDS root or derivative contract | [BIDS 1.11.1 EEG](bids-eeg-1.11.1.md) |
| Documented legacy/project release | [Non-BIDS intake](non-bids-intake.md) |
| `dsNNNNNN`, `nmNNNNNN`, or `onNNNNNN` | Resolve the provider record/version before transport; EEGDash is a catalogue/access option, not owner identity |
| Remote or ephemeral execution | Add the top-level remote-execution branch only after the source branch is known |
| Source/forward-model endpoint | Add the top-level anatomy branch; otherwise omit anatomy |

Evidence: S01, S03, S31, S50, S51.

## Minimum intake record

Record observed values, their source files/pages, conflicts, and unknowns for:

- dataset, release/snapshot, provider URI, access terms, selected recording, and
  content identity;
- subject/session/run/trial hierarchy and publisher split;
- format bundle, external payloads, sampling rate, duration, and units;
- channel names/types/status, recording reference/ground, montage variation,
  electrode coordinates, coordinate frame, and geometry provenance;
- event fields, value mapping, latency precision, discontinuities, and protocol;
- line frequency, hardware/software filters, amplifier facts, and every known
  conversion or prior preprocessing step;
- source read-only boundary and separate destinations for reports, caches,
  temporary files, and derivatives.

Evidence: S01–S03, S05, S08.

Do not infer absent acquisition or processing history from waveform appearance,
file names, parser defaults, or a successful load. (Evidence: S01–S03, S05,
S08)

## Least-access inspection

Start with publisher/release documents, file tree, README, sidecars, manifests,
and native headers. Read bounded samples only when units, event alignment, or QC
cannot be established otherwise. Keep a format parser's observations separate
from the publisher protocol that gives them meaning. (Evidence: S03, S06, S23,
S42, S43, S46)

Do not change annex state, unlock files, write indexes into the source, construct
a training-framework cache, or preload a large payload during this common pass.
Those operations require an explicit later phase and output boundary. (Evidence:
S23, S37, S44, S52, S53; local archive policy)

## Sufficiency and conflicts

Call the intake `sufficient_for:<endpoint>`, never globally sufficient. Stop the
affected operation when unresolved units, channel type, reference, coordinates,
event meaning, timing, or preprocessing history would change its interpretation.
Continue independent inspection questions that do not depend on the conflict.
(Evidence: S01, S03, S08, S09)

When documentation is missing, search the official portal, versioned release
record, primary paper, codebook, and conversion/adapter code. Record unsuccessful
routes. A missing attachment is not itself a stop condition. (Evidence: S03,
S06)
