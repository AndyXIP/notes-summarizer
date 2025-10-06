import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig

db = SQLAlchemy()

def create_app(test_config=None):
    # Create and configure the Flask app
    app = Flask(__name__, instance_relative_config=True)
    
    # Load default development config
    app.config.from_object(DevelopmentConfig)

    # Override config for testing if provided
    if test_config:
        app.config.from_mapping(test_config)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Initialize database
    db.init_app(app)

    # Import and register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
