"""User schema representation."""

from quotes_api.extensions import ma


class UserSchema(ma.Schema):
    """User marshmallow schema"""

    id = ma.String(dump_only=True)
    username = ma.String()
    email = ma.Email()
    password = ma.String(load_only=True)
    active = ma.Boolean()
    roles = ma.List(ma.String())
