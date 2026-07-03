import sys
from pandas import DataFrame
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from src.constant.training_pipeline import TARGET_COLUMN
from src.entity.config_entity import PCAConfig
from src.exception import CustomerException
from src.logger import logging

class CreateClusters:
    def __init__(self):
        self.pca_config = PCAConfig()
        
    def get_dataset_using_pca(self, preprocessed_data: DataFrame):
        try:
            pca_object = PCA(**self.pca_config.__dict__)
            return pca_object.fit_transform(preprocessed_data)
        except Exception as e:
            raise CustomerException(e, sys) from e
    
    def initialize_clustering(self, preprocessed_data: DataFrame) -> DataFrame:
        try:
            reduced_dataset = self.get_dataset_using_pca(preprocessed_data)
            model = KMeans(n_clusters=3, random_state=42).fit(reduced_dataset)
            preprocessed_data[TARGET_COLUMN] = model.labels_.astype(int)
            return preprocessed_data
        except Exception as e:
            raise CustomerException(e, sys) from e