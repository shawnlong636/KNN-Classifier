from ast import ClassDef
import logging
from abc import ABC
from src.point import Point
from math import sqrt
import heapq
from collections import Counter

log = logging.getLogger(__name__)

class Classifier(ABC):
    def __init__(self):
        pass
    def distance(self, point1: Point, point2: Point) -> float:
        return sqrt(self.distanceSquared(point1, point2))

    def distanceSquared(self, point1: Point, point2: Point) -> float:
        if not len(point1.features) == len(point2.features):
            raise Exception("Both points must be same dimmension")
        
        feature_count = len(point1.features)
        dist_squared = 0.0

        for feature_index in self.features:
            if (feature_index - 1) >= feature_count:
                raise Exception(f"Feature Index {feature_index - 1} is out of bounds (Max Feature Count: {feature_count})")
            
            feature1 = point1.features[feature_index - 1]
            feature2 = point2.features[feature_index - 1]
            dist_squared += ((feature2 - feature1) ** 2)
    
        return dist_squared

    def train(self, training_data: list):
        pass
    def test(self, point: Point) -> float:
        pass

class NaiveKNNClassifier(Classifier):
    def __init__(self, k: int):
        self.training_data = None
        self.k = k # Number of Neighbors to check
        self.isTrained = False
        self.features = []

    def setFeatures(self, features):
        if self.training_data == None:
            raise Exception("Classifier must be trained before setting the features")
        
        max_features_set = set(list(range(1, len(self.training_data[0].features) + 1)))
        features_set = set(features)
        
        if not features_set.issubset(max_features_set):
            raise Exception(f"Set of Specified Features must be a subset of Features 1 through {len(self.training_data[0].features)}")

        self.features = features
        
    def train(self, training_data, features = None):
        self.training_data = training_data
        if features == None:
            self.features = list(range(1, len(self.training_data[0].features) + 1))
        else:
            self.features = features
        self.isTrained = True

    def test(self, test_point: Point) -> Point:
        if self.training_data == None:
            raise Exception("Model must be trained before testing")
        
        # Naive Algorithm Outline
        #   construct array of (dist, point) O(d * n)
        #   convert to minHeap O(n)
        #   Extract min, k times O(k * log(n))
        #   Calculate class w/max cnt from the k nearest O(k) (single pass)
        #
        # Total Time Complexity: O(dn + klog(n))
        #     d: dimmension of each point
        #     k: number of neighbors
        #     n: number of points in training_data

        # Convert point to tuple of (distance_to_test_point, point)

        if self.k == 1:
            best_distance = float("inf")
            best_label = None
            for point in self.training_data: # O(n)
                if not point.features == test_point.features: # O(d)
                    dist_to_point = self.distanceSquared(test_point, point) # O(d)
                    if dist_to_point < best_distance:
                        best_distance = dist_to_point
                        best_label = point.label
            return Point(label = best_label, features = test_point.features)

        else:
            testing_data = [point for point in self.training_data if not point.features == test_point.features] # O(dn)
            distance_mapper = lambda point: (self.distanceSquared(point, test_point), point)
            
            queue = list(map(distance_mapper, testing_data)) # O(dn)
            heapq.heapify(queue) # O(n)
            
            # Create array of the classes of the top k elements from the queue
            k_nearest = list(map(lambda point: point.label, [heapq.heappop(queue)[1] for _ in range(self.k)])) #O(k * log(n))
            
            # Use Counter to get most_common class
            classification = Counter(k_nearest).most_common(1)[0][0] # O(k)

            # Return Modified Point with Updated Classifification
            return Point(label = classification, features = test_point.features)