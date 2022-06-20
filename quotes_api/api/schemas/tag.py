"""Tag schema representation."""

from quotes_api.extensions import ma


class TagSchema(ma.Schema):
    """Marshmallow tag schema."""

    tag = ma.String()
