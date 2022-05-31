import unittest
import logging
from src.point import Point
from src import classifier
from math import isclose

log = logging.getLogger(__name__)

class TestNaiveKNN(unittest.TestCase):
    def test_classify(self):

        for k in range(1,5):
            knn = classifier.NaiveKNNClassifier(k = k)
            data = [Point(label=1.0, features = [0.0]),
                    Point(label=1.0, features = [0.1]),
                    Point(label=1.0, features = [-0.1]),
                    Point(label=1.0, features = [0.2]),
                    Point(label=1.0, features = [-0.2]),
                    Point(label=2.0, features = [5.0]),
                    Point(label=2.0, features = [4.0]),
                    Point(label=2.0, features = [6.0]),
                    Point(label=3.0, features = [-5.0]),
                    Point(label=3.0, features = [-4.0]),
                    Point(label=3.0, features = [-6.0]),
                    ]
            knn.train(data)

            test_point1 = knn.test(Point(label=None, features=[0.0124]))
            self.assertTrue(isclose(test_point1.label, 1.0))

            test_point2 = knn.test(Point(label=None, features=[4.7]))
            self.assertTrue(isclose(test_point2.label, 2.0))
            
            test_point3 = knn.test(Point(label=None, features=[-8.123]))
            self.assertTrue(isclose(test_point3.label, 3.0))

            data = [Point(label=1.0, features = [0.0, 0.0]),
                Point(label=1.0, features = [0.1, 0.1]),
                Point(label=1.0, features = [-0.1, -0.1]),
                Point(label=1.0, features = [0.2, 0.2]),
                Point(label=1.0, features = [-0.2, -0.2]),
                Point(label=2.0, features = [5.0, 5.0]),
                Point(label=2.0, features = [4.0, 4.0]),
                Point(label=2.0, features = [6.0, 6.0]),
                Point(label=3.0, features = [-5.0, -5.0]),
                Point(label=3.0, features = [-4.0, -4.0]),
                Point(label=3.0, features = [-6.0, -6.0])
                ]
            
            knn.train(data)

            test_point1 = knn.test(Point(label=None, features=[0.0124, 0.0124]))
            self.assertTrue(isclose(test_point1.label, 1.0))

            test_point2 = knn.test(Point(label=None, features=[4.7, 4.7]))
            self.assertTrue(isclose(test_point2.label, 2.0))
            
            test_point3 = knn.test(Point(label=None, features=[-8.123, -8.123]))
            self.assertTrue(isclose(test_point3.label, 3.0))

