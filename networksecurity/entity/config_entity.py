from datetime import datetime
import os
from networksecurity.constant import training_pipeline

print(training_pipeline.PIPELINE_NAME)
print(training_pipeline.ARTIFACT_DIR)

class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        ## creating a timestamp in format month/day/year/hour/min/sec
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        ## pipeline name
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        ## artifact directory name
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        ## artifact directory path
        self.artifact_dir = os.path.join(self.artifact_name,timestamp)
        ## timestamp as an attribute of class to be used later
        self.timestamp: str = timestamp
    
class DataIngestionConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        ## data ingestion directory name
        self.data_ingestion_dir: str = os.path.join(training_pipeline_config.artifact_dir,
                                               training_pipeline.DATA_INGESTION_DIR_NAME)
        
        ## data ingestion feature store file  path
        self.feature_store_file_path: str =os.path.join(self.data_ingestion_dir, 
                                            training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
                                            training_pipeline.FILE_NAME)
        
        ## data ingestion training file path
        self.training_file_path: str = os.path.join(self.data_ingestion_dir,
                                               training_pipeline.DATA_INGESTION_INGESTED_DIR,
                                               training_pipeline.TRAIN_FILE_NAME)
        
        ## data ingestion test file path
        self.testing_file_path: str = os.path.join(self.data_ingestion_dir,
                                              training_pipeline.DATA_INGESTION_INGESTED_DIR,
                                              training_pipeline.TEST_FILE_NAME)
        
        ## MongoDB database name
        self.database_name: str = training_pipeline.DATA_INGESTION_DATABASE_NAME
        
        ## MongoDB collection name
        self.collection_name:str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        
        ## train test split ratio
        self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
    
class DataValidationConfig:
    
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        ## data validation directory name
        self.data_validation_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_VALIDATION_DIR_NAME)
        
        ## data validation valid data directory name
        self.valid_data_dir: str = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_VALID_DIR)
        ## data validation invalid data directory name
        self.invalid_data_dir:str = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_INVALID_DIR)
        ## data validation valid train file path
        self.valid_train_file_path = os.path.join(self.valid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        ## data validation valid test file path
        self.valid_test_file_path = os.path.join(self.valid_data_dir, training_pipeline.TEST_FILE_NAME)
        ## data validation invalid train file path 
        self.invalid_train_file_path = os.path.join(self.invalid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        ## data validation invalid test file path
        self.invalid_test_file_path = os.path.join(self.invalid_data_dir,training_pipeline.TEST_FILE_NAME)
        ## data validation drift report file path
        self.drift_report_file_path = os.path.join(self.data_validation_dir,
                                                   training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
                                                   training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)
        
        
class DataTransformationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        
        ## data transformation directory name
        self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir,
                                                    training_pipeline.DATA_TRANSFORMATION_DIR_NAME)
        ## data transformaton training file path
        self.data_transformation_train_file_path = os.path.join(self.data_transformation_dir,
                                                                training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                                training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy"),)
        ## data transformed test file path
        self.data_transformation_test_file_path = os.path.join(self.data_transformation_dir,
                                                               training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                               training_pipeline.TEST_FILE_NAME.replace("csv","npy"),)
        
        ## preprocessing.pkl file path
        self.transformed_object_file_path = os.path.join(self.data_transformation_dir,
                                                         training_pipeline.DATA_TRANSFRMATION_TRANSFORMED_OBJECT_DIR,
                                                         training_pipeline.PREPROCESSING_OBJECT_FILE_NAME,)
        

class ModelTrainerConfig:
    def __init__(self,training_pipeline_config: TrainingPipelineConfig):
        ## model trainer directory name
        self.model_trainer_dir = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.MODEL_TRAINER_DIR_NAME)
        
        ## model path
        self.trained_model_path = os.path.join(self.model_trainer_dir, 
                                               training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR, 
                                               training_pipeline.MODEL_TRAINER_TRAINED_MODEL_NAME)
        
        ## model accuracy
        self.expected_accuracy = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        
        ## overfitting underfitting threshold
        self.overfitting_underfitting_threshold = training_pipeline.MODEL_TRAINER_UNDERFITTING_OVERFITTING_SCORE
    
class ModelEvaluationConfig:
    
    def __init__(self):
        pass
    
class ModelPusherConfig:
    
    def __init__(self):
        pass