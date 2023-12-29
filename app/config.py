import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', '40cd37d3a972edccd64d62bb70481633446a6ea18a7f5f5e103d47b5a9833b2b')
    DEVICE_IP = int(os.environ.get('DEVICE_IP', '192.168.20.205'))
    DEVICE_PORT = os.environ.get('DEVICE_PORT', '4370')
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    pass