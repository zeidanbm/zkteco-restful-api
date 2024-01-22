from dotenv import load_dotenv
from flask import Flask
import os
import logging
import sentry_sdk
from logging.handlers import RotatingFileHandler
from zkteco.services.zk_service import get_zk_service
from zkteco.controllers.user_controller import bp as user_blueprint
from zkteco.controllers.device_controller import bp as device_blueprint
from zkteco.logger import create_log_handler

load_dotenv()

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

    return app


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
