import sys
import os
from typing import Tuple
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from src.constant.database import COLLECTION_NAME
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.data_access.customer_data import CustomerData
from src.exception import CustomerException
from src.logger import logging
from src.utils.main_utils import MainUtils

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        self.data_ingestion_config = data_ingestion_config
        self.utils = MainUtils()

    def split_data_as_train_test(self, dataframe: DataFrame) -> Tuple[DataFrame, DataFrame]:
        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            os.makedirs(self.data_ingestion_config.ingested_data_dir, exist_ok=True)
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            return train_set, test_set
        except Exception as e:
            raise CustomerException(e, sys) from e
        
    def export_data_into_feature_store(self) -> DataFrame:
        try:
            customer_data = CustomerData()
            customer_dataframe = customer_data.export_collection_as_dataframe(collection_name=COLLECTION_NAME)
            os.makedirs(os.path.dirname(self.data_ingestion_config.feature_store_file_path), exist_ok=True)
            customer_dataframe.to_csv(self.data_ingestion_config.feature_store_file_path, index=False, header=True)
            return customer_dataframe
        except Exception as e:
            raise CustomerException(e, sys) from e

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            dataframe = self.export_data_into_feature_store()
            _schema_config = self.utils.read_schema_config_file()
            dataframe = dataframe.drop(_schema_config["drop_columns"], axis=1)
            self.split_data_as_train_test(dataframe)
            return DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
        except Exception as e:
            raise CustomerException(e, sys) from e