import os
import sys
from sklearn.metrics import f1_score, precision_score, recall_score

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging
from networksecurity.entity.artifact_entity import ClassificationMetricArtifact


def get_classification_score(y_pred, y_actual)->ClassificationMetricArtifact:
    try:
        model_f1_score = f1_score
        model_precision_score = precision_score
        model_recall_score = recall_score
        
        classification_metric = ClassificationMetricArtifact(f1_score = model_f1_score,
                                                             precision_score = model_precision_score,
                                                             recall_score = model_recall_score)
        
        return classification_metric
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
    