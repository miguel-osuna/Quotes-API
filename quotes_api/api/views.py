"""API quotes views."""

from flask import Blueprint, current_app
from flask_restful import Api

from quotes_api.api.resources import (
    QuoteResource,
    QuoteList,
    QuoteRandom,
    AuthorList,
    TagList,
)
from quotes_api.extensions import apispec
from quotes_api.api.schemas import (
    QuoteSchema,
    AuthorSchema,
    TagSchema,
    LinksSchema,
    MetadataSchema,
)

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")

api = Api(blueprint)

# Route all resources
api.add_resource(QuoteResource, "/quotes/<quote_id>", endpoint="quote")
api.add_resource(QuoteList, "/quotes", endpoint="quotes")
api.add_resource(QuoteRandom, "/quotes/random", endpoint="random_quote")
api.add_resource(AuthorList, "/authors", endpoint="authors")
api.add_resource(TagList, "/tags", endpoint="tags")

# Apispec view configuration
@blueprint.before_app_first_request
def register_views():
    """Register views for API documentation."""

    # Adding Resource Schemas
    apispec.spec.components.schema("QuoteSchema", schema=QuoteSchema)
    apispec.spec.components.schema("AuthorSchema", schema=AuthorSchema)
    apispec.spec.components.schema("TagSchema", schema=TagSchema)
    apispec.spec.components.schema("LinksSchema", schema=LinksSchema)
    apispec.spec.components.schema("MetadataSchema", schema=MetadataSchema)

    # Adding Quote views
    apispec.spec.path(view=QuoteResource, app=current_app)
    apispec.spec.path(view=QuoteList, app=current_app)
    apispec.spec.path(view=QuoteRandom, app=current_app)

    # Adding Author views
    apispec.spec.path(view=AuthorList, app=current_app)

    # Adding Tag views
    apispec.spec.path(view=TagList, app=current_app)
