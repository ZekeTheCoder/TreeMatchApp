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
from flask_migrate import Migrate
from models import Plant
from exts import db
from config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)
api = Api(app, doc="/docs")
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

# model serializer
plant_model = api.model(
    'Plant', {
        'id': fields.Integer,
        'title': fields.String,
        'description': fields.String
    })


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
        return new_plant, 201


@api.route('/plant/<int:id>')
class PlantResource(Resource):
    """
    PlantResource class for handling the plant endpoint.
    It is part of the TreeMatch application API.
    """

    @api.marshal_with(plant_model)
    def get(self, id):
        """
        GET method for the Plant resource.
        Returns:
            A JSON response with the plant with the specified ID.
        """
        plant = Plant.query.get_or_404(id)
        return plant

    @api.marshal_with(plant_model)
    def put(self, id):
        """
        PUT method for the Plant resource.
        Returns:
            A JSON response with the updated plant.
        """
        plant_to_update = Plant.query.get_or_404(id)
        response_data = request.get_json()
        plant_to_update.update(response_data.get('title'),
                               response_data.get('description'))
        return plant_to_update

    # @api.marshal_with(plant_model)
    def delete(self, id):
        """
        DELETE method for the Plant resource.
        Returns:
            A JSON response with a message indicating the plant was deleted.
        """
        plant_to_delete = Plant.query.get_or_404(id)
        plant_to_delete.delete()
        # return plant_to_delete, 200  # returns deleted object
        return jsonify(f'Plant {plant_to_delete.title} deleted successfully')


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
