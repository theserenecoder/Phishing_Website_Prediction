from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    ## train file path attribute
    train_file_path: str
    ## test file path attribute
    test_file_path: str

@dataclass
class DataValidationArtifact:
    pass

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