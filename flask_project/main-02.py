from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class BookModel:
    def __init__(self, id_, title, author):
        self.id = id_
        self.title = title
        self.author = author

    def serialize(self):
        return {'id': self.id, 'title': self.title, 'author': self.author}


books = [BookModel(i, f'Title{i}', f'Author{i}') for i in range(1, 11)]

print(books)


class BooksResource(Resource):
    def get(self):
        return {'books':  [book.serialize() for book in books]}

    def post(self):
        data = request.get_json()
        last_id = len(books) - 1
        data['id_'] = last_id + 1
        new_book = BookModel(**data)
        books.append(new_book)
        return new_book.serialize(), 201


class BookResource(Resource):
    def get_single_book(self, pk):
        book = [book for book in books if book.id == pk]
        if book:
            return book[0]
        return None

    def get(self, pk):
        book = self.get_single_book(pk)
        if not book:
            return {'message': 'Book not found'}, 400
        return book.serialize(), 200

    def put(self, pk):
        book = self.get_single_book(pk)
        if not book:
            return {'message': 'Book not found'}, 400
        data = request.get_json()
        book.author = data['author']
        book.title = data['title']
        return book.serialize(), 200

    def delete(self, pk):
        book = self.get_single_book(pk)
        if not book:
            return {'message': 'Book not found'}, 400

        books.remove(book)
        return {"message": "OK"}, 200


api.add_resource(BooksResource, '/books')
api.add_resource(BookResource, '/books/<int:pk>')


if __name__ == '__main__':
    app.run(debug=True)