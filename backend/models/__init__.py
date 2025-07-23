# models/__init__.py

"""
Initialize the database models for the AI Insights Blog API.

This module:
- Sets up SQLAlchemy instance
- Defines base model class
- Imports all model classes
- Configures model relationships
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Define naming convention for constraints
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# Initialize SQLAlchemy with custom metadata
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))

class BaseModel(db.Model):
    """Base model class with common functionality"""
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def save(self):
        """Save the current instance to the database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the current instance from the database"""
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        """Update the current instance with provided attributes"""
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

# Import all models to ensure they're registered with SQLAlchemy
from .article import Article
from .article_view import ArticleView
from .author import Author
from .category import Category
from .newsletter_subscriber import NewsletterSubscriber
from .tag import Tag

__all__ = [
    'Article',
    'ArticleView',
    'Author',
    'BaseModel',
    'Category',
    'NewsletterSubscriber',
    'Tag',
    'db'
]
