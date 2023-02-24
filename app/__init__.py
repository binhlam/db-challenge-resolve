# -*- coding: utf-8 -*-
from flask import Flask, Blueprint
from flask_restful import Api
from flask_cors import CORS
from .api.generator import GeneratorRequest
from pkg.db.database import _pool
from .service.generator import GeneratorService
from .domain.repository import Repository
import logging

# Api blueprint
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Logger
logger = logging.getLogger('db-challenge')


def register_services(app):

    # Init repository
    repo = Repository(pool=_pool, logger=logger)

    # Define endpoints
    generator_service = GeneratorService(repo=repo, logger=logger)
    api.add_resource(GeneratorRequest, '/v1/xml/generate', resource_class_kwargs={'svc': generator_service})

    # # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')


def init_app():
    app = Flask("db-challenge", static_url_path="")
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    register_services(app)

    return app


flask_app = init_app()
