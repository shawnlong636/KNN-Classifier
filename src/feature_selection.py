from enum import IntEnum
from abc import ABC
from src import validator
import heapq as hq

class AlgorithmType(IntEnum):
    ForwardSelection = 1
    BackwardElimination = 2

class SelectionAlgorithm(ABC):
    def search(self, validator: validator.Validator, num_features: int):
        pass

    def possible_choices(self, features: list[int], max_features: int):
        pass

class Fetcher:
    def get(self, algorithm: AlgorithmType) -> SelectionAlgorithm:
        if algorithm == AlgorithmType.ForwardSelection:
            return ForwardSelection()
        elif algorithm == AlgorithmType.BackwardElimination:
            return BackwardElimination()

class ForwardSelection(SelectionAlgorithm):
    def possible_choices(self, features: list[int], max_features: int):

        all_features = set([i for i in range(1,max_features + 1)])
        used_features = set(features)
        possible_features = all_features.difference(used_features)
        
        return sorted(list(possible_features))

    def search(self, validator: validator.Validator, num_features: int):
        print("\nSearching using Forward Selection\n")
        best_feature_set = []
        best_accuracy = 0.00
        try:
            best_accuracy = validator.evaluate(best_feature_set)
        except Exception as error:
            print(f"Unable to complete feature search: {error}")
            return
        all_children_worse = False

        while not all_children_worse:
            print(f"\nBest Feature Set: {best_feature_set} -> Accuracy: {round(100.0 * best_accuracy) / 100.0}%\n")
            all_children_worse = True
            current_best_accuracy = best_accuracy
            current_best_features = best_feature_set


            choices = self.possible_choices(best_feature_set, max_features = num_features)
            # print(choices)
            for choice in choices:
                child_accuracy = 0.00
                try:
                    child_accuracy = validator.evaluate(best_feature_set + [choice])
                except Exception as error:
                    print(f"Unable to complete feature search: {error}")
                    return
                if child_accuracy > current_best_accuracy:
                    current_best_accuracy = child_accuracy
                    current_best_features = best_feature_set + [choice]
                    all_children_worse = False

            if all_children_worse:
                print("All children worse or no more features to add")
            best_feature_set = current_best_features
            best_accuracy = current_best_accuracy
        
        print(f"\nBest Feature Set: {best_feature_set} -> Accuracy: {round(100.0 * best_accuracy) / 100.0}%\n")
        return {"Features": best_feature_set, "Accuracy": best_accuracy}

class BackwardElimination(SelectionAlgorithm):
    def search(self, validator: validator.Validator, num_features: int):
        print("\nSearching using Backward Elimination\n")
        best_feature_set = [feature for feature in range(1, num_features + 1)]
        best_accuracy = 0.0
        try:
            best_accuracy = validator.evaluate(best_feature_set)
        except Exception as error:
            print(f"Unable to complete feature search: {error}")
        all_children_worse = False

        while not all_children_worse:
            print(f"\nBest Feature Set: {best_feature_set} -> Accuracy: {round(100.0 * best_accuracy) / 100.0}%\n")
            all_children_worse = True
            current_best_accuracy = best_accuracy
            current_best_features = best_feature_set

            feature_set = set(best_feature_set)

            for feature in best_feature_set:
                child_features = sorted(list(feature_set.difference(set([feature]))))
                child_accuracy = None
                try:
                    child_accuracy = validator.evaluate(child_features)
                except Exception as error:
                    print(f"Unable to complete feature search: {error}")

                if child_accuracy > best_accuracy:
                    current_best_accuracy = child_accuracy
                    current_best_features = child_features
                    all_children_worse = False

            if all_children_worse:
                print("All children worse or no more features to remove")
            best_feature_set = current_best_features
            best_accuracy = current_best_accuracy
        
        print(f"\nBest Feature Set: {best_feature_set} -> Accuracy: {round(100.0 * best_accuracy) / 100.0}%\n")
        return {"Features": best_feature_set, "Accuracy": best_accuracy}
