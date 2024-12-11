from flask import Flask
from flask_cors import CORS
from app.routes.graphql import graphql_blueprint
from app.database import engine, Base


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Register blueprints
    app.register_blueprint(graphql_blueprint)

    return app