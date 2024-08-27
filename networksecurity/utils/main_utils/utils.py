import os,sys
import dill
import pickle
import numpy as np
import yaml
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

