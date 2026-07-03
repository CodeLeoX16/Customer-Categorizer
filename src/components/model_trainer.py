import sys
import os
import numpy as np
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ClassificationMetricArtifact
from src.exception import CustomerException
from src.utils.main_utils import MainUtils, load_numpy_array_data
from neuro_mf import ModelFactory
from src.ml.model.estimator import CustomerSegmentationModel

class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact, model_trainer_config: ModelTrainerConfig):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config
        self.utils = MainUtils()

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_file_path)
            x_train, y_train = train_arr[:, :-1], train_arr[:, -1]
            
            model_factory = ModelFactory(model_config_path=self.model_trainer_config.model_config_file_path)
            best_model_detail = model_factory.get_best_model(X=x_train, y=y_train, base_accuracy=self.model_trainer_config.expected_accuracy)
            preprocessing_obj = self.utils.load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

            if best_model_detail.best_score < self.model_trainer_config.expected_accuracy:
                raise Exception("No best model exceeded model base requirements score threshold parameters.")
             
            customer_segmentation_model = CustomerSegmentationModel(
                preprocessing_object=preprocessing_obj,
                trained_model_object=best_model_detail.best_model
            )
            
            self.utils.save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=customer_segmentation_model)
            metric_artifact = ClassificationMetricArtifact(f1_score=best_model_detail.best_score, precision_score=best_model_detail.best_score, recall_score=best_model_detail.best_score)
            
            return ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                metric_artifact=metric_artifact
            )
        except Exception as e:
            raise CustomerException(e, sys) from e