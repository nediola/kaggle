#### The dataset
https://www.kaggle.com/datasets/sameepvani/nasa-nearest-earth-objects

#### The task
1) Load the .csv dataset to MySQL
2) Train and compare the classification models with the following instruments
- Pandas and Catboost
- PySpark and GBTClassifier
3) Save the best model, save the prediction of the test dataset to MySql table and to the archived .parquet files

#### Files description
- _csv2mysql_db.py_ - script to load the original dataset to MySQL table
- _CatBoostVsGBTClassifier.ipynb_ - the ETL-pipeline
- _models/model_catboost.cbm_ - the best CatBoost model
- _models/model_gbt_ - the best GBTClassifier model
- _data/catboost_prediction.zip_ - the CatBoost model prediction of the test dataset
- _data/gbt_prediction.zip_ - the GBTClassifier model prediction of the test dataset
- _data/neo.csv, data/neo2.csv_ - the original kaggle datasets, here the neo2.csv was used

#### ETL steps
1) Load the original dataset from the MySQL table
2) Downsample the negative not-hazardous asteroids and split the dataset to the stratified train/test datasets
3) Optimize the CatBoost hyperparameters: depth, l2_leaf_reg (5 folds, the evaluation function is f-beta with beta=2 - recall is more important)
4) Calculate precision, recall, f1, f-beta of the CatBoost model to understand results better (with a 5-folds cross-validation)
5) Calculate prediction for the test dataset with the best CatBoost model
6) Save the CatBoost model and predictions
7) Optimize GBTClassifier hyperparameters: minInstancesPerNode, maxDepth, maxBins (5 folds, the evaluation function is f-beta with beta=2 - recall is more important)
8) Calculate precision, recall, f1, f-beta of the GBTClassifier model to understand results better (with a 5-folds cross-validation)
9) Calculate prediction for the test dataset with the best GBTClassifier model
10) Save the CatBoost model and predictions

#### Results
| Metrics  | CatBoost (depth=2, l2_leaf_reg=5) | GBTClassifier (minInstancesPerNode=1, maxDepth=5, maxBins=16) |
| ------------- | ------------- | ------------- |
| Precision  | 0.8045 | 0.9819 |
| Recall  | 0.983 | 0.7664 |
| F1 | 0.8849 | 0.8747 |
| F-beta (beta=2) | 0.9413 | 0.873 |

We can see, that the CatBoost recall, F1, and F2 metrics are higher, but the GBTClassifier has good precision.

