import sys
import time
from hate_speech.logger import logging
from hate_speech.exception import CustomException
from hate_speech.components.data_ingestion import DataIngestion
from hate_speech.components.data_validation import DataValidation
from hate_speech.entity.config_entity import DataIngestionConfig
from hate_speech.entity.artifact_entity import DataIngestionArtifacts

class TrainPipeline:
    def __init__(self) -> None:
        self.data_ingestion_config = DataIngestionConfig()
    
    
    def start_data_ingestion(self) -> DataIngestionArtifacts:
        logging.info("Entered the start_data_ingestion method of TrainPipeline class")
        try:
            logging.info("Getting the data from GCloud Storage Bucket")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)

            data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
            logging.info("Got data from GCloud Storage")
            logging.info("Exiting start_data_ingestion method of TrainPipeline class")
            return data_ingestion_artifacts
        
        except Exception as e:
            raise CustomException(e, sys) from e


    def start_data_validation(self, data_ingestion_artifacts: DataIngestionArtifacts):
        logging.info("Entered start_data_validation method of TrainPipeline class")
        try:
            data_validation = DataValidation()
            data_validation.validate_imbalanced_data(data_ingestion_artifacts.imbalanced_data_file_path)
            data_validation.validate_raw_data(data_ingestion_artifacts.raw_data_file_path)
            logging.info("Exciting start_data_validation method of TrainPipeline class")
        
        except Exception as e:
            raise CustomException(e, sys) from e


    def run_pipeline(self):
        logging.info("Entered the run_pipeline method of TrainPipeline class")
        try:
            data_ingestion_artifacts = self.start_data_ingestion()
            
            time.sleep(3)
            print("Loading Data...")
            self.start_data_validation(data_ingestion_artifacts)
            logging.info("Exiting run_pipeline method of TrainPipeline class")
        
        except Exception as e:
            raise CustomException(e, sys) from e