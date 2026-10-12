# Data dictionary

## Classes and injected components

| Class | Added component |
|---|---|
| `healthy` | No class-specific sinusoid |
| `inner_race` | Amplitude 0.9 at frequency bin 45 |
| `outer_race` | Amplitude 0.8 at frequency bin 30 |
| `imbalance` | Amplitude 1.1 at frequency bin 18 |

## Features

| Feature | Meaning |
|---|---|
| RMS | Square root of mean signal energy |
| Crest factor | Peak absolute amplitude divided by RMS |
| Bin amplitudes | Two-sided sinusoidal amplitude estimates at bins 18, 30, and 45 |

`confusion_matrix.csv` uses actual rows and predicted columns. `classification_report.csv` reports per-class metrics. `metrics.json` stores aggregate results and labels the source as synthetic.
