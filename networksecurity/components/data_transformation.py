import os,sys
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging

from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact
from networksecurity.constant.training_pipeline import TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.utils.main_utils.utils import save_numpy_array, save_object


class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        try:
            self.data_transformation_config : DataTransformationConfig = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path: str)->pd.DataFrame:
        """
        It reads the file from the filepath and returns a dataframe.

        Args:
            file_path (str): file path

        Returns:
            pd.DataFrame: a dataframe object
        """
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def get_data_transfomer_object(self)->Pipeline:
        """
        It initiated a KNN imputer object with the parameter specified in the/training_pipeline/__init__.py file
        and returns a pipeline object with KNN imputer at the first step.

        Returns:
            Pipeline: A pipeline object
        """
        try:
            logging.info("Entered the get_data_transfomer_object method of the DataTransformation class")
            
            preprocessor = Pipeline([('imputer', KNNImputer(DATA_TRANSFORMATION_IMPUTER_PARAMS))])
            
            logging.info("Exited get_data_transfomer_object method of the DataTransformation class")
            
            return preprocessor
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info("Reading validated train and test dataset")
            valid_train_df = self.read_data(self.data_validation_artifact.valid_train_file_path)
            valid_test_df = self.read_data(self.data_validation_artifact.valid_test_file_path)
            logging.info("Reading validated train and test dataset completed")
            
            logging.info("loading preprocessor object")
            preprocessor_obj = self.get_data_transfomer_object()
            
            logging.info("Splitting the features into independet and dependent features")
            ## splitting features into independet and dependent features
            ## train dataframe
            input_feature_train_df = valid_train_df.drop(TARGET_COLUMN, axis=1)
            target_feature_train_df = valid_train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)
            
            ## test dataframe
            input_feature_test_df = valid_test_df.drop(TARGET_COLUMN, axis=1)
            target_feature_test_df = valid_test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0)
            
            logging.info("Applying preprocessing on train and test independent features")
            ## applying the transformation
            input_feature_train_array = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_array = preprocessor_obj.transform(input_feature_test_df)
            
            ## concatinating the test and train data as array
            train_arr = np.c_[input_feature_train_array, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_array,np.array(target_feature_test_df)]
            
            save_object(file_path= self.data_transformation_config.transformed_object_file_path,obj= preprocessor_obj)
            
            logging.info("Preprocessor pickel is created")
            
            ## train array saved
            save_numpy_array(file_path = self.data_transformation_config.data_transformation_train_file_path, arr = train_arr)
            logging.info("Train array is saved")
            
            save_numpy_array(file_path = self.data_transformation_config.data_transformation_test_file_path, arr = test_arr)
            logging.info("Test array is saved")
            
            ## preparing artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path = self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path = self.data_transformation_config.data_transformation_train_file_path,
                transformed_test_file_path = self.data_transformation_config.data_transformation_test_file_path
            )
            
            logging.info(f"Data transformation artifact: {data_transformation_artifact}")
            
            return data_transformation_artifact            
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
