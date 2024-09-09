# Fundamental Libraries
import sys
import os
import pickle

# Libraries for Data Mining & ML
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import pad_sequences
from sklearn.model_selection import train_test_split

# Custom Libraries
from hate_speech.logger import logging
from hate_speech.exception import CustomException
from hate_speech.entity.config_entity import ModelTrainerConfig
from hate_speech.entity.artifact_entity import DataTransformationArtifacts, ModelTrainerArtifacts
from hate_speech.ml.model import ModelArchitecture


class ModelTrainer:
    def __init__(
            self,
            data_transformation_artifacts: DataTransformationArtifacts,
            model_trainer_config: ModelTrainerConfig):
        self.data_transformation_artifacts = data_transformation_artifacts
        self.model_trainer_config = model_trainer_config
    
    
    def splitting_data(self, csv_path):
        logging.info("Executing splitting_data method of ModelTrainer class")
        try:
            logging.info("Reading the data")
            df = pd.read_csv(csv_path, index_col=False)
            logging.info("Splitting the data into x & y")
            x = df[self.model_trainer_config.TWEET]
            y = df[self.model_trainer_config.LABEL]

            logging.info("Applying train_test_split on the data")
            x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=42)
            print('Training Size: {}'.format(len(x_train)))
            print('Testing Size: {}'.format(len(x_test)))

            logging.info("Exiting splitting_data method of ModelTrainer Class")
            return x_train, x_test, y_train, y_test
            
        except Exception as e:
            raise CustomException(e, sys) from e
    

    def tokenizing(self, x_train):
        logging.info("Executing tokenizing method of ModelTrainer class")
        try:
            tokenizer = Tokenizer(num_words=self.model_trainer_config.MAX_WORDS)

            # Somehow there appears one record with 'nan' value.
            # Hardcoding for now by using fillna('') to resolve the error.
            for i, item in enumerate(x_train):
                if not isinstance(item, str):
                    print(f"Item at index {i} is of type {type(item)}: {item}")
            x_train = x_train.fillna('')
            for i, item in enumerate(x_train):
                if not isinstance(item, str):
                    print(f"Item at index {i} is of type {type(item)}: {item}")

            tokenizer.fit_on_texts(x_train)
            train_sequences = tokenizer.texts_to_sequences(x_train)
            logging.info(f"Converting text to sequences: {train_sequences}")
            train_sequences_matrix = pad_sequences(train_sequences, maxlen=self.model_trainer_config.MAX_LEN)
            logging.info(f"The sequence matrix is: {train_sequences_matrix}")            

            logging.info("Exiting tokenizing method of ModelTrainer Class")
            return tokenizer, train_sequences_matrix
        
        except Exception as e:
            raise CustomException(e, sys) from e
    

    def initiate_model_trainer(self) -> ModelTrainerArtifacts:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")

        """
        Method Name :   initiate_model_trainer
        Description :   This function initiates all model trainer steps
        
        Output      :   Returns model trainer artifact
        On Failure  :   Write an exception log and then raise an exception
        """

        try:
            logging.info("Executing initiate_model_trainer method of ModelTrainer class")
            x_train, x_test, y_train, y_test = self.splitting_data(csv_path=self.data_transformation_artifacts.transformed_data_path)
            model_architecture = ModelArchitecture()   
            model = model_architecture.create_architecture()
            
            logging.info(f"x_train size is : {x_train.shape}")
            logging.info(f"x_test size is : {x_test.shape}")

            # Importing tokenizer and the integer encoded text sequence
            tokenizer, sequences_matrix = self.tokenizing(x_train)

            logging.info("Entered into model training")
            model.fit(sequences_matrix, y_train, 
                        batch_size=self.model_trainer_config.BATCH_SIZE, 
                        epochs = self.model_trainer_config.EPOCH, 
                        validation_split=self.model_trainer_config.VALIDATION_SPLIT, 
                        )
            logging.info("Model training complete")
            
            os.makedirs(self.model_trainer_config.TRAINED_MODEL_DIR, exist_ok=True)
            logging.info("Saving the tokenizer vocabulary as pickle file")
            with open(self.model_trainer_config.TOKEN_VOCAB_PATH , 'wb') as handle:
                pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

            logging.info("Saving the model")
            model.save(self.model_trainer_config.TRAINED_MODEL_PATH)
            x_test.to_csv(self.model_trainer_config.X_TEST_DATA_PATH)
            y_test.to_csv(self.model_trainer_config.Y_TEST_DATA_PATH)
            x_train.to_csv(self.model_trainer_config.X_TRAIN_DATA_PATH)
            y_train.to_csv(self.model_trainer_config.Y_TRAIN_DATA_PATH)

            model_trainer_artifacts = ModelTrainerArtifacts(
                trained_model_path = self.model_trainer_config.TRAINED_MODEL_PATH,
                token_vocab_path = self.model_trainer_config.TOKEN_VOCAB_PATH,
                x_test_path = self.model_trainer_config.X_TEST_DATA_PATH,
                y_test_path = self.model_trainer_config.Y_TEST_DATA_PATH)
            logging.info("Returning the ModelTrainerArtifacts")
            return model_trainer_artifacts

        except Exception as e:
            raise CustomException(e, sys) from e