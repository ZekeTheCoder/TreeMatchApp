#!/usr/bin/env python3
"""
soil_properties.py - Module for handling soil property-related operations.
------------------------------------------------------
This module defines the API endpoints for managing soil properties in the TreeMatch application.
It includes endpoints for retrieving, creating, updating, and deleting soil property records.
"""
from flask import request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required
from models.soil_property_model import SoilProperty, SoilLocation

soil_properties_ns = Namespace(
    'soil_properties', description='A namespace for Soil Property related operations')

# SoilProperty model serializer
soil_property_model = soil_properties_ns.model(
    'SoilProperty', {
        'id': fields.Integer,
        'property_name': fields.String,
        'description': fields.String,
        'theme': fields.String,
        'unit': fields.String,
        'uncertainty': fields.Boolean,
        'value_type': fields.String
    })


@soil_properties_ns.route('/soil_properties')
class SoilPropertiesResource(Resource):
    """
    SoilPropertiesResource class for handling the soil_properties endpoint.
    It is part of the TreeMatch application API.
    """

    @soil_properties_ns.marshal_with(soil_property_model, as_list=True)
    def get(self):
        """
        GET method for the SoilProperties resource.
        Returns:
            A JSON response with a list of soil properties.
        """
        soil_properties = SoilProperty.query.all()
        return soil_properties

    @soil_properties_ns.expect(soil_property_model)
    # @jwt_required()
    def post(self):
        """
        POST method for the SoilProperties resource.
        Returns:
            A JSON response with the newly created soil property or an error message.
        """
        data = request.get_json()

        # Check if the required fields are present in the request
        if not data or 'property_name' not in data or 'description' not in data or 'theme' not in data or 'unit' not in data or 'uncertainty' not in data or 'value_type' not in data:
            return {'message': 'Invalid input, missing required fields'}, 400

        new_soil_property = SoilProperty(
            property_name=data.get('property_name'),
            description=data.get('description'),
            theme=data.get('theme'),
            unit=data.get('unit'),
            uncertainty=data.get('uncertainty'),
            value_type=data.get('value_type')
        )

        new_soil_property.save()

        return soil_properties_ns.marshal(new_soil_property, soil_property_model), 201


@soil_properties_ns.route('/<int:id>')
class SoilPropertyResource(Resource):
    """
    SoilPropertyResource class for handling the soil_property endpoint.
    It is part of the TreeMatch application API.
    """

    @soil_properties_ns.marshal_with(soil_property_model)
    def get(self, id):
        """
        GET method for the SoilProperty resource.
        Returns:
            A JSON response with the soil property with the specified ID.
        """
        soil_property = SoilProperty.query.get_or_404(id)
        return soil_property

    @soil_properties_ns.expect(soil_property_model)
    @soil_properties_ns.marshal_with(soil_property_model)
    # @jwt_required()
    def put(self, id):
        """
        PUT method for the SoilProperty resource.
        Returns:
            A JSON response with the updated soil property.
        """
        soil_property_to_update = SoilProperty.query.get_or_404(id)
        data = request.get_json()
        soil_property_to_update.update(
            property_name=data.get('property_name'),
            description=data.get('description'),
            theme=data.get('theme'),
            unit=data.get('unit'),
            depths=data.get('depths'),
            uncertainty=data.get('uncertainty'),
            value_type=data.get('value_type')
        )
        return soil_property_to_update

    # @jwt_required()
    def delete(self, id):
        """
        DELETE method for the SoilProperty resource.
        Returns:
            A JSON response with a message indicating the soil property was deleted.
        """
        soil_property_to_delete = SoilProperty.query.get_or_404(id)
        soil_property_to_delete.delete()
        return {"message": f"Soil Property {soil_property_to_delete.property_name} deleted successfully"}, 200


soil_locations_ns = Namespace(
    'soil_locations', description='A namespace for Soil Location related operations')

# SoilLocation model serializer
soil_location_model = soil_locations_ns.model(
    'SoilLocation',
    {
        'id': fields.Integer(readOnly=True, description='The unique identifier of a soil location'),
        'name': fields.String(required=True, description='The name of the soil location'),
        'latitude': fields.Float(required=True, description='The latitude of the soil location'),
        'longitude': fields.Float(required=True, description='The longitude of the soil location')
    }
)


@soil_locations_ns.route('/locations')
class SoilLocationsResource(Resource):
    @soil_locations_ns.marshal_with(soil_location_model)
    def get(self):
        """Get all soil locations"""
        return SoilLocation.query.all()

    @soil_locations_ns.expect(soil_location_model)
    @soil_locations_ns.marshal_with(soil_location_model)
    def post(self):
        """Create a new soil location"""
        data = request.json
        new_location = SoilLocation(
            name=data['name'],
            latitude=data['latitude'],
            longitude=data['longitude']
        )
        new_location.save()
        return new_location, 201


@soil_locations_ns.route('/<int:id>')
class SoilLocationResource(Resource):
    @soil_locations_ns.marshal_with(soil_location_model)
    def get(self, id):
        """Get a soil location by its ID"""
        return SoilLocation.query.get_or_404(id)

    @soil_locations_ns.expect(soil_location_model)
    @soil_locations_ns.marshal_with(soil_location_model)
    def put(self, id):
        """Update a soil location by its ID"""
        data = request.json
        location = SoilLocation.query.get_or_404(id)
        location.update(**data)
        return location

    def delete(self, id):
        """Delete a soil location by its ID"""
        location = SoilLocation.query.get_or_404(id)
        location.delete()
        return '', 204
