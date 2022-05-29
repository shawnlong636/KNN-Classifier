from src.point import Point
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
        points: list[Point] = []
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

    def normalize(data: list[Point]):
        # O(nd), n: data_size (# of pnts), d: feature_dimm

        if len(data) == 0 or len(data[0]) == 0:
            return data

        norm = lambda x, min_x, max_x: ( (x - min_x) / (max_x - min_x) ) * 100.0
        normalized_data = data.copy()
        feature_dimm = len(data[0])

        # O(d)
        for feature_idx in range(feature_dimm):
            feature_min = float("-inf")
            feature_max = float("inf")

            # O(n)
            for point in data:
                if point.features[feature_idx] < feature_min:
                    feature_min = point.features[feature_idx]
                if point.features[feature_idx] > feature_max:
                    feature_max = point.features[feature_idx]

            # O(n)
            for point_idx in range(len(data)):
                normalized_data[point_idx].features[feature_idx] = norm(data[point_idx].features[feature_idx], feature_min, feature_max)
        
        return normalized_data
