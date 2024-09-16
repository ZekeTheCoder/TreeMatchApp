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
