import os,sys
from networksecurity.logger.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import ModelEvaluationConfig
from networksecurity.entity.artifact_entity import ModelTrainerArtifact, DataValidationArtifact, ModelEvaluationArtifact
from networksecurity.utils.main_utils.utils import save_object, load_object
from networksecurity.utils.ml_utils.model.estimator import ModelResolver
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
import pandas as pd

class ModelEvaluation:
    def __init__(self,model_evaluation_config:ModelEvaluationConfig,
                 model_trainer_artifact: ModelTrainerArtifact,
                 data_validation_artifat: DataValidationArtifact):
        try:
            self.model_evaluation_config = model_evaluation_config
            self.model_trainer_artifact = model_trainer_artifact
            self.data_validation_artifact = data_validation_artifat
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_model_evaluation(self)->ModelEvaluationArtifact:
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)