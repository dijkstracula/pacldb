from datetime import datetime
from flask_user import UserMixin
from app import db

class Domain(db.Model):
    __tablename__ = 'domains'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True)
    desc = db.Column(db.String(256), unique=True)

    def __repr__(self):
        return str(self.id)

class Language(db.Model):
    __tablename__ = 'languages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True)
    geocode = db.Column(db.String(8), unique=True)

    def __repr__(self):
        return str(self.id)

class Concept(db.Model):
    __tablename__ = 'concepts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False, index=True)

    domain = db.relationship("Domain", lazy=True)
    domain_id = db.Column(db.Integer, db.ForeignKey("domains.id"))

    def __repr__(self):
        return str(self.id)

class Morph(db.Model):
    __tablename__ = 'morphs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16), index=True, nullable=False)
    desc = db.Column(db.String(256))

    def __repr__(self):
        return str(self.id)

class Gloss(db.Model):
    __tablename__ = 'glosses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gloss = db.Column(db.String(256), nullable=False)
    source = db.Column(db.String(256), nullable=False, index=True)
    page = db.Column(db.Integer)

    term_id = db.Column(db.Integer, db.ForeignKey('terms.id'), nullable=False)

    def __repr__(self):
        return str(self.id)

class Term(db.Model):
    __tablename__ = 'terms'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orthography = db.Column(db.String(128), nullable=False, index=True, unique=True)
    stem_form = db.Column(db.String(128), nullable=False, index=True)
    ipa = db.Column(db.String(128), nullable=False, index=True)

    morph = db.relationship("Morph", lazy=True)
    morph_id = db.Column(db.Integer, db.ForeignKey("morphs.id"))

    glosses = db.relationship("Gloss", backref="term", lazy=True)

    concept = db.relationship("Concept", lazy=True)
    concept_id = db.Column(db.Integer, db.ForeignKey('concepts.id'), nullable=False)

    language = db.relationship("Language", lazy=True)
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'), nullable=False)

    def __repr__(self):
        return str(self.id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    name = db.Column(db.String(256), nullable=False, index=True, server_default='')
    email = db.Column(db.String(255), nullable=False, index=True, unique=True)
    email_confirmed_at = db.Column(db.DateTime(), default=datetime.utcnow)
    password_hash = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return str(self.id)
