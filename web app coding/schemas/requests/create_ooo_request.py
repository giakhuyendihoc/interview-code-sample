from marshmallow import fields, validate

from main.enum import ContactMethod

from ..base import BaseSchema


class CreateRequestSchema(BaseSchema):
    start_date = fields.DateTime(
        required=True,
    )
    end_date = fields.DateTime(
        required=True,
    )
    pic_id = fields.Integer(required=False)
    contact_methods = fields.List(
        fields.String(validate=validate.OneOf(ContactMethod.get_list())),
        required=True,
    )
    purpose = fields.String(
        required=True,
        validate=validate.Length(min=1, max=1500),
    )
