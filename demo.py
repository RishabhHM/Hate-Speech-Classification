from hate_speech.logger import logging
from hate_speech.exception import CustomException
import sys
from hate_speech.configuration.gcloud_conn import GCloudSync

logging.info("Testing log setup")

# logging.info("Testing exception handling")
# try:
#     a = 7 / "0"
# except Exception as e:
#     raise CustomException(e, sys) from e

logging.info("Testing GCloud Sync")
gcs = GCloudSync()
gcs.sync_folder_from_gcloud("hate-speech-rm", "data.zip", "gcloud_data/dataset.zip")
logging.info("Successfully downloaded data from Cloud Storage!!")