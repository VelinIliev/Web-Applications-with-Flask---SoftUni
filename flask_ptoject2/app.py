from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_migrate import Migrate
from decouple import config

# initialise app Flask
app = Flask(__name__)

# setup database
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{config("DB_USER")}:{config("DB_PASSWORD")}' \
                                        f'@localhost:{config("DB_PORT")}/{config("DB_NAME")}'

# setup SQLAlchemy
db = SQLAlchemy(app)

# setup API
api = Api(app)

# setup migrations
migrate = Migrate(app, db)


# define and creating Models (tables)
class BookModel(db.Model):
    # define table name:
    __tablename__ = 'books'
    # define primary key: pk INT PRIMARY KEY
    pk = db.Column(db.Integer, primary_key=True)
    # define title: title VARCHAR NOT NULL
    title = db.Column(db.String, nullable=False)
    # define author: title VARCHAR NOT NULL
    author = db.Column(db.String, nullable=False)
    # define reader foreign key : reader_pk INT FOREIGN KEY REFERENCES readers(pk)
    reader_pk = db.Column(db.Integer, db.ForeignKey('readers.pk'))

    # serialise JSON:
    def as_dict(self):
        return f"<{self.pk}> {self.title} from {self.author}"


class ReaderModel(db.Model):
    __tablename__ = 'readers'
    pk = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)
    # display books of the reader, only when asked(lazy)
    books = db.relationship("BookModel", backref='book', lazy='dynamic')


# receiving data and put in tables
class BookResource(Resource):
    # create entry in table
    def post(self):
        # get data
        data = request.get_json()
        reader_pk = data.pop('reader_pk')
        new_book = BookModel(**data)
        new_book.reader_pk = reader_pk
        # insert to database
        db.session.add(new_book)
        db.session.commit()
        return new_book.as_dict()


# setup end-point
api.add_resource(BookResource, '/books/')

if __name__ == '__main__':
    app.run(debug=True)
