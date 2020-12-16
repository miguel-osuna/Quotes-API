from flask import request, jsonify, make_response, url_for
from flask_restful import Resource

from quotes_api.models import Quote
from quotes_api.common import HttpStatus
from quotes_api.api.schemas import TagSchema
from quotes_api.auth.decorators import Role, role_required


class TagList(Resource):
    """ List of tags. 
    
    ---
    get:
      tags:
        - Tag
      description: |
        Get list of supported `tags`. Requires a valid `user` `api key` for authentication.
      security:
        - user_api_key: []          
        - admin_api_key: [] 
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  tags:
                    type: array
                    items:
                      type: string
        400:
          description: Bad request.
        401: 
          description: Missing authentication header.
    """

    # Decorators applied to all class methods
    method_decorators = []

    @role_required([Role.BASIC, Role.ADMIN])
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
