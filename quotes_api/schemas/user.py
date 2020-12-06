from marshmallow import Schema, fields


class UserSchema(Schema):
    username = fields.String()
    email = fields.Email()
    password = fields.String()
    active = fields.Boolean()
    roles = fields.List(fields.String())


class UserResponseSchema(Schema):
    id = fields.String()
    username = fields.String()
    email = fields.Email()
    password = fields.String()
    active = fields.Boolean()
    roles = fields.List(fields.String())

