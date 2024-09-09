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


# Model Training Constants
MODEL_TRAINER_ARTIFACTS_DIR = 'ModelTrainerArtifacts'
TOKEN_VOCAB = 'tokenizer.pickle'
TRAINED_MODEL_NAME = 'model.h5'
X_TRAIN_FILE_NAME = 'x_train.csv'
X_TEST_FILE_NAME = 'x_test.csv'
Y_TRAIN_FILE_NAME = 'y_train.csv'
Y_TEST_FILE_NAME = 'y_test.csv'
RANDOM_STATE = 42
EPOCH = 1
BATCH_SIZE = 128
VALIDATION_SPLIT = 0.2

# Model Architecture Constants
MAX_WORDS = 50000
MAX_LEN = 300
LOSS = 'binary_crossentropy'
METRICS = ['accuracy']
ACTIVATION = 'sigmoid'