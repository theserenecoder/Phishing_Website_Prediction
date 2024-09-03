import os,sys
import dill
import pickle
import numpy as np
import yaml
import pickle
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging

def read_yaml_file(file_path):
    try:
        ## open the file in read byte mode
        with open(file_path,"rb") as file:
            ## load yaml data into python object
            return yaml.safe_load(file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def write_yaml_file(file_path:str, content:object, replace:bool = False)->None:
    try:
        ## check if replace is true or not
        if replace:
            ## if true, delete the file if exist and make a new file
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        ## open file in write mode and dump the content
        with open(file_path, "w") as file:
            yaml.dump(content,file)
            
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_numpy_array(file_path:str, arr: np.array) -> None:
    try:
        ## save numpy array data to file
        dir_name = os.path.dirname(file_path)
        os.makedirs(dir_name, exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj, arr)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def load_numpy_array(file_path: str):
    try:
        ## load numpy array data from file
        with open(file_path) as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_object(file_path:str, obj:object) -> None:
    try:
        ## saving pickle file
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path,'wb') as file_obj:
            pickle.dump(obj,file_obj)
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def load_object(file_path:str):
    try:
        ## raise error if pickle file doesn't exists
        if not os.path.exists(file_path):
            raise NetworkSecurityException(f"The file: {file_path} is not exists")
        ## load pickle object
        with open(file_path) as file_obj:
            return pickle.load(file_obj)
            
    except Exception as e:
        raise NetworkSecurityException(e,sys)

