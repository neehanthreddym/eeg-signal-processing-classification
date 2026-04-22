# Decisions & Roadblocks Log

*Maintain this log throughout the project to document methodological choices alongside the reasoning for final presentations.*

## Part 1: Sleep Spindle Detection

### Hyperparameter Log
| Participant ID | Chosen Channel | Filtering | Envelope Smoothing | Threshold (k) | Duration Checks | Notes/Roadblocks |
|----------------|----------------|-----------|--------------------|---------------|-----------------|------------------|
| 11             | CZ             | 11-16 Hz  | 100 ms             | 1.2           | 0.5 - 2.0 sec   | Validation subject. Hit optimal parity (+3.4% error) |
| 12             | CZ             | 11-16 Hz  | 100 ms             | 1.2           | 0.5 - 2.0 sec   | Generalized with moderate over-sensitivity.      |
| 13             | CZ             | 11-16 Hz  | 100 ms             | 1.2           | 0.5 - 2.0 sec   | Failed generalization: threshold too conservative. |
| 14             | CZ             | 11-16 Hz  | 100 ms             | 1.2           | 0.5 - 2.0 sec   | Generalized cleanly with highly accurate parity. |
| 15             | CZ             | 11-16 Hz  | 100 ms             | 1.2           | 0.5 - 2.0 sec   | Failed generalization: heavy over-detection.     |

### Major Roadblocks
- **Algorithmic Redundancy:** Attempting to dynamically re-run the benchmark YASA detector inside plotting loop caused massive computation overhead. *Solution:* Cached the initial detection results immediately to `yasa_events_all.csv` and filtered the DataFrame dynamically by participant, completely bypassing the heavy algorithmic recalculation for the visual proofs.
- **Inter-Subject Generalization:** The manual algorithm utilized absolute scalar amplitude thresholding which failed dramatically on patients (EPCTL13/15). *Solution:* Rather than over-engineering dynamically sliding constraints which mimics YASA, locked calibratable parameters via a Grid Search on a single subject hold-out (EPCTL11) to demonstrate the baseline weaknesses of static absolute thresholding.

### Methodological Choices
- **Broad filter limits:** `0.5 – 30 Hz`.
- **Spindle filter limits:** `11 – 16 Hz`. Chosen to strictly isolate the physiological sigma band. This ensures our Hilbert transform calculates the amplitude envelope strictly from relevant spindle-burst energy, entirely ignoring background delta or alpha waves.
- **Comparison to YASA (Generalization Insights):** Using the `k=1.2` and `smooth_ms=100` calibration, the manual detector produced mixed agreement across the dataset. It generalized cleanly to **EPCTL14** and showed only moderate over-sensitivity for **EPCTL12**. However, individual EEG variability caused outer-edge failures: the threshold remained too conservative for **EPCTL13**, but simultaneously heavily over-detected on **EPCTL15**.
- **Envelope smoothing rationale:** Evaluated lengths of 100, 200, and 300 ms on the validation subject (EPCTL11). At `k = 1.2`, counts rose quickly as smoothing increased (484 → 619 → 726). I locked in **100 ms**, which produced the closest empirical parity to YASA's 468 baseline count. A notable consequence observed across all participants is that the manual average spindle duration remained shorter than YASA's, confirming that this narrower window captures tighter spindle segments.
- **Envelope noise profile:** The raw Hilbert envelope exhibited high-frequency transients that induced artificial event fragmentation, falsely splitting single physiological spindles into multiple sub-0.5s errors, mathematically validating the need to apply a 100ms smoothing window.
- **Threshold sensitivity (k):** Tested multipliers 1.2, 1.5, and 1.8. Higher thresholds like `k=1.8` were far too strict (e.g. only 269 spindles). I permanently locked in **k = 1.2** because it yielded exactly 484 spindles (Difference = +16, Percent difference = +3.42%) on our calibration subject, representing our mathematical optimum before out-of-sample testing.


## Part 2: Motor Imagery Classification

### Parameter Summary Log
- **Band-pass filter range:** `8–30 Hz`
- **Epoch window (relative to cue):** `-1.0 to 4.0 s`
- **Baseline window:** `-1.0 to 0.0 s`
- **Classifier window:** `0.5 to 3.5 s`
- **CSP components:** `4` (Tuned: `6` for LDA, `8` for SVM)
- **LDA settings:** `solver="svd"` (Tuned: `solver="lsqr", shrinkage=0.3`)
- **SVM settings:** `kernel="linear", C=1.0` (Tuned: remained the same)

### Major Roadblocks
- **Sampling frequency discrepancy:** Three subjects (`S088`, `S092`, `S100`) were recorded at `128 Hz` while most subjects were `160 Hz`.  
  *Solution:* Kept them out of the clean baseline pool to avoid inconsistent time-series shapes during CSP evaluation.
- **Channel name inconsistency:** Some EDF channel labels had trailing dots (for example `C3..`, `Cz..`).  
  *Solution:* Added a channel-cleaning step before montage assignment and preprocessing.
- **Leakage risk in CSP pipeline:** CSP can easily leak information if fit before the split.  
  *Solution:* Fit CSP only on the training folds inside each LOSO split, then transformed the held-out run.
- **Run/session structure:** The dataset has multiple imagery runs per subject, so random trial splitting would be too optimistic.  
  *Solution:* Used **Leave-One-Session-Out** with runs `R04`, `R08`, and `R12`.

### Methodological Choices
- **Filter choice:** Used `8–30 Hz` to cover the main mu/beta motor imagery rhythms.
- **Epoch choice:** Used `-1 to 4 s` to keep pre-cue baseline and the full post-cue imagery period.
- **Classifier window choice:** Used `0.5–3.5 s` to focus on the main imagery activity and avoid the immediate cue onset period.
- **CSP choice:** Started with `4` components as a compact baseline. Hyperparameter tuning later expanded this to `6` (for LDA) and `8` (for SVM) to capture more nuanced spatial variance patterns.
- **Cross-validation strategy:** Subject-wise **LOSO across runs** instead of random trial splits.
- **Channel handling:** Used multichannel EEG with standard montage assignment; no manual single-channel selection for classification.
- **Dataset audit scope:** Verified `109` subjects total. Built the clean baseline on `106` subjects after excluding the 3 flagged `128 Hz` cases.
- **Performance differences (LDA vs SVM):** Both models performed very similarly overall, both before and after hyperparameter tuning. The difference in accuracy between classifiers remained marginal.
- **Baseline vs. Tuning result summary:**  
  - **Baseline CSP + LDA:** mean LOSO accuracy ≈ `0.615`
  - **Baseline CSP + SVM:** mean LOSO accuracy ≈ `0.617`
  - **Tuned CSP + LDA:** mean LOSO accuracy ≈ `0.627`
  - **Tuned CSP + SVM:** mean LOSO accuracy ≈ `0.624`
- **Tuning interpretation:** A Grid Search provided a small boost (~1-1.2%), mainly via increasing the number of CSP components and adding shrinkage to LDA. However, the larger obstacle remains the inherent non-stationarity across runs or subjects.

---

>**Note:** The current final baseline is on the clean `106-subject` pool, not all `109` participants.