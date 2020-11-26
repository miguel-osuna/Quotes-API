from quotes_api.extensions import odm


class Quote(odm.Document):
    quoteText = odm.StringField(required=True, null=False, unique=True)
    authorName = odm.StringField(required=True, null=False)
    authorImage = odm.StringField(required=False, null=False)
    tags = odm.ListField(
        odm.StringField(required=True, null=False),
        required=True,
        null=False,
        default=["other"],
    )
