import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.components.model_evaluation import ModelEvaluation
from networksecurity.components.model_pusher import ModelPusher

from networksecurity.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
    ModelEvaluationConfig,
    ModelPusherConfig
)

from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact,
    ModelEvaluationArtifact,
    ModelPusherArtifact
)

class TrainingPipeline:
    
    def __init__(self):
        ## creating an instance variable of class TrainingPipeline and holds an object of class TrainingPipelineConfig
        self.training_pipeline_config=TrainingPipelineConfig()
    
    def start_data_ingestion(self):
        try:
            logging.info("Starting data ingestion process")
            ## creating an instance variable of class TrainingPipeline and holds an object of class DataIngestionConfig
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config= self.training_pipeline_config)
            ## object of class data ingestion
            data_ingestion_obj = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            ## calling method initiate_data_ingestion to start the data ingestion process
            data_ingestion_artifact= data_ingestion_obj.initiate_data_ingestion()
            logging.info(f"Data ingestion process completed and artifact: {data_ingestion_artifact}")
          
            return data_ingestion_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact):
        try:
            logging.info("Starting data validation process")
            
            ## creating an instance variable of class Training pipeline and holds an object of class DataIngestionConfig
            data_validation_config = DataValidationConfig(training_pipeline_config= self.training_pipeline_config)
            ## object of class Data Validation
            data_validation_obj= DataValidation(data_validation_config=data_validation_config, data_ingestion_artifact =data_ingestion_artifact)
            ## calling method initiate_data_validation to start the data validation process
            data_validation_artifact = data_validation_obj.initiate_data_validation()
            
            logging.info(f"Data validation process completed and artifact: {data_validation_artifact}")
            
            return data_validation_artifact
               
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_transformation(self, data_validation_artifact:DataValidationArtifact):
        try:
            logging.info("Data transformation process started")
            
            data_transformation_config = DataTransformationConfig(training_pipeline_config= self.training_pipeline_config)
            
            data_transformation_obj = DataTransformation(data_transformation_config = data_transformation_config, 
                                                         data_validation_artifact = data_validation_artifact)
            
            data_transformation_artifact = data_transformation_obj.initiate_data_transformation()
            
            logging.info(f"Data validation process completed and artifact: {data_transformation_artifact}")
            
            return data_transformation_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_model_training(self, data_transformation_artifact: DataTransformationArtifact):
        try:
            logging.info("Model trainer process started")
            
            model_trainer_config = ModelTrainerConfig(training_pipeline_config= self.training_pipeline_config)
            
            model_trainer_obj = ModelTrainer(model_trainer_config=model_trainer_config,
                                             data_transformation_artifact=data_transformation_artifact)
            
            model_trainer_artifact = model_trainer_obj.initiate_model_trainer()
            
            logging.info(f"Model trainer process completed and artifact: {model_trainer_artifact}")
            
            return model_trainer_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_model_evaluation(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_model_pusher(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            print(data_ingestion_artifact)
            
            data_validation_aritfact = self.start_data_validation(data_ingestion_artifact)
            print(data_validation_aritfact)
            
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_aritfact)
            print(data_transformation_artifact)
            
            model_trainer_artifact = self.start_model_training(data_transformation_artifact=data_transformation_artifact)
            print(model_trainer_artifact)
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)