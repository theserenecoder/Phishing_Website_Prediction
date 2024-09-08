import os
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging
from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME

class NetworkModel:
    def __init__(self, preprocessor, model):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def predict(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    
class ModelResolver:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def get_best_model_path(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def is_model_exists(self)-->bool:
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)