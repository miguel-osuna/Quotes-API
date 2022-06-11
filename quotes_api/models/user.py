from mongoengine import Document, StringField, BooleanField, ListField

from quotes_api.extensions import odm, pwd_context


class UserFields(Document):
    """User Document base class."""

    username = StringField(max_lenght=80, unique=True, null=False)
    email = StringField(max_lenght=80, unique=True, null=False)
    password = StringField(max_lenght=255, null=False)
    active = BooleanField(default=True)
    roles = ListField(
        StringField(required=True, null=False),
        required=True,
        null=False,
        default=["basic"],
    )

    def __str__(self):
        return (
            f"Username: {self.username}\n"
            f"Email: {self.email}\n"
            f"Password: {self.password}\n"
            f"Active: {self.active}\n"
            f"Roles: {self.roles}\n"
        )

    def __repr__(self):
        return f"<User {str(self.id)}>"

    meta = {"abstract": True}


class User(odm.Document, UserFields):
    """User Document for mongodb database instance."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
