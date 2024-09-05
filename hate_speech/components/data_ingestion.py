import os
import sys
from zipfile import ZipFile
from hate_speech.logger import logging
from hate_speech.exception import CustomException
from hate_speech.configuration.gcloud_conn import GCloudSync
from hate_speech.entity.config_entity import DataIngestionConfig
from hate_speech.entity.artifact_entity import DataIngestionArtifacts

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config
        self.gcloud = GCloudSync()
    

    def get_data_from_gcloud(self) -> None:
        logging.info("Executing get_data_from_gcloud method of Data Ingestion class")
        try:
            os.makedirs(self.data_ingestion_config.DATA_INGESTION_ARTIFACTS_DIR, exist_ok=True)

            self.gcloud.sync_folder_from_gcloud(self.data_ingestion_config.BUCKET_NAME,
                                                self.data_ingestion_config.ZIP_FILE_NAME,
                                                self.data_ingestion_config.DATA_INGESTION_ARTIFACTS_DIR
                                                )
            logging.info("Exiting get_data_from_gcloud method of Data Ingestion Class")
            
        except Exception as e:
            raise CustomException(e, sys) from e


    def upzip_and_clean(self):
        logging.info("Executing upzip_and_clean method of Data Ingestion class")
        try:
            with ZipFile(self.data_ingestion_config.ZIP_FILE_PATH, 'r') as zip_ref:
                zip_ref.extractall(self.data_ingestion_config.ZIP_FILE_DIR)
            logging.info("Exiting upzip_and_clean method of Data Ingestion Class")

            return self.data_ingestion_config.IMB_DATA_ARTIFACTS_DIR, self.data_ingestion_config.RAW_DATA_ARTIFACTS_DIR

        except Exception as e:
            raise CustomException(e, sys) from e
    
    
    def initiate_data_ingestion(self) -> DataIngestionArtifacts:
        try:
            self.get_data_from_gcloud()
            logging.info("Successfully fetched data from GCloud Bucket!!")

            imbalanced_data_file_path, raw_data_file_path = self.upzip_and_clean()
            logging.info("Successfully extracted data from zip file!!")

            '''
            Code-block alternative for the below code
            data_ingestion_artifacts = DataIngestionArtifacts()
            data_ingestion_artifacts.imbalanced_data_file_path = imbalanced_data_file_path
            data_ingestion_artifacts.raw_data_file_path = raw_data_file_path
            '''
            data_ingestion_artifacts = DataIngestionArtifacts(
                imbalanced_data_file_path = imbalanced_data_file_path,
                raw_data_file_path = raw_data_file_path
            )

            logging.info("Exiting initiate_data_ingestion method of Data Ingestion Class")
            logging.info("Data Ingestion Artifact: {}".format(data_ingestion_artifacts))

            return data_ingestion_artifacts

        except Exception as e:
            raise CustomException(e, sys) from e