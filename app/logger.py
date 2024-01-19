import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a logger for the Flask app
app_logger = logging.getLogger('flask_app')