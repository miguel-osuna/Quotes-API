"""Author resource file."""

from flask import request, make_response
from flask_restful import Resource

from quotes_api.api.models import Quote
from quotes_api.common import HttpStatus, author_paginator
from quotes_api.api.schemas import AuthorSchema
from quotes_api.auth.decorators import Role, role_required


class AuthorList(Resource):
    """
    List of quote authors.

    ---
    get:
      tags:
        - Author
      description: |
        Get list of available `authors`. Optional `sort_order` parameter determines the order in which the
        authors are displayed. Requires a valid `user` `api key` for authentication.
      security:
        - user_api_key: []
        - admin_api_key: []
      parameters:
        - in: query
          name: page
          schema:
            type: integer
            default: 1
          description: Page number of the pagination.
        - in: query
          name: per_page
          schema:
            type: integer
            default: 5
          description: Number of results per page.
        - in: query
          name: sort_order
          schema:
            type: string
            enum: [asc, desc]
            default: asc
          description: Author's name sort order.
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - type: object
                    properties:
                      meta:
                        $ref: '#/components/schemas/MetadataSchema'
                  - type: object
                    properties:
                      records:
                        type: array
                        items:
                          $ref: '#/components/schemas/AuthorSchema'
        401:
          description: Missing authentication header.
    """

    # Decorators applied to all class methods
    method_decorators = []

    @role_required([Role.BASIC, Role.ADMIN])
    def get(self):
        """Get quote authors by alphabetical order."""

        args = request.args
        page = int(args.get("page", 1))
        per_page = int(args.get("per_page", 20))
        sort_order = str(args.get("sort_order", "asc"))

        try:
            sort = self._sort_order_parser(sort_order)

            # Generating pagination of quotes
            pagination = (
                Quote.objects()
                .order_by(sort + "author_name")
                .paginate(page=page, per_page=per_page)
            )

            response_body = author_paginator(
                pagination, "api.authors", AuthorSchema, sort_order=sort_order
            )

            return make_response(response_body, HttpStatus.OK_200.value)

        except Exception:
            return (
                {"error": "Could not retrieve authors"},
                HttpStatus.INTERNAL_SERVER_ERROR_500.value,
            )

    def _sort_order_parser(self, order):
        """
        Parses a user query input for the sort_order parameter.

        Checks if the sorting is ascending or descending.
        """

        if order in ("ascending", "asc", "1"):
            return "+"

        if order in ("descending", "desc", "-1"):
            return "-"

        return "+"
