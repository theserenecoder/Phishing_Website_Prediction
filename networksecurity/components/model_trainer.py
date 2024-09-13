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
            logging.info('Inside train model, model training start')
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
                logging.info(f"Model is {model}, Test Score: {y_test_model_score.f1_score}, Train Score: {y_train_model_score.f1_score}")
                logging.info('Exiting train model')
            return report
                
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def find_best_model(self,model_report:dict):
        try:
            logging.info('Inside find best model')
            
            model_name = max(model_report, key=lambda k : model_report[k]['test_score'].f1_score)
            model_test_score = model_report[model_name]['test_score']
            model_train_score = model_report[model_name]['train_score']
            
            logging.info('Exiting find best model, best model found')
            return (model_name, model_test_score, model_train_score)
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_model_trainer(self):
        try:
            logging.info("Initiating model trainer")
            
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            logging.info("Train and test transformed file path read")
            
            train_arr = load_numpy_array(file_path=train_file_path)
            test_arr = load_numpy_array(file_path=test_file_path)
            logging.info("Train and test array loaded")
            
            x_train, y_train, x_test, y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )
            logging.info("Train and test array split in dependent and independent variable")
            
            models = {
                'Random_Forest' : RandomForestClassifier(),
                'XGBoost' : XGBClassifier()
            }
            
            model_report = dict(self.train_model(x_train, y_train, x_test, y_test, models))
            best_model_name, best_model_test_score, best_model_train_score = self.find_best_model(model_report=model_report)
            
            if best_model_train_score.f1_score<= self.model_trainer_config.expected_accuracy:
                print("Trained model is not good to provide expected accuracy")
            
            ## check for overfit and underfit
            diff = abs(best_model_train_score.f1_score - best_model_test_score.f1_score)
            if diff > self.model_trainer_config.overfitting_underfitting_threshold:
                raise Exception(f"Model {best_model_name} is not good try to do more experimentation.Train F1 Score : {best_model_train_score.f1_score}.Test F1 Score : {best_model_test_score}")
                
            print(f'Best Model Found, Model Name : {best_model_name}, F1 Test Score : {best_model_test_score.f1_score}, F1 Train Score : {best_model_train_score.f1_score}')
            print('\n===============================================================================')
            logging.info(f'Best Model Found, Model Name : {best_model_name}, F1 Test Score : {best_model_test_score.f1_score}, F1 Train Score : {best_model_train_score.f1_score}')
            
            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            logging.info('Loading preprocessor')
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_path)
            os.makedirs(model_dir_path, exist_ok=True)
            
            Network_Model = NetworkModel(preprocessor=preprocessor, model=models[best_model_name])
            save_object(self.model_trainer_config.trained_model_path,obj=Network_Model)
            logging.info('Model saved')
            
            ## Model Trainer Artifact
            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_path,
                                                          train_metric_artifact=best_model_train_score,
                                                          test_metric_artifact= best_model_test_score)
            
            logging.info("Model training completed")
            return model_trainer_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)