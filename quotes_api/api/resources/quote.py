from flask import request
from flask_restful import Resource
from quotes_api.models import Quote
from quotes_api.extensions import odm
from quotes_api.common.http_status import HttpStatus


class QuoteResource(Resource):
    """ Single quote object resource. """

    # Decorators applied to all class methods
    method_decorators = []

    def get(self, quote_id):
        """ Get quote. """
        pass

    def put(self, quote_id):
        """ Update quote fields. """
        pass

    def delete(self, quote_id):
        """ Delete quote. """


class QuoteListResource(Resource):
    """ Quote object list resource. """

    # Decorators applied to all class methods
    method_decorators = []

    def get(self):
        """ Get list of quotes. """
        pass

    def post(self):
        """ Create new quote. """
        pass
