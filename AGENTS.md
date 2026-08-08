# Repository contribution guide

These instructions apply to the entire repository.

## Repository layout

Keep the installable skill under `skill/eeg-provenance/`. That folder
must contain only the canonical skill entrypoint and resources:
`SKILL.md`, `agents/`, `assets/`, `references/`, and `scripts/`.

Keep repository-only material outside the skill package:

- Put citation audits and executable integration verification in
  `tools/`.
- Put automated checks in `tests/` and forward-test cases in `evals/`.
- Keep dependency locks, CI, legal files, and contribution policy at
  the repository root.

Bundle a script with the skill only when an agent needs it during
normal EEG work. Keep maintainer validation harnesses in `tools/`.
Reference files longer than 100 lines must include a table of contents,
and every reference must be linked directly from `SKILL.md`.

## Commit philosophy

Write commits as durable project history. A future reader should be
able to understand what changed and why, identify a safe unit to
revert, and derive useful release notes without reconstructing intent
from the diff.

Keep each commit atomic. Stage only files that serve one coherent
purpose, and split unrelated documentation, implementation, tests,
build, and CI changes. Before committing, review `git diff --cached`
and run the checks appropriate to that commit.

## Commit message format

Use Conventional Commits:

```text
<type>[optional scope]: <imperative description>

[optional body]

[optional footer(s)]
```

Follow these rules:

- Limit the complete subject line to 50 characters.
- Capitalize the description after the colon.
- Use imperative mood, as though the subject completes “This commit
  will …”.
- Do not end the subject with a period.
- Separate the body from the subject with one blank line.
- Wrap body text at 72 characters.
- Use the body to explain what changed and why it was necessary. Do
  not merely restate filenames or implementation details visible in
  the diff.
- Add footers only for structured metadata such as issue references or
  `BREAKING CHANGE:` notes.

Avoid vague subjects such as “Update files”, “Fix stuff”, “WIP”, or
“Tweaked a few things”. Name the observable change instead.

## Types

- `feat`: Add a user-visible capability.
- `fix`: Correct faulty behavior.
- `refactor`: Restructure code without adding a feature or fixing a bug.
- `perf`: Improve performance without changing intended behavior.
- `docs`: Change documentation only.
- `test`: Add or correct tests and evaluation cases.
- `build`: Change dependencies, packaging, build tools, or project
  versions.
- `ci`: Change continuous-integration configuration or automation only.
- `ops`: Change deployment, infrastructure, backup, or recovery
  behavior.
- `chore`: Perform repository maintenance unrelated to features or
  fixes.
- `style`: Change formatting without changing meaning.
- `revert`: Revert an earlier commit and identify it in the body.

Choose the narrowest accurate type. A dependency-lock update belongs
to `build`; a workflow-only change belongs to `ci`; scientific
guidance without runtime behavior belongs to `docs`.

## Scopes

Prefer a short scope naming the affected subsystem:

- `skill`: `skill/eeg-provenance/`, agent metadata, and skill behavior.
- `evidence`: the evidence register and scientific guidance.
- `provenance`: ledger schema, templates, and provenance semantics.
- `eegdash`, `mne`, `eeglab`: source-specific tool integrations.
- `tooling`: repository scripts and command-line utilities.
- `validation`: tests, evaluation harnesses, dependencies, and CI
  checks.
- `repo`: repository-wide maintenance and contribution policy.

Omit the scope only when no single subsystem describes the change. Do
not use broad scopes such as `misc` or `all`.

## Examples

```text
feat(eegdash): Add bounded intake checks

Refuse ambiguous recording selections before lazy sample access and keep
caches outside protected source archives.
```

```text
docs(evidence): Document derivative limits

Explain why pseudo-continuous conversion cannot restore original
temporal adjacency or preprocessing history.
```

```text
test(validation): Cover archive safeguards
```

## Amending and published history

Use `git commit --amend` to correct the most recent local, unpublished
commit. Do not rewrite commits that have already been pushed to a
shared branch unless the repository owner explicitly authorizes the
history rewrite.
