import logging
from logging.handlers import RotatingFileHandler
import os


def create_log_handler():
    # Log file size from .env or default to 10MB
    log_file_size = int(os.getenv('LOG_FILE_SIZE', 10485760))

    # Set up logging
    log_file_path = os.path.join(os.getcwd(), 'app.log')
    handler = RotatingFileHandler(log_file_path, maxBytes=log_file_size, backupCount=3)

    # Define the formatter and set it for the handler
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
    handler.setFormatter(formatter)

    return handler


# Create a separate logger instance outside of the Flask app context
app_logger = logging.getLogger(__name__)
app_logger.addHandler(create_log_handler())
app_logger.setLevel(logging.INFO)