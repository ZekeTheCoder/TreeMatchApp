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
from api.plants import plants_ns
from api.invasive_plants import invasive_plants_ns
from api.soil_properties import soil_properties_ns, soil_locations_ns
from api.soil_measurements import soil_measurements_ns
from api.auth import auth_ns
from models.models import Plant, User
from models.invasive_plants_model import InvasivePlant
from models.soil_property_model import SoilProperty, SoilMeasurement, SoilLocation
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
    api.add_namespace(invasive_plants_ns)
    api.add_namespace(soil_properties_ns)
    api.add_namespace(soil_locations_ns)
    api.add_namespace(soil_measurements_ns)
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    CORS(app, supports_credentials=True)  # Allow credentials

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
            'InvasivePlant': InvasivePlant,
            'SoilProperty': SoilProperty,
            'SoilLocation': SoilLocation,
            'SoilMeasurement': SoilMeasurement,
            'User': User}

    return app
