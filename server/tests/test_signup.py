#!/usr/bin/env python3
import unittest
from flask import Flask
from unittest.mock import patch, MagicMock
from main import create_app  # Import your Flask app
from exts import db  # Assuming exts is where db is initialized
from models import User  # Import the User model
from config import TestConfig
from werkzeug.security import generate_password_hash


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        """
        Setup test client and initialize the database.
        """
        # Create a Flask app instance with testing configuration
        self.app = create_app(TestConfig)  # Use 'testing' config
        self.client = self.app.test_client()

        # Set up the application context
        self.app_context = self.app.app_context()
        self.app_context.push()

        with self.app.app_context():
            db.init_app(self.app)
            db.create_all()

    @patch('models.User.query')  # Mocking the User.query filter
    def test_signup_success(self, mock_query):
        """
        Test successful user signup.
        """
        # Simulate that no user exists
        mock_query.filter_by.return_value.first.return_value = None

        # Simulate a valid POST request
        response = self.client.post(
            '/auth/signup',
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "password123"
            }
        )

        # Check the status code and response data
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json, {"message": "User created successfully!"})

    @patch('models.User.query')  # Mocking the User.query filter
    def test_signup_user_already_exists(self, mock_query):
        """
        Test signup when the user already exists.
        """
        # Simulate an existing user being found in the database
        mock_query.filter_by.return_value.first.return_value = User(
            username="existinguser", email="existinguser@example.com"
        )

        # Simulate a POST request to the signup endpoint with an existing username
        response = self.client.post(
            '/auth/signup',
            json={
                "username": "existinguser",
                "email": "existinguser@example.com",
                "password": "password123"
            }
        )

        # Check the status code and response data
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json, {"message": "User existinguser already exists!"})

    def tearDown(self):
        """
        Tear down the database after each test.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

        # Remove the application context
        self.app_context.pop()


if __name__ == "__main__":
    unittest.main()
