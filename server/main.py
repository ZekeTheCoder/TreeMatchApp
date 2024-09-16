#!/usr/bin/env python3
"""
main.py
--------
This module initializes and configures the Flask application for the TreeMatchApp server.
It sets up CORS, RESTful API routes, and configures the application
using the development configuration.
"""
from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from plants import plants_ns
from auth import auth_ns
from models import Plant, User
from exts import db


def create_app(config):
    """
    Creates and configures the Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(config)
    api = Api(app, doc="/docs")
    api.add_namespace(auth_ns)
    api.add_namespace(plants_ns)
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    CORS(app)

    @app.shell_context_processor
    def make_shell_context():
        """
        Provides shell context for Flask CLI.

        Returns:
                dict: A dictionary containing database instance and Plant model.
        """
        return {
            'db': db,
            'Plant': Plant,
            'User': User}

    return app
