import logging
from abc import ABC
from src import Point

log = logging.getLogger(__name__)

class Classifer(ABC):
    def train(self, data):
        pass
    def test(self, data):
        pass