import os
from datetime import datetime

# Common Constants
TIMESTAMP: str = datetime.now().strftime("%Y%m%d_%H%M%S")
ARTIFACTS_DIR = os.path.join("artifacts", TIMESTAMP)
BUCKET_NAME = "hate-speech-rm"
ZIP_FILE_NAME = "data.zip"
LABEL = 'label'
TWEET = 'tweet'

# Data Ingestion Constants
DATA_INGESTION_ARTIFACTS_DIR = "DataIngestionArtifacts"
DATA_INGESTION_IMBALANCED_DATA_DIR = "imbalanced_data.csv"
DATA_INGESTION_RAW_DATA_DIR = "raw_data.csv"