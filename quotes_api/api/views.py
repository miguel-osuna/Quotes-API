from flask import Blueprint, request, jsonify
from flask_restful import Api


from quotes_api.extensions import docs
from quotes_api.api.resources import (
    QuoteResource,
    QuoteList,
    QuoteRandom,
    AuthorList,
    TagList,
    TestResource,
)
from quotes_api.common import HttpStatus

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")

api = Api(blueprint)

# Test route
blueprint.add_url_rule("/test", view_func=TestResource.as_view("Test"))

# Quotes routes
api.add_resource(QuoteResource, "/quotes/<quote_id>", endpoint="quote_by_id")
api.add_resource(QuoteList, "/quotes", endpoint="quotes")
api.add_resource(QuoteRandom, "/quotes/random", endpoint="quote_random")


# Authors routes
api.add_resource(AuthorList, "/authors", endpoint="authors")

# Tags routes
api.add_resource(TagList, "/tags", endpoint="tags")

