#!/usr/bin/env python3
"""
invasive_plants.py - Module for handling invasive plant-related operations.
------------------------------------------------------
This module defines the API endpoints for managing invasive plants in the TreeMatch application.
It includes endpoints for retrieving, creating, updating, and deleting invasive plant records.
"""
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required
from flask import request
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from models.invasive_plants_model import InvasivePlant

invasive_plants_ns = Namespace(
    'invasive_plants', description='A namespace for Invasive Plant related operations')

# InvasivePlant model serializer
invasive_plant_model = invasive_plants_ns.model(
    'InvasivePlant', {
        'id': fields.Integer,
        'scientific_name': fields.String,
        'common_name': fields.String,
        'category': fields.String
    })


@invasive_plants_ns.route('/invasive_plants')
class InvasivePlantsResource(Resource):
    """
    InvasivePlantsResource class for handling the invasive_plants endpoint.
    It is part of the TreeMatch application API.
    """

    @invasive_plants_ns.marshal_with(invasive_plant_model, as_list=True)
    def get(self):
        """
        GET method for the InvasivePlants resource.
        Returns:
            A JSON response with a list of invasive plants.
        """
        invasive_plants = InvasivePlant.query.all()
        return invasive_plants

    @invasive_plants_ns.expect(invasive_plant_model)
    # @jwt_required()
    def post(self):
        """
        POST method for the InvasivePlants resource.
        Returns:
            A JSON response with the newly created invasive plant or an error message.
        """
        data = request.get_json()

        # Check if the required fields are present in the request
        if not data or 'scientific_name' not in data or 'common_name' not in data or 'category' not in data:
            return {'message': 'Invalid input, missing scientific_name, common_name, or category'}, 400

        new_invasive_plant = InvasivePlant(
            scientific_name=data.get('scientific_name'),
            common_name=data.get('common_name'),
            category=data.get('category')
        )

        new_invasive_plant.save()

        return invasive_plants_ns.marshal(new_invasive_plant, invasive_plant_model), 201


@invasive_plants_ns.route('/<int:id>')
class InvasivePlantResource(Resource):
    """
    InvasivePlantResource class for handling the invasive_plant endpoint.
    It is part of the TreeMatch application API.
    """

    @invasive_plants_ns.marshal_with(invasive_plant_model)
    def get(self, id):
        """
        GET method for the InvasivePlant resource.
        Returns:
            A JSON response with the invasive plant with the specified ID.
        """
        invasive_plant = InvasivePlant.query.get_or_404(id)
        return invasive_plant

    # @invasive_plants_ns.expect(invasive_plant_model)
    @invasive_plants_ns.marshal_with(invasive_plant_model)
    # @jwt_required()
    def put(self, id):
        """
        PUT method for the InvasivePlant resource.
        Returns:
            A JSON response with the updated invasive plant.
        """
        invasive_plant_to_update = InvasivePlant.query.get_or_404(id)
        data = request.get_json()
        invasive_plant_to_update.update(
            scientific_name=data.get('scientific_name'),
            common_name=data.get('common_name'),
            category=data.get('category')
        )
        return invasive_plant_to_update

    # @jwt_required()
    def delete(self, id):
        """
        DELETE method for the InvasivePlant resource.
        Returns:
            A JSON response with a message indicating the invasive plant was deleted.
        """
        invasive_plant_to_delete = InvasivePlant.query.get_or_404(id)
        invasive_plant_to_delete.delete()
        return {"message": f"Invasive Plant {invasive_plant_to_delete.common_name} deleted successfully"}, 200


@invasive_plants_ns.route('/search')
class InvasivePlantSearch(Resource):
    """
    InvasivePlantSearch class for handling the invasive_plants/search endpoint.
    It is part of the TreeMatch application API.
    """
    @invasive_plants_ns.doc(params={
        'invasive_plant_name': 'Name of the invasive plant (common or scientific) you seraching for',
        'page': 'Page number',
        'per_page': 'Number of items per page'
    })
    # @invasive_plants_ns.marshal_with(invasive_plant_model, as_list=True)
    @jwt_required()
    def get(self):
        """
        GET method to search for invasive plants by scientific name or common name.
        Returns:
            A JSON response with the list of matching invasive plants.
        """
        try:
            invasive_name = request.args.get('invasive_plant_name')
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)

            query = InvasivePlant.query
            if invasive_name:
                query = query.filter(
                    or_(
                        InvasivePlant.scientific_name.ilike(
                            f'%{invasive_name}%'),
                        InvasivePlant.common_name.ilike(f'%{invasive_name}%')
                    )
                )

            pagination = query.paginate(
                page=page, per_page=per_page, error_out=False)
            results = [plant.to_dict() for plant in pagination.items]

            return {
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': pagination.page,
                'per_page': pagination.per_page,
                'results': results
            }

        except SQLAlchemyError as e:
            return {'message': 'An error occurred while querying the database.', 'error': str(e)}, 500
        # exceptions that are not SQLAlchemy-related.
        except Exception as e:
            return {'message': 'An unexpected error occurred.', 'error': str(e)}, 500
