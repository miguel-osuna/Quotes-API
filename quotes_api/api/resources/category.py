from flask import request, jsonify, make_response, url_for
from flask_restful import Resource

from quotes_api.models import Quote
from quotes_api.extensions import odm
from quotes_api.common.http_status import HttpStatus


class CategoryList(Resource):
    """ List of categories. """

    # Decorators applied to all class methods
    method_decorators = []

    def get(self):
        """ Get list of all categories. """


class CategoryQuoteList(Resource):
    """ Category quote object list. """

    # Decorators applied to all class methods
    method_decorators = []

    def get(self, category_name):
        """ Get list of category quotes. """

        args = request.args
        print(args)

        page = int(args.get("page", 1))
        limit = int(args.get("limit", 5))

