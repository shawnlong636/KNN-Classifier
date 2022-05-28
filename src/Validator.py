import logging
import random
from abc import ABC
from src import classifier
from src.point import Point

log = logging.getLogger(__name__)

class Validator(ABC):
    def __init__(self, classifier: classifier.Classifier, validation_data):
        self.classifier = classifier
        self.data = validation_data
    def evaluate(self, classifier: classifier.Classifier, features: list[int]):
        pass

class RandomValidator(Validator):
    def __init__(self):
        self.classifier = None
        self.data = None
        
    def evaluate(self, features: list[int]):
        accuracy = random.uniform(0.0, 100.0)
        print(f"Features: {features} -> Accuracy: {round(100.0 * accuracy) / 100.0 }%")
        return accuracy

class LeaveOneOutValidator(Validator):
    def __init__(self, classifier, validation_data):
        self.classifier = classifier
        self.validation_data = validation_data

    def evaluate(self, features: list[int]):
        point_count = len(self.validation_data)
        accuracy_sum = 0.0
        test_count = 0
        self.classifier.setFeatures(features)

        if len(features) == 0:
            return 0.0

        if point_count <= 1:
            raise Exception("More than 1 point required to determine accuracy of classifier")

        for exclude_index in range(point_count):
            correct_count = 0

            for include_index in range(point_count):
                if not include_index == exclude_index:
                    actual_point = self.validation_data[include_index]
                    classified_point = self.classifier.test(Point(label=None, features=actual_point.features))

                    if int(actual_point.label) == int(classified_point.label):
                        correct_count += 1

            current_test_accuracy = 100.00 * (float(correct_count) / float((point_count - 1)))
            accuracy_sum += current_test_accuracy
            test_count += 1

        if test_count <= 0:
            raise Exception("Unable to Calculate Accuracy due to having zero valid tests")
        
        total_accuracy = accuracy_sum / float(test_count)
        print(f"Features: {features} -> Accuracy: {round(100.0 * total_accuracy) / 100.0 }%")
        return total_accuracy