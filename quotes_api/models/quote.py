from quotes_api.extensions import odm


class Quote(odm.Document):
    quote_text = odm.StringField(required=True, null=False, unique=True)
    author_name = odm.StringField(required=True, null=False)
    author_image = odm.StringField(required=False, null=False)
    tags = odm.ListField(
        odm.StringField(required=True, null=False),
        required=True,
        null=False,
        default=["other"],
    )

    def __str__(self):
        return (
            f"Quote: {self.quote_text}\n"
            f"Author: {self.author_name}\n"
            f"Image: {self.author_image}\n"
            f"tags: {self.tags}\n"
        )

    def __repr__(self):
        return f"<Quote {str(self.id)}>"

    meta = {
        "indexes": [
            {
                "fields": ["$quote_text"],
                "default_language": "english",
                "weights": {"quote_text": 1},
            }
        ]
    }
