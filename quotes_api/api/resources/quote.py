from flask import request, jsonify, make_response, url_for
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
        try:
            quote = Quote.objects.get(id=quote_id)
        except:
            return (
                {"error": "The requested URL was not found on the server."},
                HttpStatus.not_found_404.value,
            )

        response_body = {
            "quote": {
                "id": str(quote.id),
                "quote_content": quote.quote_content,
                "author_name": quote.author_name,
                "author_image": quote.author_image,
                "tags": quote.tags,
            }
        }

        return make_response(jsonify(response_body), HttpStatus.ok_200.value)

    def put(self, quote_id):
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
                {"error": "Couldn't delete quote."},
                HttpStatus.internal_server_error_500.value,
            )


class QuoteListResource(Resource):
    """ Quote object list resource. """

    # Decorators applied to all class methods
    method_decorators = []

    def get(self):
        # paginated_quotes = Quotes.objects.paginate(page=page, per_page=per_page)
        """ Get list of quotes. """
        try:
            args = request.args
            print(args)

            page = int(args["page"])
            per_page = int(args["per_page"])
        except:
            return {"error": "Missing data."}, HttpStatus.bad_request_400.value

        try:
            # Generating pagination of quotes
            pagination = Quote.objects.paginate(page=page, per_page=per_page)

            # Creating list of quotes
            quote_items = []
            for quote in pagination.items:
                quote_object = {
                    "id": str(quote.id),
                    "quote_content": quote.quote_content,
                    "author_name": quote.author_name,
                    "author_image": quote.author_image,
                    "tags": quote.tags,
                }
                quote_items.append(quote_object)

            self_link = url_for(
                "api.quotes",
                page=pagination.page,
                per_page=pagination.per_page,
                _external=True,
            )

            next_link = (
                url_for(
                    "api.quotes",
                    page=pagination.next_num,
                    per_page=pagination.per_page,
                    _external=True,
                )
                if pagination.has_next
                else None
            )

            previous_link = (
                url_for(
                    "api.quotes",
                    page=pagination.prev_num,
                    per_page=pagination.per_page,
                    _external=True,
                )
                if pagination.has_prev
                else None
            )

            body_response = {
                "meta": {
                    "page_number": pagination.page,
                    "page_size": pagination.per_page,
                    "total_pages": pagination.pages,
                    "total_records": pagination.total,
                    "links": {
                        "self": self_link,
                        "prev": previous_link,
                        "next": next_link,
                    },
                },
                "records": quote_items,
            }
            return make_response(jsonify(body_response), HttpStatus.ok_200.value)

        except Exception as e:
            return (
                {"error": "Couldn't retrieve quotes.", "detail": str(e)},
                HttpStatus.internal_server_error_500.value,
            )

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
