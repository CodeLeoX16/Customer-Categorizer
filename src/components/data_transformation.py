import sys
from datetime import datetime
import numpy as np
import os
import pandas as pd
from typing import Tuple
from pandas import DataFrame
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, PowerTransformer

from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import DataTransformationArtifact, DataIngestionArtifact, DataValidationArtifact
from src.components.data_clustering import CreateClusters
from src.constant.training_pipeline import TARGET_COLUMN
from src.entity.config_entity import SimpleImputerConfig
from src.exception import CustomerException
from src.utils.main_utils import MainUtils

class DataTransformation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_artifact: DataValidationArtifact, data_transformation_config: DataTransformationConfig):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation_artifact = data_validation_artifact
        self.data_transformation_config = data_transformation_config
        self.imputer_config = SimpleImputerConfig()
        self.utils = MainUtils()
        
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomerException(e, sys) from e
        
    # FIXED: Indented properly to sit natively inside the DataTransformation class structure
    def get_new_features(self, train_set: DataFrame, test_set: DataFrame):
        try:
            train_out = pd.DataFrame()
            test_out = pd.DataFrame()

            datasets = {
                "train_set": train_set,
                "test_set": test_set
            }

            for key, dataset in datasets.items():

                # ---------------- Age ----------------
                # FIXED: Cast the series explicitly to numeric integers to handle any mixed string types
                dataset["Year_Birth"] = pd.to_numeric(dataset["Year_Birth"], errors='coerce').fillna(1980).astype(int)
                dataset["Age"] = 2022 - dataset["Year_Birth"]

                # ---------------- Education ----------------
                education_map = {
                    "Basic": 0,
                    "2n Cycle": 1,
                    "Graduation": 2,
                    "Master": 3,
                    "PhD": 4
                }

                dataset["Education"] = dataset["Education"].map(education_map)

                # ---------------- Marital Status ----------------
                marital_map = {
                    "Married": 1,
                    "Together": 1,
                    "Absurd": 0,
                    "Widow": 0,
                    "YOLO": 0,
                    "Divorced": 0,
                    "Single": 0,
                    "Alone": 0
                }

                dataset["Marital_Status"] = dataset["Marital_Status"].map(marital_map)

                # Handle unseen categories
                dataset["Education"] = dataset["Education"].fillna(0).astype(int)
                dataset["Marital_Status"] = dataset["Marital_Status"].fillna(0).astype(int)

                # ---------------- Features ----------------
                # FIXED: Cast to numeric integers to prevent type mismatches during feature addition
                dataset["Kidhome"] = pd.to_numeric(dataset["Kidhome"], errors='coerce').fillna(0).astype(int)
                dataset["Teenhome"] = pd.to_numeric(dataset["Teenhome"], errors='coerce').fillna(0).astype(int)
                
                dataset["Children"] = (
                    dataset["Kidhome"] +
                    dataset["Teenhome"]
                )

                dataset["Family_Size"] = (
                    dataset["Marital_Status"] +
                    dataset["Children"] +
                    1
                )

                # FIXED: Cast spending blocks cleanly to numeric types before summation
                spending_cols = ["MntWines", "MntFruits", "MntMeatProducts", "MntFishProducts", "MntSweetProducts", "MntGoldProds"]
                for col in spending_cols:
                    if col in dataset.columns:
                        dataset[col] = pd.to_numeric(dataset[col], errors='coerce').fillna(0)

                dataset["Total_Spending"] = (
                    dataset["MntWines"]
                    + dataset["MntFruits"]
                    + dataset["MntMeatProducts"]
                    + dataset["MntFishProducts"]
                    + dataset["MntSweetProducts"]
                    + dataset["MntGoldProds"]
                )

                # FIXED: Cast promo columns cleanly to numeric types before summation
                promo_cols = ["AcceptedCmp1", "AcceptedCmp2", "AcceptedCmp3", "AcceptedCmp4", "AcceptedCmp5"]
                for col in promo_cols:
                    if col in dataset.columns:
                        dataset[col] = pd.to_numeric(dataset[col], errors='coerce').fillna(0).astype(int)

                dataset["Total Promo"] = (
                    dataset["AcceptedCmp1"]
                    + dataset["AcceptedCmp2"]
                    + dataset["AcceptedCmp3"]
                    + dataset["AcceptedCmp4"]
                    + dataset["AcceptedCmp5"]
                )

                # ---------------- Date ----------------
                dataset["Dt_Customer"] = pd.to_datetime(
                    dataset["Dt_Customer"],
                    errors="coerce"
                )

                today = datetime.today()

                dataset["Days_as_Customer"] = (
                    today - dataset["Dt_Customer"]
                ).dt.days
                
                # Fill na values for rows where parsing might have failed out
                dataset["Days_as_Customer"] = dataset["Days_as_Customer"].fillna(0).astype(int)

                dataset["Parental Status"] = np.where(
                    dataset["Children"] > 0,
                    1,
                    0
                )

                # ---------------- Drop ----------------
                dataset.drop(
                    columns=[
                        "Year_Birth",
                        "Kidhome",
                        "Teenhome"
                    ],
                    inplace=True
                )

                # ---------------- Rename ----------------
                dataset.rename(columns={
                    "Marital_Status": "Marital Status",
                    "MntWines": "Wines",
                    "MntFruits": "Fruits",
                    "MntMeatProducts": "Meat",
                    "MntFishProducts": "Fish",
                    "MntSweetProducts": "Sweets",
                    "MntGoldProds": "Gold",
                    "NumWebPurchases": "Web",
                    "NumCatalogPurchases": "Catalog",
                    "NumStorePurchases": "Store",
                    "NumDealsPurchases": "Discount Purchases"
                }, inplace=True)

                processed = dataset[
                    [
                        "Age",
                        "Education",
                        "Marital Status",
                        "Parental Status",
                        "Children",
                        "Income",
                        "Total_Spending",
                        "Days_as_Customer",
                        "Recency",
                        "Wines",
                        "Fruits",
                        "Meat",
                        "Fish",
                        "Sweets",
                        "Gold",
                        "Web",
                        "Catalog",
                        "Store",
                        "Discount Purchases",
                        "Total Promo",
                        "NumWebVisitsMonth"
                    ]
                ].copy()

                if key == "train_set":
                    train_out = processed
                else:
                    test_out = processed

            return train_out, test_out

        except Exception as e:
            raise CustomerException(e, sys) from e

    def transform_data(self, train_set: DataFrame, test_set: DataFrame) -> Tuple[DataFrame, DataFrame]:
        try:
            numeric_features = [feature for feature in train_set.columns if train_set[feature].dtype != 'O']
            outlier_features = ["Wines", "Fruits", "Meat", "Fish", "Sweets", "Gold", "Age", "Total_Spending"]
            numeric_features = [x for x in numeric_features if x not in outlier_features]

            numeric_pipeline = Pipeline(steps=[
                ("Imputer", SimpleImputer(**self.imputer_config.__dict__)), 
                ("StandardScaler", StandardScaler())
            ])
            
            outlier_features_pipeline = Pipeline(steps=[
                ("Imputer", SimpleImputer(**self.imputer_config.__dict__)),
                ("transformer", PowerTransformer(standardize=True))
            ])

            preprocessor = ColumnTransformer([
                ("numeric pipeline", numeric_pipeline, numeric_features),
                ("Outliers Features Pipeline", outlier_features_pipeline, outlier_features)
            ])
            
            preprocessed_train = preprocessor.fit_transform(train_set)
            preprocessed_test = preprocessor.transform(test_set)
            
            # FIXED: Column mapping correction layer to match layout orders
            transformed_columns = numeric_features + outlier_features
            df_train = pd.DataFrame(preprocessed_train, columns=transformed_columns)
            df_test = pd.DataFrame(preprocessed_test, columns=transformed_columns)
            
            self.utils.save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)
            return df_train, df_test
        except Exception as e:
            raise CustomerException(e, sys) from e

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            if self.data_validation_artifact.validation_status:
                train_set = DataTransformation.read_data(self.data_ingestion_artifact.trained_file_path)
                test_set = DataTransformation.read_data(self.data_ingestion_artifact.test_file_path)
                train_set, test_set = self.get_new_features(train_set, test_set)

                preprocessed_train_set, preprocessed_test_set = self.transform_data(train_set, test_set)
                cluster_creator = CreateClusters()

                labelled_train_set = cluster_creator.initialize_clustering(preprocessed_data=preprocessed_train_set)
                labelled_test_set = cluster_creator.initialize_clustering(preprocessed_data=preprocessed_test_set)
                
                X_train = labelled_train_set.drop(columns=[TARGET_COLUMN])
                y_train = labelled_train_set[TARGET_COLUMN]
                X_test = labelled_test_set.drop(columns=[TARGET_COLUMN])
                y_test = labelled_test_set[TARGET_COLUMN]
                
                train_arr = np.c_[np.array(X_train), np.array(y_train)]
                test_arr = np.c_[np.array(X_test), np.array(y_test)]
                
                self.utils.save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
                self.utils.save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)

                return DataTransformationArtifact(
                    transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                    transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                    transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
                )
            else:
                raise Exception("Data Validation Fault Encountered.")
        except Exception as e:
            raise CustomerException(e, sys) from e