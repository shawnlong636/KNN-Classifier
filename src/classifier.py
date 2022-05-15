import logging
from abc import ABC
from src import point

log = logging.getLogger(__name__)

class Classifier(ABC):
    def train(self, data):
        pass
    def test(self, data):
        pass
