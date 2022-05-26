     __  ,_ __  _ __      ,___ _                          
    ( /,/( /  )( /  )    /   ///             o  /)o       
     /<   /  /  /  /    /    // __,  (   (  ,  //,  _  _  
    /  \_/  (_ /  (_   (___/(/_(_/(_/_)_/_)_(_//_(_(/_/ (_
       w/ Feature Selection & Validation     /)  by Shawn Long         
                                            (/  SID: 862154223



The goal of this project is to use the K-Nearest Neighbors algorithm to create an unspervised ML model for a data set. To improve the model, a validator is provided to evaluate the classifier, which can then be used with feature selection to narrow down the features to a more accurate subset of features.

## Usage

To run the app, simply run the following command from the project root:

```bash
python main.py
```

To run the app tests, run:

```
python main.py --test
```

or

```
python main.py -t
```

To run the app and tests at the same time, run:

```
python main.py --test --continue
```

or

```
python main.py -t -c
```



## References

Below is a list of sources I uses as reference while developing this application:

- [Zubair Khalid: Fast kNN - KD Tree](https://www.youtube.com/watch?v=lZs7VXdasnI)

- [Computerphile: K-d Trees](https://www.youtube.com/watch?v=BK5x7IUTIyU)
- [University of Colorado: K-D Trees aznd KNN Searches](https://www.colorado.edu/amath/sites/default/files/attached-files/k-d_trees_and_knn_searches.pdf)
- [Virginia Tech: Acceleration Struture for Ray Tracing - K-D Tree Traversal](https://people.cs.vt.edu/yongcao/teaching/csx984/fall2010/documents/Lecture10_Acceleration_structure.pdf)
