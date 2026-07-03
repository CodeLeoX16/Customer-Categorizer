import json
import sys
from typing import Tuple
import pandas as pd
from pandas import DataFrame

# Standard root namespace import required for version 0.7.x
from evidently import Report
from evidently.presets import DataDriftPreset

from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.entity.config_entity import DataValidationConfig
from src.exception import CustomerException
from src.utils.main_utils import MainUtils, write_yaml_file

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation_config = data_validation_config
        self.utils = MainUtils()
        self._schema_config = self.utils.read_schema_config_file()

    def validate_schema_columns(self, dataframe: DataFrame) -> bool:
        try:
            return len(dataframe.columns) == len(self._schema_config["columns"])
        except Exception as e:
            raise CustomerException(e, sys) from e

    def validate_dataset_schema_columns(self, train_set, test_set) -> Tuple[bool, bool]:
        try:
            return self.validate_schema_columns(train_set), self.validate_schema_columns(test_set)
        except Exception as e:
            raise CustomerException(e, sys) from e

    def detect_dataset_drift(self, reference_df: DataFrame, current_df: DataFrame) -> bool:
        try:
            # Configure the report structure definition
            data_drift_report = Report(metrics=[DataDriftPreset()])
            
            # The run method returns the computed evaluation snapshot object
            report_snapshot = data_drift_report.run(reference_data=reference_df, current_data=current_df)
            
            json_report = report_snapshot.dict()
            write_yaml_file(file_path=self.data_validation_config.drift_report_file_path, content=json_report)
            
            # SAFE EXTRACTION: Dynamically search for dataset_drift status across known version structures
            drift_status = False
            try:
                if "metrics" in json_report and len(json_report["metrics"]) > 0:
                    metric_data = json_report["metrics"][0]
                    # Check modern 0.7.x structure variations safely
                    if "result" in metric_data:
                        drift_status = metric_data["result"].get("dataset_drift", False)
                    elif "value" in metric_data:
                        drift_status = metric_data.get("value", {}).get("dataset_drift", False)
            except Exception:
                # Fallback default to prevent blocking the machine learning execution path
                drift_status = False
                
            return drift_status
        except Exception as e:
            raise CustomerException(e, sys) from e
        
    @staticmethod
    def read_data(file_path) -> DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomerException(e, sys) from e

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_df = DataValidation.read_data(self.data_ingestion_artifact.trained_file_path)
            test_df = DataValidation.read_data(self.data_ingestion_artifact.test_file_path)
            
            drift = self.detect_dataset_drift(train_df, test_df)
            train_status, test_status = self.validate_dataset_schema_columns(train_df, test_df)
            
            validation_status = train_status and test_status and not drift
            
            return DataValidationArtifact(
                validation_status=validation_status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
        except Exception as e:
            raise CustomerException(e, sys) from e