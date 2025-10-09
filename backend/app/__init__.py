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
    os.makedirs(app.instance_path, exist_ok=True)

    # Initialize database
    db.init_app(app)

    # Enable CORS for frontend access
    try:
        from flask_cors import CORS
        CORS(app)
    except ImportError:
        pass

    # Import and register blueprints
    from .routes import main
    app.register_blueprint(main)

    # Error for file size limit
    @app.errorhandler(413)
    def request_entity_too_large(error):
        return "File is too large. Max size is {} MB.".format(app.config['MAX_CONTENT_LENGTH'] // (1024*1024)), 413

    return app