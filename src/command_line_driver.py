import logging
from sys import stdin
from src import feature_selection as fs
from src import validator
from src import classifier
from src import data_fetcher
from src.point import Point
import os

# Global Function
input = stdin.readline

class CLI:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.fetcher = data_fetcher.Fetcher()

        # Default Values for Data and Classifiers
        self.data_file = "small-test-dataset.txt"
        self.data = self.fetcher.load_dataset(self.data_file)
        # self.data = self.fetcher.normalize(self.data) # Uncomment to enable normalization by default
        self.classifier = classifier.NaiveKNNClassifier(k=1)

        self.status_message = "Welcome to KNN Clasifier!"

    # MAIN METHOD FOR THE CLI
    def run(self):

        while True:
            self.header()

            if not self.status_message == "":
                print("\n" + self.status_message)
                self.status_message = ""

            print("\nPlease select an option:")
            print("\n\t(1) Select a Dataset")
            print("\t(2) Select a Classifier")
            print("\t(3) Normalize Dataset")

            print("\n\t(4) Feature Selection")
            print("\t(5) Train a Model")
            print("\t(6) Validate a Model")
            
            print("\n\t(7) Classify a Data Point")

            print("\n\t(9) Quit")
            
            menuChoice = self.selectOption(choices = [1, 2, 3, 4, 5, 6, 9])

            if menuChoice == 1: # (1) Select a Dataset
                self.selectInputData()

            elif menuChoice == 2: # (2) Select a Classifier
                self.classifierSelection()
            elif menuChoice == 3: # (3) Normalize Dataset
                self.fetcher.normalize(self.data)
                self.status_message = "Data sucessfully Normalized"

            elif menuChoice == 4: # (4) Feature Selection
                self.featureSelection()

            elif menuChoice == 5: # (5) Train a Model
                self.classifier.train(self.data)
                self.status_message = "Training Successful!"

            elif menuChoice == 6: # (6) Validate a Model
                self.validateModel()

            elif menuChoice == 7: # (7) Classify a Data Point
                self.testNewPoint()

            elif menuChoice == 9: # (9) Quit
                exit()

    # MAIN FEATURE METHODS

    def selectInputData(self):
        self.header()
        print("\nTo import a custom dataset, please follow the instructions in the readme.")

        available_datasets = self.fetcher.available_datasets()

        if len(available_datasets) == 0:
            print("No datasets found. Please double check your file/formatting.")
            print("Quitting Application.")
            exit()
        else:
            print(f"\nFound {len(available_datasets)} datasets! Please select one of the following:")
            for (index, dataset) in enumerate(available_datasets):
                print(f"\t({index + 1}) {dataset}")

        option = self.selectOption(choices = list(range(1, len(available_datasets) + 1)))
        self.data_file = available_datasets[option - 1]
        self.data = self.fetcher.load_dataset(self.data_file)
        self.classifier.isTrained = False
        self.status_message = "Sucessfully Loaded data!"

    def featureSelection(self):
        if not self.checkModelIsTrained():
            return
        
        num_features = len(self.data[0].features)

        if num_features == -1:
            return

        self.header()
        print("\nPlease select a feature selction algorithm: ")
        print("\t(1) Forward Selection")
        print("\t(2) Backward Elimination")
        feat_sel_alg_choice = self.selectOption(choices = [1, 2])

        model_validator = self.getValidator()

        self.header()
        fetcher = fs.Fetcher()
        selection_alg = fetcher.get(fs.AlgorithmType(feat_sel_alg_choice))
        result_dict = selection_alg.search(validator = model_validator, num_features = num_features)
        
        print("Press Enter to continue: ")
        _ = input()

    def classifierSelection(self):

        self.header()
        print("\nPlease select a Classifier: ")
        print("\t (1) Naive KNN Classifier")

        classifierChoice = self.selectOption(choices = [1])

        self.header()
        print("\n Please select the number of neighbors to use for k: ")
        k = self.enterInteger()

        if classifierChoice == 1:
            self.classifier = classifier.NaiveKNNClassifier(k)
        
        self.status_message = "Classifier Updated!"
    
    def testNewPoint(self):
        if not self.checkModelIsTrained():
            return

        self.header()
        feature_dimmensions = len(self.data[0].features)
        print(f"\nCurrent Feature Space Dimmension: {feature_dimmensions}")
        print("\nPlease enter features separated by space: ")

        try:
            features = self.enterFloats(num_vals = feature_dimmensions)
            if len(features) == 0:
                self.status_message = "Unable to Classify Point: Cancelled by User"
                return
            test_point = Point(label = None, features = features)
            test_point = self.classifier.test(test_point)
            print(f"\nClassification is {test_point.label}")
        except Exception as error:
            print(f"error: {error}")

        print("\nPress Enter to continue: ")
        _ = input()

    def validateModel(self):
        if not self.checkModelIsTrained():
            return

        self.header()
        available_features = [idx + 1 for idx in range(len(self.data[0].features))]

        print("\nWhich features would you like to test?")
        print(f"Available Features: {available_features}")
        print("Please enter features separated by spaces or press enter to use all of them.")
        chosen_features = self.enterFeatures(available_features)

        if chosen_features == None:
            return
        
        model_validator = self.getValidator()
        accuracy = model_validator.evaluate(chosen_features)

        print(f"Accuracy using features {chosen_features} is  {round(100.0 * accuracy) / 100.0 }%")

        print("\nPress Enter to continue: ")
        _ = input()
    
    def getValidator(self) -> validator.Validator:
        self.header()
        print("\nPlease select a validation algorithm:")
        print("\t(1) Random Validator")
        print("\t(2) Leave-One-Out Validator")

        validator_alg_choice = self.selectOption(choices = [1, 2])

        model_validator = None
        if validator_alg_choice == 1:
            model_validator = validator.RandomValidator()     
        elif validator_alg_choice == 2:
            model_validator = validator.LeaveOneOutValidator(classifier = self.classifier, validation_data = self.data)
        
        return model_validator
    
    def checkModelIsTrained(self):
        self.header()

        if not self.classifier.isTrained:
            print(f"\nModel must be trained first! Would you like to train using dataset: {self.data_file}?")
            print("\t(1) Yes")
            print("\t(2) No")

            defaultTrainingChoice = self.selectOption(choices = [1, 2])
            
            if defaultTrainingChoice == 1:
                self.classifier.train(self.data)

            elif defaultTrainingChoice == 2:
                return False
        
        return True


    # HELPER METHODS
    def header(self):
        title = """     __  ,_ __  _ __      ,___ _                          
    ( /,/( /  )( /  )    /   ///             o  /)o       
     /<   /  /  /  /    /    // __,  (   (  ,  //,  _  _  
    /  \_/  (_ /  (_   (___/(/_(_/(_/_)_/_)_(_//_(_(/_/ (_
       w/ Feature Selection & Validation     /)  by Shawn Long         
                                            (/  SID: 862154223
        """

        if os.name == "nt":
            _ = os.system("cls")
        else:
            _ = os.system("clear")

        print(title)

    def enterInteger(self):
        cancelledByUser = False
        try:
            input_str = input().strip()

            val = int(input_str)
        except:
            isInteger = False

            while not isInteger and not cancelledByUser:
                try:
                    isInteger = True
                    print(f"Invalid selection. Please enter an integer greater than zero or q to return to main menu:")
                    input_str = input().strip()

                    if input_str == "q":
                        cancelledByUser = True
                        break
                    val = int(input_str)
                except:
                    isInteger = False
        if cancelledByUser:
            return -1
        else:
            return val

    def enterFeatures(self, available_features):
        try:
            feature_set = set(available_features)
            cancelledByUser = False
            input_str = input().strip()

            vals = None
            if input_str == "":
                vals = available_features
            else:
                vals = list(set([int(val) for val in input_str.split(" ") if not val == ""]))
            
            if not set(vals).issubset(feature_set):
                vals = None
                raise Exception("Must enter a subset of the available features")

        except:
            valuesAreValid = False

            iterations = 1
            while not valuesAreValid and not cancelledByUser:
                try:
                    valuesAreValid = True
                    print(f"Invalid selection. Please enter list of features separated by spaces, enter to include all available features, or q to return to main menu:")
                    input_str = input().strip()

                    if input_str == "q":
                        cancelledByUser = True
                        break
                    elif input_str == "":
                        vals = available_features
                    else:
                        vals = list(set([int(val) for val in input_str.split(" ") if not val == ""]))
                    if not set(vals).issubset(available_features):
                        vals = None
                        raise Exception("Must enter a subset of the available features")
                    iterations += 1
                except:
                    valuesAreValid = False
                    iterations += 1
        if cancelledByUser:
            return None
        else:
            return vals

    def enterFloats(self, num_vals):
        try:
            input_str = input().strip()
            cancelledByUser = False

            vals = [float(val) for val in input_str.split(" ") if not val == ""]
            if not len(vals) == num_vals:
                raise ValueError(f"Must enter {num_vals} values")
        except:
            valsAreFloats = False

            iterations = 1
            while not valsAreFloats and not cancelledByUser:
                try:
                    valsAreFloats = True
                    print(f"Invalid selection. Please enter list of {num_vals} floats separated by spaces or q to return to main menu:")
                    input_str = input().strip()

                    if input_str == "q":
                        cancelledByUser = True
                        break
                    vals = [float(val) for val in input_str.split(" ") if not val == ""]
                    if not len(vals) == num_vals:
                        raise ValueError(f"Must enter {num_vals} values")
                    iterations += 1
                except:
                    valsAreFloats = False
                    iterations += 1
        if cancelledByUser:
            return []
        else:
            return vals

    def selectOption(self, choices) -> int:
        try:
            val = int(input())
            if not val in choices:
                raise ValueError()
        except:
            val = -1
            while not (val in choices):
                print(f"Invalid selection. Please enter one the following; {choices}, or q to return to main menu")
                try:
                    val = input()
                    if str(val).strip() == "q":
                        print("Exiting program")
                        exit()
                    val = int(val)
                except Exception as e:
                    self.log.debug(f"CAUGHT ERROR: {e}")
        return val

if __name__ == '__main__':
    cli = CLI()
    cli.run()
