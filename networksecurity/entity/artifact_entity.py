from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    ## train file path attribute
    train_file_path: str
    ## test file path attribute
    test_file_path: str

@dataclass
class DataValidationArtifact:
    validation_status:bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str

@dataclass
class DataTransformationArtifact:
    pass

@dataclass
class ModelTrainerArtifact:
    pass

@dataclass
class ModelEvaluationArtifact:
    pass

@dataclass
class ModelPusherArtifact:
    pass