import logging
from sys import stdin
from src import feature_selection as fs
from src import validator
from src import classifier
from src import data_fetcher
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

            print("\n\t(3) Feature Selection")
            print("\t(4) Train A Model")
            print("\t(5) Test a Model")
            print("\t(6) Validate a Model")

            print("\n\t(9) Quit")
            
            menuChoice = self.selectOption(choices = [1, 2, 3, 4, 5, 6, 9])

            if menuChoice == 1:
                self.selectInputData()

            elif menuChoice == 2:
                self.classifierSelection()

            elif menuChoice == 3:
                self.featureSelection()

            elif menuChoice == 4:
                my_classifier = classifier.NaiveKNNClassifier(3)

            elif menuChoice == 5:
                print("This feature is still in progress!")

            elif menuChoice == 6:
                print("This feature is still in progress!")

            elif menuChoice == 9:
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
        self.status_message = "Sucessfully Loaded data!"

    def featureSelection(self):
        self.header()
        
        print("\nPlease enter the total number of features: ")
        num_features = self.enterInteger()

        self.header()
        print("\nPlease select a feature selction algorithm: ")
        print("\t(1) Forward Selection")
        print("\t(2) Backward Elimination")
        choice = self.selectOption(choices = [1, 2])

        self.header()
        fetcher = fs.Fetcher()
        selection_alg = fetcher.get(fs.AlgorithmType(choice))
        rand_validator = validator.RandomValidator()
        result_dict = selection_alg.search(validator = rand_validator, num_features = num_features)
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
        try:
            val = int(input())
        except:
            inputIsInteger = False
            
            while not inputIsInteger:
                try:
                    inputIsInteger = True
                    print("Invalid selction. Please enter an integer greater than zero: ")
                    val = int(input())
                except:
                    inputIsInteger = False
        return val


    def selectOption(self, choices) -> int:
        try:
            val = int(input())
            if not val in choices:
                raise ValueError()
        except:
            val = -1
            while not (val in choices):
                print(f"Invalid selection. Please enter one the following; {choices}, or q to quit")
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
