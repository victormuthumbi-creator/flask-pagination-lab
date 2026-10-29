# app_config.py
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    DEBUG = True

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True

config_dict = {
    "dev": DevConfig,
    "test": TestConfig,
}

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

def create_app(env="dev"):
    app = Flask(__name__)
    app.config.from_object(config_dict[env])
    app.json.compact = False

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    return app

db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
api = Api()
