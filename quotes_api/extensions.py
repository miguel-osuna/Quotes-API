""" Extensions registry

All extensions here are used as singletons and 
initialized in application factory
"""

from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from passlib.context import CryptContext

odm = MongoEngine()
jwt = JWTManager()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
