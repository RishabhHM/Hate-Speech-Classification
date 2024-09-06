'''
1. Open imbalanced data and check if 3 columns are present
2. If 3 columns are present, then see if the column names are same or not.
3. Return True if all is well

4. Load raw data and check if 7 columns are present and if the names are same
5. Return True if all is well
'''
import sys
import pandas as pd
from hate_speech.logger import logging
from hate_speech.exception import CustomException

class DataValidation:
    def validate_imbalanced_data(self, imbalanced_data_file_path):
        logging.info("Executing validate_imbalanced_data method of DataValidation class ")
        try:
            imbal_data = pd.read_csv(imbalanced_data_file_path)
            req_col_names = ['id', 'label', 'tweet']
            if list(imbal_data.columns) == req_col_names:
                logging.info("All expected columns present and headings match the required format in imbalanced dataset.")
            else:
                error_message = "Columns in the imbalanced dataset do not match the required format."
                logging.error(error_message)
                raise ValueError(error_message)
        except Exception as e:
            raise CustomException(e, sys) from e


    def validate_raw_data(self, raw_data_file_path):
        logging.info("Executing validate_raw_data method of DataValidation class ")
        try:
            raw_data = pd.read_csv(raw_data_file_path)
            req_col_names = ['Unnamed: 0', 'count', 'hate_speech', 'offensive_language', 'neither', 'class', 'tweet']
            if list(raw_data.columns) == req_col_names:
                logging.info("All expected columns present and headings match the required format in raw dataset.")
            else:
                error_message = "Columns in the raw dataset do not match the required format."
                logging.error(error_message)
                raise ValueError(error_message)
        except Exception as e:
            raise CustomException(e, sys) from e