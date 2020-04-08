from flask import Flask, jsonify, request, Response

from BookModel import Book
from settings import app
import json

books = [
    {
        'name': 'Green Eggs and Ham',
        'price': 7.99,
        'isbn': 978039400165
    },
    {
        'name': 'The Cat in the Hat',
        'price': 6.99,
        'isbn': 9782371000193
    }
]


# GET
@app.route('/books')
def get_books():
    return jsonify({ 'books': Book.get_all_books()})

# GET by isbn
@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_val = Book.get_book(isbn)

    return jsonify(return_val)

def validBookObject(bookObject):
    if ('name' in bookObject and 
        'price' in bookObject and 
        'isbn' in bookObject):
        return True
    else:
        return False
    
#POST /books   
@app.route('/books', methods=['POST'])
def add_book():
    bookObject = request.get_json()
    if validBookObject(bookObject):
        Book.add_book(bookObject['name'],bookObject['price'],bookObject['isbn'])
        response = Response('Post successful', 201, mimetype='application/json')
        response.headers['Location'] = '/books/' + str(bookObject['isbn'])
        return response
    else:
        return Response('Invalid book format', 400, mimetype='application/json')

#PUT
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    req = request.get_json()
    Book.replace_book(isbn, req['name'], req['price'])
        
    return Response('', 204)

#PATCH
@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    req = request.get_json()

    if 'name' in req:
        Book.update_book_name(isbn, req['name'])
    if 'price' in req:
        Book.update_book_price(isbn, req['price'])
        
    res = Response('', status=204)
    res.headers['Location'] = '/books/' + str(isbn)
    return res

#DELETE
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    
    if Book.delete_book(isbn):
        return Response('', 204)
    
    return Response('', status=404, mimetype='application/json')

app.run(port=5000) 








