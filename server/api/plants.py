#!/usr/bin/env python3
""" 
plants.py - Module for handling plant-related operations.
------------------------------------------------------
This module defines the API endpoints for managing plants in the TreeMatch application.
It includes endpoints for retrieving, creating, updating, and deleting plant records.
"""
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required
from flask import request, jsonify
from models.models import Plant
from utils import identify_plant  # Adjust the import path as necessary
import json
from utils import get_simulated_response


plants_ns = Namespace(
    'plants', description='A namespace for Plant related operations')

# plant_model serializer
plant_model = plants_ns.model(
    'Plant', {
        'id': fields.Integer,
        'title': fields.String,
        'description': fields.String
    })


@plants_ns.route('/plants')
class PlantsResource(Resource):
    """
    Plants Resource class for handling the plants endpoint.
    It is part of the TreeMatch application API.
    """
    # welcome route
    @plants_ns.route('/welcome')
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
            # return jsonify('Hello, Welcome to TreeMatch!')
            return {"message": "Hello, Welcome to TreeMatch!"}

    # model serializer decorator
    @plants_ns.marshal_with(plant_model, as_list=True)
    # @plants_ns.marshal_list_with(plant_model)
    def get(self):
        """
        GET method for the Plants resource.
        Returns:
            A JSON response with a list of plants.
        """
        plants = Plant.query.all()
        return plants

    # validates the incoming request data according to the plant_model or 400 error.
    @plants_ns.expect(plant_model)
    @jwt_required()
    def post(self):
        """
        POST method for the Plants resource.
        Returns:
            A JSON response with the newly created plant or an error message.
        """
        data = request.get_json()

        # Check if the required fields are present in the request
        if not data or 'title' not in data or 'description' not in data:
            return {'message': 'Invalid input, missing title or description'}, 400

        new_plant = Plant(
            title=data.get('title'),
            description=data.get('description')
        )

        new_plant.save()

        # Use marshal_with here only when successful
        return plants_ns.marshal(new_plant, plant_model), 201


@plants_ns.route('/plant/<int:id>')
class PlantResource(Resource):
    """
    PlantResource class for handling the plant endpoint.
    It is part of the TreeMatch application API.
    """

    @plants_ns.marshal_with(plant_model)
    def get(self, id):
        """
        GET method for the Plant resource.
        Returns:
            A JSON response with the plant with the specified ID.
        """
        plant = Plant.query.get_or_404(id)
        return plant

    @plants_ns.marshal_with(plant_model)
    @jwt_required()
    def put(self, id):
        """
        PUT method for the Plant resource.
        Returns:
            A JSON response with the updated plant.
        """
        plant_to_update = Plant.query.get_or_404(id)
        data = request.get_json()
        plant_to_update.update(data.get('title'),
                               data.get('description'))
        return plant_to_update

    # @plants_ns.marshal_with(plant_model)
    @jwt_required()
    def delete(self, id):
        """
        DELETE method for the Plant resource.
        Returns:
            A JSON response with a message indicating the plant was deleted.
        """
        plant_to_delete = Plant.query.get_or_404(id)
        plant_to_delete.delete()
        # return plant_to_delete, 200  # returns deleted object
        return {"message": f"Plant {plant_to_delete.title} deleted successfully"}, 200


@plants_ns.route('/identify')
class IdentifyPlantResource(Resource):
    """
    IdentifyPlantResource class for handling the plant identification endpoint.
    """
    @plants_ns.doc(params={
        'image': 'Base64 encoded image data',
        'latitude': 'Latitude of the location',
        'longitude': 'Longitude of the location'
    })
    def post(self):
        """
        POST method for identifying a plant.
        Expects:
            A JSON payload with 'image', 'latitude', and 'longitude'.
        Returns:
            A JSON response with the plant identification information.
        """
        data = request.get_json()
        # print(data)

        if data is None:
            return {'message': 'Invalid JSON payload'}, 400

        image_data_base64 = data.get('image')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        print(latitude, longitude)

        if not image_data_base64 or latitude is None or longitude is None:
            return {'message': 'Missing required parameters'}, 400

        plant_info = identify_plant(image_data_base64, latitude, longitude)

        # Simulate response using the response file
        # with open('response', 'r') as file:
        #     plant_info = json.load(file)
        plant_response_json = get_simulated_response(plant_info)

        print(plant_response_json)
        return jsonify(json.loads(plant_response_json))
