#!/usr/bin/env python3

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Text
# from sqlalchemy.orm import scoped_session, sessionmaker
# from flask_migrate import Migrate
# from flask_cors import CORS
# from flask_restx import Api

# Initialize extensions
db = SQLAlchemy()
# migrate = Migrate()
# cors = CORS()
# api = Api()

# def init_app(app):
#     """
#     Initialize extensions with the Flask app instance.

#     :param app: Flask application instance
#     """
#     db.init_app(app)
#     migrate.init_app(app, db)
#     cors.init_app(app)
#     api.init_app(app)
