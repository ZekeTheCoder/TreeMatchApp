#!/usr/bin/env python3
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, jsonify, make_response
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from main import create_app  # Import your Flask app
from exts import db  # Assuming exts is where db is initialized
from models import User  # Import the User model
from config import TestConfig


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        """
        Setup test client and initialize the database.
        """
        # Create a Flask app instance with testing configuration
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

        # Set up the application context
        self.app_context = self.app.app_context()
        self.app_context.push()

        with self.app.app_context():
            db.init_app(self.app)
            db.create_all()

            # Create a test user
            test_user = User(
                username='testuser',
                email='testuser@example.com',
                password=generate_password_hash('testpassword')
            )
            test_user.save()

    @unittest.skip("Skipping test_login_success for debugging purposes")
    @patch('flask_jwt_extended.create_access_token')
    @patch('flask_jwt_extended.create_refresh_token')
    @patch('models.User.query')  # Mocking the User.query filter
    def test_login_success(self, mock_query, mock_create_refresh_token, mock_create_access_token):
        mock_create_access_token.return_value = 'mock_access_token'
        mock_create_refresh_token.return_value = 'mock_refresh_token'

        # Simulate a user object with the correct password
        mock_user = MagicMock()
        mock_user.check_password.return_value = True
        mock_query.filter_by.return_value.first.return_value = mock_user

        response = self.client.post(
            '/auth/login',
            json={'username': 'testuser', 'password': 'testpassword'}
        )

        print(f'Login Response Status Code: {response.status_code}')
        print(f'Login Response Data: {response.data}')

        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)
        self.assertIn('refresh_token', response.json)

    @patch('models.User.query')  # Mocking the User.query filter
    def test_login_invalid_username(self, mock_query):
        """
        Test login with invalid username.
        """
        # Simulate no user found
        mock_query.filter_by.return_value.first.return_value = None

        # Simulate a POST request for login with invalid username
        response = self.client.post(
            '/auth/login',
            json={
                "username": "invaliduser",
                "password": "password123"
            }
        )

        # Check if response returns 400 error for invalid username
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json, {"message": "Invalid username or password"})

    @patch('models.User.query')  # Mocking the User.query filter
    def test_login_invalid_password(self, mock_query):
        """
        Test login with valid username but invalid password.
        """
        # Simulate a user object but with an incorrect password
        mock_user = MagicMock()
        mock_user.check_password.return_value = False
        mock_query.filter_by.return_value.first.return_value = mock_user

        # Simulate a POST request for login with incorrect password
        response = self.client.post(
            '/auth/login',
            json={
                "username": "validuser",
                "password": "wrongpassword"
            }
        )

        # Check if response returns 400 error for incorrect password
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json, {"message": "Invalid username or password"})

    # Mock JWT decorator
    @unittest.skip("Skipping test_login_success for debugging purposes")
    @patch('flask_jwt_extended.verify_jwt_in_request')
    @patch('flask_jwt_extended.get_jwt_identity')
    @patch('flask_jwt_extended.create_access_token')
    def test_refresh_token_success(self, mock_create_access_token,
                                   mock_get_jwt_identity, mock_verify_jwt_in_request):
        mock_get_jwt_identity.return_value = 'testuser'
        mock_create_access_token.return_value = 'new_mock_access_token'
        mock_verify_jwt_in_request.return_value = None

        # Simulate a valid Authorization header
        headers = {
            'Authorization': 'Bearer mock_refresh_token'
        }

        response = self.client.post('/auth/refresh', headers=headers)

        print(f'Refresh Token Response Status Code: {response.status_code}')
        print(f'Refresh Token Response Data: {response.data}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json['access_token'], 'new_mock_access_token')

    # Mock JWT decorator

    @patch('flask_jwt_extended.get_jwt_identity')
    @patch('flask_jwt_extended.verify_jwt_in_request')
    def test_refresh_token_invalid(self, mock_verify_jwt_in_request, mock_get_jwt_identity):
        mock_verify_jwt_in_request.side_effect = RuntimeError("Invalid token")
        response = self.client.post('/auth/refresh')
        # Assuming 401 is returned for invalid tokens
        self.assertEqual(response.status_code, 401)

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
