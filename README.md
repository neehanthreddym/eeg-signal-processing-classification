# EEG Signal Processing & Classification

## Overview

This work consists of two core components analyzing EEG data using classical signal processing and machine learning techniques:

### Part 1 — Sleep Spindle Detection
**Goal:** Detect sleep spindles from EEG using manual signal processing (Hilbert amplitude envelope) and benchmark against YASA's implementation.
- **Dataset:** ANPHY-Sleep (Participants 11-15)

### Part 2 — Motor Imagery Classification
**Goal:** Classify left vs. right hand motor imagery using Common Spatial Patterns (CSP) spatial filtering and classic ML models (LDA vs. SVM).
- **Dataset:** PhysioNet EEG Motor Movement/Imagery Dataset

## Project Structure

```text
.
├── data/
│   ├── spindle_detection/      # Sleep spindle analysis (Part 1)
│   │   ├── raw/                # Original ANPHY-Sleep EDF files
│   │   └── processed/          # Generated detection summaries (Manual vs. YASA)
│   └── motor_imagery/          # Motor imagery classification (Part 2)
├── notebooks/                  # Primary experiment and analysis workflows
│   ├── part1_spindles.ipynb    # Hilbert envelope detection & benchmarking
│   └── part2_motor_imagery.ipynb # CSP, LDA/SVM classification pipeline
├── results/                    # Critical CSV exports (Lead selection, Hyperparameters, Performance)
├── figures/                    # Visual outputs (PSD plots, Visual proofs, Topographic maps)
├── notes/                      # Project documentation
│   └── decisions_and_roadblocks.md # Detailed log of choices and troubleshooting
├── src/                        # Supporting Python modules and utilities
└── README.md                   # Navigation and project overview
