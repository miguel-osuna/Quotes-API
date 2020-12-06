from marshmallow import Schema, fields


class QuoteSchema(Schema):
    quoteText = fields.String()
    authorName = fields.String()
    authorImage = fields.URL()
    tags = fields.List(fields.String())


class QuoteResponseSchema(Schema):
    id = fields.String()
    quoteText = fields.String()
    authorName = fields.String()
    authorImage = fields.URL()
    tags = fields.List(fields.String())
