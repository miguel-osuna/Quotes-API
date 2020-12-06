from marshmallow import Schema, fields


class TagSchema(Schema):
    tag = fields.String()
