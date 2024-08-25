import os
import sys
import pandas as pd
import numpy as np
import pymongo
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging

from networksecurity.entity.config_entity import  DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

class DataIngestion:
    
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_collection_as_dataframe(self):
        try:
            ## getting mongodb database name
            database_name = self.data_ingestion_config.database_name
            
            ## mongodb collection name
            collection_name = self.data_ingestion_config.collection_name
            
            ## creating a connection with mongodb
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            
            ## accessing the collection from mongodb
            collection = self.mongo_client[database_name][collection_name]
            
            ## converting the documents into dataframe
            df = pd.DataFrame(list(collection.find()))
            
            ## dropping the _id column from our dataframe
            if "_id" in df.columns.to_list():
                df = df.drop(columns = ["_id"], axis=1)
                
            ## replacing all na as nan
            df.replace({"na":np.nan}, inplace=True)

            ## returning the dataframe
            return df
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_data_into_framestore(self, dataframe: pd.DataFrame):
        try:
            ## reading the path for saving feature store file
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            
            ## creating a directory to save the feature store file
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            
            ## saving the raw file in csv format
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            
            ## returning the dataframe
            return dataframe
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            ## splitting the data in train and test set
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            
            ## creating a directory to save the train set file
            dir_path_train = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path_train, exist_ok=True)
            
            ## saving the train file in csv format
            train_set.to_csv(self.data_ingestion_config.training_file_path, index = False, header = True)
            
            ## creating a directory to save the test set file
            dir_path_test = os.path.dirname(self.data_ingestion_config.testing_file_path)
            os.makedirs(dir_path_test,exist_ok=True)
            
            ## saving the train file in csv format
            test_set.to_csv(self.data_ingestion_config.testing_file_path)
            
            return(
                self.data_ingestion_config.training_file_path,
                self.data_ingestion_config.testing_file_path
            )
            
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_ingestion(self):
        try:
            ## calling method to get data
            dataframe = self.export_collection_as_dataframe()
            
            ## calling method to save the raw file
            dataframe = self.export_data_into_framestore(dataframe)
            
            ## calling method to split the data and return train test file path
            train_set_path, test_set_path= self.split_data_as_train_test(dataframe)
            
            data_ingestion_artifact = DataIngestionArtifact(train_file_path = train_set_path, test_file_path = test_set_path)
            
            return data_ingestion_artifact
            
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)