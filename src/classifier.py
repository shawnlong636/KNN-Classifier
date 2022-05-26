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
        
        dist_squared = 0.0
        for (feature1, feature2) in zip(point1.features, point2.features):
            dist_squared += ((feature2 - feature1) ** 2)
        
        return dist_squared

    def train(self, training_data: list[Point]):
        pass
    def test(self, point: Point) -> float:
        pass

class NaiveKNNClassifier(Classifier):
    def __init__(self, k: int):
        self.training_data = None
        self.k = k # Number of Neighbors to check

    def train(self, training_data: list[Point]):
        self.training_data = training_data

    def test(self, test_point: Point) -> float:
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
        distance_mapper = lambda point: (self.distance(point, test_point), point)
        
        queue = map(distance_mapper, self.training_data)
        heapq.heapify(queue)

        # Create array of the classes of the top k elements from the queue
        k_nearest = map(lambda point: point.label, [heapq.heappop(queue) for _ in range(self.k)])
        
        # Use Counter to get most_common class and return it
        return Counter(k_nearest).most_common(1)[0][0]
