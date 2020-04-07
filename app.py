from flask import Flask, jsonify, request, Response

from bookModel import *
from settings import *
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
    return jsonify({ 'books': books})


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
        new_book = {
                'name': bookObject['name'],
                'price': bookObject['price'],
                'isbn': bookObject['isbn'],
                }
        books.insert(0, new_book)
        response = Response('Post successful', 201, mimetype='application/json')
        response.headers['Location'] = '/books/' + str(new_book['isbn'])
        return response
    else:
        return Response('Invalid book format', 400, mimetype='application/json')

# GET by isbn
@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_val = {}
    for book in books:
        if book['isbn'] == isbn:
            return_val = { 'name': book['name'], 'price': book['price'] }

    return jsonify(return_val)

#PUT
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    req = request.get_json()
    new_book = {
        "name": req['name'],
        "price": req['price'],
        "isbn": isbn
    }
    
    i=0
    for book in books:
        if book['isbn'] == isbn:
            books[i] = new_book
        i+=1
        
    return Response('', 204)

#PATCH
@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    req = request.get_json()
    updated_book = {}
    if 'name' in req:
        updated_book["name"] =  req['name']
    if 'price' in req:
        updated_book["price"]= req['price']
    
    for book in books:
        if book['isbn'] == isbn:
            book.update(updated_book)
        
    res = Response('', status=204)
    res.headers['Location'] = '/books/' + str(isbn)
    return res

#DELETE
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    
    i=0
    for book in books:
        if book['isbn'] == isbn:
            books.pop(i)
            return Response('', 204)
        i+=1
    return Response('', status=404, mimetype='application/json')

app.run(port=5000) 








