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
        # quote = Quote.objects.get_or_404(_id=quote_id)
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

    def get(self, page, per_page):
        # paginated_quotes = Quotes.objects.paginate(page=page, per_page=per_page)
        """ Get list of quotes. """
        pass

    def post(self):
        """ Create new quote. """
        pass
