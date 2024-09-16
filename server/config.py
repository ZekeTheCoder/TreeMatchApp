#!/usr/bin/env python3
"""
config.py - Configuration module for the TreeMatchApp server.
------------------------------------------------------
This module defines configuration classes for different environments
(development, production, and testing) using environment variables to set
configuration values. The configuration classes inherit from a base Config.
"""
import os
from decouple import config
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class Config:
    """
    Base configuration class with default settings.
    Uses environment variables to set configuration values.
    """
    # SECRET_KEY = os.getenv("SECRET_KEY", "secret")
    SECRET_KEY = config("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = config("SQLALCHEMY_TRACK_MODIFICATIONS",
                                            default=False, cast=bool)
    # SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", False)


class DevConfig(Config):
    """
    Development configuration class.
    Inherits from Config and sets development-specific settings.
    """
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///dev.db")
    DEBUG = True
    # SQLALCHEMY_ECHO = True


class ProdConfig(Config):
    """
    Production configuration class.
    Inherits from Config and sets production-specific settings.
    """
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///prod.db")
    DEBUG = os.getenv("DEBUG", "False")
    SQLALCHEMY_ECHO = os.getenv("ECHO", "False")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv(
        "SQLALCHEMY_TRACK_MODIFICATIONS", "False")


class TestConfig(Config):
    """
    Testing configuration class.
    Inherits from Config and sets testing-specific settings.
    """
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SQLALCHEMY_ECHO = False
    TESTING = True

# The DevConfig, ProdConfig, and TestConfig classes extend the base Config
# class, allowing the Flask application to adapt its settings based
# on the current environment (development, production, or testing).
