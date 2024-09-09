# Fundamental Libraries
import sys
import time

# Custom Libraries
from hate_speech.logger import logging
from hate_speech.exception import CustomException

# Custom Libraries for Building Pipeline
from hate_speech.components.data_ingestion import DataIngestion
from hate_speech.components.data_validation import DataValidation
from hate_speech.components.data_transformation import DataTransformation
from hate_speech.components.model_trainer import ModelTrainer
from hate_speech.entity.config_entity import DataIngestionConfig, DataTransformationConfig, ModelTrainerConfig
from hate_speech.entity.artifact_entity import DataIngestionArtifacts, DataTransformationArtifacts, ModelTrainerArtifacts

class TrainPipeline:
    def __init__(self) -> None:
        self.data_ingestion_config = DataIngestionConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()

    
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
        
    
    def start_data_transformation(self, data_ingestion_artifacts = DataIngestionArtifacts) -> DataTransformationArtifacts:
        logging.info("Entered start_data_transformation method of TrainPipeline class")
        try:
            data_transformation = DataTransformation(self.data_transformation_config, data_ingestion_artifacts)
            data_transformation_artifacts = data_transformation.initiate_data_transformation()
            logging.info("Exiting start_data_transformation method of TrainPipeline class")
            return data_transformation_artifacts
        
        except Exception as e:
            raise CustomException(e, sys) from e
    

    def start_model_training(self, data_transformation_artifacts: DataTransformationArtifacts) -> ModelTrainerArtifacts:
        logging.info("Entered start_model_training method of TrainPipeline class")
        try:
            model_trainer = ModelTrainer(data_transformation_artifacts, model_trainer_config=self.model_trainer_config)
            model_trainer_artifacts = model_trainer.initiate_model_trainer()
            logging.info("Exiting start_model_training method of TrainPipeline class")
            return model_trainer_artifacts
        
        except Exception as e:
            raise CustomException(e, sys) from e



    def run_pipeline(self):
        logging.info("Entered the run_pipeline method of TrainPipeline class")
        try:
            print("***** Starting Data Ingestion *****")
            data_ingestion_artifacts = self.start_data_ingestion()
            print("***** Completed Data Ingestion *****")
            print("\n\n")

            print("***** Starting Data Validation *****")
            time.sleep(3)
            print("Loading Data...")
            self.start_data_validation(data_ingestion_artifacts)
            print("***** Completed Data Validation *****")
            print("\n\n")

            print("***** Starting Data Transformation *****")
            data_transformation_artifacts = self.start_data_transformation(data_ingestion_artifacts=data_ingestion_artifacts)
            print("***** Completed Data Transformation *****")
            print("\n\n")

            print("***** Starting Model Training *****")
            data_transformation_artifacts = self.start_model_training(data_transformation_artifacts=data_transformation_artifacts)
            print("***** Completed Model Training *****")
            print("\n\n")

            logging.info("Exiting run_pipeline method of TrainPipeline class")
        
        except Exception as e:
            raise CustomException(e, sys) from e