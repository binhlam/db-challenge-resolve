# -*- coding: utf-8 -*-
from flask import Flask, Blueprint
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api
from flask_cors import CORS
from .api.generator import Generatorequest

# Api blueprint
api_bp = Blueprint('api', __name__)
api = Api(api_bp)


def register_services(app):
    # Define endpoints
    api.add_resource(Generatorequest, '/v1/xml/generate')

    # # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')


def init_app():
    app = Flask("db-challenge", static_url_path="")
    # CORS(app, resources={r"/api/*": {"origins": "*"}})

    auth = HTTPBasicAuth()
    register_services(app)

    return app


flask_app = init_app()
