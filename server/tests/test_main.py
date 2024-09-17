#!/usr/bin/env python3
import unittest
from main import create_app
from config import TestConfig
from exts import db


class APITestCase(unittest.TestCase):
    def setUp(self):
        # new Flask app instance using the TestConfig.
        self.app = create_app(TestConfig)
        # test client, allowing interaction with the app's routes without running the server.
        self.client = self.app.test_client(self)

        with self.app.app_context():
            # initializes the database with the app context.
            db.init_app(self.app)
            # creates all necessary tables (db.create_all) within the application context.
            db.create_all()

    # @unittest.skip("skip test")
    def test_welcome(self):
        """ welcome message. """
        hello_response = self.client.get("/plants/welcome")
        # debugging messages
        # print("Response status code:", hello_response.status_code)
        # print("Response data:", hello_response.data)
        json_response = hello_response.json
        status_code = hello_response.status_code

        # Test message and status code
        self.assertEqual(
            json_response, {"message": "Hello, Welcome to TreeMatch!"})
        self.assertEqual(status_code, 200)

# Test Auth Functionality
    def test_signup(self):
        """ signup/register user """
        signup_response = self.client.post(
            "/auth/signup",
            json={
                "username": "testuser",
                "email": "testuser@test.com",
                "password": "password",
            },
        )
        status_code = signup_response.status_code
        self.assertEqual(status_code, 201)

    def test_login(self):
        """ Login a user"""
        signup_response = self.client.post(
            "/auth/signup",
            json={
                "username": "testuser",
                "email": "testuser@test.com",
                "password": "password",
            },
        )

        login_response = self.client.post(
            "/auth/login", json={"username": "testuser", "password": "password"}
        )

        status_code = login_response.status_code
        # json_response = login_response.json
        # print(json_response)
        self.assertEqual(status_code, 200)
        self.assertIn('access_token', login_response.json)
        self.assertIn('refresh_token', login_response.json)

    def test_logout(self):
        """Test the logout functionality to ensure that the JWT token is blacklisted"""

        signup_response = self.client.post(
            "/auth/signup",
            json={
                "username": "testuser",
                "email": "testuser@test.com",
                "password": "password",
            },
        )

        login_response = self.client.post(
            "/auth/login", json={"username": "testuser", "password": "password"}
        )

        status_code = login_response.status_code
        access_token = login_response.json["access_token"]
        # print('status code:', status_code)
        # print('Login response:', access_token)

        # Log out
        logout_response = self.client.post(
            "/auth/logout",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        # Check the response
        self.assertEqual(logout_response.status_code, 200)
        self.assertEqual(
            logout_response.json["message"], "Successfully logged out")

    def test_refresh(self):
        """Test the /refresh endpoint to ensure it issues a new access token"""

        signup_response = self.client.post(
            "/auth/signup",
            json={
                "username": "testuser",
                "email": "testuser@test.com",
                "password": "password",
            },
        )

        # Log in to get access and refresh tokens
        login_response = self.client.post(
            "/auth/login",
            json={"username": "testuser", "password": "password"}
        )

        # print('Login response:', login_response.json)
        # Check if refresh_token is in the response
        self.assertIn('refresh_token', login_response.json,
                      'Login response does not contain refresh_token')
        refresh_token = login_response.json["refresh_token"]

        # print('refresh_token:', refresh_token)
        # Refresh the access token
        refresh_response = self.client.post(
            "/auth/refresh",
            headers={"Authorization": f"Bearer {refresh_token}"}
        )

        # print('refresh_response:', refresh_response.json)
        # Check the response
        self.assertEqual(refresh_response.status_code, 200)
        self.assertIn('access_token', refresh_response.json,
                      'Refresh response does not contain access_token')

        # Ensure the new access token is different from the old one
        new_access_token = refresh_response.json["access_token"]
        self.assertNotEqual(
            new_access_token, login_response.json["access_token"], 'The new access token should be different from the old one')


# Test Plant Functionality

    def test_get_all_plants(self):
        """Get all plants"""
        response = self.client.get("/plants/plants")
        # print(response.json)
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_create_plant(self):
        """create a new plant"""
        signup_response = self.client.post(
            "/auth/signup",
            json={
                "username": "testuser",
                "email": "testuser@test.com",
                "password": "password",
            },
        )

        login_response = self.client.post(
            "auth/login", json={"username": "testuser", "password": "password"}
        )

        access_token = login_response.json["access_token"]

        create_plant_response = self.client.post(
            "/plants/plants",
            json={"title": "Test Cookie", "description": "Test description"},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        status_code = create_plant_response.status_code
        # print(create_plant_response.json)
        self.assertEqual(status_code, 201)
        self.assertIn('title', create_plant_response.json)
        self.assertIn('description', create_plant_response.json)

    def test_create_plant_without_token(self):
        """create plant without token"""
        create_plant_response = self.client.post(
            "/plants/plants",
            json={"title": "Test Cookie", "description": "Test description"},
        )
        status_code = create_plant_response.status_code
        response_json = create_plant_response.json
        # print(response_json)
        # print(status_code)
        self.assertEqual(status_code, 401)
        self.assertEqual(response_json['msg'], 'Missing Authorization Header')

    def test_get_one_plants(self):
        """get plant by id"""
        signup_response = self.client.post(
            "/auth/signup",
            json={
                "username": "testuser",
                "email": "testuser@test.com",
                "password": "password",
            },
        )

        login_response = self.client.post(
            "auth/login", json={"username": "testuser", "password": "password"}
        )

        access_token = login_response.json["access_token"]

        create_plant_response = self.client.post(
            "/plants/plants",
            json={"title": "Test Cookie", "description": "Test description"},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        status_code = create_plant_response.status_code
        # print(create_plant_response.json)

        self.assertEqual(status_code, 201)
        self.assertIn('title', create_plant_response.json)
        self.assertIn('description', create_plant_response.json)

    def test_invalid_get_one_plant(self):
        """Invalid get plant by id"""
        id = 1
        response = self.client.get(f"/plants/plant/{id}")

        status_code = response.status_code
        print(status_code)
        self.assertEqual(status_code, 404)

    def test_update_plant(self):
        """Update plant by id"""
        signup_response = self.client.post(
            "/auth/signup",
            json={
                "username": "testuser",
                "email": "testuser@test.com",
                "password": "password",
            },
        )

        login_response = self.client.post(
            "auth/login", json={"username": "testuser", "password": "password"}
        )

        access_token = login_response.json["access_token"]

        create_plant_response = self.client.post(
            "/plants/plants",
            json={"title": "Test Cookie", "description": "Test description"},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        status_code = create_plant_response.status_code

        # id = 1
        plant_id = create_plant_response.json['id']

        update_response = self.client.put(
            f"plants/plant/{plant_id}",
            json={
                "title": "Test Cookie Updated",
                "description": "Test description updated",
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        status_code = update_response.status_code
        self.assertEqual(status_code, 200)

    def test_delete_plant(self):
        signup_response = self.client.post(
            "/auth/signup",
            json={
                "username": "testuser",
                "email": "testuser@test.com",
                "password": "password",
            },
        )

        login_response = self.client.post(
            "/auth/login", json={"username": "testuser", "password": "password"}
        )

        access_token = login_response.json["access_token"]

        create_plant_response = self.client.post(
            "/plants/plants",
            json={"title": "Test Cookie", "description": "Test description"},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        # id = 1
        plant_id = create_plant_response.json['id']
        delete_response = self.client.delete(
            f"/plants/plant/{plant_id}", headers={"Authorization": f"Bearer {access_token}"}
        )

        status_code = delete_response.status_code
        # print(delete_response.json)
        self.assertEqual(status_code, 200)

    # Runs after each test to clean up
    def tearDown(self):
        """ Removes the database session
        and drops all tables to ensure a clean environment for the next test.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


# test runner
if __name__ == "__main__":
    unittest.main()
