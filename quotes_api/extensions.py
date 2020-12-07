""" Extensions registry

All extensions here are used as singletons and 
initialized in application factory
"""

from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from passlib.context import CryptContext

from quotes_api.common import APISpecExt

odm = MongoEngine()
jwt = JWTManager()
ma = Marshmallow()
apispec = APISpecExt()
pwd_context = CryptContext(schemes=["sha256_crypt"])  # , deprecated="auto")
