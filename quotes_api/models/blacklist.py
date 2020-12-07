import mongoengine
from quotes_api.extensions import odm
from quotes_api.models import User


class TokenBlacklist(odm.Document):
    """ Token blacklist representation. """

    jti = odm.StringField(max_length=36, null=False, unique=True)
    tokenType = odm.StringField(max_length=10, null=False)
    user = odm.ReferenceField(User, null=False, reverse_delete_rule=mongoengine.CASCADE)
    revoked = odm.BooleanField(null=False)
    expires = odm.DateTimeField(null=True)

    def __str__(self):
        return (
            f"JTI: {self.jti}\n"
            f"Token Type: {self.tokenType}\n"
            f"User ID: {self.user.id}\n"
            f"Revoked: {self.revoked}\n"
            f"Expires: {self.expires}\n"
        )

    def __repr__(self):
        return f"<Token {str(self.id)}>"
