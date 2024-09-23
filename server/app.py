#!/usr/bin/env python3
"""
app.py - This module initializes and runs the Flask application.
-----------------------------------------------------------------------------
It imports the `create_app` function from the `main` module and configuration
classes from the `config` module.
The application is created using the `DevConfig` configuration by default,
but can be switched to use `ProdConfig` or `TestConfig'.

To run the application, execute this script directly.
"""
from main import create_app
# from import_functions import import_csv_to_db, import_soil_properties_csv_to_db
from exts import db
from config import DevConfig  # , ProdConfig, TestConfig
from models.soil_property_model import SoilMeasurement, SoilProperty, SoilLocation
from sqlalchemy.orm import sessionmaker
from utils import get_simulated_response

app = create_app(DevConfig)
# app = create_app(ProdConfig)
# app = create_app(TestConfig)


# def run_query():
#     location_name = 'Johannesburg'
#     property_name = 'Aluminium, extractable'

#     Session = sessionmaker(bind=db.engine)
#     session = Session()

#     # Print debug information
#     print(
#         f"Querying for location: {location_name} and property: {property_name}")

#     result = session.query(SoilMeasurement).join(SoilProperty).join(SoilLocation).filter(
#         SoilLocation.name == location_name,
#         SoilProperty.property_name == property_name
#     ).all()

#     if not result:
#         print("No results found.")
#     else:
#         for measurement in result:
#             print(
#                 f"Value: {measurement.value} {measurement.soil_property.unit}")

#     session.close()


if __name__ == "__main__":
    with app.app_context():
        # db.create_all()
        # import_csv_to_db('invasive1.csv')
        # import_soil_properties_csv_to_db('soil_properties.csv')
        # run_query()
        # app.run(debug=True, port=5000)
        # get_simulated_response('response')
