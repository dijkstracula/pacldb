from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class StaticContent(db.Model):
    __tablename__ = 'static_content'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), unique=True)
    text = db.Column(db.Text())

    def __repr__(self):
        return str(self.id)

class Domain(db.Model):
    __tablename__ = 'domains'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), unique=True)
    description = db.Column(db.String(512), unique=True)

    def __repr__(self):
        return str(self.id)

class Language(db.Model):
    __tablename__ = 'languages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), unique=True)
    geocode = db.Column(db.String(8), unique=True)

    def __repr__(self):
        return str(self.id)

class Concept(db.Model):
    __tablename__ = 'concepts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(512), nullable=False, index=True)

    domain = db.relationship("Domain", lazy=True)
    domain_id = db.Column(db.Integer, db.ForeignKey("domains.id"))

    def __repr__(self):
        return str(self.id)

class Morph(db.Model):
    __tablename__ = 'morphs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16), index=True, nullable=False)
    description = db.Column(db.String(512))

    def __repr__(self):
        return str(self.id)

class Gloss(db.Model):
    __tablename__ = 'glosses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gloss = db.Column(db.String(512), nullable=False, index=True)
    source = db.Column(db.String(512), nullable=False, index=True)
    page = db.Column(db.Integer)

    term_id = db.Column(db.Integer, db.ForeignKey('terms.id'), nullable=False, index=True)

    def __repr__(self):
        return str(self.id)

class Term(db.Model):
    __tablename__ = 'terms'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orthography = db.Column(db.String(256), nullable=False, index=True, unique=True)
    stem_form = db.Column(db.String(256), nullable=False, index=True)
    ipa = db.Column(db.String(256), nullable=False, index=True)

    morph = db.relationship("Morph", lazy=True)
    morph_id = db.Column(db.Integer, db.ForeignKey("morphs.id"))

    glosses = db.relationship("Gloss", backref="term", lazy=True)
    literal_gloss = db.Column(db.String(256), index=True)

    concept = db.relationship("Concept", lazy=True)
    concept_id = db.Column(db.Integer, db.ForeignKey('concepts.id'), nullable=False)

    language = db.relationship("Language", lazy=True)
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'), nullable=False)

    def __repr__(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Invitation(db.Model):
    __tablename__ = 'invitations'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False, index=True, unique=True)
    should_be_admin = db.Column(db.Boolean, default=False)

    def generate_secure_token(self, expiration=3600 * 24 * 7):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False, index=True, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return str(self.id)
