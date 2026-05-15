 
import time
import logging
from utils.logging_config import setup_logging
logger = logging.getLogger(__name__)

setup_logging()

 
logger.critical('This is a critical message')

for i in range(10):
    logger.info(f'Info message {i}')
    time.sleep(1)