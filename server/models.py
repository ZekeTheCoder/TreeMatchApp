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
