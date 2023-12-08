from marshmallow import fields, validate

from main.enum import RequestStatus

from ..base import BaseSchema


class Accept_Reject_RequestSchema(BaseSchema):
    status = fields.String(
        required=True,
        validate=validate.OneOf([RequestStatus.APPROVED, RequestStatus.REJECTED]),
    )
    reject_reason = fields.String(
        required=True if status == RequestStatus.REJECTED else False,
        validate=validate.Length(min=1, max=1500),
    )
