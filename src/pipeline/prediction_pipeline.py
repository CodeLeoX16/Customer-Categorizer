import sys
import pandas as pd
from src.ml.model.s3_estimator import CustomerClusterEstimator
from src.entity.config_entity import Prediction_config, PredictionPipelineConfig
from src.exception import CustomerException

class CustomerData:
    def __init__(self):
        pass
        
    def get_input_dataset(self, column_schema: dict, input_data):
        columns = list(column_schema.keys())
        # Correctly mapping array items into corresponding sequence maps
        input_dataset = pd.DataFrame([input_data], columns=columns)
        for key, value in column_schema.items():
            input_dataset[key] = input_dataset[key].astype(value)
        return input_dataset

    @staticmethod
    def form_input_dataframe(data):
        prediction_config = Prediction_config()
        column_schema = prediction_config.prediction_schema['columns']
        return CustomerData().get_input_dataset(column_schema=column_schema, input_data=data)

class PredictionPipeline:
    def __init__(self):
        pass
        
    def prepare_input_data(self, input_data: list) -> pd.DataFrame:
        try:
            return CustomerData.form_input_dataframe(data=input_data)
        except Exception as e:
            raise CustomerException(e, sys) from e
        
    def get_trained_model(self):
        try:
            prediction_config = PredictionPipelineConfig()
            return CustomerClusterEstimator(bucket_name=prediction_config.model_bucket_name, model_path=prediction_config.model_file_name)
        except Exception as e:
            raise CustomerException(e, sys) from e
        
    def run_pipeline(self, input_data: list):
        try:
            input_dataframe = self.prepare_input_data(input_data) 
            model = self.get_trained_model()
            return model.predict(input_dataframe)
        except Exception as e:
            raise CustomerException(e, sys) from e