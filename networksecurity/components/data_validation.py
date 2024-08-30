import os
import sys
import pandas as pd

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.pipeline.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
from networksecurity.utils.main_utils import read_yaml_file, write_yaml_file

class DataValidation:
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation_config = data_validation_config
        self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
    
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            ## read file 
            return pd.read_csv(file_path)
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def validate_number_of_columns(self, dataframe:pd.DataFrame)->bool:
        try:
            ## calculate number of columns from schema.yaml file
            number_of_columns = len(self._schema_config['columns'])
            
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Dataframe has columns: {len(dataframe.columns)}")
            
            ## compare number of dataframe columns with schema columns return if matched
            if len(dataframe.columns)==number_of_columns:
                return True
            
            else:
                return False
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def is_numerical_column_exists(self, dataframe: pd.DataFrame)->bool:
        try:
            ## get all numerical columns
            numerical_columns = self._schema_config["numerical_columns"]
            ## set the trigger as True
            num_col_present = True
            ## create and empty list to store all the missing columns
            missing_col = []
            ## check that all the numerical columns from schema are present in the dataframe
            for num in numerical_columns:
                if num not in dataframe.columns:
                    ## if not set the trigger to false
                    num_col_present = False
                    ## append missing columns to the list
                    missing_col.append(num)
                    
            logging.info(f"Missing numerical columns: [{missing_col}]")
            return num_col_present    
                    
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def detect_dataset_drift(self, base_df, current_df, threshold=0.5)->bool:
        """Method to check if both the dataframes are drawn from the same distribution"""
        try:
            ## set status default to True, this will be return and will tell us therewas any drift between the 2 dataframes
            status = True
            ## create an empty dictionary
            report = {}
            ## run a loop to get data column wise from two seprate dataframes
            for col in base_df.columns:
                d1 = base_df[col]
                d2 = current_df[col]
                ## run ks test for goodness of fit test
                good_fit_test = ks_2samp(d1,d2)
                ## check if pvalue is less than threshold then reject null hypothesis
                if ks_2samp.pvalue <= threshold:
                    is_found = True
                    status = False
                ## else we fail to reject null hypothesis
                else:
                    is_found = False
                ## update the dictionary with pvalue and drift status
                report.update({col:{"p_value":float(good_fit_test.pvalue),
                                    "drift_status":is_found}})
                
                drift_report_file_path=self.data_validation_config.drift_report_file_path
                
                ## create directory
                dir_path = os.path.dirname(drift_report_file_path)
                os.makedirs(dir_path, exist_ok=True)
                ## write content on yaml file
                write_yaml_file(file_path=drift_report_file_path, content = report)
                
                return status
                
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_validation(self):
        try:
            ## train file path from data ingestion artifact
            train_file_path  = self.data_ingestion_artifact.train_file_path
            ## test file path from data ingestion artifact
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            ## reading data from train and test files from artifact folder
            train_dataframe = self.read_data(file_path=train_file_path)
            test_dataframe = self.read_data(file_path=test_file_path)
            
            ## validate number of columns
            train_status = self.validate_number_of_columns(train_dataframe)
            if not train_status:
                ## if status is false set error message
                error_message = f"Train dataframe does not contain all columns."
                logging.error(error_message)
            test_status = self.validate_number_of_columns(test_dataframe)
            if not test_status:
                error_message = f"Test dataframe does not contain all columns."
                logging.error(error_message)
            # if len(error_message)>0:
            #    raise Exception(error_message)
                
            ## check datadrift status
            drift_status = self.detect_dataset_drift(train_dataframe, test_dataframe)
            
            if train_status and test_status and drift_status:
                ## make valid directory
                dir_path = self.data_validation_config.valid_train_file_path
                os.makedirs(dir_path, exist_ok=True)
                ## save train dataframe
                train_dataframe.to_csv(self.data_validation_config.valid_train_file_path, header=True, index=False)
                logging.info("Train dataframe validated")
                ## save test dataframe
                test_dataframe.to_csv(self.data_validation_config.valid_test_file_path, header=True, index=False)
                logging.info("Test dataframe validated")
            else:
                logging.info("Dataset failed validation")
                ## make invalid directory
                dir_path = self.data_validation_config.invalid_train_file_path
                os.makedirs(dir_path, exist_ok=True)
                ## save train dataframe
                train_dataframe.to_csv(self.data_validation_config.invalid_train_file_path, header=True, index=False)
                ## save test dataframe
                test_dataframe.to_csv(self.data_validation_config.invalid_test_file_path,header=True,index=False)
                
            data_validation_artifact = DataValidationArtifact(
                validation_status=drift_status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            
            logging.info(f"Data validation artifact : {data_validation_artifact}")
            
            return data_validation_artifact
             
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    