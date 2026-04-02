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
- `data/`: Raw and processed dataset files
  - `raw/`: Untouched ANPHY-Sleep EDF files
  - `processed/`: Generated outputs (e.g., `yasa_detections/`, `manual_detection/`)
- `notebooks/`: Jupyter notebooks for experiments and modeling
- `src/`: Core logic and helper scripts
- `figures/`: PSD plots, topographic maps, etc.
- `results/`: Output tables, confusion matrices, logs
- `notes/`: Project logs and literature notes
