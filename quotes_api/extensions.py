""" Extensions registry

All extensions here are used as singletons and 
initialized in application factory
"""

from flask_mongoengine import MongoEngine

odm = MongoEngine()
