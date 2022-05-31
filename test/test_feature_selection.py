import unittest
import logging
import random
from src import classifier
from src import feature_selection
from src import validator

log = logging.getLogger(__name__)

class TestForwardSelection(unittest.TestCase):
    def test_random_validator(self):
        for _ in range(5):
            num_features = random.randint(1, 30)
            selection_alg = feature_selection.ForwardSelection()
            random_validator = validator.RandomValidator()
            result_dict = selection_alg.search(validator=random_validator, num_features=num_features, display_text = False)
            
            self.assertGreaterEqual(result_dict["Accuracy"], 0.0)
            self.assertLessEqual(result_dict["Accuracy"], 100.0)
            self.assertLessEqual(len(result_dict["Features"]), num_features)

class TestBackwardElimination(unittest.TestCase):
    def test_random_validator(self):
        for _ in range(5):
            num_features = random.randint(1, 30)
            selection_alg = feature_selection.BackwardElimination()
            random_validator = validator.RandomValidator()
            result_dict = selection_alg.search(validator=random_validator, num_features=num_features, display_text=False)
            
            self.assertGreaterEqual(result_dict["Accuracy"], 0.0)
            self.assertLessEqual(result_dict["Accuracy"], 100.0)
            self.assertLessEqual(len(result_dict["Features"]), num_features)

if __name__ == "__main__":
    unittest.main()