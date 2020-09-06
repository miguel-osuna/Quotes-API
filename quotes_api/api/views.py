from flask import Blueprint
from flask_restful import Api

from quotes_api.api.resources import QuoteResource, QuoteListResource
from quotes_api.common.http_status import HttpStatus

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)

api.add_resource(QuoteResource, "/quotes/<int:quote_id>", endpoint="quote_by_id")
api.add_resource(QuoteListResource, "/quotes", endponit="quotes")
