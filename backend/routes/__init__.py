"""
Routes initialization module for AI Insights Blog API.

This module initializes all API routes and blueprints for the application.
It follows RESTful conventions and organizes routes by resource type.
"""

from flask import Blueprint

from . import admin, analytics, authors, categories, feeds, newsletter, posts, tags

# Main API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Register all route blueprints
api_bp.register_blueprint(posts.bp)
api_bp.register_blueprint(authors.bp)
api_bp.register_blueprint(categories.bp)
api_bp.register_blueprint(tags.bp)
api_bp.register_blueprint(newsletter.bp)
api_bp.register_blueprint(analytics.bp)
api_bp.register_blueprint(admin.bp)
api_bp.register_blueprint(feeds.bp)

# Health check endpoint
@api_bp.route('/health')
def health_check():
    """Endpoint for health checks and monitoring."""
    return {'status': 'healthy'}, 200

def init_app(app):
    """Initialize routes with the Flask application."""
    app.register_blueprint(api_bp)

    # Register error handlers
    from .errors import register_error_handlers
    register_error_handlers(app)
