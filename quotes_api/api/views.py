from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from quotes_api.api.resources import (
    QuoteResource,
    QuoteList,
    QuoteRandom,
    AuthorList,
    TagList,
)
from quotes_api.common import HttpStatus
from quotes_api.extensions import apispec
from quotes_api.api.schemas import QuoteSchema, AuthorSchema, TagSchema

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
print(__name__)

api = Api(blueprint)

# Quotes routes
api.add_resource(QuoteResource, "/quotes/<quote_id>", endpoint="quote")
api.add_resource(QuoteList, "/quotes", endpoint="quotes")
api.add_resource(QuoteRandom, "/quotes/random", endpoint="random_quote")
# Authors routes
api.add_resource(AuthorList, "/authors", endpoint="authors")
# Tags routes
api.add_resource(TagList, "/tags", endpoint="tags")


@blueprint.before_app_first_request
def register_views():

    # Adding Quote resources
    apispec.spec.components.schema("QuoteSchema", schema=QuoteSchema)
    apispec.spec.path(view=QuoteResource, app=current_app)
    apispec.spec.path(view=QuoteList, app=current_app)
    apispec.spec.path(view=QuoteRandom, app=current_app)

    # Adding Author resources
    apispec.spec.components.schema("AuthorSchema", schema=AuthorSchema)
    apispec.spec.path(view=AuthorList, app=current_app)

    # Adding Tag resources
    apispec.spec.components.schema("TagSchema", schema=TagSchema)
    apispec.spec.path(view=TagList, app=current_app)

