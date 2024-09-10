import os
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging
from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME

class NetworkModel:
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def data_predict(self,x):
        try:
            ## transform and predict the new values
            x_transformed = self.preprocessor.transform(x)
            y_pred = self.model.predict(x_transformed)
            return y_pred
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    
class ModelResolver:
    def __init__(self, model_dir = SAVED_MODEL_DIR):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def get_best_model_path(self)->str:
        try:
            ## find the path of the best model
            timestamp = list(map(int,os.listdir(self.model_dir)))
            latest_timestamp = max(timestamp)
            latest_model_path = os.path.join(self.model_dir,f"{latest_timestamp}",MODEL_FILE_NAME)
            return latest_model_path
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def is_model_exists(self)->bool:
        try:
            ## check if model path exists if not return False else True
            if not os.path.exists(self.model_dir):
                return False
            
            timestamp = os.listdir(self.model_dir)
            if len(timestamp)==0:
                return False
            
            latest_model_path = self.get_best_model_path()
            
            if not os.path.exists(latest_model_path):
                return False
            
            return True
            
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)