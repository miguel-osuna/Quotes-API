from flask import request, jsonify, make_response, url_for
from flask_restful import Resource

from quotes_api.models import Quote
from quotes_api.extensions import odm
from quotes_api.common import HttpStatus, multipurpose_paginator
from quotes_api.auth.decorators import user_required, admin_required


class QuoteResource(Resource):
    """ Single quote object resource. """

    # Decorators applied to all class methods
    method_decorators = []

    @user_required
    def get(self, quote_id):
        """ Get quote by id. """
        try:
            quote = Quote.objects.get_or_404(id=quote_id)

        except:
            return (
                {"error": "The requested URL was not found on the server."},
                HttpStatus.not_found_404.value,
            )

        response_body = {
            "quote": {
                "id": str(quote.id),
                "quoteText": quote.quoteText,
                "authorName": quote.authorName,
                "authorImage": quote.authorImage,
                "tags": quote.tags,
            }
        }

        return make_response(jsonify(response_body), HttpStatus.ok_200.value)

    @admin_required
    def put(self, quote_id):
        """ Replace entire quote. """
        try:
            quote = Quote.objects.get_or_404(id=quote_id)
        except:
            return {"error": "The requested URL was not found on the server."}

        try:
            data = request.get_json()
            quote.update(**data)
            quote.save()

            return "", HttpStatus.no_content_204.value

        except:
            return (
                {"error": "Missing data."},
                HttpStatus.bad_request_400.value,
            )

    @admin_required
    def patch(self, quote_id):
        """ Update quote fields. """
        try:
            quote = Quote.objects.get_or_404(id=quote_id)
        except:
            return (
                {"error": "The requested URL was not found on the server."},
                HttpStatus.not_found_404.value,
            )

        try:
            data = request.get_json()
            quote.update(**data)
            quote.save()

            return "", HttpStatus.no_content_204.value

        except:
            return {"error": "Missing data."}, HttpStatus.bad_request_400.value

    @admin_required
    def delete(self, quote_id):
        """ Delete quote. """

        try:
            quote = Quote.objects.get_or_404(id=quote_id)
        except:
            return (
                {"error": "The requested URL was not found on the server."},
                HttpStatus.not_found_404.value,
            )

        try:
            quote.delete()
            return "", HttpStatus.no_content_204.value

        except:
            return (
                {"error": "Could not delete quote."},
                HttpStatus.internal_server_error_500.value,
            )


class QuoteList(Resource):
    """ Quote object list. """

    # Decorators applied to all class methods
    method_decorators = []

    @user_required
    def get(self):
        """ Get list of quotes. """

        args = request.args

        page = int(args.get("page", 1))
        per_page = int(args.get("per_page", 5))

        try:
            # Generating pagination of quotes
            pagination = Quote.objects.paginate(page=page, per_page=per_page)

            response_body = multipurpose_paginator(pagination, "api.quotes")

            return make_response(jsonify(response_body), HttpStatus.ok_200.value)

        except:
            return (
                {"error": "Couldn't retrieve quotes."},
                HttpStatus.internal_server_error_500.value,
            )

    @admin_required
    def post(self):
        """ Create new quote. """
        try:
            # Get quote data from the request
            data = request.get_json()
        except:
            return {"error": "Missing data."}, HttpStatus.bad_request_400.value
        try:
            # Create new database entry
            quote = Quote(**data)
            quote.save()
            id = quote.id

            # Send success response
            response_body = {"id": str(id)}
            return make_response(jsonify(response_body), HttpStatus.created_201.value)

        except:
            # Error creating quote entry
            return (
                {"error": "Couldn't create quote entry."},
                HttpStatus.internal_server_error_500.value,
            )


class QuoteRandom(Resource):
    """ Random quote object. """

    # Decorators applied to all class methods
    method_decorators = []

    @user_required
    def get(self):

        try:
            # Bypassing mongoengine to use pymongo (driver)
            quote_collection = Quote._get_collection()

            # Defining the pipeline for the aggregate
            pipeline = [{"$sample": {"size": 1}}]

            # Converting CommandCursor class iterator into a list and then getting the only item in it
            random_quote = [quote for quote in quote_collection.aggregate(pipeline)][0]

            response_body = {
                "id": str(random_quote["_id"]),
                "quoteText": random_quote["quoteText"],
                "authorName": random_quote["authorName"],
                "authorImage": random_quote["authorImage"],
                "tags": random_quote["tags"],
            }

            return make_response(jsonify(response_body), HttpStatus.ok_200.value)

        except:
            return (
                {"error": "Couldn't retrieve quote."},
                HttpStatus.internal_server_error_500.value,
            )


class QuoteSearch(Resource):
    """ Query search for quote object. """

    # Decorators applied to all class methods
    method_decorators = []

    @user_required
    def get(self):
        args = request.args

        try:
            query = str(args["query"])
            page = int(args.get("page", 1))
            per_page = int(args.get("per_page", 5))

        except:
            {"error": "Missing data."}, HttpStatus.bad_request_400.value

        try:

            # Get the documents that match the text search and order them by score
            # After that, create a paginator with the results
            pagination = (
                Quote.objects.search_text(query)
                .order_by("$text_score")
                .paginate(page=page, per_page=per_page)
            )

            response_body = multipurpose_paginator(pagination, "api.quote_search")

            return make_response(jsonify(response_body), HttpStatus.ok_200.value)

        except:
            return (
                {"error": "Couldn't retrieve quotes."},
                HttpStatus.internal_server_error_500.value,
            )
