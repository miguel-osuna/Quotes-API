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
# api.add_resource(, "/quotes/random", endpoint="quote_random")
# api.add_resource(, "/quotes/search/<string:quote_fragment>", endpoint="quote_search")

api.add_resource(
    AuthorQuoteList, "/authors/<string:author_name>", endpoint="quotes_by_author"
)
# Pending
# api.add_resource(, "/authors/random, endpoint="author_random)

api.add_resource(CategoryList, "/categories", endpoint="categories")
api.add_resource(
    CategoryQuoteList,
    "/categories/<string:category_name>",
    endpoint="quotes_by_category",
)
# Pending
# api.add_resource(, "/categories/random", endpoint="category_random")
