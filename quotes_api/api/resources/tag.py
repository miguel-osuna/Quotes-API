from flask import request, jsonify, make_response, url_for
from flask_restful import Resource
from flask_apispec import use_kwargs, marshal_with, doc
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields

from quotes_api.models import Quote
from quotes_api.common import HttpStatus, paginator
from quotes_api.auth.decorators import user_required, admin_required


class TagSchema(Schema):
    tag = fields.String()


class TagList(MethodResource, Resource):
    """ List of tags. """

    # Decorators applied to all class methods
    method_decorators = []

    @doc(description="Get list of tags.", tags=["Tags"])
    @user_required
    def get(self):
        """ Get list of all tags. """

        try:
            response_body = {
                "tags": [
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
                {"error": "Could not retrieve list of tags"},
                HttpStatus.internal_server_error_500.value,
            )
