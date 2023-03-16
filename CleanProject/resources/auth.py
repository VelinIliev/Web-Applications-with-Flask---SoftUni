from flask import request
from flask_restful import Resource
from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash

from managers.auth import AuthManager
from models import User
from schemas.request_scheams.users import UserRegisterRequestSchema, UserLoginRequestSchema
from schemas.response_schemas.users import UserAuthResponseSchema
from utils.decorators import validate_schema


class RegisterResource(Resource):
    @validate_schema(UserRegisterRequestSchema)
    def post(self):
        data = request.get_json()
        user = AuthManager.create_user(data)
        token = AuthManager.encode_token(user)
        return UserAuthResponseSchema().dump({"token": token})


class LoginResource(Resource):
    @validate_schema(UserLoginRequestSchema)
    def post(self):
        data = request.get_json()
        user = AuthManager.login_user(data)
        token = AuthManager.encode_token(user)
        return UserAuthResponseSchema().dump({"token": token})
