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

---

## Part 2: Motor Imagery Classification

### Parameter Summary Log
- **Band-pass filter range:** ...
- **Epoch window (relative to cue):** ...
- **CSP components:** ...
- **LDA settings:** ...
- **SVM settings:** ...

### Major Roadblocks
- **Sampling Frequency Discrepancy:** Identified that three subjects (`S088`, `S092`, `S100`) were recorded at **128 Hz**, while the rest of the dataset is **160 Hz**. *Solution:* Excluded these subjects from the clean pool to maintain identical time-series shapes and frequency resolution for the CSP baseline.
- **Channel Name Inconsistency:** Raw PhysioNet EDF annotations include trailing dots in channel labels (e.g., `C3..`, `Cz..`). *Solution:* Implemented an automated renaming step during data loading to strip these characters, ensuring compatibility with standard MNE 10-20 montages.

### Methodological Choices
- **Dataset Audit Scope:** Verified 109 participants across all 3 imagery runs (4, 8, 12). Confirmed that while minor class imbalances exist per run (e.g., 8 vs 7), every subject in the clean pool (106 participants) has both classes present across the concatenated sessions.
- **Cross-validation strategy:** ...
- **Channel selection (if any):** ...
- **Performance differences (LDA vs SVM):** ...
