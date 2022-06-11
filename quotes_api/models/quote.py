from mongoengine import Document, StringField, ListField

from quotes_api.extensions import odm


class QuoteFields(Document):
    """Quote Document base class."""

    quote_text = StringField(required=True, null=False, unique=True)
    author_name = StringField(required=True, null=False)
    author_image = StringField(required=False, null=False)
    tags = ListField(
        StringField(required=True, null=False),
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
        ],
        "abstract": True,
    }


class Quote(odm.Document, QuoteFields):
    """Quote Document for mongodb database instance."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
