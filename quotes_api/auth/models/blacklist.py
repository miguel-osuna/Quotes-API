"""Black list model file"""

from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    BooleanField,
    DateTimeField,
    CASCADE,
)

from quotes_api.extensions import odm
from quotes_api.auth.models import UserFields


class TokenBlacklistFields(Document):
    """Token blacklist base class representation."""

    jti = StringField(max_length=36, null=False, unique=True)
    token_type = StringField(max_length=10, null=False)
    user = ReferenceField(UserFields, null=False, reverse_delete_rule=CASCADE)
    revoked = BooleanField(null=False)
    expires = DateTimeField(null=True)

    def __str__(self):
        return (
            f"JTI: {self.jti}\n"
            f"Token Type: {self.token_type}\n"
            f"User ID: {self.user.id}\n"
            f"Revoked: {self.revoked}\n"
            f"Expires: {self.expires}\n"
        )

    def __repr__(self):
        return f"<Token {str(self.id)}>"

    meta = {"abstract": True}


class TokenBlacklist(odm.Document, TokenBlacklistFields):
    """Token blacklist Document for mongodb database instance."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
