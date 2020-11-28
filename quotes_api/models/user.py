from quotes_api.extensions import odm, pwd_context


class User(odm.Document):
    """ Basic user document. """

    username = odm.StringField(max_lenght=80, unique=True, null=False)
    email = odm.StringField(max_lenght=80, unique=True, null=False)
    password = odm.StringField(max_lenght=255, null=False)
    active = odm.BooleanField(default=True)

    def __init__(self, **kwargs):
        """ User initialization with password encryption. """
        super().__init__(**kwargs)
        self.password = pwd_context.hash(self.password)

    def __repr__(self):
        return "<User {}>".format(self.username)

    def to_dict(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "active": self.active,
        }

