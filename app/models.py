from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from app import db, exceptions, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

import bleach
from markdown import markdown

class StaticContent(db.Model):
    __tablename__ = 'static_content'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), unique=True)
    text = db.Column(db.Text())

    @staticmethod
    def on_changed_text(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.text = bleach.linkify(bleach.clean(
            markdown(value, output_format="html"),
            tags=allowed_tags, strip=True))

    def __repr__(self):
        return str(self.id)

db.event.listen(StaticContent.text, 'set', StaticContent.on_changed_text)

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

class Morph(db.Model):
    __tablename__ = 'morphs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16), index=True, nullable=False, unique=True)
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

    @staticmethod
    def from_json(json_post):
        body = json_post.get("body")
        if not body or body == "":
            raise ValidationError("Post doesn't have a body")
        return Gloss(body=body)

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

    glosses = db.relationship("Gloss", backref="term", cascade="all, delete-orphan", lazy=True)
    literal_gloss = db.Column(db.String(256), index=True)

    concept = db.Column(db.String(512), nullable=False, index=True)

    language = db.relationship("Language", lazy=True)
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'), nullable=False)

    domain = db.relationship("Domain", lazy=True)
    domain_id = db.Column(db.Integer, db.ForeignKey("domains.id"))

    last_edited_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    last_edited_by = db.relationship("User", foreign_keys=[last_edited_by_id])

    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_by = db.relationship("User", foreign_keys=[created_by_id])

    last_edited_on = db.Column(db.DateTime(), default=datetime.utcnow)

    comment = db.Column(db.String())

    def to_json(self):
        blob = {
            "id": self.id,
            "orthography": self.orthography,
            "stem_form": self.stem_form,
            "ipa": self.ipa,
            "morph_id": self.morph_id,
            "concept": self.concept,
            "language_id": self.language_id,
            "domain_id": self.domain_id
        }
        return blob

    @staticmethod
    def from_json(json_post):
        body = json_post.get("body")
        if not body or body == "":
            raise ValidationError("Post doesn't have a body")
        return Term(body=body)

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
    invited_at = db.Column(db.DateTime(), default=datetime.utcnow)

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

    def formatted(self):
        if not self.first_name and not self.last_name:
            return self.email
        return "{} {}".format(self.first_name, self.last_name)

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

    def can_edit(self, result):
        if self.is_admin:
            return True
        if not result.created_by:
            return False
        return self.id == result.created_by.id
