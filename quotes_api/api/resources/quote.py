from flask import request, jsonify, make_response, url_for
from flask_restful import Resource

from quotes_api.models import Quote
from quotes_api.common import HttpStatus, paginator
from quotes_api.api.schemas import QuoteSchema
from quotes_api.auth.decorators import user_required, admin_required


class QuoteResource(Resource):
    """ Single quote object resource. 
    
    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: quote_id
          schema: 
            type: integer
          description: Quote ID
      responses:
        200:
          content:
            application/json:
              schema:
                type: object 
                properties:
                  quote: QuoteSchema
        404:
          description: Quote does not exist

    put:
      tags:
        - api
      parameters:
        - in: path
          name: quote_id
          schema:
            type: integer
          description: Quote ID
      requestBody:
        content: 
          application/json:
            schema:
              QuoteSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object 
                properties:
                  message:
                    type: string
                    example: Quote updated
                  quote: QuoteSchema
        404:
          description: Quote does not exist

    patch:
      tags:
        - api
      parameters:
        - in: path
          name: quote_id
          schema:
            type: integer
          description: Quote ID
      requestBody:
        content: 
          application/json:
            schema:
              QuoteSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object 
                properties:
                  message:
                    type: string
                    example: Quote updated
                  quote: QuoteSchema
        404:
          description: Quote does not exist

    delete:
      tags:
        - api
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
          description: Quote ID
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: User deleted
        404:
          description: User does not exist
    """

    # Decorators applied to all class methods
    method_decorators = []

    # @doc(description="Get quote resource by id.", tags=["Quote"])
    @user_required
    def get(self, quote_id):
        """ Get quote by id. """
        try:
            quote = Quote.objects.get_or_404(id=quote_id)
        except:
            return (
                {"error": "Quote does not exist."},
                HttpStatus.not_found_404.value,
            )
        quote_schema = QuoteSchema()
        return make_response(quote_schema.dump(quote), HttpStatus.ok_200.value)

    # @doc(description="Update quote resource by id.", tags=["Quote"])
    @admin_required
    def put(self, quote_id):
        """ Replace entire quote. """
        try:
            quote = Quote.objects.get_or_404(id=quote_id)
        except:
            return {"error": "Qutoe does not exist."}
        try:
            # Create quote schema instance
            quote_schema = QuoteSchema()

            data = quote_schema.load(request.json)
            quote.update(**data)
            quote.save()

            return "", HttpStatus.no_content_204.value
        except:
            return (
                {"error": "Missing data."},
                HttpStatus.bad_request_400.value,
            )

    # @doc(description="Patch quote resource by id.", tags=["Quote"])
    @admin_required
    def patch(self, quote_id):
        """ Update quote fields. """
        try:
            quote = Quote.objects.get_or_404(id=quote_id)
        except:
            return (
                {"error": "Quote does not exist."},
                HttpStatus.not_found_404.value,
            )
        try:
            # Check quote schema instance
            quote_schema = QuoteSchema(partial=True)

            data = quote_schema.load(request.json)
            quote.update(**data)
            quote.save()

            return "", HttpStatus.no_content_204.value
        except:
            return {"error": "Missing data."}, HttpStatus.bad_request_400.value

    # @doc(description="Delete quote resource by id.", tags=["Quote"])
    @admin_required
    def delete(self, quote_id):
        """ Delete quote. """
        try:
            quote = Quote.objects.get_or_404(id=quote_id)
        except:
            return (
                {"error": "Quote does not exist."},
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
    """ Quote object list. 
    
    ---
    get:
      tags:
        - api
      parameters:
        - in: query
          name: page
          schema:
            type: integer
          description: Page number for pagination
        - in: query
          name: per_page
          schema:
            type: integer 
          description: Number of results per page
        - in: query
          name: tags
          schema: 
            type: string
          description: Quote tags for filtering
        - in: query
          name: author
          schema:
            type: string
          description: Author name for filtering
        - in: query
          name: query
          schema:
            type: string
          description: Query for quote search
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/MetadataSchema'
                  - type: object
                    properties:
                      type: array
                      items:
                        $ref: '#/components/schemas/QuoteSchema'
    post:
      tags:
        - api
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
                    message:
                      type: string
                      example: Quote created
                    quote: QuoteSchema
    """

    # Decorators applied to all class methods
    method_decorators = []

    # @doc(description="Get a list of quote resources.", tags=["Quote"])
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
            response_body = paginator(pagination, "api.quotes", QuoteSchema)
            return make_response(response_body, HttpStatus.ok_200.value)

        except Exception as e:
            return (
                {"error": "Could not retrieve quotes.", "detail": str(e)},
                HttpStatus.internal_server_error_500.value,
            )

    # @doc(description="Create a quote resource.", tags=["Quote"])
    @admin_required
    def post(self):
        """ Create new quote. """
        try:
            # Create quote schema instace
            quote_schema = QuoteSchema()
            data = quote_schema.load(request.json)
        except:
            return {"error": "Missing data."}, HttpStatus.bad_request_400.value
        try:
            # Create new database entry
            quote = Quote(**data)
            quote.save()

            # Create new quote schema instance that only dumps the id
            quote_schema = QuoteSchema(only=["id"])
            return make_response(quote_schema.dump(quote), HttpStatus.created_201.value)

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
    """ Random quote object. 
    
    ---
    get:
      tags:
        - api
      parameters:
        - in: query
          name: tags
          schema:
            type: string
          description: Quote tags for filtering
        - in: query
          name: author
          schema:
            type: Author name for filtering
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  quote: QuoteSchema
        500:
          description: Could not retrieve quote

    """

    # Decorators applied to all class methods
    method_decorators = []

    # @doc(description="Get a random quote resource.", tags=["Quote"])
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

            # Create quote schema instance
            quote_schema = QuoteSchema()

            return make_response(
                quote_schema.dump(random_quote), HttpStatus.ok_200.value
            )

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

