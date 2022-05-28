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

                while line:
                    values = [float(item) for item in line.split(" ") if not item == ""]
                    points.append(Point(label=values[0],features=values[1:]))
                    line = file.readline()
                
                print("Read Successfully")
                return points

        except Exception as error:
            print(f"Unable to read file: {error}")

