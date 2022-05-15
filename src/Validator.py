import logging
import random
from abc import ABC
from src import classifier

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
        return random.uniform(0.0, 100.0)