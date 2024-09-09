# Creating model architecture
import sys
from hate_speech.constants import *
from hate_speech.logger import logging
from hate_speech.exception import CustomException
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Activation, Dense, Dropout, Input, Embedding, SpatialDropout1D
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

class ModelArchitecture:
    def __init__(self):
        pass
        # Note that for this module, we are not creating a model_trainer_config instance.
        # It is recommended to use the above approach.
        # However for convenience we will directly use the defined constants here.


    def create_architecture(self):
        logging.info("Executing create_architecture method of ModelArchitecture class")
        try:
            model = Sequential()
            model.add(Embedding(MAX_WORDS, 100))
            model.add(SpatialDropout1D(0.2))
            model.add(LSTM(100, dropout=0.2, recurrent_dropout=0.2))
            model.add(Dense(1, activation=ACTIVATION))
            model.summary()
            model.compile(loss=LOSS, optimizer=RMSprop(), metrics=METRICS)

            logging.info("Exiting create_architecture method of ModelArchitecture Class")
            return model
        
        except Exception as e:
            raise CustomException(e, sys) from e