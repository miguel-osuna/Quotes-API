"""Quote resource file."""

from flask import request, make_response
from flask_restful import Resource

from quotes_api.models import Quote
from quotes_api.common import HttpStatus, paginator
from quotes_api.api.schemas import QuoteSchema
from quotes_api.auth.decorators import Role, role_required


class QuoteResource(Resource):
    """
    Single quote object resource.

    ---
    get:
      tags:
        - Quote
      description: |
        Get `quote` resource by id. Requires a valid `user` `api key` for authentication.
      security:
        - user_api_key: []
        - admin_api_key: []
      parameters:
        - in: path
          name: quote_id
          required: true
          schema:
            type: string
          description: Quote id.
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  quote: QuoteSchema
        401:
          description: Missing authentication header.
        404:
          description: Quote does not exist.

    put:
      tags:
        - Quote
      description: |
        Update `quote` resource by id. Requires a valid `admin` `api key` for authentication.
      security:
        - admin_api_key: []
      parameters:
        - in: path
          name: quote_id
          required: true
          schema:
            type: string
          description: Quote id.
      requestBody:
        content:
          application/json:
            schema:
              QuoteSchema
      responses:
        204:
          description: The quote resource was successfully updated.
        401:
          description: Missing authentication header.
        404:
          description: Quote does not exist.

    patch:
      tags:
        - Quote
      description: |
        Patch `quote` resource by id. Requires a valid `admin` `api key` for authentication.
      security:
        - admin_api_key: []
      parameters:
        - in: path
          name: quote_id
          required: true
          schema:
            type: string
          description: Quote id.
      requestBody:
        content:
          application/json:
            schema:
              QuoteSchema
      responses:
        204:
          description: The quote resource was successfully patched.
        401:
          description: Missing authentication header.
        404:
          description: Quote does not exist.

    delete:
      tags:
        - Quote
      description: |
        Delete `quote` resource by id. Requires a valid `admin` `api key` for authentication.
      security:
        - admin_api_key: []
      parameters:
        - in: path
          name: quote_id
          required: true
          schema:
            type: string
          description: Quote id.
      responses:
        204:
          description: The quote resource was successfully deleted.
        401:
          description: Missing authentication header.
        404:
          description: Quote does not exist.
    """

    # Decorators applied to all class methods
    method_decorators = []

    @role_required([Role.BASIC, Role.ADMIN])
    def get(self, quote_id):
        """Get quote by id."""
        try:
            quote = Quote.objects.get_or_404(id=quote_id)
        except Exception:
            return (
                {"error": "Quote does not exist."},
                HttpStatus.NOT_FOUND_404.value,
            )
        quote_schema = QuoteSchema()
        return make_response(quote_schema.dump(quote), HttpStatus.OK_200.value)

    @role_required([Role.ADMIN])
    def put(self, quote_id):
        """Replace entire quote."""
        try:
            quote = Quote.objects.get_or_404(id=quote_id)

        except Exception:
            return (
                {"error": "Quote does not exist."},
                HttpStatus.NOT_FOUND_404.value,
            )

        try:
            # Create quote schema instance
            quote_schema = QuoteSchema()

            data = quote_schema.load(request.json)
            quote.update(**data)
            quote.save()

            return "", HttpStatus.NO_CONTENT_204.value

        except Exception:
            return (
                {"error": "Missing data."},
                HttpStatus.BAD_REQUEST_400.value,
            )

    @role_required([Role.ADMIN])
    def patch(self, quote_id):
        """Update quote fields."""
        try:
            quote = Quote.objects.get_or_404(id=quote_id)

        except Exception:
            return (
                {"error": "Quote does not exist."},
                HttpStatus.NOT_FOUND_404.value,
            )

        try:
            # Check quote schema instance
            quote_schema = QuoteSchema(partial=True)

            data = quote_schema.load(request.json)
            quote.update(**data)
            quote.save()

            return "", HttpStatus.NO_CONTENT_204.value

        except Exception:
            return {"error": "Missing data."}, HttpStatus.BAD_REQUEST_400.value

    @role_required([Role.ADMIN])
    def delete(self, quote_id):
        """Delete quote."""
        try:
            quote = Quote.objects.get_or_404(id=quote_id)

        except Exception:
            return (
                {"error": "Quote does not exist."},
                HttpStatus.NOT_FOUND_404.value,
            )

        try:
            quote.delete()
            return "", HttpStatus.NO_CONTENT_204.value

        except Exception:
            return (
                {"error": "Could not delete quote."},
                HttpStatus.INTERNAL_SERVER_ERROR_500.value,
            )


class QuoteList(Resource):
    """
    Quote object list.

    ---
    get:
      tags:
        - Quote
      description: |
        Get a list of `quote` resources. Optional `tags`, `author` and `query` parameters
        filter the results. Requires a valid `user` `api key` for authentication.
      security:
        - user_api_key: []
        - admin_api_key: []
      parameters:
        - in: query
          name: page
          schema:
            type: integer
            default: 1
          description: Page number for pagination.
        - in: query
          name: per_page
          schema:
            type: integer
            default: 5
          description: Number of results per page.
        - in: query
          name: tags
          schema:
            type: string
          description: Quote tags for filtering.
        - in: query
          name: author
          schema:
            type: string
          description: Author name for filtering.
        - in: query
          name: query
          schema:
            type: string
          description: Query for quote search.
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
                          $ref: '#/components/schemas/QuoteSchema'
        401:
          description: Missing authentication header.

    post:
      tags:
        - Quote
      description: |
        Create a `quote` resource. Requires a valid `admin` `api key` for authentication.
      security:
        - admin_api_key: []
      requestBody:
        content:
          application/json:
            schema:
              QuoteSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: string
                    example: quoteid
        401:
          description: Missing authentication header.
    """

    # Decorators applied to all class methods
    method_decorators = []

    @role_required([Role.BASIC, Role.ADMIN])
    def get(self):
        """Get list of quotes."""

        args = request.args

        page = int(args.get("page", 1))
        per_page = int(args.get("per_page", 5))
        tags = args.get("tags", None)
        author = args.get("author", None)
        query = args.get("query", None)

        try:
            # Build the filters for the database query
            filters = self._build_quote_list_filters(tags, author)

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
            response_body = paginator(pagination, "api.quotes", QuoteSchema)
            return make_response(response_body, HttpStatus.OK_200.value)

        except Exception:
            return (
                {"error": "Could not retrieve quotes."},
                HttpStatus.INTERNAL_SERVER_ERROR_500.value,
            )

    @role_required([Role.ADMIN])
    def post(self):
        """Create new quote."""
        try:
            # Create quote schema instace
            quote_schema = QuoteSchema()
            data = quote_schema.load(request.json)

        except Exception:
            return {"error": "Missing data."}, HttpStatus.BAD_REQUEST_400.value

        try:
            # Create new database entry
            quote = Quote(**data)
            quote.save()

            # Create new quote schema instance that only dumps the id
            quote_schema = QuoteSchema(only=["id"])
            return make_response(quote_schema.dump(quote), HttpStatus.CREATED_201.value)

        except Exception:
            # Error creating quote entry
            return (
                {"error": "Could not create quote entry."},
                HttpStatus.INTERNAL_SERVER_ERROR_500.value,
            )

    def _build_quote_list_filters(self, tags, author):
        """Filter generation for quote list match."""

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
            filters["author_name"] = author

        return filters


class QuoteRandom(Resource):
    """
    Random quote object.

    ---
    get:
      tags:
        - Quote
      description: |
        Get a random `quote` resource. Optional `tags` and `author` parameters filter the result.
        Requires a valid `user` `api key` for authentication.
      security:
        - user_api_key: []
        - admin_api_key: []
      parameters:
        - in: query
          name: tags
          schema:
            type: string
          description: Quote tags for filtering.
        - in: query
          name: author
          schema:
            type: string
          description: Author name for filtering.
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  quote: QuoteSchema
        401:
          description: Missing authentication header.
    """

    # Decorators applied to all class methods
    method_decorators = []

    @role_required([Role.BASIC, Role.ADMIN])
    def get(self):
        """Get random quote filtered by tags and author."""
        args = request.args

        tags = args.get("tags", None)
        author = args.get("author", None)

        try:
            # Build the filters for the database query
            filters = self._build_random_quote_filters(tags, author)

            # Baypassing mongoengine to use pymongo (driver)
            quote_collection = Quote._get_collection()

            # Defining the pipeline for the aggregate
            pipeline = [
                {
                    "$project": {
                        "_id": 1,
                        "quote_text": 1,
                        "author_name": 1,
                        "author_image": 1,
                        "tags": 1,
                    }
                },
                {"$match": {"$and": [filters]}},
                {"$sample": {"size": 1}},
            ]

            # Converting CommandCursor class iterator into a list and
            # then getting the only item in it
            random_quote = list(quote_collection.aggregate(pipeline))
            random_quote["id"] = random_quote["_id"]

            # Create quote schema instance
            quote_schema = QuoteSchema()

            return make_response(
                quote_schema.dump(random_quote), HttpStatus.OK_200.value
            )

        except Exception:
            return (
                {"error": "Could not retrieve quote."},
                HttpStatus.INTERNAL_SERVER_ERROR_500.value,
            )

    def _build_random_quote_filters(self, tags, author):
        """Filter generation for random quote match."""

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
            filters["author_name"] = author

        return filters
