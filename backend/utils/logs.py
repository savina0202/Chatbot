import logging
from config import LOGGING_LEVEL, BACKEND_LOG_PATH, FRONTEND_LOG_PATH

# For backend logs
def enable_log(side):
    if side=="backend":
        log_path=BACKEND_LOG_PATH
        logging.basicConfig(
            filename=log_path,
            filemode='a',
            level=LOGGING_LEVEL,
            format='%(asctime)s %(levelname)s: %(message)s'
        )
    elif side=="frontend":
        log_path=FRONTEND_LOG_PATH
        logging.basicConfig(
            filename=log_path,
            filemode='a',
            level=LOGGING_LEVEL,
            format='%(asctime)s %(levelname)s: %(message)s'
        )
    else:
        raise ValueError("Invalid log setup specified.")
    logging.info(f"Logging enabled for {side}.")

    
