from flask import Blueprint, request, jsonify, abort
import uuid
from datetime import datetime

book_bp = Blueprint('book_bp', __name__)

# In-memory data storage
books = {}

# Helper function to create book ID
def generate_uuid():
    return str(uuid.uuid4())

# Helper function to parse date
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None

@book_bp.route('/books', methods=['GET'])
def get_books():
    return jsonify(list(books.values())), 200

@book_bp.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):
    if book_id in books:
        return jsonify(books[book_id]), 200
    abort(404, description="Book not found")

@book_bp.route('/books', methods=['POST'])
def create_book():
    data = request.json
    if not data or 'title' not in data or 'author' not in data or 'price' not in data or 'category' not in data or 'publication_year' not in data:
        abort(400, description="Missing book data in request")
    book_id = generate_uuid()
    book = {
        'id': book_id,
        'title': data['title'],
        'author': data['author'],
        'price': data['price'],
        'category': data['category'],
        'publication_year': parse_date(data['publication_year'])
    }
    if not book['publication_year']:
        abort(400, description="Invalid publication year format. Use YYYY-MM-DD.")
    books[book_id] = book
    return jsonify(book), 201

@book_bp.route('/books/<book_id>', methods=['PUT'])
def update_book(book_id):
    if book_id not in books:
        abort(404, description="Book not found")
    data = request.json
    if not data:
        abort(400, description="Bad request")
    book = books[book_id]
    book['title'] = data.get('title', book['title'])
    book['author'] = data.get('author', book['author'])
    book['price'] = data.get('price', book['price'])
    book['category'] = data.get('category', book['category'])
    new_date = parse_date(data.get('publication_year', book['publication_year']))
    if not new_date:
        abort(400, description="Invalid publication year format. Use YYYY-MM-DD.")
    book['publication_year'] = new_date
    return jsonify(book)

@book_bp.route('/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    if book_id in books:
        del books[book_id]
        return jsonify({'message': 'Book deleted successfully'}), 200
    abort(404, description="Book not found")
