from marshmallow import Schema, fields


def AuthorSchema(Schema):
    authorName = fields.String()
    authorImage = fields.Image()
