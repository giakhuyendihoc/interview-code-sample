from marshmallow import fields, validate

from main.enum import RequestStatus

from ..base import BaseSchema


class CancelRequestSchema(BaseSchema):

    status = fields.String(
        required=True, validate=validate.OneOf([RequestStatus.CANCELLED])
    )
