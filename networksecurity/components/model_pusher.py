import os, sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging
from networksecurity.entity.config_entity import ModelPusherConfig
from networksecurity.entity.artifact_entity import ModelPusherArtifact, ModelEvaluationArtifact
import shutil

class ModelPusher:
    def __init__(self, model_pusher_config:ModelPusherConfig,
                 model_evaluation_artifact:ModelEvaluationArtifact):
        try:
            self.model_pusher_config = model_pusher_config
            self.model_evaluation_artifact = model_evaluation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def initiate_model_pusher(self)->ModelPusherArtifact:
        try:
            logging.info("Initiating model pusher")
            trained_model_path = self.model_evaluation_artifact.trained_model_path
            
            ## saving model in artifact
            model_file_path = self.model_pusher_config.model_file_path
            os.makedirs(os.path.dirname(model_file_path), exist_ok=True)
            shutil.copy(src=trained_model_path, dst=model_file_path)
            logging.info("Model saved in artifact")
            
            ## saving model in saved model
            saved_model_path = self.model_pusher_config.saved_model_path
            os.makedirs(os.path.dirname(saved_model_path),exist_ok=True)
            shutil.copy(src=trained_model_path,dst=saved_model_path)
            logging.info("Model saved in saved model")
            
            ## artifact
            model_pusher_artifact = ModelPusherArtifact(
                saved_model_path=saved_model_path,
                model_file_path=model_file_path
            )
            logging.info("Model puhser completed")
            return model_pusher_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)