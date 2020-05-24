# Docs: https://python-gino.org/docs/en/master/how-to/schema.html#gino-orm
from backend.db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    hashed_password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return self.email


class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(None, db.ForeignKey('users.id'))
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return self.name
