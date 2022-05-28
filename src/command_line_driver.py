import logging
from sys import stdin
from src import feature_selection as fs
from src import validator
from src import classifier
from src import data_fetcher

# Global Function
input = stdin.readline

class CLI:
    # CLI ATTRIBUTES
    log = logging.getLogger(__name__)

    # MAIN METHOD FOR THE CLI
    def run(self):
        self.header()
        print("\nWelcome to KNN Clasifier!")
        print("Please select an option:")
        print("\t(1) Feature Selection")
        print("\t(2) Train A Model")
        print("\t(3) Test a Model")
        print("\t(4) Validate a Model")
        
        menuChoice = self.selectOption(choices = [1, 2, 3, 4])

        print("\nWould you like to use a custom dataset?")
        print("\t(1) Yes")
        print("\t(2) No")

        customDataChoice = self.selectOption(choices = [1, 2])

        if customDataChoice == 1:
            self.selectInputData()
        elif customDataChoice == 2:
            print("Using default data set")    

        if menuChoice == 1:
            self.featureSelection()
        elif menuChoice == 2:
            my_classifier = classifier.NaiveKNNClassifier(3)
            print("This feature is still in progress!")
        elif menuChoice == 3:
            print("This feature is still in progress!")
        elif menuChoice == 4:
            print("This feature is still in progress!")


    # MAIN FEATURE METHODS

    def featureSelection(self):
        print("\nPlease enter the total number of features: ")
        num_features = self.enterInteger()
        print("\nPlease select a feature selction algorithm: ")
        print("\t(1) Forward Selection")
        print("\t(2) Backward Elimination")
        choice = self.selectOption(choices = [1, 2])

        fetcher = fs.Fetcher()
        selection_alg = fetcher.get(fs.AlgorithmType(choice))
        rand_validator = validator.RandomValidator()
        result_dict = selection_alg.search(validator = rand_validator, num_features = num_features)


    # HELPER METHODS
    def header(self):
        title = """     __  ,_ __  _ __      ,___ _                          
    ( /,/( /  )( /  )    /   ///             o  /)o       
     /<   /  /  /  /    /    // __,  (   (  ,  //,  _  _  
    /  \_/  (_ /  (_   (___/(/_(_/(_/_)_/_)_(_//_(_(/_/ (_
       w/ Feature Selection & Validation     /)  by Shawn Long         
                                            (/  SID: 862154223
        """
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

    def selectInputData(self):
        print("\nTo import a custom dataset, please follow the instructions in the readme.")

        fetcher = data_fetcher.Fetcher()
        available_datasets = fetcher.available_datasets()

        if len(available_datasets) == 0:
            print("No datasets found. Please double check your file/formatting.")
            print("Quitting Application.")
        else:
            print(f"\nFound {len(available_datasets)} datasets! Please select one of the following:")
            for (index, dataset) in enumerate(available_datasets):
                print(f"\t({index + 1}) {dataset}")

        option = self.selectOption(choices = list(range(1, len(available_datasets) + 1)))
        dataset = available_datasets[option - 1]
        return fetcher.load_dataset(dataset)

if __name__ == '__main__':
    cli = CLI()
    cli.run()
