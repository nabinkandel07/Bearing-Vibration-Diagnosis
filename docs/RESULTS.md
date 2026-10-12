# Results and interpretation

All 80 held-out synthetic windows were correctly classified, giving accuracy and macro F1 of **1.000**. Every class has precision, recall, and F1 of 1.000 with support 20.

![Confusion matrix](../results/confusion_matrix.svg)

The perfect separation is expected because each synthetic fault adds energy at a distinct frequency that is explicitly included in the feature vector. This result confirms the generator, Fourier-amplitude calculation, classifier, and evaluation pipeline. It is not evidence that the same model will generalize to a real bearing test rig.

A credible experimental extension should calculate geometry- and RPM-dependent characteristic frequencies, include multiple loads and speeds, compare raw-spectrum and envelope-spectrum features, and reserve entire machines for final testing.
