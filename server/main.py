#!/usr/bin/env python3
"""
main.py
--------
This module initializes and configures the Flask application for the TreeMatchApp server. 
It sets up CORS, RESTful API routes, and configures the application
using the development configuration.
"""
from flask import Flask, jsonify
from flask_cors import CORS
from flask_restx import Api, Resource
from config import DevConfig

app = Flask(__name__)
CORS(app)
api = Api(app, doc='/docs')
app.config.from_object('config.DevConfig')


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return jsonify('Hello, Welcome to TreeMatch!')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
