from flask import Flask
from flask_cors import CORS
from .models import db

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # ✅ Make sure this import matches your routes file
    from .routes import comments_bp
    app.register_blueprint(comments_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

    return app

