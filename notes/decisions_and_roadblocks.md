# Decisions & Roadblocks Log

*Maintain this log throughout the project to document methodological choices alongside the reasoning for final presentations.*

## Part 1: Sleep Spindle Detection

### Hyperparameter Log
| Participant ID | Chosen Channel | Filtering | Envelope Smoothing | Threshold (k) | Duration Checks | Notes/Roadblocks |
|----------------|----------------|-----------|--------------------|---------------|-----------------|------------------|
| 11             |                |           |                    |               |                 |                  |
| 12             |                |           |                    |               |                 |                  |
| 13             |                |           |                    |               |                 |                  |
| 14             |                |           |                    |               |                 |                  |
| 15             |                |           |                    |               |                 |                  |

### Major Roadblocks
- *Example: Envelope amplitude was too noisy initially, added X smoothing window.*

### Methodological Choices
- **Broad filter limits:** ...
- **Spindle filter limits:** ...
- **Comparison to YASA:** ...

---

## Part 2: Motor Imagery Classification

### Parameter Summary Log
- **Band-pass filter range:** ...
- **Epoch window (relative to cue):** ...
- **CSP components:** ...
- **LDA settings:** ...
- **SVM settings:** ...

### Major Roadblocks
- *Example: Leakage identified during scaling, moved scaler to inside the pipeline/CV loop.*

### Methodological Choices
- **Cross-validation strategy:** ...
- **Channel selection (if any):** ...
- **Performance differences (LDA vs SVM):** ...
