from src.point import Point
import math
import os

class Fetcher:
    def __init__(self):
        self.path = "./Datasets/"

    def available_datasets(self):
        try:
            files = [file for file in os.listdir(self.path)
                if file.endswith(".txt")]
            return files

        except Exception as error:
            print(f"Unable to load file list, reason: {error}")
            return None

    def load_dataset(self, file_name):
        file_path = self.path + file_name
        points = []
        try:
            with open(file_path, "r") as file:
                line = file.readline()
                feature_dimmensions = len([item for item in line.split(" ") if not item == ""]) - 1
                if feature_dimmensions <= 0:
                    raise Exception("Data Formatting Error: Must Contain at least one feature (Min 2 columns)")

                while line:
                    values = [float(item) for item in line.split(" ") if not item == ""]
                    if not len(values) == feature_dimmensions + 1:
                        raise Exception("Data Formatting Error: Every Row must contain the same number of features (Null Values Unsupported)")
                    points.append(Point(label=values[0],features=values[1:]))
                    line = file.readline()
                
                if len(points) == 0:
                    raise Exception("Data Formatting Error: Must contain at least one point (Min 1 Row)")

                print("Read Successfully")
                return points

        except Exception as error:
            print(f"Unable to read file: {error}")

    def normalize(self, data):
        # O(nd), n: data_size (# of pnts), d: feature_dimm

        if len(data) == 0 or len(data[0].features) == 0:
            return data

        normalized_data = data.copy()
        feature_dimm = len(data[0].features)

        # O(d)
        for feature_idx in range(feature_dimm):

            # O(n)
            features = list(map(lambda point: point.features[feature_idx], data))
            feature_min = min(features) # O(n)
            feature_max = max(features) # O(n)

            for point_idx in range(len(data)): # O(n)
                normalized_data[point_idx].features[feature_idx] = self.norm(data[point_idx].features[feature_idx], feature_min, feature_max)
        
        return normalized_data
    def norm(self, value, min_val, max_val):
        if math.isclose(min_val, max_val) or math.isclose(value, min_val):
            return 0.0

        return ( (value - min_val) / (max_val - min_val) ) * 100.0
