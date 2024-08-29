from hate_speech.logger import logging
from hate_speech.exception import CustomException
import sys

# logging.info("Testing log setup")

try:
    a = 7 / "0"
except Exception as e:
    raise CustomException(e, sys) from e