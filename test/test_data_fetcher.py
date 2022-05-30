from turtle import pos
import unittest
import logging
import random
from src import data_fetcher
from src.point import Point

log = logging.getLogger(__name__)

class TestForwardSelection(unittest.TestCase):
    def test_norm(self):
        fetcher = data_fetcher.Fetcher()
        positive_floats = [random.random() * 1e9] * 1_000

        min_val = min(positive_floats)
        max_val = max(positive_floats)
        for val in positive_floats:
            normalized_val = fetcher.norm(val, min_val, max_val)
            self.assertGreaterEqual(normalized_val, 0.0)
            self.assertLessEqual(normalized_val, 100.0)

        negative_floats = [(random.random()) * -1e9] * 1_000

        min_val = min(negative_floats)
        max_val = max(negative_floats)
        for val in negative_floats:
            normalized_val = fetcher.norm(val, min_val, max_val)
            self.assertGreaterEqual(normalized_val, 0.0)
            self.assertLessEqual(normalized_val, 100.0)

        mixed_floats = [(random.random() - 0.5) ] * 1_000
        
        min_val = min(mixed_floats)
        max_val = max(mixed_floats)
        for val in mixed_floats:
            normalized_val = fetcher.norm(val, min_val, max_val)
            self.assertGreaterEqual(normalized_val, 0.0)
            self.assertLessEqual(normalized_val, 100.0)

        same_floats = [random.random()] * 10
        min_val = min(same_floats)
        max_val = max(same_floats)
        for val in same_floats:
            normalized_val = fetcher.norm(val, min_val, max_val)
            self.assertGreaterEqual(normalized_val, 0.0)
            self.assertLessEqual(normalized_val, 100.0)

        two_floats = []
        for _ in range(1000):
            if random.randint(0, 100) % 2 == 0:
                two_floats.append(-87.93721)
            two_floats.append(103.23847)
        
        min_val = min(two_floats)
        max_val = max(two_floats)
        for val in two_floats:
            normalized_val = fetcher.norm(val, min_val, max_val)
            self.assertGreaterEqual(normalized_val, 0.0)
            self.assertLessEqual(normalized_val, 100.0)

    def test_data_normalization(self):
        fetcher = data_fetcher.Fetcher()
        data = fetcher.load_dataset("small-test-dataset.txt")
        data = fetcher.normalize(data)
        for point in data:
            for feature in point.features:
                self.assertGreaterEqual(feature, 0.0)
                self.assertLessEqual(feature, 100.0)

if __name__ == "__main__":
    unittest.main()