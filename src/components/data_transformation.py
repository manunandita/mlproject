import os 
import sys
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_file_path=os.path.join("artifacts","preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transfromation_config=DataTransformationConfig()
    def generate_data_transformtion(self):
        try:
            numerical_features=["PM2.5","PM10","O3","SO2","CO","Wind Speed","Humidity","Temp"]
            categorical_features=["State","City","AQI Type"]

            num_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="mean")),
                    ("standardscaler",StandardScaler())
                ]
            )
            cat_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoding",OneHotEncoder(drop="first",handle_unknown="ignore")),
                    ("standardscaler",StandardScaler(with_mean=False))
                ]
            )

            logging.info(f"numerical features:{numerical_features}")
            logging.info(f"categorical features:{categorical_features}")

            preprocessor=ColumnTransformer(
                transformers=[
                    ("num_transformation",num_pipeline,numerical_features),
                    ("cat_transformation",cat_pipeline,categorical_features)
                ]
            )

            logging.info("transformation has initiated")
            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)

    def initiating_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("read the train and test data")

            target_train_column_feature=train_df["AQI"]
            input_train_column_feature=train_df.drop("AQI",axis=1)

            target_test_column_feature=test_df["AQI"]
            input_test_column_feature=test_df.drop("AQI",axis=1)
            logging.info("extarcted the dependent and independent features from train and test data")

            preprocessor_obj=self.generate_data_transformtion()

            preprocessor_obj.fit_transform(input_train_column_feature)
            preprocessor_obj.transform(input_test_column_feature)

            logging.info("transformation done on both train as well as test data")

            train_arr=np.c_[input_train_column_feature,np.array(target_train_column_feature)]
            test_arr=np.c_[input_test_column_feature,np.array(target_test_column_feature)]

            save_object(
                file_path=self.data_transfromation_config.preprocessor_file_path,
                file_obj=preprocessor_obj
            )

            return(
                train_arr,test_arr,self.data_transfromation_config.preprocessor_file_path
            )

        except Exception as e:
            raise CustomException(e,sys)




