import logging
import random
from src import point
from tqdm import tqdm
from collections import Counter
from abc import ABC
from src import classifier
from src.point import Point

log = logging.getLogger(__name__)

class Validator(ABC):
    def __init__(self, classifier: classifier.Classifier):
        self.classifier = classifier
    def evaluate(self, classifier: classifier.Classifier, features):
        pass

class RandomValidator(Validator):
    def __init__(self):
        self.classifier = None
        self.data = None
        
    def evaluate(self, features):
        accuracy = random.uniform(0.0, 100.0)
        # print(f"Features: {features} -> Accuracy: {round(100.0 * accuracy) / 100.0 }%")
        return accuracy

class LeaveOneOutValidator(Validator):
    def __init__(self, classifier):
        self.classifier = classifier

    def get_default_rate(self):
        classes = list(map(lambda point: point.label, self.classifier.training_data))
        counter = Counter(classes)

        _ , cnt_most_common = counter.most_common(1)[0]
        point_count = len(classes)
        return (float(cnt_most_common) / float(point_count)) * 100.0

    def evaluate(self, features):
        # Time Complexity: 
        # - For each point: O(n)
        #   - Exclude the point, and for all other points # O(n)
        #       - # Test the other point and record result: O(dn + klogn)
        # - Calculate the avg: O(1)
        #
        # Total time complexity: O(dn^2 + kn * log(n))
        point_count = len(self.classifier.training_data)

        if not self.classifier.isTrained:
            raise Exception("Model must be trained before evaluating")
        if len(features) == 0:
            return self.get_default_rate()
        if point_count <= 1:
            raise Exception("More than 1 point required to determine accuracy of classifier")

        orig_training_data = self.classifier.training_data
        correct_count = 0

        for test_idx in tqdm(range(point_count), leave=False, colour="#FABE0E", desc="Testing Model"): # O(n)
            test_point = self.classifier.training_data[test_idx]
            training_data = self.classifier.training_data[:test_idx] + self.classifier.training_data[test_idx+1:]

            self.classifier.train(training_data, features)
            
            if int(self.classifier.test(test_point).label) == int(test_point.label):
                correct_count += 1
        
            self.classifier.train(orig_training_data, features)

        return (float(correct_count) / float(point_count)) * 100.0
