import logging
from sys import stdin

# Global Function
input = stdin.readline

class CLI:
    # CLI Attributes
    log = logging.getLogger(__name__)

    # THE Main CLI Function
    def run(self):
        self.header()
        print("Welcome to KNN Clasifier!")
        


    # Beginning of Helper Function
    def header(self):
        title = """     __  ,_ __  _ __      ,___ _                          
    ( /,/( /  )( /  )    /   ///             o  /)o       
     /<   /  /  /  /    /    // __,  (   (  ,  //,  _  _  
    /  \_/  (_ /  (_   (___/(/_(_/(_/_)_/_)_(_//_(_(/_/ (_
    w/ Feature Selection and Validation      /)           
                                            (/            
    BY SHAWN LONG (SID: 862154223)
        """
        print(title)

if __name__ == '__main__':
    cli = CLI()
    cli.run()