from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os


# Initialize SQLAlchemy, Migrate, and load environment variables from .env file
db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


# Function to create the Flask application
# test_config parameter set to None by default (can be changed to True for testing)


def create_app(test_config=None):
    # Create Flask application instance
    app = Flask(__name__)

    # # Enable Cross-Origin Resource Sharing (CORS) for
    # # handling requests from different origins
    CORS(app)

    # Disable SQLAlchemy modification tracking to improve performance
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Set up database URI based on environment (for testing or production)
    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI"
        )
    else:
        # If test configuration is provided, enable testing mode
        # and use test database URI
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI"
        )

    # Initialize SQLAlchemy and Migrate with the Flask application
    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints for different parts of the application
    # blueprint allows definition of application routes in a modular way
    # (better organization, reusability, maintainability)

    # blueprints define their own routes such as "/students"
    from app.student_routes import student_bp

    app.register_blueprint(student_bp)

    # Return the Flask application instance
    return app
