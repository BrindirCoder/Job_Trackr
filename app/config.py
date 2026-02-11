import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key"

    JWT_SECRET_KEY = "super-secret-jwt-key-super-secret-32bytes"
    JWT_TOKEN_LOCATION = ["headers"]          
    JWT_HEADER_NAME = "Authorization"          
    JWT_HEADER_TYPE = "Bearer"                

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "..", "instance", "jobtracker.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_ACCESS_TOKEN_EXPIRES = False
