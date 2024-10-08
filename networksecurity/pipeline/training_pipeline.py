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

from networksecurity.cloud.s3_syncer import S3Sync
from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR, TRAINING_BUCKET_NAME

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
    is_pipeline_running = False
    def __init__(self):
        ## creating an instance variable of class TrainingPipeline and holds an object of class TrainingPipelineConfig
        self.training_pipeline_config=TrainingPipelineConfig()
        self.s3_sync = S3Sync()
    
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
        
    def start_model_evaluation(self, model_trainer_artifact: ModelTrainerArtifact,
                               data_validation_artifact:DataValidationArtifact):
        try:
            logging.info("Model evaluation process started")
            
            model_evaluation_config = ModelEvaluationConfig(training_pipeline_config=self.training_pipeline_config)
            ## creating obj of model evaluation
            model_evaluation_obj = ModelEvaluation(model_evaluation_config = model_evaluation_config,
                                                   model_trainer_artifact = model_trainer_artifact,
                                                   data_validation_artifact = data_validation_artifact)
            
            ## model evaluation artifact
            model_evaluation_artifact = model_evaluation_obj.initiate_model_evaluation()
            logging.info(f"Model pusher process completed and artifact: {model_evaluation_artifact}")
                       
            return model_evaluation_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_model_pusher(self,model_evaluation_artifact: ModelEvaluationArtifact):
        try:
            logging.info("Model pusher process started")
            
            model_pusher_config = ModelPusherConfig(training_pipeline_config=self.training_pipeline_config)
            
            model_pusher_obj = ModelPusher(model_pusher_config=model_pusher_config,
                                           model_evaluation_artifact=model_evaluation_artifact)
            model_pusher_artifact = model_pusher_obj.initiate_model_pusher()
            
            return model_pusher_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def sync_artifact_dir_to_s3(self):
        try:
            ## aws bucker url
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder=self.training_pipeline_config.artifact_dir,aws_bucker_url=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def sync_saved_model_to_s3(self):
        try:
            aws_bucker_url = f"s3://{TRAINING_BUCKET_NAME}/{SAVED_MODEL_DIR}"
            self.s3_sync.sync_folder_to_s3(folder=SAVED_MODEL_DIR, aws_bucker_url=aws_bucker_url)
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
            
            model_evaluation_artifact = self.start_model_evaluation(model_trainer_artifact= model_trainer_artifact, 
                                                                    data_validation_artifact=data_validation_aritfact)
            print(model_evaluation_artifact)
            
            model_pusher_artifact = self.start_model_pusher(model_evaluation_artifact=model_evaluation_artifact)
            print(model_pusher_artifact)
            
            TrainingPipeline.is_pipeline_running = False
            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_to_s3()
            logging.info("AWS Sync Completed")
            
        except Exception as e:
            self.sync_artifact_dir_to_s3()
            TrainingPipeline.is_pipeline_running = False
            raise NetworkSecurityException(e,sys)