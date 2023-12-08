from flask import jsonify
from marshmallow import EXCLUDE, Schema, fields, pre_load

from main.libs.utils import strip_strings_recursively


class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    def jsonify(self, obj, many=False):
        return jsonify(self.dump(obj, many=many))

    @pre_load
    def strip_strings(self, data, **__):
        """
        Strip all strings in the input before serializing.
        """
        return strip_strings_recursively(data)


class PaginationSchema(BaseSchema):
    items_per_page = fields.Integer()
    page = fields.Integer()
    total_items = fields.Integer()
