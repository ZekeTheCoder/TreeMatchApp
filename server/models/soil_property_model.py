#!/usr/bin/env python3
"""soil_properties_models.py - Module for defining the soil properties database model.
------------------------------------------------------
This module defines the Soil Properties classes for the TreeMatchApp server.
"""
from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from exts import db


# SoilLocation model
class SoilLocation(db.Model):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # Relationship to soil measurements
    measurements = relationship('SoilMeasurement', back_populates='location')

    def __repr__(self):
        return f"<SoilLocation(id={self.id}, name={self.name}, latitude={self.latitude}, longitude='{self.longitude}')>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()


# SoilProperty model
class SoilProperty(db.Model):
    __tablename__ = 'soil_properties'

    id = Column(Integer, primary_key=True)
    property_name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    theme = Column(String(255), nullable=False)
    unit = Column(String(50), nullable=False)
    uncertainty = Column(Boolean, nullable=False)
    value_type = Column(String(50), nullable=False)

    # Relationship to soil measurements
    measurements = relationship(
        'SoilMeasurement', back_populates='soil_property')

    def __repr__(self):
        return f"<SoilProperty(id={self.id}, property_name='{self.property_name}', description='{self.description}', theme='{self.theme}', unit='{self.unit}', uncertainty={self.uncertainty}, value_type='{self.value_type}')>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()


# SoilMeasurement model
class SoilMeasurement(db.Model):
    __tablename__ = 'soil_measurements'

    id = Column(Integer, primary_key=True)
    value = Column(Float, nullable=False)
    depth = Column(String(10), nullable=False)
    uncertainty_50 = Column(String(255), nullable=True)
    uncertainty_68 = Column(String(255), nullable=True)
    uncertainty_90 = Column(String(255), nullable=True)
    # Foreign Keys
    property_id = Column(Integer, ForeignKey('soil_properties.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))

    # Relationships
    soil_property = relationship('SoilProperty', back_populates='measurements')
    location = relationship('SoilLocation', back_populates='measurements')

    def __repr__(self):
        return f"<SoilMeasurement(id={self.id}, property_id={self.property_id}, value={self.value}, depth='{self.depth}', uncertainty_50='{self.uncertainty_50}', uncertainty_68='{self.uncertainty_68}', uncertainty_90='{self.uncertainty_90}')>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
