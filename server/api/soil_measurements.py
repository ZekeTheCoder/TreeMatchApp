#!/usr/bin/env python3
"""
soil_measurements.py - Module for handling soil measurement-related operations.
------------------------------------------------------
This module defines the API endpoints for managing soil measurements in the TreeMatch application.
It includes endpoints for retrieving, creating, updating, and deleting soil measurement records.
"""
import requests
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required
from flask import request, jsonify
from models.soil_property_model import SoilMeasurement
from utils import get_soil_property, get_recommendation, soil_recommendation

soil_measurements_ns = Namespace(
    'soil_measurements', description='A namespace for Soil Measurement related operations')

# SoilMeasurement model serializer
soil_measurement_model = soil_measurements_ns.model(
    'SoilMeasurement', {
        'id': fields.Integer,
        'property_id': fields.Integer,
        'location_id': fields.Integer,
        'value': fields.Float,
        'depth': fields.String,
        'uncertainty_50': fields.String,
        'uncertainty_68': fields.String,
        'uncertainty_90': fields.String
    })


@soil_measurements_ns.route('/soil_measurements')
class SoilMeasurementsResource(Resource):
    """
    SoilMeasurementsResource class for handling the soil_measurements endpoint.
    It is part of the TreeMatch application API.
    """

    @soil_measurements_ns.marshal_with(soil_measurement_model, as_list=True)
    def get(self):
        """
        GET method for the SoilMeasurements resource.
        Returns:
            A JSON response with a list of soil measurements.
        """
        soil_measurements = SoilMeasurement.query.all()
        return soil_measurements

    @soil_measurements_ns.expect(soil_measurement_model)
    # @jwt_required()
    def post(self):
        """
        POST method for the SoilMeasurements resource.
        Returns:
            A JSON response with the newly created soil measurement or an error message.
        """
        data = request.get_json()

        # Check if the required fields are present in the request
        if not data or 'property_id' not in data or 'location_id' not in data or 'value' not in data or 'depth' not in data:
            return {'message': 'Invalid input, missing required fields'}, 400

        new_soil_measurement = SoilMeasurement(
            property_id=data.get('property_id'),
            location_id=data.get('location_id'),
            value=data.get('value'),
            depth=data.get('depth'),
            uncertainty_50=data.get('uncertainty_50'),
            uncertainty_68=data.get('uncertainty_68'),
            uncertainty_90=data.get('uncertainty_90')
        )

        new_soil_measurement.save()

        return soil_measurements_ns.marshal(new_soil_measurement, soil_measurement_model), 201


@soil_measurements_ns.route('/<int:id>')
class SoilMeasurementResource(Resource):
    """
    SoilMeasurementResource class for handling the soil_measurement endpoint.
    It is part of the TreeMatch application API.
    """

    @soil_measurements_ns.marshal_with(soil_measurement_model)
    def get(self, id):
        """
        GET method for the SoilMeasurement resource.
        Returns:
            A JSON response with the soil measurement with the specified ID.
        """
        soil_measurement = SoilMeasurement.query.get_or_404(id)
        return soil_measurement

    @soil_measurements_ns.expect(soil_measurement_model)
    @soil_measurements_ns.marshal_with(soil_measurement_model)
    # @jwt_required()
    def put(self, id):
        """
        PUT method for the SoilMeasurement resource.
        Returns:
            A JSON response with the updated soil measurement.
        """
        soil_measurement_to_update = SoilMeasurement.query.get_or_404(id)
        data = request.get_json()
        soil_measurement_to_update.update(
            property_id=data.get('property_id'),
            location_id=data.get('location_id'),
            value=data.get('value'),
            depth=data.get('depth'),
            uncertainty_50=data.get('uncertainty_50'),
            uncertainty_68=data.get('uncertainty_68'),
            uncertainty_90=data.get('uncertainty_90')
        )
        return soil_measurement_to_update

    # @jwt_required()
    def delete(self, id):
        """
        DELETE method for the SoilMeasurement resource.
        Returns:
            A JSON response with a message indicating the soil measurement was deleted.
        """
        soil_measurement_to_delete = SoilMeasurement.query.get_or_404(id)
        soil_measurement_to_delete.delete()
        return {"message": f"Soil Measurement {soil_measurement_to_delete.id} deleted successfully"}, 200


@soil_measurements_ns.route('/get_soil_property')
class GetSoilPropertyResource(Resource):
    @jwt_required()
    @soil_measurements_ns.doc(params={
        'latitude': 'Latitude of the location (e.g 9.4425)',
        'longitude': 'Longitude of the location (e.g -0.7770)',
        # 'property_name': 'The soil property to query (e.g., "ph")'
    })
    def get(self):
        lat = request.args.get('latitude', type=float)
        lon = request.args.get('longitude', type=float)
        # property_name = request.args.get('property_name', type=str)
        # auth_header = request.headers.get('Authorization')

        if not lat or not lon:
            return {'message': 'Missing required parameters'}, 400

        # result = get_soil_property(lat, lon, property_name)
        # property_name = result.get('property')
        # value = result.get('value')

        # print(f"Property: {property_name}, Value: {value}")
        # print(f"Recommendation: {get_recommendation(property_name, value)}")

        # properties = ["ph", "bulk_density", "carbon_organic", "carbon_total"]
        properties = ["ph", "bulk_density"]

        report = soil_recommendation(lat, lon, properties)
        # Destructure and print the report
        for propety, details in report.items():
            value = details.get('value')
            recommendation = details.get('recommendation')
            print(
                f"Property: {propety}, Value: {value}, Recommendation: {recommendation}")

        return report, 200
        # return (f"Property: {property_name}, Value: {value}"), 200


@soil_measurements_ns.route('/get_recommendation')
class GetRecommendationResource(Resource):
    # @jwt_required()
    @soil_measurements_ns.doc(params={
        'latitude': 'Latitude of the location',
        'longitude': 'Longitude of the location',
        'property_name': 'The soil property to query (e.g., "ph","bulk_density")',
        'value': 'The value of the property is measured (e.g., "6.5")'
    })
    def get(self):
        lat = request.args.get('latitude', type=float)
        lon = request.args.get('longitude', type=float)
        property_name = request.args.get('property_name', type=str)
        value = request.args.get('value', type=float)
        # auth_header = request.headers.get('Authorization')

        if not lat or not lon or not property_name or not value:
            return {'message': 'Missing required parameters'}, 400

        result = get_recommendation(property_name, value)
        return result, 200
