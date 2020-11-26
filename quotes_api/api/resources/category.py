from flask import request, jsonify, make_response, url_for
from flask_restful import Resource

from quotes_api.models import Quote
from quotes_api.extensions import odm
from quotes_api.common.http_status import HttpStatus


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
    """ Category quote object list. """

    # Decorators applied to all class methods
    method_decorators = []

    def get(self, category_name):
        """ Get list of category quotes. """

        args = request.args
        print(args)

        page = int(args.get("page", 1))
        per_page = int(args.get("per_page", 5))

        try:
            # Generating pagination of filtered quotes by category
            pagination = Quote.objects(tags=str(category_name)).paginate(
                page=page, per_page=per_page
            )

        except Exception as e:
            return (
                {"error": "Resource not found", "details": str(e)},
                HttpStatus.not_found_404.value,
            )

        try:
            quote_items = []
            for quote in pagination.items:
                print(quote)
                quote_object = {
                    "id": str(quote.id),
                    "quoteText": quote.quoteText,
                    "authorName": quote.authorName,
                    "authorImage": quote.authorImage,
                    "tags": quote.tags,
                }
                quote_items.append(quote_object)

            self_link = url_for(
                "api.quotes_by_category",
                category_name=category_name,
                page=pagination.page,
                per_page=pagination.per_page,
                _external=True,
            )

            next_link = (
                url_for(
                    "api.quotes_by_category",
                    category_name=category_name,
                    page=pagination.next_num,
                    per_page=pagination.per_page,
                    _external=True,
                )
                if pagination.has_next
                else None
            )

            pervious_link = (
                url_for(
                    "api.quotes_by_category",
                    category_name=category_name,
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
                        "prev": pervious_link,
                        "next": next_link,
                    },
                },
                "records": quote_items,
            }

            return make_response(jsonify(body_response), HttpStatus.ok_200.value)

        except Exception as e:
            return (
                {"error": "Couldn't retrieve list of categories", "detail": str(e)},
                HttpStatus.internal_server_error_500.value,
            )

