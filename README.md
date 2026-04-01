# EEG Signal Processing & Classification

## Overview

This work consists of two core components analyzing EEG data using classical signal processing and machine learning techniques:

### Part 1 — Sleep Spindle Detection
**Goal:** Detect sleep spindles from EEG using manual signal processing (Hilbert amplitude envelope) and benchmark against YASA's implementation.
- **Dataset:** ANPHY-Sleep (Participants 11-15)
- **Deadline/Target:** April 3

### Part 2 — Motor Imagery Classification
**Goal:** Classify left vs. right hand motor imagery using Common Spatial Patterns (CSP) spatial filtering and classic ML models (LDA vs. SVM).
- **Dataset:** PhysioNet EEG Motor Movement/Imagery Dataset
- **Deadline/Target:** April 7

### Final Presentation
- **Target:** April 8-9

## Project Structure
- `data/`: Raw and processed dataset files
- `notebooks/`: Jupyter notebooks for experiments and modeling
- `src/`: Core logic and helper scripts
- `figures/`: PSD plots, topographic maps, etc.
- `results/`: Output tables, confusion matrices, logs
- `slides/`: Final presentation files
- `notes/`: Project logs and literature notes
