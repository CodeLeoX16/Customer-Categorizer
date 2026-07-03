import os
import sys
import pickle
import importlib
from io import StringIO
from typing import Union, List
from botocore.exceptions import ClientError
from pandas import DataFrame, read_csv
from mypy_boto3_s3.service_resource import Bucket

from src.configuration.aws_connection import S3Client
from src.exception import CustomerException
from src.logger import logging

class SimpleStorageService:
    def __init__(self):
        s3_client = S3Client()
        self.s3_resource = s3_client.s3_resource
        self.s3_client = s3_client.s3_client

    @staticmethod
    def _install_numpy_compat_shim() -> None:
        try:
            import numpy

            sys.modules.setdefault("numpy._core", numpy.core)
            sys.modules.setdefault("numpy._core.multiarray", importlib.import_module("numpy.core.multiarray"))
            sys.modules.setdefault("numpy._core._multiarray_umath", importlib.import_module("numpy.core._multiarray_umath"))
        except Exception:
            pass

    def s3_key_path_available(self, bucket_name, s3_key) -> bool:
        try:
            bucket = self.get_bucket(bucket_name)
            file_objects = [file_object for file_object in bucket.objects.filter(Prefix=s3_key)]
            return len(file_objects) > 0
        except Exception as e:
            raise CustomerException(e, sys) from e

    @staticmethod
    def read_object(object_name: str, decode: bool = True, make_readable: bool = False) -> Union[StringIO, str, bytes]:
        try:
            body = object_name.get()["Body"].read()
            raw_data = body.decode() if decode else body
            return StringIO(raw_data) if make_readable else raw_data
        except Exception as e:
            raise CustomerException(e, sys) from e

    def get_bucket(self, bucket_name: str) -> Bucket:
        try:
            return self.s3_resource.Bucket(bucket_name)
        except Exception as e:
            raise CustomerException(e, sys) from e

    def get_file_object(self, filename: str, bucket_name: str) -> Union[List[object], object]:
        try:
            bucket = self.get_bucket(bucket_name)
            file_objects = [file_object for file_object in bucket.objects.filter(Prefix=filename)]
            return file_objects[0] if len(file_objects) == 1 else file_objects
        except Exception as e:
            raise CustomerException(e, sys) from e

    def load_model(self, model_name: str, bucket_name: str, model_dir: str = None) -> object:
        try:
            model_file = model_name if model_dir is None else f"{model_dir}/{model_name}"
            file_object = self.get_file_object(model_file, bucket_name)
            model_obj = self.read_object(file_object, decode=False)
            self._install_numpy_compat_shim()
            return pickle.loads(model_obj)
        except Exception as e:
            raise CustomerException(e, sys) from e

    def create_folder(self, folder_name: str, bucket_name: str) -> None:
        try:
            self.s3_resource.Object(bucket_name, folder_name).load()
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                self.s3_client.put_object(Bucket=bucket_name, Key=f"{folder_name}/")
            else:
                raise CustomerException(e, sys) from e

    def upload_file(self, from_filename: str, to_filename: str, bucket_name: str, remove: bool = True):
        try:
            self.s3_resource.meta.client.upload_file(from_filename, bucket_name, to_filename)
            if remove:
                os.remove(from_filename)
        except Exception as e:
            raise CustomerException(e, sys) from e

    def upload_df_as_csv(self, data_frame: DataFrame, local_filename: str, bucket_filename: str, bucket_name: str) -> None:
        try:
            data_frame.to_csv(local_filename, index=None, header=True)
            self.upload_file(local_filename, bucket_filename, bucket_name)
        except Exception as e:
            raise CustomerException(e, sys) from e

    def get_df_from_object(self, object_: object) -> DataFrame:
        try:
            content = self.read_object(object_, make_readable=True)
            return read_csv(content, na_values="na")
        except Exception as e:
            raise CustomerException(e, sys) from e

    def read_csv(self, filename: str, bucket_name: str) -> DataFrame:
        try:
            csv_obj = self.get_file_object(filename, bucket_name)
            return self.get_df_from_object(csv_obj)
        except Exception as e:
            raise CustomerException(e, sys) from e