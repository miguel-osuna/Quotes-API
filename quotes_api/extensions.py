""" Extensions registry

All extensions here are used as singletons and 
initialized in application factory
"""

from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_apispec.extension import FlaskApiSpec
from passlib.context import CryptContext

odm = MongoEngine()
jwt = JWTManager()
ma = Marshmallow()
docs = FlaskApiSpec()
pwd_context = CryptContext(schemes=["sha256_crypt"])  # , deprecated="auto")
