from flask import Blueprint, request, jsonify
from flask_restful import Api

from quotes_api.api.resources import (
    QuoteResource,
    QuoteList,
    AuthorQuoteList,
    CategoryList,
    CategoryQuoteList,
)
from quotes_api.common.http_status import HttpStatus

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")

api = Api(blueprint)

# Quotes
api.add_resource(QuoteResource, "/quotes/<quote_id>", endpoint="quote_by_id")
api.add_resource(QuoteList, "/quotes", endpoint="quotes")

# Pending
# api.add_resource(QuoteResource, "/quotes/random", endpoint="quote_random")

api.add_resource(
    AuthorQuoteList, "/authors/<string:author_name>", endpoint="quote_by_author_name"
)

api.add_resource(CategoryList, "/categories", endpoint="categories")
api.add_resource(
    CategoryQuoteList,
    "categories/<string:category_name>",
    endpoint="quote_by_category_name",
)
