from decouple import config
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = \
    f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}@localhost:{config('DB_PORT')}/{config('DB_NAME')}"
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)


class BookModel(db.Model):
    __tablename__ = 'books'
    pk = db.Column(db.Integer, primary_key=True,)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    reader_pk = db.Column(db.Integer, db.ForeignKey('readers.pk'))
    reader = db.relationship('ReaderModel')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ReaderModel(db.Model):
    __tablename__ = 'readers'
    pk = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    books = db.relationship("BookModel", backref='book', lazy='dynamic')


class BookResource(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        reader_pk = data.pop("reader_pk")
        book = BookModel(**data)
        book.reader_pk = reader_pk
        db.session.add(book)
        db.session.commit()
        return book.as_dict()


api.add_resource(BookResource, "/books/")

if __name__ == '__main__':
    app.run()
