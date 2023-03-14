import enum
from datetime import datetime, timedelta

import jwt
from decouple import config
from flask import Flask, request
from flask_httpauth import HTTPTokenAuth
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from jwt import DecodeError, InvalidSignatureError
from marshmallow import Schema, fields, validate, ValidationError
from marshmallow_enum import EnumField
from password_strength import PasswordPolicy
from werkzeug.exceptions import BadRequest, InternalServerError, Forbidden
from werkzeug.security import generate_password_hash

app = Flask(__name__)

db_user = config('DB_USER')
db_password = config("DB_PASSWORD")
db_port = config("DB_PORT")
db_name = config("DB_NAME")

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@localhost:{db_port}/{db_name}'

db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)


auth = HTTPTokenAuth(scheme='Bearer')


# authentication decorator
def permission_required(permissions_needed):
    def decorated_func(func):
        def wrapper(*args, **kwargs):
            if auth.current_user().role in permissions_needed:
                return func(*args, **kwargs)
            raise Forbidden("You have permission to access this resource")
        return wrapper
    return decorated_func


def validate_schema(schema_name):
    def decorated_func(func):
        def wrapper(*args, **kwargs):
            data = request.get_json()
            schema = schema_name()
            errors = schema.validate(data)
            if not errors:
                return func(*args, **kwargs)
            raise BadRequest(errors)
        return wrapper
    return decorated_func


@auth.verify_token
def verify_token(token):
    token_decode_data = User.decode_token(token)
    # SELECT * FROM USERS WHERE id = token_decoded_id
    user = User.query.filter_by(id=token_decode_data["sub"]).first()
    return user


class UserRolesEnum(enum.Enum):
    super_admin = 'super admin'
    admin = 'admin'
    user = 'user'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.Text)
    role = db.Column(
        db.Enum(UserRolesEnum),
        server_default=UserRolesEnum.user.name,
        nullable=False
    )
    # USE UTC instead of datetime.now()
    create_on = db.Column(db.DateTime, default=datetime.utcnow())
    updated_on = db.Column(db.DateTime, onupdate=datetime.utcnow())

    # create token
    def encode_token(self):
        payload = {
            "sub": self.id,
            "exp": datetime.utcnow() + timedelta(days=2)
        }
        return jwt.encode(payload, key=config('SECRET_KEY'), algorithm="HS256")

    # decode token
    @staticmethod
    def decode_token(token):
        try:
            return jwt.decode(token, key=config('SECRET_KEY'), algorithms=["HS256"])
        except (DecodeError, InvalidSignatureError) as ex:
            raise BadRequest("Invalid or missing token")
        except Exception:
            raise InternalServerError("Something went wrong")


# drop down menu (predefine values)
class ColorEnum(enum.Enum):
    pink = "pink"
    black = "black"
    white = "white"
    yellow = "yellow"


# drop down menu (predefine values)
class SizeEnum(enum.Enum):
    xs = "xs"
    s = "s"
    m = "m"
    l = "l"
    xl = "xl"
    xxl = "xxl"


class Clothes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    color = db.Column(
        db.Enum(ColorEnum),
        default=ColorEnum.white,
        nullable=False
    )
    size = db.Column(
        db.Enum(SizeEnum),
        default=SizeEnum.s,
        nullable=False
    )
    photo = db.Column(db.String(255), nullable=False)
    create_on = db.Column(db.DateTime, default=datetime.utcnow())
    updated_on = db.Column(db.DateTime, onupdate=datetime.utcnow())


# Many-to-many table
users_clothes = db.Table(
    "users_clothes",
    db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("clothes_id", db.Integer, db.ForeignKey("clothes.id")),
)


# custom validator function
def validate_name(name):
    try:
        first_name, last_name = name.split()
    except ValueError:
        # always raise Validation Error
        raise ValidationError('At least two names are required')


# define password check parameters
policy = PasswordPolicy.from_names(
    uppercase=1,  # need min. 1 uppercase letters
    numbers=1,  # need min. 1 digits
    special=1,  # need min. 1 special characters
    nonletters=1,  # need min. 1 non-letter characters (digits, specials, anything)
)


def validate_password(value):
    errors = policy.test(value)
    if errors:
        raise ValidationError(f"Not a valid password. Password must contains at least:"
                              f"one uppercase letter, one number and one special character")


class BaseUserSchema(Schema):
    # check for valid email
    email = fields.Email(required=True)
    # check for name with function
    full_name = fields.String(required=True, validate=validate.And(validate.Length(min=3, max=255), validate_name))

    # # check for name with method
    # full_name = fields.String(
    #     required=True
    # )

    # # custom validator method
    # @validates('full_name')
    # def validate_name(self, name):
    #     if len(name) < 3 or len(name) > 255:
    #         raise ValidationError('Length must be between 3 and 255.')
    #     try:
    #         first_name, last_name = name.split()
    #     except ValueError:
    #         # always raise Validation Error
    #         raise ValidationError('At least two names are required')


class UserSignInSchema(BaseUserSchema):
    # check password
    password = fields.String(required=True, validate=validate.And(validate.Length(min=3, max=20), validate_password))


# return object
class UserOutSchema(BaseUserSchema):
    id = fields.Integer()


class SingleClothSchemaBase(Schema):
    name = fields.String(required=True)
    color = EnumField(ColorEnum, by_value=True)
    size = EnumField(SizeEnum, by_value=True)


class SingleClothSchemaIn(SingleClothSchemaBase):
    photo = fields.String(required=True)


class SingleClothSchemaOut(SingleClothSchemaBase):
    id = fields.Integer()
    create_on = fields.DateTime()
    updated_on = fields.DateTime()


class UserRegisterResource(Resource):
    @validate_schema(UserSignInSchema)
    def post(self):
        data = request.get_json()
        data['password'] = generate_password_hash(data['password'], 'sha256')
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return {"token": user.encode_token()}


class ClothesResource(Resource):
    @auth.login_required
    @permission_required([UserRolesEnum.user, UserRolesEnum.admin, UserRolesEnum.super_admin])
    def post(self):
        data = request.get_json()
        schema = SingleClothSchemaIn()
        errors = schema.validate(data)
        if errors:
            return errors
        clothes = Clothes(**data)
        db.session.add(clothes)
        db.session.commit()
        return SingleClothSchemaOut().dump(clothes)


api.add_resource(UserRegisterResource, '/register/')
api.add_resource(ClothesResource, '/clothes/')


if __name__ == "__main__":
    app.run(debug=True)
