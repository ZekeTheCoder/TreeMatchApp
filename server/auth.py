#!/usr/bin/env python3
""" 
auth.py - Module for handling user authentication.
------------------------------------------------------
This module defines the authentication resources for the TreeMatchApp server.
It includes the SignUp, Login, and RefreshResource classes for handling user
signup, login, and token refresh endpoints.
"""
from flask_jwt_extended import JWTManager
from flask_restx import Resource, Namespace, fields
from flask import request, jsonify, make_response
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)
from werkzeug.security import generate_password_hash  # , check_password_hash
from models import User

# Define the blacklist set to store token JTI values
blacklist = set()


auth_ns = Namespace(
    "auth", description="A namespace for Authentication related operations")

# signup_model serializer
signup_model = auth_ns.model(
    "SignUp",
    {
        "username": fields.String(),
        "email": fields.String(),
        "password": fields.String(),
    },
)


@auth_ns.route('/signup')
class SignUp(Resource):
    """
    SignUp Resource class for handling user signup endpoint.
    """

    @auth_ns.expect(signup_model)
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
login_model = auth_ns.model(
    "Login", {
        "username": fields.String(),
        "password": fields.String()
    })


@auth_ns.route('/login')
class Login(Resource):
    """
    Login Resource class for handling user login endpoint.
    """

    @auth_ns.expect(login_model)
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


@auth_ns.route("/refresh")
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


@auth_ns.route('/logout')
class Logout(Resource):
    """Logout Resource class for handling user logout."""
    @jwt_required()
    def post(self):
        """ POST method for logging out the user by revoking their JWT.
        Returns:
            A JSON response confirming logout.
        """
        # Log request cookies or session info
        # print('Request cookies:', request.cookies)
        jti = get_jwt()["jti"]  # JTI is the unique identifier for a JWT
        print(f'unique identifier for a JWT: {jti}')
        blacklist.add(jti)  # Add the JTI of the token to the blacklist
        print(f'Blacklisted JWT: {blacklist}')
        return {"message": "Successfully logged out"}, 200


# Ensure you handle the blacklist check when validating tokens

# jwt = JWTManager()


# @jwt.token_in_blocklist_loader
# def check_if_token_is_blacklisted(jwt_header, jwt_payload):
#     jti = jwt_payload["jti"]
#     return jti in blacklist
