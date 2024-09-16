import os,sys
from networksecurity.logger.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import ModelEvaluationConfig
from networksecurity.entity.artifact_entity import ModelTrainerArtifact, DataValidationArtifact, ModelEvaluationArtifact
from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.utils.main_utils.utils import save_object, load_object, write_yaml_file
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
            '''
            Each time we run our training pipeline a new model will be saved, with time there will be multiple models saved.
            Therefore we need to compare the saved model with the recently trained model and use the best one.
            '''
            logging.info("Initiate Model Evaluation")
            
            train_file_path = self.data_validation_artifact.valid_train_file_path
            test_file_path = self.data_validation_artifact.valid_test_file_path
            
            ## read train and test file
            train_df = pd.read_csv(train_file_path)
            test_df = pd.read_csv(test_file_path)
            
            ## concat both test and train df to make a single df
            df = pd.concat([train_df,test_df])
            ## target variable
            y_true = df[TARGET_COLUMN]
            ## replace -1 to 0
            y_true.replace(to_replace=-1,value=0, inplace=True)
            ## dropping target variable from the df
            df.drop(TARGET_COLUMN, axis=1, inplace=True)
            ## path of model which was trained in model trainer
            trained_model_file_path = self.model_trainer_artifact.trained_model_file_path
            ## defining ModelResolver object
            model_resolver = ModelResolver()
            
            is_model_accepted = True
            ## when there is no model saved by model pusher
            if not model_resolver.is_model_exists():
                model_evaluation_artifact = ModelEvaluationArtifact(
                    is_model_accepted=is_model_accepted,
                    improved_accuracy=None,
                    saved_model_path=None,
                    trained_model_path=trained_model_file_path,
                    saved_model_metric_artifact=None,
                    trained_model_metric_artifact=self.model_trainer_artifact.test_metric_artifact
                )
                logging.info(f"Model Evaluation artifact: {model_evaluation_artifact}")
                
                ## creating a report
                model_eval_report = model_evaluation_artifact.__dict__
                write_yaml_file(self.model_evaluation_config.report_file_path,model_eval_report)

                return model_evaluation_artifact
            
            ## loading the model which is saved in Saved_model folder 
            saved_model_path = model_resolver.get_best_model_path()
            saved_model = load_object(saved_model_path)
            ## loading the model which was trained in model trainer component
            trained_model = load_object(trained_model_file_path)
            logging.info("Trained and test model loaded")
            
            ## predicting from both the models
            y_saved_pred = saved_model.predict(df)
            y_trained_pred = trained_model.predict(df)
            
            ## getting the classification score metrics 
            saved_model_metric = get_classification_score(y_pred=y_saved_pred, y_actual=y_true)
            trained_model_metric = get_classification_score(y_pred=y_trained_pred, y_actual=y_true)
            
            # checking the improvement of the trained model over saved model
            improved_accuracy = trained_model_metric.f1_score - saved_model_metric.f1_score
            logging.info(f"Improved accuracy: {improved_accuracy}, trained model: {trained_model_metric.f1_score}, saved model: {saved_model_metric.f1_score}")
            if self.model_evaluation_config.change_threshold < improved_accuracy:
                is_model_accepted = True
            else:
                is_model_accepted= False
                
            ## saving model evaluation artifact
            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted=is_model_accepted,
                improved_accuracy=improved_accuracy,
                saved_model_path=saved_model_path,
                trained_model_path=trained_model_file_path,
                saved_model_metric_artifact=saved_model_metric,
                trained_model_metric_artifact=trained_model_metric
            )
            
            model_eval_report = model_evaluation_artifact.__dict__
            write_yaml_file(self.model_evaluation_config.report_file_path, model_eval_report)
            logging.info(f"Model Evaluation artifact: {model_evaluation_artifact}")
            logging.info("Model evaluation completed")
            return model_evaluation_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)