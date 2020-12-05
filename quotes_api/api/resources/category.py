from flask import request, jsonify, make_response, url_for
from flask_restful import Resource

from quotes_api.models import Quote
from quotes_api.extensions import odm
from quotes_api.common import HttpStatus, paginator
from quotes_api.auth.decorators import user_required, admin_required


class CategoryList(Resource):
    """ List of categories. """

    # Decorators applied to all class methods
    method_decorators = []

    @user_required
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
                {"error": "Could not retrieve list of categories"},
                HttpStatus.internal_server_error_500.value,
            )
