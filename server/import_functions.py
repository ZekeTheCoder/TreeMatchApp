#!/usr/bin/env python3
"""
import_function.py - Module for importing plant data from a CSV file into the database.
------------------------------------------------------
This module defines the import_csv_to_db function for the TreeMatchApp server.
"""
import csv
from flask import current_app as app
from exts import db
from invasive_plants_model import InvasivePlant
from soil_property_model import SoilProperty


def import_csv_to_db(csv_file_path):
    """
    function to import invasive plant data from csv contents to store in db
    """
    with app.app_context():
        # Create the database and the tables
        db.create_all()

        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='|')
        for row in reader:
            existing_plant = InvasivePlant.query.get(int(row['id']))
            if existing_plant:
                print(f"Skipping duplicate entry with id: {row['id']}")
                continue

            invasive_plant = InvasivePlant(
                id=int(row['id']),
                scientific_name=row['scientific_name'],
                common_name=row['common_name'],
                category=row['category']
            )

            db.session.add(invasive_plant)
            print(f"Entry with id: {row['id']}  added to db")

        db.session.commit()

        for row in reader:
            added_plant = InvasivePlant.query.get(int(row['id']))
            if added_plant:
                print(f"Successfully added entry with id: {row['id']}")
            else:
                print(f"Failed to add entry with id: {row['id']}")

            # # Verify that the records have been added
            # added_plants = InvasivePlant.query.all()
            # for plant in added_plants:
            #     print(
            #         f"Successfully added entry with id: {plant.id}, "
            #         f"scientific_name: {plant.scientific_name}, "
            #         f"common_name: {plant.common_name}, "
            #         f"category: {plant.category}"
            #     )


def import_soil_properties_csv_to_db(csv_file_path):
    """
    Imports soil properties data from a CSV file into the database.

    Args:
        csv_file_path (str): The path to the CSV file containing soil properties data.
    """
    # Create the database and the tables
    db.create_all()

    added_properties = []

    with open(csv_file_path, 'r', encoding='utf-8', newline='') as file:
        reader = csv.DictReader(file, delimiter='|')
        for row in reader:
            soil_property = SoilProperty(
                property_name=row['Property'],
                description=row['Description'],
                theme=row['Theme'],
                unit=row['Unit'],
                depths=row['Depths (cm)'],
                uncertainty=row['Uncertainty'].lower() == 'yes',
                value_type=row['Type']
            )
            db.session.add(soil_property)
            added_properties.append(soil_property)

    db.session.commit()

    for soil_property in added_properties:
        print(
            f"Successfully added entry with id: {soil_property.id}, "
            f"property_name: {soil_property.property_name}, "
            f"description: {soil_property.description}, "
            f"theme: {soil_property.theme}, "
            f"unit: {soil_property.unit}, "
            f"depths: {soil_property.depths}, "
            f"uncertainty: {soil_property.uncertainty}, "
            f"value_type: {soil_property.value_type}"
        )


# if __name__ == '__main__':
#     import_csv_to_db('plants.csv')
#     import_soil_properties_csv_to_db('soil_properties.csv')
