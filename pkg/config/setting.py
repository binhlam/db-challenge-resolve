# -*- coding: utf-8 -*-
from .default import __DEFAULT__
import os

# file path
base_path = os.path.dirname(__file__)
app_api_path = '{}/{}'.format(base_path, 'db-challenge-resolve/app/__init__.py')
FLASK_APP = os.environ.get('FLASK_APP', app_api_path)
FLASK_DEBUG = os.environ.get('FLASK_DEBUG', __DEFAULT__['FLASK_DEBUG'])
DB_HOST = os.environ.get('DB_HOST', __DEFAULT__['DB_HOST'])
DB_NAME = os.environ.get('DB_NAME', __DEFAULT__['DB_NAME'])
DB_USER = os.environ.get('DB_USER', __DEFAULT__['DB_USER'])
DB_PORT = int(os.environ.get('DB_PORT', __DEFAULT__['DB_PORT']))
DB_PASSWORD = os.environ.get('DB_PASSWORD', __DEFAULT__['DB_PASSWORD'])
DB_MINCONN = int(os.environ.get('DB_MINCONN', __DEFAULT__['DB_MINCONN']))
DB_MAXCONN = int(os.environ.get('DB_MAXCONN', __DEFAULT__['DB_MAXCONN']))

# SET ENV VAR FOR LATER ACCESS
__ENV_VARIABLES__ = {
    'FLASK_APP': FLASK_APP,
    'FLASK_DEBUG': FLASK_DEBUG,
    'DB_HOST': DB_HOST,
    'DB_NAME': DB_NAME,
    'DB_PASSWORD': DB_PASSWORD,
    'DB_USER': DB_USER,
    'DB_MAXCONN': DB_MAXCONN,
    'DB_MINCONN': DB_MINCONN,
    'DB_PORT': DB_PORT,
}
