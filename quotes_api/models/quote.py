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

    meta = {
        "indexes": [
            {
                "fields": ["$quoteText"],
                "default_language": "english",
                "weights": {"quoteText": 1},
            }
        ]
    }

    def to_dict(self):
        return {
            "id": str(self.id),
            "quoteText": self.quoteText,
            "authorName": self.authorName,
            "authorImage": self.authorImage,
            "tags": self.tags,
        }
