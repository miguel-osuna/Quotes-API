"""Quote schema representation."""

from quotes_api.extensions import ma


class QuoteSchema(ma.Schema):
    """Marshmallow quote schema."""

    id = ma.String(dump_only=True)
    quote_text = ma.String(required=True)
    author_name = ma.String(required=True)
    author_image = ma.URL()
    tags = ma.List(ma.String(required=True))
