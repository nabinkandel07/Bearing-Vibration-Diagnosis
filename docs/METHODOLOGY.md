# Methodology

## Research question

Can selected-frequency vibration amplitudes provide an interpretable baseline for separating idealized bearing and imbalance conditions?

## Synthetic dataset

The generator uses random seed 7 and creates 80 signals for each of four balanced conditions. Each signal contains 256 samples, a low-amplitude 8-bin shaft component, and Gaussian noise with standard deviation `0.10`. Inner-race, outer-race, and imbalance cases add sinusoids at bins 45, 30, and 18 respectively.

## Feature extraction

The five features are RMS amplitude, crest factor, and direct discrete-Fourier amplitudes at bins 18, 30, and 45. The implementation evaluates only those bins using sine and cosine projections, making the signal processing inspectable and dependency-free.

## Classification and evaluation

A deterministic 75/25 split produces 240 training and 80 held-out windows, balanced across classes. A nearest-centroid classifier uses unscaled Euclidean distance. Evaluation includes the confusion matrix, per-class precision/recall/F1, overall accuracy, and macro F1.

## Limitations

The frequencies are intentionally separated and fixed. Real characteristic frequencies depend on bearing geometry and shaft speed, while measured signals include harmonics, slip, resonance, load changes, sensor mounting effects, and domain shift. Real evaluation should split data by machine and acquisition session.
