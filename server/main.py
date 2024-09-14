#!/usr/bin/env python3
"""
main.py
--------
This module initializes and configures the Flask application for the TreeMatchApp server.
It sets up CORS, RESTful API routes, and configures the application
using the development configuration.
"""
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from flask_migrate import Migrate
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import generate_password_hash  # , check_password_hash
from models import Plant, User
from exts import db
from config import DevConfig


app = Flask(__name__)
app.config.from_object(DevConfig)
api = Api(app, doc="/docs")
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)


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


# signup_model serializer
signup_model = api.model(
    "SignUp",
    {
        "username": fields.String(),
        "email": fields.String(),
        "password": fields.String(),
    },
)


@api.route('/signup')
class SignUp(Resource):
    """
    SignUp Resource class for handling user signup endpoint.
    """

    @api.expect(signup_model)
    def post(self):
        """
        POST method for the SignUp resource.
        Returns:
        A JSON response with the newly created user.
        """
        data = request.get_json()

        # check if user already exists, if so, return 400 error or create new user
        username = data.get('username')
        user = User.query.filter_by(username=username).first()

        if user:
            return {"message": f"User {username} already exists!"}, 400

        new_user = User(
            username=data.get('username'),
            email=data.get('email'),
            password=generate_password_hash(data.get('password'))
            # password=bcrypt.hashpw(data.get('password').encode('utf-8'),
            #                        bcrypt.gensalt())
        )
        new_user.save()
        # return new_user, 201 # returns object & need @api.marshal_with(signup_model)
        return {"message": "User created successfully!"}, 201


# login_model serializer
login_model = api.model(
    "Login", {
        "username": fields.String(),
        "password": fields.String()
    })


@api.route('/login')
class Login(Resource):
    """
    Login Resource class for handling user login endpoint.
    """

    @api.expect(login_model)
    def post(self):
        """
        POST method for the Login resource.
        Returns:
        A JSON response with the user that was logged in.
        """
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        # check if user exists and password match, if not, return 400 error or login user
        user = User.query.filter_by(username=username).first()

        if not user:
            return {"message": "Invalid username or password"}, 400

        # check if password matches
        if not user.check_password(password):
            return {"message": "Invalid username or password"}, 400

        # create JWT tokens if authentication is successful
        access_token = create_access_token(identity=user.username)
        refresh_token = create_refresh_token(identity=user.username)

        return {"access_token": access_token, "refresh_token": refresh_token}, 200


@api.route("/refresh")
class RefreshResource(Resource):
    """ RefreshResource class for handling the token refresh endpoint. """
    @jwt_required(refresh=True)
    def post(self):
        """ POST method for the Refresh resource. 
        Returns:
            A JSON response with the new access token.
        """

        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return make_response(jsonify({"access_token": new_access_token}), 200)


# plant_model serializer
plant_model = api.model(
    'Plant', {
        'id': fields.Integer,
        'title': fields.String,
        'description': fields.String
    })


@ api.route('/plants')
class PlantsResource(Resource):
    """
    Plants Resource class for handling the plants endpoint.
    It is part of the TreeMatch application API.
    """

    @ api.marshal_with(plant_model, as_list=True)  # model serializer decorator
    # @api.marshal_list_with(plant_model)
    def get(self):
        """
        GET method for the Plants resource.
        Returns:
                                A JSON response with a list of plants.
        """
        plants = Plant.query.all()
        return plants

    # validates the incoming request data according to the plant_model or 400 error.
    @api.expect(plant_model)
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
        return api.marshal(new_plant, plant_model), 201


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

    # @api.marshal_with(plant_model)
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
