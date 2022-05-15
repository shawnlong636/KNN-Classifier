import logging
from sys import stdin

# Global Function
input = stdin.readline

class CLI:
    # CLI ATTRIBUTES
    log = logging.getLogger(__name__)

    # MAIN METHOD FOR THE CLI
    def run(self):
        self.header()
        print("Welcome to KNN Clasifier!")
        
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

if __name__ == '__main__':
    cli = CLI()
    cli.run()