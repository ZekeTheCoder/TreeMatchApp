#!/usr/bin/env python3
""" invasive_plants_models.py - Module for defining the invasive plants database model.
------------------------------------------------------
This module defines the Invasive Plants classes for the TreeMatchApp server.
"""
# Ignore Pylint no-member errors for db.session
# pylint: disable=E1101
import csv
from flask import current_app as app
from exts import db


# Invasive plant model
class InvasivePlant(db.Model):
    """
    class Plant:
        id: int primary key
        common_name: str
        scientific_name: str
        category: str (text)
    """

    __tablename__ = 'invasive_plants'

    id = db.Column(db.Integer, primary_key=True)
    common_name = db.Column(db.String(255), nullable=False)
    scientific_name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    # notes = db.Column(db.String(255))
    # additional_conditions = db.Column(db.String(255))

    def __repr__(self):
        """string representation of the InvasivePlant instance."""
        return (f"< InvasivePlant(id={self.id}, scientific_name='{self.scientific_name}', "
                f"common_name='{self.common_name}', category='{self.category}') >")

    def to_dict(self):
        """dictionary representation of invasive plant model instance."""
        return {
            'id': self.id,
            'common_name': self.common_name,
            'scientific_name': self.scientific_name,
            'category': self.category,
        }

    def save(self):
        """Saves current instance to database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """delete current instance from database"""
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        """update current instance from database"""
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    @staticmethod
    def get_by_id(plant_id):
        """ retrieve an InvasivePlant instance by its ID. """
        return InvasivePlant.query.get(plant_id)


def import_csv_to_db(csv_file_path):
    """
    function to import from csv contents to store in db
    """
    with app.app_context():
        # Create the database and the tables
        db.create_all()

        # Open and read the CSV file
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='|')
            for row in reader:
                # Check if the record already exists
                existing_plant = InvasivePlant.query.get(int(row['id']))
                if existing_plant:
                    print(f"Skipping duplicate entry with id: {row['id']}")
                    continue
                # Create a new InvasivePlant object
                invasive_plant = InvasivePlant(
                    id=int(row['id']),
                    scientific_name=row['scientific_name'],
                    common_name=row['common_name'],
                    category=row['category'],
                    # notes=row['notes'],
                    # additional_conditions=row['additional_conditions']
                )
                # Add the Plant object to the session
                db.session.add(invasive_plant)

            # Commit the session to save the changes
            db.session.commit()

            # # Verify that the records have been added
            # for row in reader:
            #     added_plant = InvasivePlant.query.get(int(row['id']))
            #     if added_plant:
            #         print(f"Successfully added entry with id: {row['id']}")
            #     else:
            #         print(f"Failed to add entry with id: {row['id']}")

            # Verify that the records have been added
            added_plants = InvasivePlant.query.all()
            for plant in added_plants:
                print(
                    f"Successfully added entry with id: {plant.id}, "
                    f"scientific_name: {plant.scientific_name}, "
                    f"common_name: {plant.common_name}, "
                    f"category: {plant.category}"
                )


# if __name__ == '__main__':
#     import_csv_to_db('plants.csv')
