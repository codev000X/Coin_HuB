import logging
import os

# creating the Log directory if it doesn't exist
LOG_DIR = 'logs'
os.makedirs(LOG_DIR , exist_ok = True)

# Creating the log file.
LOG_FILE = os.path.join(os.path.abspath(LOG_DIR), "etl.log")

def get_logger(name):
    """
    Returns the configured logger with file and console handlers.
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # preventing the duplicate handlers
    if logger.handlers:
        return logger


    # log message format.
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # File Handler
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Attach Handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger