#!/usr/bin/env python3
"""
main.py
--------
This module initializes and configures the Flask application for the TreeMatchApp server.
It sets up CORS, RESTful API routes, and configures the application
using the development configuration.
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from config import DevConfig
from models import Plant
from exts import db

app = Flask(__name__)
app.config.from_object(DevConfig)
api = Api(app, doc="/docs")
db.init_app(app)
CORS(app)

# model serializer
plant_model = api.model(
    'Plant', {
        'id': fields.Integer,
        'title': fields.String,
        'description': fields.String
    })


@api.route('/plants')
class PlantsResource(Resource):
    """
    Plants Resource class for handling the plants endpoint.
    It is part of the TreeMatch application API.
    """

    @api.marshal_with(plant_model, as_list=True)  # model serializer decorator
    # @api.marshal_list_with(plant_model)
    def get(self):
        """
        GET method for the Plants resource.
        Returns:
                                A JSON response with a list of plants.
        """
        plants = Plant.query.all()
        return plants

    @api.marshal_with(plant_model)
    def post(self):
        """
        POST method for the Plants resource.
        Returns:
                                A JSON response with the newly created plant.
        """
        data = request.get_json()
        new_plant = Plant(
            title=data.get('title'),
            description=data.get('description')
        )
        new_plant.save()
        return new_plant

    # validate the incoming request payload against the plant_model.
    # @api.expect(plant_model)
    # def post(self):
    #     """
    #     POST method for the Plants resource.
    #     Returns:
    #         A JSON response with the newly created plant.
    #     """
    #     new_plant = Plant(
    #         **api.payload)  # Unpacks the payload directly into the Plant model
    #     new_plant.save()
    #     return new_plant


@api.route('/welcome')
class Welcome(Resource):
    """
    Welcome Resource class for handling the welcome endpoint.
    It is part of the TreeMatch application API.
    """

    def get(self):
        """
            GET method for the Welcome resource.
            Returns:
                            A JSON response with a welcome message.
            """
        return jsonify('Hello, Welcome to TreeMatch!')


@app.shell_context_processor
def make_shell_context():
    """
    Provides shell context for Flask CLI.

    Returns:
        dict: A dictionary containing database instance and Plant model.
    """
    return {'db': db, 'Plant': Plant}


if __name__ == '__main__':
    app.run(debug=True, port=5000)
