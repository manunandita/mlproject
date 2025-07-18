import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
import pandas as pd
from sklearn.model_selection import train_test_split
from src.components.data_transformation import DataTransformation,DataTransformationConfig

@dataclass
class DataIngestionConfig:
    train_data_path:str=os.path.join("artifacts","train.csv")
    test_data_path:str=os.path.join("artifacts","test.csv")
    raw_data_path:str=os.path.join("artifacts","data.csv")

class DataIngestion:
    def __init__(self):
        self.data_ingestion_config=DataIngestionConfig()
    def initiate_data_ingestion(self):
        logging.info("data ingestion has initiated")
        try:
            df_data=pd.read_csv("notebook/data/AQI_Data.csv")
            logging.info('read the data')
            os.makedirs(os.path.dirname(self.data_ingestion_config.raw_data_path),exist_ok=True)
            df_data.to_csv(self.data_ingestion_config.raw_data_path)

            os.makedirs(os.path.dirname(self.data_ingestion_config.train_data_path),exist_ok=True)
            os.makedirs(os.path.dirname(self.data_ingestion_config.test_data_path),exist_ok=True)

            logging.info("train test split initiated")
            train_set,test_set=train_test_split(df_data,test_size=.3,random_state=42)
            train_set.to_csv(self.data_ingestion_config.train_data_path)
            test_set.to_csv(self.data_ingestion_config.test_data_path)

            logging.info("train test split completed")

            return(
                self.data_ingestion_config.train_data_path,
                self.data_ingestion_config.test_data_path,
            )


        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":
    o=DataIngestion()
    train_data,test_data=o.initiate_data_ingestion()

    obj=DataTransformation()
    obj.initiating_data_transformation(train_data,test_data)

