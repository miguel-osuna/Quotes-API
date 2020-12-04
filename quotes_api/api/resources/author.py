from flask import request, jsonify, make_response, url_for
from flask_restful import Resource

from quotes_api.models import Quote
from quotes_api.extensions import odm
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


class AuthorList(Resource):
    """ List of quote authors. """

    # Decorators applied to all class methods
    method_decorators = []

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


class AuthorQuoteRandom(Resource):
    """ Random quote object filtered by author. """

    # Decorators applied to all class methods
    method_decorators = []

    @user_required
    def get(self, author_name):

        try:
            # Bypassing mongoengine to use pymongo (driver)
            quote_collection = Quote._get_collection()

            # Defining the pipeline for the aggregate
            pipeline = [
                {"$match": {"authorName": author_name}},
                {"$sample": {"size": 1}},
            ]

            # Converting CommandCursor class iterator into a list and then getting the only item in it
            random_author_quote = [
                quote for quote in quote_collection.aggregate(pipeline)
            ][0]

            response_body = {
                "id": str(random_author_quote["_id"]),
                "quoteText": random_author_quote["quoteText"],
                "authorName": random_author_quote["authorName"],
                "authorImage": random_author_quote["authorImage"],
                "tags": random_author_quote["tags"],
            }

            return make_response(jsonify(response_body), HttpStatus.ok_200.value)

        except:
            return (
                {"error": "Could not retrieve quote."},
                HttpStatus.internal_server_error_500.value,
            )

