# Remote acquisition and cache execution

Use this workflow when the compute host is remote, the prepared dataset is already online, or transferring a large local archive would be slow, costly, or duplicative. It turns remote acquisition, preprocessing, and durable cache publication into explicit gated activities instead of assuming that a submitted notebook or batch job has working network, storage, and data-manager support. [[S05]](evidence-register.md#s05) [[S50]](evidence-register.md#s50)

## Contents

- [Separate the storage roles](#separate-the-storage-roles)
- [Gate 0: probe the runtime](#gate-0-probe-the-runtime)
- [Choose an acquisition route](#choose-an-acquisition-route)
- [Run a resumable state machine](#run-a-resumable-state-machine)
- [Define the cache identity](#define-the-cache-identity)
- [Publish and verify durable shards](#publish-and-verify-durable-shards)
- [Preserve evaluation boundaries](#preserve-evaluation-boundaries)
- [Handle failures as states](#handle-failures-as-states)
- [Record remote provenance](#record-remote-provenance)
- [Colab case study and limits](#colab-case-study-and-limits)

## Separate the storage roles

Declare three roots before acquisition: a protected source checkout or object view whose source bytes are never edited, an ephemeral work/staging root on the compute host, and a durable cache root that survives job or VM termination. Annex content availability may change during bounded retrieval and release, but the source files must not become preprocessing outputs. [[S23]](evidence-register.md#s23) [[S50]](evidence-register.md#s50)

Prefer acquisition from the publisher, object store, or configured dataset remote directly to the compute host when that route is authorized and avoids a large client-to-server transfer. Record why this route was selected, the estimated transfer size, applicable access terms, and which party pays or meters ingress and egress. [[S05]](evidence-register.md#s05) [[S06]](evidence-register.md#s06) [[S50]](evidence-register.md#s50)

Treat a repository clone as metadata until content availability has been checked. A git-annex work tree can name files whose content is absent, and a parser-visible path does not prove that the annex object is materialized. [[S37]](evidence-register.md#s37) [[S50]](evidence-register.md#s50)

## Gate 0: probe the runtime

Run a small preflight in the same image, account, scheduler partition, and mounted-storage context as the real job. Do not begin a bulk retrieval until the required capabilities pass or an explicit fallback is selected. [[S50]](evidence-register.md#s50)

For a pinned Python image, apply the
[runtime compatibility matrix](runtime-compatibility.md) before changing the
environment. A sufficient installed stack is preferable to an in-place
upgrade; `uv` is optional, and a conflicting framework belongs in a separate
site-approved module, Conda environment, container, or virtual environment.
[[S58]](evidence-register.md#s58) [[S61]](evidence-register.md#s61)

Record at least:

- operating system, architecture, kernel, Python version, package environment or image digest, and accelerator visibility; software behavior and standalone binaries are platform-specific. [[S03]](evidence-register.md#s03) [[S50]](evidence-register.md#s50)
- writable ephemeral and durable roots, free space or quota, inode/file-count constraints, and whether the durable root remains available after the process or VM exits. [[S05]](evidence-register.md#s05) [[S50]](evidence-register.md#s50)
- DNS and authorized outbound access to the exact metadata, package, data, authentication, and signature endpoints needed by the selected route; do not infer general network availability from one successful request. [[S50]](evidence-register.md#s50)
- availability and versions of Git, git-annex, DataLad or the provider-native client, GPG when a downloaded tool requires signature verification, and any scheduler wall-time or preemption limit. [[S37]](evidence-register.md#s37) [[S50]](evidence-register.md#s50)
- a bounded metadata query and one small authorized object retrieval, checksum verification, cache write, close/reopen, and cleanup cycle. [[S05]](evidence-register.md#s05) [[S50]](evidence-register.md#s50)

Examples of non-mutating or bounded probes are:

```bash
uname -srm
python -VV
df -h /path/to/work /path/to/persistent-cache
command -v git-annex && git-annex version
getent hosts documented-data-host.example
curl --fail --location --head https://documented-host.example/small-metadata-object
```

Replace the paths and host with the declared execution contract. A cluster may intentionally block DNS, HTTPS, package repositories, TCP or UDP protocol lookup, interactive authentication, or privilege escalation; report the failed capability rather than repeatedly submitting the full job. [[S50]](evidence-register.md#s50)

## Choose an acquisition route

Choose the first route that is both supported by the dataset release and permitted on the compute host. Preserve the selected remote, URL, object identifier, release version or commit, and tool version in the ledger. [[S05]](evidence-register.md#s05) [[S06]](evidence-register.md#s06) [[S50]](evidence-register.md#s50)

1. Use the installed, configured dataset manager when it can prove content availability and retrieve only the selected records. For DataLad/git-annex, clone the metadata, inspect the configured remote, and `get` explicit paths instead of materializing the full dataset. [[S37]](evidence-register.md#s37) [[S50]](evidence-register.md#s50)
2. If the legacy image lacks a packaged git-annex but policy permits a user-space tool, select the official standalone bundle for the detected architecture and kernel, keep it outside the source dataset, and verify its published signature before use. Do not treat an unverified executable downloaded by the notebook as a reproducible dependency. [[S50]](evidence-register.md#s50)
3. If git-annex cannot run, use a documented provider-native HTTPS, S3, OpenNeuro, NeMAR, EEGDash, or other release-supported route only when it preserves the same object identity and access terms. Record that this is a different acquisition implementation, not evidence of a different dataset. [[S31]](evidence-register.md#s31) [[S32]](evidence-register.md#s32) [[S33]](evidence-register.md#s33) [[S50]](evidence-register.md#s50)
4. If no compliant direct route passes preflight, stop before bulk transfer and request a compatible image, network rule, staged server-side copy, or smaller authorized manifest. A low-bandwidth client upload is a last-resort transport decision, not the default merely because remote acquisition failed. [[S05]](evidence-register.md#s05) [[S50]](evidence-register.md#s50)

Do not bypass authentication, license, data-use, or access-review requirements while changing transport routes. Apply-to-access data remain controlled even when a library contains an adapter or a URL is technically reachable. [[S03]](evidence-register.md#s03) [[S44]](evidence-register.md#s44) [[S50]](evidence-register.md#s50)

Do not assume that TUH EEG is already mounted on the execution host. The provider's current documented route requires approved access, an SSH key, and `rsync`; test the provider's small test path first, then stage the exact release or bounded selection directly to a protected server-side source root. A large transfer may run as an asynchronous or scheduled acquisition job, but downstream preprocessing must wait for a verified selection manifest rather than treating job submission or process exit as proof that all files arrived. Keep private keys and credentials outside repositories, logs, ledgers, and cache artifacts. [[S05]](evidence-register.md#s05) [[S40]](evidence-register.md#s40) [[S50]](evidence-register.md#s50) [[S54]](evidence-register.md#s54)

## Run a resumable state machine

Represent execution as observable states rather than one opaque `submit-and-run` action. A useful minimum is `preflighted`, `metadata_ready`, `selection_frozen`, `source_verified`, `processing`, `shard_staged`, `shard_published`, `source_released`, and `cache_verified`. [[S05]](evidence-register.md#s05) [[S50]](evidence-register.md#s50)

For each bounded batch:

1. Resolve the exact recording bundle and companion metadata from the frozen selection manifest before retrieving sample payloads. [[S01]](evidence-register.md#s01) [[S03]](evidence-register.md#s03)
2. Retrieve only those objects into the ephemeral source view and verify annex keys, publisher checksums, or recorded byte identities before preprocessing. [[S05]](evidence-register.md#s05) [[S37]](evidence-register.md#s37) [[S50]](evidence-register.md#s50)
3. Execute the preprocessing contract and write a complete shard plus record metadata to a staging name. Do not expose a partial file under its final cache identity. [[S03]](evidence-register.md#s03) [[S05]](evidence-register.md#s05) [[S50]](evidence-register.md#s50)
4. Close, reopen, structurally verify, hash, and publish the shard into the durable root; update progress only after the durable copy passes verification. [[S05]](evidence-register.md#s05) [[S50]](evidence-register.md#s50)
5. Release ephemeral source content only after the durable shard and its provenance record are verified. Use normal availability checks unless a reviewed execution contract explicitly accepts a reckless drop policy. [[S37]](evidence-register.md#s37) [[S50]](evidence-register.md#s50)

Rerunning a completed batch should detect the verified durable shard and avoid re-fetching or recomputing it. A progress marker without the expected file, checksum, record count, and cache identity is incomplete state, not permission to skip work. [[S05]](evidence-register.md#s05) [[S50]](evidence-register.md#s50)

## Define the cache identity

Bind the cache identity to the dataset release or commit, selected recording manifest, preprocessing code version, ordered fixed parameters, channel/montage policy, output representation, and relevant software versions. A human label alone cannot distinguish caches produced from different source bytes or contracts. [[S03]](evidence-register.md#s03) [[S05]](evidence-register.md#s05) [[S06]](evidence-register.md#s06)

Keep acquisition transport outside the scientific identity when two routes demonstrably resolve the same verified source objects, but record the transport, remote, retrieval time, and verification result as execution provenance. If object equivalence cannot be proved, treat the source entities as different. [[S05]](evidence-register.md#s05) [[S50]](evidence-register.md#s50)

Record whether a cache stores full continuous records, epochs, windows, features, or model-ready tensors. Windowing, padding, label transforms, balancing, augmentation, and fitted processor state are processing choices and cannot be hidden behind a generic cache name. Braindecode save directories and PyHealth dataset/task LitData caches must use declared derivative roots; inventory framework-specific fallback locations before a remote job or protected-archive run. [[S03]](evidence-register.md#s03) [[S44]](evidence-register.md#s44) [[S52]](evidence-register.md#s52) [[S53]](evidence-register.md#s53)

## Publish and verify durable shards

Keep mutable progress state separate from immutable payload identities. Publish a machine-readable record index, per-shard counts and byte sizes, payload checksums, source-to-output relations, and a final cache manifest. [[S05]](evidence-register.md#s05) [[S50]](evidence-register.md#s50)

Write to a temporary name in the durable destination, verify the closed object there, then rename within that destination when its filesystem provides the required atomicity. Do not assume that a move between ephemeral and mounted storage is atomic. [[S05]](evidence-register.md#s05) [[S50]](evidence-register.md#s50)

Mark the whole cache complete only after all expected shards, record metadata, checksums, and provenance artifacts pass an independent reopen/verification pass. Keep failed or interrupted shard state distinguishable so a later run can resume or quarantine it without deleting valid work. [[S05]](evidence-register.md#s05) [[S50]](evidence-register.md#s50)

Avoid layouts with thousands of tiny files on a mounted Colab Drive path because the official Colab FAQ documents mount and I/O failures for large folder item counts and many small reads. Prefer bounded shard counts and test the chosen persistent backend under the expected access pattern. [[S50]](evidence-register.md#s50)

## Preserve evaluation boundaries

A reusable cache may contain immutable source-aligned data or deterministic fixed transforms shared across folds. Any operation that learns thresholds, decompositions, normalization statistics, feature selection, balancing, or augmentation policy from observations belongs inside the training partition and, when tuned, inside the resampling loop. [[S20]](evidence-register.md#s20) [[S21]](evidence-register.md#s21) [[S22]](evidence-register.md#s22)

Include participant, session, visit, site, and recording identifiers needed to construct the declared generalization split downstream. Do not trade away leakage-safe grouping merely to make a cache easier to stream. [[S20]](evidence-register.md#s20) [[S21]](evidence-register.md#s21)

## Handle failures as states

- `network_unavailable`: retain the preflight evidence and do not start a full job that depends on the failed endpoint. [[S50]](evidence-register.md#s50)
- `tool_unavailable`: try a permitted packaged or verified standalone route, then a release-supported provider client; do not silently replace git-annex object selection with an unversioned scraper. [[S37]](evidence-register.md#s37) [[S50]](evidence-register.md#s50)
- `protocol_database_missing`: inspect the actual error and `/etc/protocols`; the case-study Colab image used `netbase`, but this is not a universal repair and may be impossible without a compatible package manager or privileges. [[S50]](evidence-register.md#s50)
- `quota_or_space_exhausted`: stop acquisition, preserve verified durable shards and progress, release only safely recoverable ephemeral content, and revise batch size or destination quota. [[S05]](evidence-register.md#s05) [[S50]](evidence-register.md#s50)
- `preempted_or_vm_reset`: resume from independently verified durable shards; never infer completion from notebook position or scheduler success alone. [[S05]](evidence-register.md#s05) [[S50]](evidence-register.md#s50)
- `source_remote_changed`: preserve the original commit, keys, URLs, and failure result; do not relabel replacement bytes as the same source entity without identity evidence. [[S05]](evidence-register.md#s05) [[S06]](evidence-register.md#s06)

## Record remote provenance

Represent acquisition, source verification, each preprocessing batch, durable publication, and final cache verification as separate ordered ledger activities. Record the runtime/image, host class, ephemeral and persistent roots, network preflight result, source remote and commit, selected object identities, commands/tool versions, timestamps, retry/resume state, output checksums, and unresolved failures. [[S03]](evidence-register.md#s03) [[S05]](evidence-register.md#s05) [[S50]](evidence-register.md#s50)

Record a durable URI or storage identity for every cache output in addition to any runtime mount path. A path such as `/content/drive/...` describes one mount view and does not by itself identify the persistent object across environments. [[S05]](evidence-register.md#s05) [[S06]](evidence-register.md#s06) [[S50]](evidence-register.md#s50)

## Colab case study and limits

The reviewed `brainprint-rseeg-data` commit `cd4adb9d2b72f9f3953302892f6050b921821173` demonstrates one bounded implementation: `/content/input` for source checkouts, `/content/working` for staging, `/content/lib` for helper code and a standalone git-annex bundle, and mounted Google Drive for durable TFRecord shards, state, record metadata, and checksums. Its builder clones source metadata, retrieves required paths for a record batch, writes and verifies shards, then drops fetched content to bound VM disk. [[S50]](evidence-register.md#s50)

Treat that repository as a case study, not a universal script. Its standalone-binary architecture, `netbase` repair, Google Drive mount, source remotes, TFRecord representation, and paths are specific to its hosted Colab contract. [[S50]](evidence-register.md#s50)

Do not copy its notebook setting that disables standalone-bundle signature verification into a new environment without an independently verified image or artifact policy. Official git-annex documentation provides signed standalone downloads and verification instructions. [[S50]](evidence-register.md#s50)

Do not generalize its `reckless="availability"` drop call. DataLad documents that reckless availability mode disables the normal check for sufficient remote copies, so use it only when the source is independently protected and the risk is explicitly accepted. [[S50]](evidence-register.md#s50)

Hosted Colab VMs are ephemeral and have enforced lifetime limits, while Drive mounts have quota and file-count/I/O caveats. Persist verified cache products incrementally and design every build to resume after runtime loss. [[S50]](evidence-register.md#s50)
