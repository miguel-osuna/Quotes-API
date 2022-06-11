from quotes_api.extensions import ma


class TagSchema(ma.Schema):
    tag = ma.String()
