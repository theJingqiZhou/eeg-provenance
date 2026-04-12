# ClaudeEEG

A Claude Code skill that turns Claude into a domain expert for EEG/MEG analysis, BCI development, and neuroscience signal processing — from raw messy recordings to production-grade models.

---

## What This Skill Does

ClaudeEEG loads a comprehensive neuroscience knowledge base into Claude's context, giving it deep expertise across the full EEG analysis stack:

- **Theory** — frequency band biology, ERP components, cross-frequency coupling, volume conduction, artifact physics
- **Preprocessing** — gold-standard pipeline ordering (filtering, ICA, ASR, AutoReject, re-referencing)
- **Libraries** — MNE-Python, EEGLAB/MATLAB, SciPy, scikit-learn, braindecode, pyRiemann
- **ML/DL modeling** — CSP+LDA, Riemannian geometry, EEGNet, ShallowConvNet, foundation models (LaBraM, BIOT, SignalJEPA)
- **Statistics** — permutation tests, FDR/Bonferroni correction, cluster-based inference, mixed-effects models
- **BCI paradigms** — Motor Imagery, P300, SSVEP, neurofeedback
- **Clinical applications** — sleep staging, seizure detection, resting-state connectivity
- **Data formats** — EDF, BrainVision, EEGLAB .set, FIF, CNT, EGI/MFF, BIDS

---

## Use Cases

### Preprocessing & Cleaning
```
"I have 64-channel EEG from a motor imagery task. Walk me through a full preprocessing pipeline."
"My data has heavy ocular artifacts. How should I set up ICA in MNE?"
"Should I use ASR before or after ICA for a mobile EEG recording?"
"Help me implement the dual-dataset ICA trick to preserve slow ERPs."
```

### ERP Analysis
```
"Extract and plot P300 components from my oddball task data."
"What baseline correction window should I use for a CNV paradigm?"
"My N200 amplitudes look wrong after filtering — what's going on?"
```

### BCI Development
```
"Build a real-time motor imagery classifier using CSP + LDA."
"Compare Riemannian MDM vs EEGNet for cross-subject motor imagery — which should I use?"
"Set up a P300 speller pipeline with xDAWN spatial filtering."
"Implement an SSVEP decoder using CCA for a 4-target paradigm."
```

### Machine Learning & Deep Learning
```
"Train EEGNet on BCI Competition IV 2a using braindecode."
"My classifier has 95% within-session accuracy but drops to 60% cross-session. How do I fix this?"
"Fine-tune LaBraM (the EEG foundation model) on my small dataset."
"Set up proper leave-one-subject-out cross-validation to avoid data leakage."
```

### Time-Frequency & Connectivity
```
"Compute alpha ERD/ERS during motor preparation using Morlet wavelets."
"Measure theta-gamma phase-amplitude coupling in my working memory data."
"Calculate wPLI connectivity between frontal and parietal channels."
```

### Sleep & Clinical
```
"Stage sleep from polysomnography data using AASM criteria."
"Detect interictal epileptiform discharges in a long EEG recording."
"Compute individual alpha frequency (IAF) per subject."
```

### Debugging & QC
```
"My ICA components all look like noise — what went wrong?"
"Walk me through interpreting these ICLabel labels and probabilities."
"Why does my source localization look wrong?"
"Critique this preprocessing pipeline and flag any ordering errors."
```

---

## Skill Trigger Keywords

The skill activates on: `EEG`, `MEG`, `electrophysiology`, `brain-computer interface`, `BCI`, `ICA`, `ERP`, `epochs`, `artifact removal`, `EEGLAB`, `MNE`, `braindecode`, `NeuroPype`, `neural decoding`, `oscillations`, `frequency bands`, `power spectral density`, `source localization`, `motor imagery`, `P300`, `SSVEP`, `neurofeedback`, `neuro`.

---

## Installation

```
npx skills add https://github.com/Krish-mal15/ClaudeEEG
```


```

Once installed, the skill is available in any Claude Code session. Simply start a message with a relevant keyword or explicitly invoke it:

```
/ClaudeEEG  help me preprocess this EEG dataset
```

---

## Repo Structure

```
ClaudeEEG/
├── SKILL.md          # The skill itself — loaded into Claude's context
├── README.md         # This file
├── scripts/          # Runnable Python pipeline examples
└── references/
    ├── MNE Resources/    # MNE tutorials (preprocessing, epochs, inverse, stats, ...)
    └── NumPy Resources/  # NumPy reference docs
```

---

## Requirements

For the Python pipelines referenced by the skill:

```
mne >= 1.6
mne-icalabel
braindecode
pyriemann
autoreject
meegkit        # Zapline, DSS
scipy
scikit-learn
torch
```

Install all at once:

```bash
pip install mne mne-icalabel braindecode pyriemann autoreject meegkit scikit-learn torch
```

---

## Notes

- **Gamma skepticism is built in.** The skill knows that scalp gamma (30–80 Hz) fully overlaps the muscle artifact range and will flag uncritical gamma claims.
- **ICA ordering is enforced.** The skill will warn you if you try to filter after epoching, run ICA on unfiltered data, or skip ASR for mobile recordings.
- **Cross-validation hygiene.** For ML pipelines, the skill always recommends subject-stratified splits and warns against temporal data leakage.
- **2024 literature is included.** Findings like the Kang et al. result (ICA may hurt DL decoding performance) and the Callan et al. ASR-before-ICA evidence are baked in.
