import os
import logging
from datetime import datetime

PIPELINE_NAME = "customer_segmentation"
ARTIFACT_DIR = "artifact"
LOG_DIR = "logs"
TIMESTAMP = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
LOG_FILE = f"log_{TIMESTAMP}.log"

try:
    from from_root import from_root
    base_path = from_root()
except Exception:
    base_path = os.getcwd()

logs_path = os.path.join(base_path, PIPELINE_NAME, ARTIFACT_DIR, LOG_DIR)
os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)