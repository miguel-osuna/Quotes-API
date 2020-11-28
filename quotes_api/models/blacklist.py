import mongoengine
from quotes_api.extensions import odm
from quotes_api.models import User


class TokenBlacklist(odm.Document):
    """ Token blacklist representation. """

    jti = odm.StringField(max_length=36, null=False, unique=True)
    tokenType = odm.StringField(max_length=10, null=False)
    user = odm.ReferenceField(User, null=False, reverse_delete_rule=mongoengine.CASCADE)
    revoked = odm.BooleanField(null=False)
    expires = odm.DateTimeField(null=False)

    def to_dict(self):
        return {
            "id": str(self.id),
            "jit": self.jit,
            "tokenType": self.tokenType,
            "user": str(self.user.id),
            "revoked": self.revoked,
            "expires": self.expires,
        }

