"""Author schema representation."""

from quotes_api.extensions import ma


class AuthorSchema(ma.Schema):
    """Marshmallow author schema."""

    author_name = ma.String()
