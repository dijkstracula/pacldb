from datetime import datetime
from flask_user import UserMixin
from app import db

class Concept(db.Model):
    __tablename__ = 'concepts'
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(128), nullable=False, index=True, unique=True)

    # One concept has many terms
    terms = db.relationship("Term", lazy="dynamic")

    def __repr__(self):
        return '<Concept {}>'.format(self.domain)


class Gloss(db.Model):
    __tablename__ = 'glosses'
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(128), nullable=False, index=True)
    page = db.Column(db.Integer)

    def __repr__(self):
        return '<Gloss {}:{}>'.format(self.source, self.page)


class Term(db.Model):
    __tablename__ = 'terms'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(128), nullable=False, index=True, unique=True)
    morph_type = db.Column(db.String(16))
    # One term has many glosses
    glosses = db.relationship("Gloss", lazy="dynamic")

    def __repr__(self):
        return '<Term {}>'.format(self.text)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    name = db.Column(db.String(256, collation='NOCASE'), nullable=False, index=True, server_default='')
    email = db.Column(db.String(255, collation='NOCASE'), nullable=False, index=True, unique=True)
    email_confirmed_at = db.Column(db.DateTime(), default=datetime.utcnow)
    password = db.Column(db.String(255), nullable=False, server_default='')

    def __repr__(self):
        return '<User {}>'.format(self.name)
