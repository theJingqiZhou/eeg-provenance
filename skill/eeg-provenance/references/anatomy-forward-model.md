# Anatomy and forward-model readiness

Use this reference only when the requested EEG endpoint includes source imaging, a lead field/forward solution, or another operation that needs a head model. It provides the minimum asset-discovery and provenance branch; it does not select an inverse estimator or expand the skill into general MRI/MEG analysis. [[S34]](evidence-register.md#s34) [[S36]](evidence-register.md#s36)

## Readiness gate

Do not begin an individualized forward computation until the contract identifies all of these as files or explicit model choices. [[S34]](evidence-register.md#s34) [[S36]](evidence-register.md#s36)

1. EEG sensor positions with coordinate system and units; [[S34]](evidence-register.md#s34)
2. an applicable subject anatomy or an explicitly declared template alternative;
3. a sensor/head-to-MRI coregistration transform;
4. a source space;
5. a head/volume-conductor model with tissue compartments and conductivities;
6. a solver implementation and version.

MNE exposes these as distinct inputs. Surfaces alone are therefore not a forward solution, and a T1w image alone does not supply electrode geometry, a transform, tissue conductivities, or a source space. [[S34]](evidence-register.md#s34) [[S36]](evidence-register.md#s36)

## Locate raw anatomy

For the selected EEG subject and session, search the protected BIDS source for: [[S01]](evidence-register.md#s01)

```text
sub-<label>/[ses-<label>/]anat/
  sub-<label>[_ses-<label>][_acq-...][_rec-...][_run-...]_T1w.nii[.gz]
  sub-<label>[_ses-<label>][_acq-...][_rec-...][_run-...]_T1w.json
```

Inventory every applicable T1w candidate rather than taking the first match. Record the full BIDS entities, NIfTI and JSON hashes, acquisition/session relationship to the EEG, and any ambiguity that requires a scientific choice. [[S01]](evidence-register.md#s01)

From the T1w JSON, retain `AnatomicalLandmarkCoordinates` when present. BIDS defines these coordinates directly as voxel indices beginning at `[0, 0, 0]`; they are not interchangeable with EEG electrode coordinates or an MNE head-to-MRI transform. [[S01]](evidence-register.md#s01) [[S34]](evidence-register.md#s34)

Record defacing/deidentification metadata and any released `defacemask`. Inspect whether removal of face/scalp anatomy prevents the intended coregistration or surface workflow. That is a tool- and image-specific QC decision, not something BIDS validity alone answers. [[S01]](evidence-register.md#s01) [[S34]](evidence-register.md#s34)

## Locate released derivatives

Inspect `derivatives/*/dataset_description.json` before interpreting any child tree. Record `DatasetType`, `GeneratedBy`, `SourceDatasets`, and `DatasetLinks`, then search the matching subject/session for:

- FreeSurfer-style subject roots containing `mri/`, `surf/`, `label/`, `bem/`, and `scripts/`;
- BIDS-named surface GIFTI files and anatomical segmentations; [[S23]](evidence-register.md#s23)
- `*-trans.fif` or equivalent documented coregistration transforms;
- BEM surfaces/solutions or FEM tissue segmentations/meshes;
- source-space files and forward solutions, if already released.

Treat `derivatives/<pipeline>/sub-<label>/...` and `derivatives/<pipeline>/subjects/sub-<label>/...` as discovery conventions, not proof of BIDS conformance. A normal FreeSurfer `SUBJECTS_DIR` tree is tool-specific by default; validate its log/completion state and provenance separately. [[S23]](evidence-register.md#s23) [[S35]](evidence-register.md#s35)

## If `recon-all` outputs are absent

Absence from the published derivatives does not mean the source T1w is unusable, and it does not authorize writing into the source dataset. If an individual T1w is present and its use is permitted, plan reconstruction in a new derivative root or external workspace. Bind the planned subject identifier to the BIDS subject/session explicitly and record the input T1w hashes, FreeSurfer version/build, complete command and flags, `SUBJECTS_DIR`, logs, manual edits, completion status, and surface/segmentation QC. [[S23]](evidence-register.md#s23) [[S35]](evidence-register.md#s35)

Do not describe a newly run reconstruction as publisher-provided. Do not reuse an existing subject directory merely because its folder name matches; verify its input identity and build/log provenance. [[S03]](evidence-register.md#s03) [[S35]](evidence-register.md#s35)

## Choose BEM or FEM conditionally

State the forward-model question before choosing a solver. For BEM, record boundary surfaces, nesting/topology QC, compartments, conductivity values, and solver settings. For FEM, record tissue segmentations, volume mesh generation and QC, compartment labels, conductivity values or tensors, source representation, and solver settings. Head geometry and conductivity assumptions both belong in the provenance record. [[S36]](evidence-register.md#s36)

Do not claim BEM or FEM is universally superior. Choose the represented tissues and numerical method for the endpoint and available anatomy, then report sensitivity when a consequential modeling choice is uncertain. [[S03]](evidence-register.md#s03) [[S36]](evidence-register.md#s36)

## Template and stop branches

If individual anatomy is unavailable or unusable, either stop individualized forward modeling or declare a separate template-head branch. Record the template name/version, scaling or warping method, assumed fiducials, sensor registration, head-model parameters, and the limitation that the result is not subject-specific anatomy. MNE documents template MRI as a distinct workflow, not a recovery of missing subject MRI. [[S34]](evidence-register.md#s34)

Stop if coordinate units/frame are unresolved, the EEG-to-MRI transform cannot be established, surfaces or meshes fail topology/geometry QC, the T1w-to-subject/session mapping is ambiguous, or a supposedly reusable reconstruction lacks traceable inputs. Return the three required artifacts with execution marked `not_executed` and the blocking evidence preserved. [[S03]](evidence-register.md#s03) [[S34]](evidence-register.md#s34)

## Minimum ledger additions

Record source T1w and sidecar hashes; derivative dataset identity; anatomy/reconstruction tool versions; subject/session mapping; all transforms with direction and coordinate frames; fiducials and sensor geometry source; surfaces, segmentations, meshes, source spaces, and conductivities; solver parameters; manual edits; QC artifacts; output hashes; and unresolved limitations. Keep raw anatomy and publisher derivatives immutable. [[S05]](evidence-register.md#s05) [[S23]](evidence-register.md#s23) [[S34]](evidence-register.md#s34)
