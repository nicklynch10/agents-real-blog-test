
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])
cors = CORS()

def create_app(config_name=None):
    """Application factory function"""
    app = Flask(__name__)

    # Load environment variables
    load_dotenv()

    # Configure the application
    if config_name == 'testing':
        app.config.from_object('config.TestingConfig')
    elif config_name == 'production':
        app.config.from_object('config.ProductionConfig')
    else:
        app.config.from_object('config.DevelopmentConfig')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    from routes.admin import admin_bp
    from routes.authors import authors_bp
    from routes.categories import categories_bp
    from routes.newsletter import newsletter_bp
    from routes.posts import posts_bp
    from routes.search import search_bp

    app.register_blueprint(posts_bp, url_prefix='/api/posts')
    app.register_blueprint(authors_bp, url_prefix='/api/authors')
    app.register_blueprint(categories_bp, url_prefix='/api/categories')
    app.register_blueprint(search_bp, url_prefix='/api/search')
    app.register_blueprint(newsletter_bp, url_prefix='/api/newsletter')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return {'error': 'Rate limit exceeded'}, 429

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500

    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200

    # Shell context for Flask CLI
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'Post': models.Post,
            'Author': models.Author,
            'Category': models.Category,
            'Tag': models.Tag
        }

    return app

# Initialize the app
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
