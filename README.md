# Bearing Vibration Diagnosis

A dependency-free vibration-classification baseline for four conditions: `healthy`, `inner_race`, `outer_race`, and `imbalance`. It creates deterministic synthetic signals, extracts RMS, crest factor, and selected-frequency amplitudes, then evaluates a nearest-centroid classifier.

## Run

```bash
python src/run_demo.py
```

Python 3.10 or newer is recommended. No third-party packages are required.

## Reproducible demo result

| Metric | Result |
|---|---:|
| Held-out samples | 80 |
| Classification accuracy | 100% |
| Diagnostic frequencies | 18, 30, and 45 bins |

The synthetic fault frequencies are intentionally distinct, making this a pipeline and feature-extraction demonstration. The perfect score should not be interpreted as real-machine performance.

Generated artifacts are committed under `results/`: `metrics.json`, `confusion_matrix.csv`, `classification_report.csv`, and `confusion_matrix.svg`.

For academic review, see the [methodology](docs/METHODOLOGY.md), [result interpretation](docs/RESULTS.md), and [data dictionary](docs/DATA_DICTIONARY.md). Verify the spectral calculations with `python -m unittest discover -s tests -v`.

## Method

Each signal contains a low-amplitude shaft component and noise. Fault cases add a class-specific sinusoid. The script calculates selected discrete Fourier amplitudes directly, so it does not need NumPy or SciPy.

## Next steps

Use real accelerometer data, estimate RPM-dependent bearing frequencies, add envelope analysis, and evaluate across loads, speeds, and machines.
