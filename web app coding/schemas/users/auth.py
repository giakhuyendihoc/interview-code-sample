from marshmallow import fields, validate

from ..base import BaseSchema


class UserSignInSchema(BaseSchema):
    email = fields.Email(
        required=True,
        validate=validate.Length(min=1, max=256),
    )
    password = fields.String(
        required=True,
        validate=validate.Length(min=1),
    )
