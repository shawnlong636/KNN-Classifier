import logging
from abc import ABC
from src import Classifier

log = logging.getLogger(__name__)

class Validator(ABC):
    def __init__(self, classifier: Classifier, validation_data):
        self.classifier = classifier
        self.data = validation_data
    def evaluate(self):
        pass
