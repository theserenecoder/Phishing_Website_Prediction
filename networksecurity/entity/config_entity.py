from datetime import datetime
import os
from networksecurity.constant import training_pipeline

print(training_pipeline.PIPELINE_NAME)
print(training_pipeline.ARTIFACT_DIR)
print(training_pipeline.DATA_INGESTION_DATABASE_NAME)
print(training_pipeline.DATA_INGESTION_COLLECTION_NAME)

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
        self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir,
                                               training_pipeline.DATA_INGESTION_DIR_NAME)
        
        ## data ingestion feature store file  path
        self.feature_store_file_path=os.path.join(self.data_ingestion_dir, 
                                            training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
                                            training_pipeline.FILE_NAME)
        
        ## data ingestion training file path
        self.training_file_path = os.path.join(self.data_ingestion_dir,
                                               training_pipeline.DATA_INGESTION_INGESTED_DIR,
                                               training_pipeline.TRAIN_FILE_NAME)
        
        ## data ingestion test file path
        self.testing_file_path = os.path.join(self.data_ingestion_dir,
                                              training_pipeline.DATA_INGESTION_INGESTED_DIR,
                                              training_pipeline.TEST_FILE_NAME)
        
        ## MongoDB database name
        self.database_name = training_pipeline.DATA_INGESTION_DATABASE_NAME
        
        ## MongoDB collection name
        self.collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        
        ## train test split ratio
        self.train_test_split_ratio = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
    
class DataValidationConfig:
    
    def __init__(self,training_pipeline_config):
        pass
        
        
class DataTransformationConfig:
    
    def __init__(self):
        pass

class ModelTrainerConfig:
    
    def __init__(self):
        pass
    
class ModelEvaluationConfig:
    
    def __init__(self):
        pass
    
class ModelPusherConfig:
    
    def __init__(self):
        pass