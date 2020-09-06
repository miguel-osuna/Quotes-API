from quotes_api.extensions import odm


class Quote(odm.Document):
    quote_content = odm.StringField(required=True, null=False)
    author_name = odm.StringField(required=True, null=False)
    author_image = odm.StringField(required=False, null=False)
    tags = odm.ListField(odm.StringField(required=True, null=False))
