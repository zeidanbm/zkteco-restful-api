import os
from distutils.util import strtobool

SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = bool(strtobool(os.getenv("FLASK_DEBUG", "false")))

DEVICE_IP = os.environ.get('DEVICE_IP', '192.168.3.18')
DEVICE_PORT = int(os.getenv("DEVICE_PORT", "4370"))

LOG_FILE_SIZE = os.getenv("LOG_FILE_SIZE", "10485760")
