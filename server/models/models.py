#!/usr/bin/env python3
""" models.py - Module for defining the database model.
------------------------------------------------------
This module defines the Plant and User classes for the TreeMatchApp server.
The Plant class represents a plant object with title and description attributes.
The User class represents a user object with username, email, and password attributes.
"""
# Ignore Pylint no-member errors for db.session
# pylint: disable=E1101
from werkzeug.security import check_password_hash
from sqlalchemy import Column, String, Integer, Text
from exts import db

# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy()

# plant model


class Plant(db.Model):
    """
    class Plant:
        id: int primary key
        title: str
        description: str (text)
    """

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    def __repr__(self):
        """string representation"""
        return f"<Plant {self.title} >"

    def save(self):
        """save in database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """delete from database"""
        db.session.delete(self)
        db.session.commit()

    def update(self, title, description):
        """update from database"""
        self.title = title
        self.description = description
        db.session.commit()


# user model
class User(db.Model):
    """
    class User:
        id:integer
        username:string
        email:string
        password:string
    """

    id = Column(Integer, primary_key=True)
    username = Column(String(25), nullable=False, unique=True)
    email = Column(String(80), nullable=False)
    password = Column(Text(), nullable=False)

    def __repr__(self):
        """
        returns string rep of user object
        """
        return f"<User {self.username}>"

    def save(self):
        """
        save user object in database
        """
        db.session.add(self)
        db.session.commit()

    def check_password(self, password):
        """Check if the provided password matches the stored hashed password."""
        return check_password_hash(self.password, password)
