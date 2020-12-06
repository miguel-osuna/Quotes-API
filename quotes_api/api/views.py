from flask import Blueprint, request, jsonify
from flask_restful import Api


from quotes_api.extensions import docs
from quotes_api.api.resources import (
    QuoteResource,
    QuoteList,
    QuoteRandom,
    AuthorList,
    TagList,
)
from quotes_api.common import HttpStatus

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

