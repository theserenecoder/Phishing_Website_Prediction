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
        
    def start_data_validation(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_transfromation(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_model_training(self):
        try:
            pass
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
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)