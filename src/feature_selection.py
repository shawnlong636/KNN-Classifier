from enum import IntEnum
from abc import ABC
from src import validator

class AlgorithmType(IntEnum):
    ForwardSelection = 1
    BackwardElimination = 2

class SelectionAlgorithm(ABC):
    def search(self, validator: validator.Validator, num_features: int):
        pass

class Fetcher:
    def get(self, algorithm: AlgorithmType) -> SelectionAlgorithm:
        if algorithm == AlgorithmType.ForwardSelection:
            return ForwardElimination()
        elif algorithm == AlgorithmType.BackwardElimination:
            return BackwardElimination()

class ForwardElimination(SelectionAlgorithm):
    def search(self, validator: validator.Validator, num_features: int):
        print("Searching using Forward Elimination")

class BackwardElimination(SelectionAlgorithm):
    def search(self, validator,  num_features: int):
        print("Searching using Backward Elimination")
