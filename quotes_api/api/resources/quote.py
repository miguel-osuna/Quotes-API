from flask import request, jsonify, make_response, url_for
from flask_restful import Resource

from quotes_api.models import Quote
from quotes_api.extensions import odm
from quotes_api.common import HttpStatus, paginator
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

        response_body = {"quote": quote.to_dict()}

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
        tags = args.get("tags", None)
        author = args.get("author", None)
        query = args.get("query", None)

        try:
            # Build the filters for the database query
            filters = self.build_quote_list_filters(tags, author)

            # Do a search query if the user provided a query
            if query is not None:
                pagination = (
                    Quote.objects.filter(**filters)
                    .search_text(query)
                    .order_by("$text_score")
                    .paginate(page=page, per_page=per_page)
                )

            else:
                pagination = Quote.objects.filter(**filters).paginate(
                    page=page, per_page=per_page
                )

            response_body = paginator(pagination, "api.quotes")
            return make_response(jsonify(response_body), HttpStatus.ok_200.value)

        except Exception as e:
            return (
                {"error": "Could not retrieve quotes.", "detail": str(e)},
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
                {"error": "Could not create quote entry."},
                HttpStatus.internal_server_error_500.value,
            )

    def build_quote_list_filters(self, tags, author):
        """ Filter generation for quote list match. """

        filters = {}

        # Check if the user provided any tags for filtering
        if tags is not None:

            # Looks for quotes that have at least one tag in their tags
            # It acts as an OR operator.
            if "|" in tags:
                filters["tags__in"] = tags.split("|")

            # Looks for quotes that have every tag in their tags.
            # It acts as an AND operator.
            elif "," in tags:
                filters["tags__all"] = tags.split(",")

            # User normal filtering when just 1 tag is provided
            else:
                filters["tags"] = tags

        # Check if the user provided an author name
        if author is not None:
            filters["authorName"] = author

        return filters


class QuoteRandom(Resource):
    """ Random quote object. """

    # Decorators applied to all class methods
    method_decorators = []

    @user_required
    def get(self):
        """ Get random quote filtered by tags and author. """
        args = request.args

        tags = args.get("tags", None)
        author = args.get("author", None)

        try:
            # Build the filters for the database query
            filters = self.build_random_quote_filters(tags, author)

            # Baypassing mongoengine to use pymongo (driver)
            quote_collection = Quote._get_collection()

            # Defining the pipeline for the aggregate
            pipeline = [
                {
                    "$project": {
                        "_id": 1,
                        "quoteText": 1,
                        "authorName": 1,
                        "authorImage": 1,
                        "tags": 1,
                    }
                },
                {"$match": {"$and": [filters]}},
                {"$sample": {"size": 1}},
            ]

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

        except Exception as e:
            return (
                {"error": "Could not retrieve quote.", "detail": str(e)},
                HttpStatus.internal_server_error_500.value,
            )

    def build_random_quote_filters(self, tags, author):
        """ Filter generation for random quote match. """

        filters = {}

        # Check if the user provided any tags for filtering
        if tags is not None:
            # Looks for quotes that have at least one tag in their tags
            # It acts as an OR operator
            if "|" in tags:
                filters["tags"] = {"$in": tags.split("|")}

            # Looks for quotes that have every tag in their tags.
            # It acts as an AND operator
            elif "," in tags:
                filters["tags"] = {"$all": tags.split(",")}

            # User normal filtering when just 1 tag is provided
            else:
                filters["tags"] = tags

        # Check if the user provided an author name
        if author is not None:
            filters["authorName"] = author

        return filters

