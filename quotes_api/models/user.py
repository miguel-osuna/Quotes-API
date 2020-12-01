from quotes_api.extensions import odm, pwd_context


class User(odm.Document):
    """ Basic user document. """

    username = odm.StringField(max_lenght=80, unique=True, null=False)
    email = odm.StringField(max_lenght=80, unique=True, null=False)
    password = odm.StringField(max_lenght=255, null=False)
    active = odm.BooleanField(default=True)
    roles = odm.ListField(
        odm.StringField(required=True, null=False),
        required=True,
        null=False,
        default=["basic"],
    )

    def __init__(self, **kwargs):
        """ User initialization with password encryption. """
        super().__init__(**kwargs)
        self.password = pwd_context.hash(self.password)

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

    def to_dict(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "active": self.active,
            "roles": self.roles,
        }

