import os, sys
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier


from networksecurity.logger.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel, ModelResolver
from networksecurity.utils.main_utils.utils import load_numpy_array, save_object,load_object


class ModelTrainer:
    def __init__(self, model_trainer_config:ModelTrainerConfig, 
                 data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def perform_hyper_parameter_tuning(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def train_model(self,x_train,y_train,x_test,y_test,models):
        try:
            report = {}
            
            ## iterate over each model
            for i in range(len(models)):
                model = list(models.values())[i]
                ## model fit
                model.fit(x_train,y_train)
                ## model prediction
                y_test_pred = model.predict(x_test)
                y_train_pred = model.predict(x_train)
                ## return classification score
                y_test_model_score=get_classification_score(y_test,y_test_pred)
                y_train_model_score = get_classification_score(y_train, y_train_pred)
                
                ## saving the evaluation in report
                report[list(models.keys())[i]] = {'test_score':y_test_model_score,'train_score': y_train_model_score}
                
            return report
                
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def find_best_model(model_report):
        try:
            model_name = max(model_report, key=lambda k : model_report[k]['test_score'].f1_score)
            model_test_f1_score = model_report[model_name]['test_score'].f1_score
            model_train_f1_score = model_report[model_name]['train_score'].f1_score
            return (model_name, model_test_f1_score, model_train_f1_score)
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_model_trainer(self):
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            
            train_arr = load_numpy_array(file_path=train_file_path)
            test_arr = load_numpy_array(file_path=test_file_path)
            
            x_train, y_train, x_test, y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )
            
            models = {
                'Random_Forest' : RandomForestClassifier(),
                'XGBoost' : XGBClassifier()
            }
            
            model_report = dict(self.train_model(x_train, y_train, x_test, y_test, models))
            best_model_name, best_model_test_score, best_model_train_score = self.find_best_model(model_report)
            
            if best_model_train_score<= self.model_trainer_config.expected_accuracy:
                print("Trained model is not good to provide expected accuracy")
            
            ## check for overfit and underfit
            diff = abs(best_model_train_score - best_model_test_score)
            if diff > self.model_trainer_config.overfitting_underfitting_threshold:
                raise Exception(f'Model {best_model_name} is not good try to do more experimentation.
                                \n Train F1 Score : {best_model_train_score} 
                                \n Test F1 Score : {best_model_test_score}')
                
            print(f'Best Model Found, Model Name : {best_model_name}, F1 Score : {best_model_test_score}')
            print('\n===============================================================================')
            
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)