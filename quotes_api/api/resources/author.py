from flask import request, jsonify, make_response, url_for
from flask_restful import Resource

from quotes_api.models import Quote
from quotes_api.extensions import odm
from quotes_api.common import HttpStatus, quote_paginator


class AuthorQuoteList(Resource):
    """ Quote object list filtered by author. """

    # Decorators applied to all class methods
    method_decorators = []

    def get(self, author_name):
        """ Get list of author quotes. """
        args = request.args

        page = int(args.get("page", 1))
        per_page = int(args.get("per_page", 5))

        try:
            # Generating pagination of filtered quotes by author
            pagination = Quote.objects(authorName=str(author_name)).paginate(
                page=page, per_page=per_page
            )

            response_body = quote_paginator(
                pagination, "api.quotes_by_author", author_name=author_name
            )

            return make_response(jsonify(response_body, HttpStatus.ok_200.value))

        except:
            {
                "error": "Couldn't retrieve quotes"
            }, HttpStatus.internal_server_error_500.value


class AuthorQuoteRandom(Resource):
    """ Random quote object filtered by author. """

    # Decorators applied to all class methods
    method_decorators = []

    def get(self, author_name):
        # Bypassing mongoengine to use pymongo (driver)
        quote_collection = Quote._get_collection()

        # Defining the pipeline for the aggregate
        pipeline = [{"$match": {"authorName": author_name}}, {"$sample": {"size": 1}}]

        # Converting CommandCursor class iterator into a list and then getting the only item in it
        random_author_quote = [quote for quote in quote_collection.aggregate(pipeline)][
            0
        ]

        response_body = {
            "id": str(random_author_quote["_id"]),
            "quoteText": random_author_quote["quoteText"],
            "authorName": random_author_quote["authorName"],
            "authorImage": random_author_quote["authorImage"],
            "tags": random_author_quote["tags"],
        }

        return make_response(jsonify(response_body), HttpStatus.ok_200.value)

