import shutil
import sys
from typing import Dict, Tuple
import os
import numpy as np
import pandas as pd
import pickle
from sklearn import linear_model
import yaml

from pandas import DataFrame
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GridSearchCV
from sklearn.utils import all_estimators
from yaml import safe_dump

from src.constant.training_pipeline import SCHEMA_FILE_PATH, MODEL_TRAINER_MODEL_CONFIG_FILE_PATH
from src.exception import CustomerException
from src.logger import logging

def load_numpy_array_data(file_path: str) -> np.ndarray:
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise CustomerException(e, sys) from e
    
def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise CustomerException(e, sys) from e

class MainUtils:
    def __init__(self) -> None:
        pass

    def read_yaml_file(self, filename: str) -> dict:
        try:
            with open(filename, "r", encoding="utf-8") as yaml_file:
                return yaml.safe_load(yaml_file)
        except Exception as e:
            raise CustomerException(e, sys) from e

    def read_schema_config_file(self) -> dict:
        try:
            return self.read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomerException(e, sys) from e

    def read_model_config_file(self) -> dict:
        try:
            return self.read_yaml_file(MODEL_TRAINER_MODEL_CONFIG_FILE_PATH)
        except Exception as e:
            raise CustomerException(e, sys) from e

    def get_tuned_model(
        self, model_name: str, train_x: DataFrame, train_y: DataFrame, test_x: DataFrame, test_y: DataFrame
    ) -> Tuple[float, object, str]:
        logging.info("Entered get_tuned_model method")
        try:
            model = self.get_base_model(model_name)
            model_best_params = self.get_model_params(model, train_x, train_y)
            model.set_params(**model_best_params)
            model.fit(train_x, train_y)
            preds = model.predict(test_x)
            model_score = self.get_model_score(test_y, preds)
            return model_score, model, model.__class__.__name__
        except Exception as e:
            raise CustomerException(e, sys) from e

    @staticmethod
    def get_model_score(test_y: DataFrame, preds: DataFrame) -> float:
        try:
            model_score = roc_auc_score(test_y, preds)
            return model_score
        except Exception as e:
            raise CustomerException(e, sys) from e

    @staticmethod
    def get_base_model(model_name: str) -> object:
        try:
            if model_name.lower().startswith("logistic"):
                return linear_model.__dict__[model_name]()
            else:
                model_idx = [model[0] for model in all_estimators()].index(model_name)
                return all_estimators().__getitem__(model_idx)[1]()
        except Exception as e:
            raise CustomerException(e, sys) from e

    def get_model_params(self, model: object, x_train: DataFrame, y_train: DataFrame) -> Dict:
        try:
            model_name = model.__class__.__name__
            model_config = self.read_model_config_file()
            model_param_grid = model_config["train_model"][model_name]
            model_grid = GridSearchCV(model, model_param_grid, verbose=2, cv=2, n_jobs=-1)
            model_grid.fit(x_train, y_train)
            return model_grid.best_params_
        except Exception as e:
            raise CustomerException(e, sys) from e

    @staticmethod
    def save_object(file_path: str, obj: object) -> None:
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as file_obj:
                pickle.dump(obj, file_obj)
        except Exception as e:
            raise CustomerException(e, sys) from e

    @staticmethod
    def get_best_model_with_name_and_score(model_list: list) -> Tuple[object, float]:
        try:
            return max(model_list)[1], max(model_list)[0]
        except Exception as e:
            raise CustomerException(e, sys) from e

    @staticmethod
    def load_object(file_path: str) -> object:
        try:
            with open(file_path, "rb") as file_obj:
                return pickle.load(file_obj)
        except Exception as e:
            raise CustomerException(e, sys) from e

    @staticmethod
    def create_artifacts_zip(file_name: str, folder_name: str) -> None:
        try:
            shutil.make_archive(file_name, "zip", folder_name)
        except Exception as e:
            raise CustomerException(e, sys) from e

    @staticmethod
    def unzip_file(filename: str, folder_name: str) -> None:
        try:
            shutil.unpack_archive(filename, folder_name)
        except Exception as e:
            raise CustomerException(e, sys) from e

    def update_model_score(self, best_model_score: float) -> None:
        try:
            model_config = self.read_model_config_file()
            model_config["base_model_score"] = str(best_model_score)
            with open(MODEL_TRAINER_MODEL_CONFIG_FILE_PATH, "w+") as fp:
                safe_dump(model_config, fp, sort_keys=False)
        except Exception as e:
            raise CustomerException(e, sys) from e
        
    def save_numpy_array_data(self, file_path: str, array: np.ndarray):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as file_obj:
                np.save(file_obj, array)
        except Exception as e:
            raise CustomerException(e, sys) from e