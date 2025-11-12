from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize database instance
db = SQLAlchemy()

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    CORS(app)  # Enable CORS for frontend requests

    # Database configuration (using SQLite for simplicity)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database with the app
    db.init_app(app)

    # Import and register routes (blueprints)
    from app.routes.comments import comments_bp
    app.register_blueprint(comments_bp)

    # Create database tables (if not already created)
    with app.app_context():
        db.create_all()

    return app
