from quotes_api.extensions import ma


class AuthorSchema(ma.Schema):
    author_name = ma.String()
