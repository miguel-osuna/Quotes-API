from flask import request, jsonify, make_response, url_for
from flask_restful import Resource
from flask_apispec import use_kwargs, marshal_with, doc
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields

from quotes_api.models import Quote
from quotes_api.common import HttpStatus, paginator, author_paginator
from quotes_api.auth.decorators import user_required, admin_required


def sort_order_parser(input):
    """ 
    Parses a user query input for the sort_order parameter.

    Checks if the sorting is ascending or descending.
    """
    if input == "ascending" or input == "asc" or input == "1":
        return "+"

    elif input == "descending" or input == "desc" or input == "-1":
        return "-"

    else:
        return "+"


def AuthorSchema(Schema):
    authorName = fields.String()
    authorImage = fields.Image()


class AuthorList(MethodResource, Resource):
    """ List of quote authors. """

    # Decorators applied to all class methods
    method_decorators = []

    @doc(description="Get list of authors.", tags=["Authors"])
    @user_required
    def get(self):
        """ Get quote authors by alphabetical order. """

        args = request.args
        page = int(args.get("page", 1))
        per_page = int(args.get("per_page", 10))
        sort_order = str(args.get("sort_order", "asc"))

        try:
            sort = sort_order_parser(sort_order)

            # Generating pagination of quotes
            pagination = (
                Quote.objects()
                .order_by(sort + "authorName")
                .paginate(page=page, per_page=per_page)
            )

            response_body = author_paginator(
                pagination, "api.authors", sort_order=sort_order
            )

            return make_response(jsonify(response_body, HttpStatus.ok_200.value))

        except:
            return (
                {"error": "Could not retrieve authors"},
                HttpStatus.internal_server_error_500.value,
            )

