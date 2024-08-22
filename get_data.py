import os
import sys
import json

import pymongo.mongo_client

## load_dotenv reads key-value pairs from .env file and set them as enviornment variables.
from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

## Certify provides Mozilla's collection of Root certificates for validating the trustworthiness of SSL cartificates while verifying the identity of TLS hosts.
## where() function installs the certificate authority bundel
import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging

class NetworkDataExtraction():
    
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json_convertor(self, file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def pushing_data_to_mongobd(self, records, database,collection):
        try:
            self.database = database
            self.collection=collection
            self.records = records
            
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return len(self.records)
            
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
if __name__ == '__main__':
    obj = NetworkDataExtraction()
    FilePath = "./Network_Data/NetworkData.csv"
    Database = "Phishing_Website_Prediction"
    Collection = "Phishing_Website_Prediction_Data"
    Records = obj.csv_to_json_convertor(FilePath)
    noofobj=obj.pushing_data_to_mongobd(Records,Database,Collection)
    print(noofobj)