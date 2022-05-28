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

