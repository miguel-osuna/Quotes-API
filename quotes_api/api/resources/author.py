from flask import request, jsonify, make_response, url_for
from flask_restful import Resource

from quotes_api.models import Quote
from quotes_api.extensions import odm
from quotes_api.common.http_status import HttpStatus


class AuthorQuoteList(Resource):
    """ Author quote object list. """

    # Decorators applied to all class methods
    method_decorators = []

    def get(self):
        """ Get list of author quotes. """
        pass

