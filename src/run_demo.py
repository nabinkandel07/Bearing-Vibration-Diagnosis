"""Bearing condition classification from synthetic vibration signals."""

import csv
import json
import math
import random
import statistics
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
CLASSES = ("healthy", "inner_race", "outer_race", "imbalance")
FREQUENCIES = (18, 30, 45)


def make_signal(label, rng, n=256):
    signal = []
    for i in range(n):
        t = i / n
        value = 0.15 * math.sin(2 * math.pi * 8 * t) + rng.gauss(0, 0.10)
        if label == "inner_race":
            value += 0.9 * math.sin(2 * math.pi * 45 * t)
        elif label == "outer_race":
            value += 0.8 * math.sin(2 * math.pi * 30 * t)
        elif label == "imbalance":
            value += 1.1 * math.sin(2 * math.pi * 18 * t)
        signal.append(value)
    return signal


def amplitude(signal, frequency):
    n = len(signal)
    real = sum(x * math.cos(2 * math.pi * frequency * i / n) for i, x in enumerate(signal))
    imag = sum(x * math.sin(2 * math.pi * frequency * i / n) for i, x in enumerate(signal))
    return 2 * math.hypot(real, imag) / n


def features(signal):
    rms = math.sqrt(sum(x * x for x in signal) / len(signal))
    crest = max(abs(x) for x in signal) / rms
    return (rms, crest, *(amplitude(signal, f) for f in FREQUENCIES))


def class_report(matrix):
    report = {}
    for label in CLASSES:
        tp = matrix[label][label]
        fp = sum(matrix[actual][label] for actual in CLASSES if actual != label)
        fn = sum(matrix[label][predicted] for predicted in CLASSES if predicted != label)
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        report[label] = (precision, recall, f1, sum(matrix[label].values()))
    return report


def confusion_svg(matrix):
    cell, left, top = 95, 160, 80
    width, height = left + cell * len(CLASSES) + 20, top + cell * len(CLASSES) + 40
    maximum = max(value for row in matrix.values() for value in row.values())
    parts = []
    for row, actual in enumerate(CLASSES):
        parts.append(f'<text x="10" y="{top + row * cell + 55}" font-family="sans-serif">{actual}</text>')
        for column, predicted in enumerate(CLASSES):
            value = matrix[actual][predicted]
            shade = 245 - int(155 * value / maximum)
            x, y = left + column * cell, top + row * cell
            parts.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="rgb({shade},255,{shade})" stroke="white"/>')
            parts.append(f'<text x="{x + 47}" y="{y + 55}" text-anchor="middle" font-family="sans-serif" font-size="20">{value}</text>')
    headers = "".join(f'<text x="{left + i * cell + 47}" y="60" text-anchor="middle" font-family="sans-serif">{label}</text>' for i, label in enumerate(CLASSES))
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"><rect width="100%" height="100%" fill="white"/><text x="10" y="22" font-family="sans-serif" font-size="16">Actual rows, predicted columns</text>{headers}{"".join(parts)}</svg>'


def main():
    RESULTS.mkdir(exist_ok=True)
    rng = random.Random(7)
    samples = [(label, features(make_signal(label, rng))) for label in CLASSES for _ in range(80)]
    train = [s for i, s in enumerate(samples) if i % 4]
    test = [s for i, s in enumerate(samples) if not i % 4]
    centroids = {label: tuple(statistics.mean(v) for v in zip(*(x for y, x in train if y == label))) for label in CLASSES}
    matrix = {a: {p: 0 for p in CLASSES} for a in CLASSES}
    for actual, vector in test:
        predicted = min(CLASSES, key=lambda label: sum((a - b) ** 2 for a, b in zip(vector, centroids[label])))
        matrix[actual][predicted] += 1
    correct = sum(matrix[label][label] for label in CLASSES)
    report = class_report(matrix)
    metrics = {"test_samples": len(test), "accuracy": correct / len(test), "macro_f1": statistics.mean(row[2] for row in report.values()), "frequencies_hz": list(FREQUENCIES), "data": "deterministic synthetic vibration signals"}
    with (RESULTS / "confusion_matrix.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["actual/predicted", *CLASSES])
        for actual in CLASSES:
            writer.writerow([actual, *(matrix[actual][predicted] for predicted in CLASSES)])
    with (RESULTS / "classification_report.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["class", "precision", "recall", "f1", "support"])
        for label, row in report.items():
            writer.writerow([label, *row])
    (RESULTS / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    (RESULTS / "confusion_matrix.svg").write_text(confusion_svg(matrix), encoding="utf-8")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
