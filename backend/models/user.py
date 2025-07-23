# models/user.py
import re
from datetime import datetime

from flask_sqlalchemy import db
from marshmallow import Schema, fields, validate
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    """
    User model representing blog authors and administrators.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.Text)
    profile_image = db.Column(db.String(255))
    role = db.Column(db.String(20), default='author')  # author, admin
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    articles = db.relationship('Article', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)

    def __init__(self, username, email, password, first_name, last_name, **kwargs):
        self.username = username
        self.email = email
        self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name
        for key, value in kwargs.items():
            setattr(self, key, value)

    def set_password(self, password):
        """Create hashed password."""
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r'[0-9]', password):
            raise ValueError("Password must contain at least one number")
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password_hash, password)

    def get_full_name(self):
        """Return the full name of the user."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f'<User {self.username}>'

class UserSchema(Schema):
    """
    Marshmallow schema for User model serialization/deserialization.
    """
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, required=True, validate=validate.Length(min=8))
    first_name = fields.Str(required=True, validate=validate.Length(min=2, max=50))
    last_name = fields.Str(required=True, validate=validate.Length(min=2, max=50))
    bio = fields.Str()
    profile_image = fields.Str()
    role = fields.Str()
    is_active = fields.Bool()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    class Meta:
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'bio',
                  'profile_image', 'role', 'is_active', 'created_at', 'updated_at')
        ordered = True

# Export the models
__all__ = ['User', 'UserSchema']
