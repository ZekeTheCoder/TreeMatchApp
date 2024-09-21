#!/usr/bin/env python3
"""soil_properties_models.py - Module for defining the soil properties database model.
------------------------------------------------------
This module defines the Soil Properties classes for the TreeMatchApp server.
"""
from sqlalchemy import Column, String, Integer, Text, Float
from exts import db


# SoilProperty model
class SoilProperty(db.Model):
    """
    class SoilProperty:
        id: int primary key
        property_name: str (name of the soil property)
        unit: str (unit of measurement, e.g., g/kg, ppm)
        low_threshold: float (low threshold value)
        moderate_threshold: float (moderate threshold value)
        high_threshold: float (high threshold value)
        recommendation_low: str (recommendation when below low threshold)
        recommendation_moderate: str (recommendation when between low and high thresholds)
        recommendation_high: str (recommendation when above high threshold)
    """

    __tablename__ = 'soil_properties'

    id = Column(Integer, primary_key=True)
    property_name = Column(String(255), nullable=False)
    unit = Column(String(10), nullable=True)
    low_threshold = Column(Float, nullable=False)
    moderate_threshold = Column(Float, nullable=False)
    high_threshold = Column(Float, nullable=False)
    recommendation_low = Column(String(255), nullable=False)
    recommendation_moderate = Column(String(255), nullable=False)
    recommendation_high = Column(String(255), nullable=False)

    def __repr__(self):
        """String representation of the SoilProperty instance."""
        return (f"<SoilProperty(id={self.id}, property_name='{self.property_name}', "
                f"unit='{self.unit}')>")

    def to_dict(self):
        """Dictionary representation of the soil property model instance."""
        return {
            'id': self.id,
            'property_name': self.property_name,
            'unit': self.unit,
            'low_threshold': self.low_threshold,
            'moderate_threshold': self.moderate_threshold,
            'high_threshold': self.high_threshold,
            'recommendation_low': self.recommendation_low,
            'recommendation_moderate': self.recommendation_moderate,
            'recommendation_high': self.recommendation_high,
        }

    def save(self):
        """Saves current instance to the database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Deletes current instance from the database."""
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        """Updates current instance from the database."""
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    @staticmethod
    def get_by_id(property_id):
        """Retrieve a SoilProperty instance by its ID."""
        return SoilProperty.query.get(property_id)
