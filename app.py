from flask import Flask, jsonify, request, Response
from BookModel import Book
from UserModel import User
from settings import app
from functools import wraps
import json
import jwt, datetime


app.config['SECRET_KEY'] = 'meow'

books = Book.get_all_books()

@app.route('/login', methods=['POST'])
def get_token():
    req = request.get_json()
    username = str(req['username'])
    password = str(req['password'])
    
    match = User.username_password_match(username, password)
    
    if match:
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds = 100)
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        return Response('', 401, mimetype='application/json')

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except:
            return jsonify({'error': 'Need valid token'}), 401
    return wrapper



# GET
@app.route('/books')
def get_books():
    return jsonify({ 'books': books})

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
@token_required
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
@token_required
def replace_book(isbn):
    req = request.get_json()
    Book.replace_book(isbn, req['name'], req['price'])
        
    return Response('', 204)

#PATCH
@app.route('/books/<int:isbn>', methods=['PATCH'])
@token_required
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
@token_required
def delete_book(isbn):
    
    if Book.delete_book(isbn):
        return Response('', 204)
    
    return Response('', status=404, mimetype='application/json')

app.run(port=5000) 








