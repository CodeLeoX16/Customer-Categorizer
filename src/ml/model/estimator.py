import sys
from pandas import DataFrame
from sklearn.pipeline import Pipeline
from src.exception import CustomerException

class CustomerSegmentationModel:
    def __init__(self, preprocessing_object: Pipeline, trained_model_object: object):
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def _ensure_preprocessing_compatibility(self) -> None:
        if hasattr(self.preprocessing_object, "transformers_") and not hasattr(self.preprocessing_object, "_name_to_fitted_passthrough"):
            self.preprocessing_object._name_to_fitted_passthrough = {}

    def predict(self, dataframe: DataFrame) -> DataFrame:
        try:
            self._ensure_preprocessing_compatibility()
            transformed_feature = self.preprocessing_object.transform(dataframe)
            return self.trained_model_object.predict(transformed_feature)
        except Exception as e:
            raise CustomerException(e, sys) from e

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"