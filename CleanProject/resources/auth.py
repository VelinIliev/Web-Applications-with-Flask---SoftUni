from flask import request
from flask_restful import Resource

from app import db
from models import User
from schemas.request_scheams.users import UserRegisterRequestSchema
from utils.decorators import validate_schema


class RegisterResource(Resource):
    @validate_schema(UserRegisterRequestSchema)
    def post(self):
        data = request.get_json()
        user = User(**data)
        db.session.add(user)
        db.session.commit()