from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book
from rest_framework.permissions import IsAuthenticated

class BookAPITestCase(APITestCase):
  def setUp(self):
    """
      Setup test env
      Create test user, auth & create demo book data.
    """
    self.user = User.objects.create_user(username='test-user-demo', password='pass1234')
    self.book_data = {
        'title': 'Atomic Habits',
        'author': 'James Clear',
        'publication_year': 2018
    }
    self.book = Book.objects.create(**self.book_data)
    self.url_list = '/api/books/'
    self.url_detail = f'/api/books/{self.book.id}/'
    self.client.login(username='test-user-demo', password='pass1234')

  def test_create_book(self):
    """Test the creation of a book."""
    data = {
        'title': 'Think and Grow Rich',
        'author': 'Napoleon Hill',
        'publication_year': 1937
    }
    response = self.client.post(self.url_list, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response.data['title'], data['title'])
    self.assertEqual(response.data['author'], data['author'])
    self.assertEqual(response.data['publication_year'], data['publication_year'])

  def test_retrieve_books(self):
    """Test retrieving a list of books."""
    response = self.client.get(self.url_list, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)  # At least one book is returned

  def test_retrieve_single_book(self):
    """Test retrieving a single book."""
    response = self.client.get(self.url_detail, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['title'], self.book.title)

  def test_update_book(self):
    """Test updating an existing book."""
    data = {
        'title': 'The Richest Man in Babylon',
        'author': 'George S. Clason',
        'publication_year': 1926
    }
    response = self.client.put(self.url_detail, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.book.refresh_from_db()
    self.assertEqual(self.book.title, data['title'])
    self.assertEqual(self.book.author, data['author'])
    self.assertEqual(self.book.publication_year, data['publication_year'])

  def test_delete_book(self):
    """Test deleting a book."""
    response = self.client.delete(self.url_detail, format='json')
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    # Book is deleted
    self.assertEqual(Book.objects.count(), 0)

  def test_permissions_for_create(self):
    """Test that creating a book is restricted to authenticated users."""
    self.client.logout()
    data = {
        'title': 'The Art of Seduction',
        'author': 'Robert Greene',
        'publication_year': 2001
    }
    response = self.client.post(self.url_list, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  def test_search_books(self):
    """Test searching books by title or author."""
    response = self.client.get(self.url_list, {'search': 'Test'}, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertGreater(len(response.data), 0)  # Ensure some books match the search query

  def test_filter_books(self):
    """Test filtering books by title, author, and publication year."""
    response = self.client.get(self.url_list, {'title': 'The Art of Seduction'}, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)

  def test_ordering_books(self):
    """Test ordering books by title or publication year."""
    response = self.client.get(self.url_list, {'ordering': 'title'}, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertTrue(response.data[0]['title'] <= response.data[-1]['title'])