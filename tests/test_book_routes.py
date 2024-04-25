import unittest
from flask import json
from app import create_app

class BookTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test variables. This method will run before every test."""
        self.app = create_app('testing')
        self.client = self.app.test_client()

        # This is a simple in-memory structure to store books during tests.
        self.app.books = {}

        # Example book data
        self.book_data = {
            'title': '1984',
            'author': 'George Orwell',
            'price': 20,
            'category': 'Dystopian',
            'publication_year': '1949-06-08'
        }

    def test_get_books(self):
        """Test API can get all books (GET request)."""
        res = self.client.get('/books')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(json.loads(res.data)), 2)  

    def test_create_book(self):
        """Test API can create a book (POST request)."""
        res = self.client.post('/books', json=self.book_data)
        self.assertEqual(res.status_code, 201)
        self.assertIn('1984', str(res.data))

    def test_get_book(self):
        """Test API can get a single book by its ID (GET request)."""
        # Create a book first
        res = self.client.post('/books', json=self.book_data)
        self.assertEqual(res.status_code, 201)
        book_id = json.loads(res.data)['id']

        # Retrieve the book
        res = self.client.get(f'/books/{book_id}')
        self.assertEqual(res.status_code, 200)
        self.assertIn('1984', str(res.data))


    def test_delete_book(self):
        """Test API can delete an existing book (DELETE request)."""
        # Create a book first
        res = self.client.post('/books', json=self.book_data)
        self.assertEqual(res.status_code, 201)
        book_id = json.loads(res.data)['id']

        # Delete the book
        res = self.client.delete(f'/books/{book_id}')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Book deleted successfully', str(res.data))

        # Try to get the deleted book
        res = self.client.get(f'/books/{book_id}')
        self.assertEqual(res.status_code, 404)

    def tearDown(self):
        """Tear down all initialized variables."""
        pass

# Running the tests
if __name__ == "__main__":
    unittest.main()
