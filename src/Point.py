import logging
import uuid

log = logging.getLogger(__name__)

class Point:
    def __init__(self, label: float, features: list[float]):
        self.id = uuid.uuid1()
        self.label = label
        self.features = features