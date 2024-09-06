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
DATA_INGESTION_IMBALANCED_DATA_DIR = "data/TwitterHate.csv"
DATA_INGESTION_RAW_DATA_DIR = "data/raw_data.csv"

# Data Transformation Constants
DATA_TRANSFORMATION_ARTIFACTS_DIR = 'DataTransformationArtifacts'
TRANSFORMED_FILE_NAME = "final.csv"
DATA_DIR = "data"
ID = 'id'
AXIS = 1
INPLACE = True
DROP_COLUMNS = ['Unnamed: 0','count','hate_speech','offensive_language','neither']
CLASS = 'class'