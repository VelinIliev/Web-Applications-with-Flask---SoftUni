from marshmallow import Schema, fields

from models import State
from schemas.base import ComplaintBaseSchema


class ComplaintResponseSchema(ComplaintBaseSchema):
    id = fields.Integer(required=True)
    create_at = fields.DateTime(required=True)
    status = fields.Enum(State, by_value=True)
    user_id = fields.Integer(required=True)
    # TODO: nest user inside the schema


class ComplaintsResponseSchema(ComplaintBaseSchema):
    # TODO: make schema work without list of complaints schema
    complaints = fields.Nested(ComplaintResponseSchema, many=True)
