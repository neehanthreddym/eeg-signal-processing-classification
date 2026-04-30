# EEG Signal Processing & Classification

This repository contains two EEG tasks completed in Python:

1. **Sleep spindle detection** using a manual signal-processing pipeline and comparison against **YASA**.
2. **Motor imagery classification** using **Common Spatial Patterns (CSP)** with **LDA** and **linear SVM** baselines.

The work follows the assignment requirements for:
- **Part 1:** ANPHY-Sleep participants **11-15** ([Dataset Link](https://osf.io/r26fh/files/osfstorage))
- **Part 2:** PhysioNet EEG Motor Movement/Imagery Dataset ([Dataset Link](https://www.physionet.org/content/eegmmidb/1.0.0/))


## Part 1 - Sleep Spindle Detection

### Objective
Detect sleep spindles in EEG and compare a transparent manual detector against an automated baseline.

<img src="figures/diagrams/manual_spindle_detector_design.svg" alt="Manual Spindle Detector Design" width="800">

### What was implemented
The manual detector was built as a simple, interpretable approximation of spindle-band energy tracking:

- broad band-pass filter: **0.5-30 Hz**
- single central lead selection
- spindle-band filter: **11-16 Hz**
- **Hilbert amplitude envelope**
- envelope smoothing
- thresholding with **mean + k * std**
- duration filtering: **0.5-2.0 s**
- benchmark comparison against **YASA**

### Final Part 1 choices
- **Chosen channel:** `CZ`
- **Spindle band:** `11-16 Hz`
- **Envelope smoothing:** `100 ms`
- **Threshold multiplier:** `k = 1.2`
- **Duration bounds:** `0.5-2.0 s`

### Why `CZ` was used
`C3`, `CZ`, and `C4` were visually inspected across early, middle, and late N2 windows. `C4` showed repeated drift/noise, while `CZ` gave stable central activity across participants and was selected as the common lead for comparison.

### Part 1 summary
- The manual detector matched YASA reasonably well on some participants, especially **EPCTL11** and **EPCTL14**.
- It was less stable on others, especially **EPCTL13** and **EPCTL15**, showing the limitation of using a single threshold multiplier (`k`) calibrated on one subject across all participants.
- The manual detector generally produced **shorter average spindle durations** than YASA.
- The raw Hilbert envelope was noisy, so smoothing was necessary to reduce fragmentation of events.

### Main takeaway
The manual pipeline is useful as a clear engineering baseline because every step is easy to explain. However, it is also brittle across subjects. In practice, the comparison shows why automated tools such as YASA are often more robust for multi-subject spindle analysis.


## Part 2 - Motor Imagery Classification

### Objective
Classify **left vs right hand motor imagery** using a classical EEG decoding pipeline.

<img src="figures/diagrams/simple_CSP_workflow.svg" alt="Simple CSP Workflow" width="800">

### What was implemented
- dataset audit across all available subjects
- event parsing for motor imagery runs
- band-pass filtering in the motor-imagery range
- cue-locked epoching
- CSP feature extraction
- classifier comparison:
  - **LDA**
  - **linear SVM**
- subject-wise **Leave-One-Session-Out (LOSO)** validation
- confusion matrices, PSD plots, and CSP spatial pattern maps

### Final Part 2 choices
- **Filter band:** `8-30 Hz`
- **Epoch window:** `-1.0 to 4.0 s`
- **Baseline window:** `-1.0 to 0.0 s`
- **Classifier window:** `0.5 to 3.5 s`
- **CSP components:** `4`
- **LDA:** `solver="svd"`
- **SVM:** `kernel="linear", C=1.0`
- **Validation:** LOSO across runs `R04`, `R08`, `R12`

### Data audit summary
- **109** subjects were audited.
- **106** subjects were used in the clean baseline.
- **3** subjects (`S088`, `S092`, `S100`) were excluded from the main baseline because their runs were sampled at **128 Hz** instead of the expected **160 Hz**.

### Baseline vs. Tuning results
- **Baseline CSP + LDA:** mean LOSO accuracy about **0.615** (4 components, svd)
- **Baseline CSP + SVM:** mean LOSO accuracy about **0.617** (4 components, linear, C=1.0)
- **Tuned CSP + LDA:** mean LOSO accuracy **0.627** (6 components, lsqr, shrinkage=0.3)
- **Tuned CSP + SVM:** mean LOSO accuracy **0.624** (8 components, linear, C=1.0)

### Interpretation
- Both models performed **very similarly** before and after tuning.
- Hyperparameter tuning provided a small but measurable performance boost (~1-1.2%), primarily by increasing the number of CSP components (from 4 to 6/8) and adding shrinkage to LDA.
- The difference between LDA and SVM remained small, so the bigger issue was not classifier choice.
- The harder problem was **subject/session variability**. Tuning cannot easily overcome non-stationarity across runs or subjects.
- This makes the project a good example of how much performance in EEG decoding depends on preprocessing, fold design, and signal stability over just model optimization.

### Main takeaway
A classical **CSP + linear classifier** pipeline gives a solid and explainable baseline for binary motor imagery. It does not solve all variability issues, but it is a strong first benchmark and aligns well with standard BCI literature.


## Engineering decisions and roadblocks

### Part 1
- Re-running YASA inside plotting code was too expensive, so benchmark detections were cached and reused.
- A global threshold multiplier (`k`) calibrated on one subject did not generalize equally across all participants, despite the threshold itself being computed per subject.
- Envelope smoothing was required because the unsmoothed Hilbert envelope split real events into short fragments.

### Part 2
- CSP was fit **only on training folds** to avoid data leakage.
- Random trial splits were avoided because they would be too optimistic for multi-run EEG data.
- Channel names required cleanup because some EDF labels contained trailing dots.
- A subject exclusion decision was documented instead of silently mixing 128 Hz and 160 Hz recordings in the same clean baseline.


## Repository structure

```text
.
├── figures/               # Generated plots and visual proofs
├── notebooks/             # Primary analysis notebooks
│   ├── part1_spindles.ipynb
│   └── part2_motor_imagery.ipynb
├── notes/                 # Research notes and roadblock docs
├── results/               # CSV summaries and evaluation metrics
│   ├── part1/
│   └── part2/
├── src/                   # Reusable Python utility modules
├── main.py                # Pipeline entry point
├── pyproject.toml         # Python project configuration (uv)
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```


## How to run

### Environment
This project uses `uv` for lightning-fast dependency management. To set up the exact environment from the provided `pyproject.toml` and `uv.lock` files, run:

```bash
uv sync
```

### Part 1
Run: `notebooks/part1_spindles.ipynb`

Expected outputs:
- lead inspection summary
- manual spindle detections
- YASA comparison tables
- overlay plots and PSD plots

### Part 2
Run: `notebooks/part2_motor_imagery.ipynb`

Expected outputs:
- dataset audit summary
- PSD before/after filtering
- LOSO results for LDA and SVM
- confusion matrices
- CSP spatial pattern plots


## Notes on reproducibility

- Large EEG datasets are not included in the repository.
- Update dataset paths in the notebooks before running.
- Reproduce figures and CSV summaries by running the notebooks from top to bottom.
- For Part 2, keep the current anti-leakage design: fit CSP only inside each training fold.


## References

[1] Tsanas, A., & Clifford, G. D. (2015). *Stage-independent, single lead EEG sleep spindle detection using the continuous wavelet transform and local weighted smoothing*. Frontiers in Human Neuroscience, 9, 181. https://doi.org/10.3389/fnhum.2015.00181

[2] Pfurtscheller, G., & Lopes da Silva, F. H. (1999). *Event-related EEG/MEG synchronization and desynchronization: basic principles*. Clinical Neurophysiology, 110(11), 1842-1857. https://doi.org/10.1016/S1388-2457(99)00141-8

[3] Ramoser, H., Muller-Gerking, J., & Pfurtscheller, G. (2000). *Optimal spatial filtering of single trial EEG during imagined hand movement*. IEEE Transactions on Rehabilitation Engineering, 8(4), 441-446. https://doi.org/10.1109/86.895946


## Citation rationale for this repo

- Part 1 is grounded in the spindle-detection literature, but the implementation here uses a **simplified Hilbert-envelope baseline** instead of reproducing the full CWT-based method in [1].
- Part 2 uses the **ERD/ERS interpretation** from [2] and the **CSP-based decoding approach** from [3] as the main methodological references.