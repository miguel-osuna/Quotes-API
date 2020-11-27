from flask import request, jsonify, make_response, url_for
from flask_restful import Resource

from quotes_api.models import Quote
from quotes_api.extensions import odm
from quotes_api.common import HttpStatus, quote_paginator


class CategoryList(Resource):
    """ List of categories. """

    # Decorators applied to all class methods
    method_decorators = []

    def get(self):
        """ Get list of all categories. """

        try:
            response_body = {
                "categories": [
                    "love",
                    "life",
                    "inspiration",
                    "humor",
                    "philosophy",
                    "god",
                    "truth",
                    "widsom",
                    "romance",
                    "poetry",
                    "death",
                    "happiness",
                    "hope",
                    "faith",
                    "religion",
                    "life-lessons",
                    "success",
                    "motivational",
                    "time",
                    "knowledge",
                    "love",
                    "spirituality",
                    "science",
                    "books",
                    "other",
                ]
            }

            return make_response(jsonify(response_body), HttpStatus.ok_200.value)

        except:
            return (
                {"error": "Couldn't retrieve list of categories"},
                HttpStatus.internal_server_error_500.value,
            )


class CategoryQuoteList(Resource):
    """ Quote object list filtered by category. """

    # Decorators applied to all class methods
    method_decorators = []

    def get(self, category_name):
        """ Get list of category quotes. """

        args = request.args

        page = int(args.get("page", 1))
        per_page = int(args.get("per_page", 5))

        try:
            # Generating pagination of filtered quotes by category
            pagination = Quote.objects(tags=str(category_name)).paginate(
                page=page, per_page=per_page
            )

            response_body = quote_paginator(
                pagination, "api.quotes_by_category", category_name=category_name
            )

            return make_response(jsonify(response_body), HttpStatus.ok_200.value)

        except:
            return (
                {"error": "Couldn't retrieve quotes"},
                HttpStatus.internal_server_error_500.value,
            )


class CategoryQuoteRandom(Resource):
    """ Random quote object filtered by category. """

    # Decorators applied to all class methods
    method_decorators = []

    def get(self, category_name):

        # Bypassing mongoengine to use pymongo (driver)
        quote_collection = Quote._get_collection()

        # Defining the pipeline for the aggregate
        pipeline = [
            {"$match": {"tags": {"$elemMatch": {"$eq": category_name}}}},
            {"$sample": {"size": 1}},
        ]

        # Converting CommandCursor class iterator into a list and then getting the only item in it
        random_category_quote = [
            quote for quote in quote_collection.aggregate(pipeline)
        ][0]

        response_body = {
            "id": str(random_category_quote["_id"]),
            "quoteText": random_category_quote["quoteText"],
            "authorName": random_category_quote["authorName"],
            "authorImage": random_category_quote["authorImage"],
            "tags": random_category_quote["tags"],
        }

        return make_response(jsonify(response_body), HttpStatus.ok_200.value)
