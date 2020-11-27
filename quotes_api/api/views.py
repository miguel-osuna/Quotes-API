from flask import Blueprint, request, jsonify
from flask_restful import Api

from quotes_api.api.resources import (
    QuoteResource,
    QuoteList,
    QuoteRandom,
    QuoteSearch,
    AuthorQuoteList,
    AuthorQuoteRandom,
    CategoryList,
    CategoryQuoteList,
    CategoryQuoteRandom,
)
from quotes_api.common.http_status import HttpStatus

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")

api = Api(blueprint)

# Quotes
api.add_resource(QuoteResource, "/quotes/<quote_id>", endpoint="quote_by_id")
api.add_resource(QuoteList, "/quotes", endpoint="quotes")
api.add_resource(QuoteRandom, "/quotes/random", endpoint="quote_random")
api.add_resource(QuoteSearch, "/quotes/search", endpoint="quote_search")

# Authors
api.add_resource(
    AuthorQuoteList, "/authors/<string:author_name>", endpoint="quotes_by_author"
)
api.add_resource(
    AuthorQuoteRandom, "/authors/<string:author_name>/random", endpoint="author_random"
)

# Categories
api.add_resource(CategoryList, "/categories", endpoint="categories")
api.add_resource(
    CategoryQuoteList,
    "/categories/<string:category_name>",
    endpoint="quotes_by_category",
)
api.add_resource(
    CategoryQuoteRandom,
    "/categories/<string:category_name>/random",
    endpoint="category_random",
)
