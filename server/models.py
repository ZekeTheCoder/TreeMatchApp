from werkzeug.security import check_password_hash
from exts import db


class Plant(db.Model):
    """
    class Plant:
        id: int primary key
        title: str
        description: str (text)
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

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

"""
class User:
    id:integer
    username:string
    email:string
    password:string
"""


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.Text(), nullable=False)

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
