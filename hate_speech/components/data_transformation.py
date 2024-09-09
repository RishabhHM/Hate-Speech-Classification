# Fundamental Libraries
import os
import re
import sys
import string

# Libraries for Data Mining & ML
import pandas as pd
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from sklearn.model_selection import train_test_split

# Custom Libraries
from hate_speech.logger import logging
from hate_speech.exception import CustomException
from hate_speech.entity.config_entity import DataTransformationConfig
from hate_speech.entity.artifact_entity import DataIngestionArtifacts, DataTransformationArtifacts

class DataTransformation:
    def __init__(self, data_transformation_config: DataTransformationConfig, data_ingestion_artifacts: DataIngestionArtifacts):
        self.data_transformation_config = data_transformation_config
        self.data_ingestion_artifacts = data_ingestion_artifacts

    
    # Function to clean imbalanced dataset
    def imbalanced_data_cleaning(self):
        logging.info("Executing imbalanced_data_cleaning method of DataTransformation class")
        try:
            imbalanced_data = pd.read_csv(self.data_ingestion_artifacts.imbalanced_data_file_path)
            imbalanced_data.drop(
                self.data_transformation_config.ID,
                axis=self.data_transformation_config.AXIS,
                inplace=self.data_transformation_config.INPLACE
                )
            logging.info("Exiting imbalanced_data_cleaning method of DataTransformation Class")
            return imbalanced_data
        
        except Exception as e:
            raise CustomException(e, sys) from e
    

    # Function to clean raw dataset
    def raw_data_cleaning(self):
        logging.info("Executing raw_data_cleaning method of DataTransformation class")
        try:
            raw_data = pd.read_csv(self.data_ingestion_artifacts.raw_data_file_path)
            raw_data.drop(
                self.data_transformation_config.DROP_COLUMNS,
                axis = self.data_transformation_config.AXIS,
                inplace = self.data_transformation_config.INPLACE
                )

            # Labels 0 & 1 indicate "Hate" whereas label 2 indicates "No Hate"
            # Code to label all "Hate" as 1 and all "No Hate" as 0
            raw_data.loc[raw_data[self.data_transformation_config.CLASS]==0][self.data_transformation_config.CLASS] = 1
            raw_data[self.data_transformation_config.CLASS].replace({2:0}, inplace = self.data_transformation_config.INPLACE)

            # Let's change the name of the target variable from 'class' to 'label'
            raw_data.rename(
                    columns={self.data_transformation_config.CLASS:self.data_transformation_config.LABEL},
                    inplace = self.data_transformation_config.INPLACE
                    )
            logging.info("Exiting raw_data_cleaning method of DataTransformation Class")
            return raw_data

        except Exception as e:
            raise CustomException(e,sys) from e


    # We have 2 datasets. One is imbalanced_data and the other is raw_data
    # Here, we clean and concatenate the 2 datasets into a single dataset
    def concat_dataframe(self):
        logging.info("Executing concat_dataframe method of DataTransformation class")
        try:
            # Let's concatenate both datasets into a single data frame.
            # Note that this function calls the data cleaning functions
            frame = [self.raw_data_cleaning(), self.imbalanced_data_cleaning()]
            df = pd.concat(frame, ignore_index=True)
            print(df.head())
            logging.info(f"Returned the concatenated data-frame {df}")
            logging.info("Exiting concat_dataframe method of DataTransformation Class")
            return df

        except Exception as e:
            raise CustomException(e, sys) from e


    # Function to perform Text-Preprocessing
    def concat_data_cleaning(self, sentence):
        try:
            # Applying stemming and stopwords on the data
            stemmer = nltk.SnowballStemmer("english")
            stopword = set(stopwords.words('english'))

            sentence = str(sentence).lower() # converts sentence into lower case
            
            # removes stopwords from sentence
            words = [word for word in sentence.split(' ') if word not in stopword]
            sentence = " ".join(words)
            # extracts root-words from all words in the sentence
            words = [stemmer.stem(word) for word in sentence.split(' ')]
            sentence = " ".join(words)

            sentence = re.sub('\[.*?\]', '', sentence) # removes text inside [] brackets
            sentence = re.sub('https?://\S+www\.\S+', '', sentence) # removes URLs starting with http or https
            sentence = re.sub('<.*?>', '', sentence) # removes HTML Tags
            sentence = re.sub('[%s]' % re.escape(string.punctuation), '', sentence) # removes all punctuations
            sentence = re.sub('\n', '', sentence) # removes all line brakes
            sentence = re.sub('\w*\d\w*', '', sentence) # removes all words that have number in them

            return sentence

        except Exception as e:
            raise CustomException(e, sys) from e


    def initiate_data_transformation(self):
        logging.info("Executing initiate_data_transformation method of DataTransformation class")
        try:
            df = self.concat_dataframe()

            logging.info("Executing concat_data_cleaning method of DataTransformation class")
            df[self.data_transformation_config.TWEET]=df[self.data_transformation_config.TWEET].apply(self.concat_data_cleaning)
            logging.info("Exiting concat_data_cleaning method of DataTransformation Class")

            os.makedirs(self.data_transformation_config.DATA_TRANSFORMATION_ARTIFACTS_DIR, exist_ok=True)
            
            df.to_csv(self.data_transformation_config.TRANSFORMED_FILE_PATH, index=False, header=True)
            data_transformation_artifact = DataTransformationArtifacts(
                transformed_data_path = self.data_transformation_config.TRANSFORMED_FILE_PATH
            )
            logging.info("Returning DataTransformationArtifacts")
            logging.info("Exiting initiate_data_transformation method of DataTransformation Class")
            return data_transformation_artifact

        except Exception as e:
            raise CustomException(e, sys) from e