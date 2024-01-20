from flask import Flask
import os
import logging
import sentry_sdk
from logging.handlers import RotatingFileHandler
from zkteco.services.zk_service import get_zk_service
from zkteco.controllers.user_controller import bp as user_blueprint
from zkteco.controllers.device_controller import bp as device_blueprint


def create_app():
    init_sentry()
    # create and configure the app
    app = Flask(__name__)
    
    app.config.from_object("zkteco.config.settings")

    handler = create_log_handler()

    # Add the handler to the app's logger
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    # Register the blueprints
    app.register_blueprint(user_blueprint)
    app.register_blueprint(device_blueprint)

    with app.app_context():
        get_zk_service()

    return app


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


def init_sentry():
    sentry_sdk.init(
        dsn="https://5f9be5c667e175dcb31118d107c5551b@o4504142684422144.ingest.sentry.io/4506604971819008",
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )