#!/usr/bin/env python3
"""
run.py - This module initializes and runs the Flask application.
-----------------------------------------------------------------------------
It imports the `create_app` function from the `main` module and configuration
classes from the `config` module.
The application is created using the `DevConfig` configuration by default,
but can be switched to use `ProdConfig` or `TestConfig'.

To run the application, execute this script directly. The application will
start on port 5000.

Usage:
  python run.py
"""
from main import create_app
from config import DevConfig  # , ProdConfig, TestConfig
from invasive_plants_model import import_csv_to_db

app = create_app(DevConfig)
# app = create_app(ProdConfig)
# app = create_app(TestConfig)

if __name__ == "__main__":
    # with app.app_context():
    #     import_csv_to_db('invasive.csv')
    app.run(debug=True, port=5000)
