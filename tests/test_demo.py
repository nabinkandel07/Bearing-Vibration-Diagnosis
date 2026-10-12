import math
import unittest

from src.run_demo import amplitude, features


class SpectrumTests(unittest.TestCase):
    def test_selected_bin_amplitude(self):
        signal = [math.sin(2 * math.pi * 18 * i / 256) for i in range(256)]
        self.assertAlmostEqual(amplitude(signal, 18), 1.0, places=12)
        self.assertAlmostEqual(amplitude(signal, 30), 0.0, places=12)

    def test_feature_vector_length(self):
        self.assertEqual(len(features([0.2, -0.2] * 128)), 5)


if __name__ == "__main__":
    unittest.main()
