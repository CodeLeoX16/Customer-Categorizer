import sys
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.data_validation import DataValidation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation
from src.components.model_pusher import ModelPusher
from src.exception import CustomerException
from src.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact, DataValidationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact
from src.entity.config_entity import DataIngestionConfig, DataTransformationConfig, DataValidationConfig, ModelEvaluationConfig, ModelPusherConfig, ModelTrainerConfig

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()
        self.model_evaluation_config = ModelEvaluationConfig()
        self.model_pusher_config = ModelPusherConfig()
        
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            return DataIngestion(data_ingestion_config=self.data_ingestion_config).initiate_data_ingestion()
        except Exception as e:
            raise CustomerException(e, sys) from e
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            return DataValidation(data_ingestion_artifact=data_ingestion_artifact, data_validation_config=self.data_validation_config).initiate_data_validation()
        except Exception as e:
            raise CustomerException(e, sys) from e
        
    def start_data_transformation(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        try:
            return DataTransformation(data_ingestion_artifact=data_ingestion_artifact, data_validation_artifact=data_validation_artifact, data_transformation_config=self.data_transformation_config).initiate_data_transformation()
        except Exception as e:
            raise CustomerException(e, sys) from e
        
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            return ModelTrainer(data_transformation_artifact=data_transformation_artifact, model_trainer_config=self.model_trainer_config).initiate_model_trainer()
        except Exception as e:
            raise CustomerException(e, sys) from e
        
    def start_model_evaluation(self, data_ingestion_artifact: DataIngestionArtifact, model_trainer_artifact: ModelTrainerArtifact, data_transformation_artifact: DataTransformationArtifact) -> ModelEvaluationArtifact:
        try:
            return ModelEvaluation(model_eval_config=self.model_evaluation_config, data_ingestion_artifact=data_ingestion_artifact, model_trainer_artifact=model_trainer_artifact, data_transformation_artifact=data_transformation_artifact).initiate_model_evaluation()
        except Exception as e:
            raise CustomerException(e, sys) from e

    def start_model_pusher(self, model_trainer_artifact: ModelTrainerArtifact):
        try:
            return ModelPusher(model_trainer_artifact=model_trainer_artifact, model_pusher_config=self.model_pusher_config).initiate_model_pusher()
        except Exception as e:
            raise CustomerException(e, sys) from e

    def run_pipeline(self) -> None:
        try:
            di_artifact = self.start_data_ingestion()
            dv_artifact = self.start_data_validation(di_artifact)
            dt_artifact = self.start_data_transformation(di_artifact, dv_artifact)
            mt_artifact = self.start_model_trainer(dt_artifact)
            me_artifact = self.start_model_evaluation(di_artifact, mt_artifact, dt_artifact)
            
            if me_artifact.is_model_accepted:
                self.start_model_pusher(mt_artifact)
        except Exception as e:
            raise CustomerException(e, sys) from e