import logging

log = logging.getLogger(__name__)

class Point:
    def __init__(self, id, label, features):
        self.id = id
        self.label = label
        self.features = features
