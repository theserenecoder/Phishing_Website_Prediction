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
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def initiate_model_pusher(self)->ModelPusherArtifact:
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)