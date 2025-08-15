from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework import status

from book.models import Book
from book.views import BookListView, BookDetailView


class BookListViewTestsWithArtificialHTTP(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.book1 = Book.objects.create(title="Test Book 1", author="Test Author 1")
        self.book2 = Book.objects.create(title="Test Book 2", author="Test Author 2")

    def test_get_list(self):
        url = reverse("book-list")
        request = self.factory.get(url)
        view = BookListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'Test Book 1')
        self.assertEqual(response.data[1]['title'], 'Test Book 2')

    def test_get_detail(self):
        url = reverse("book-detail", kwargs={'pk': self.book1.pk})
        request = self.factory.get(url)
        view = BookDetailView.as_view()
        response = view(request, pk=self.book1.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Book 1")  
        self.assertEqual(response.data['author'], "Test Author 1")

    def test_post_create(self):
        url = reverse("book-list")
        data = {"title": "New Book", "author": "New Author"}
        request = self.factory.post(url, data, format="json")
        view = BookListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        new_book = Book.objects.get(title='New Book')
        self.assertEqual(new_book.author, 'New Author')


    def test_put_update(self):
        url = reverse("book-detail", kwargs={'pk': self.book1.pk})
        data = {"title": "Updated Book", "author": "Updated Author"}
        request = self.factory.put(url, data, format="json")
        view = BookDetailView.as_view()
        response = view(request, pk=self.book1.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Book")
        self.assertEqual(self.book1.author, "Updated Author")

    def test_delete_destroy(self):
        url = reverse("book-detail", kwargs={'pk': self.book1.pk})
        request = self.factory.delete(url)
        view = BookDetailView.as_view()
        response = view(request, pk=self.book1.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)


class BookListViewTestsWithRealHTTP(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book1 = Book.objects.create(title="Test Book 1", author="Test Author 1")
        self.book2 = Book.objects.create(title="Test Book 2", author="Test Author 2")

    def test_get_list(self):
        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'Test Book 1')
        self.assertEqual(response.data[1]['title'], 'Test Book 2')

    def test_get_detail(self):
        url = reverse("book-detail", kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Book 1")
        self.assertEqual(response.data['author'], "Test Author 1")

    def test_post_create(self):
        url = reverse("book-list")
        data = {"title": "New Book", "author": "New Author"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        new_book = Book.objects.get(title='New Book')
        self.assertEqual(new_book.author, 'New Author')

    def test_put_update(self):
        url = reverse("book-detail", kwargs={'pk': self.book1.pk})
        data = {"title": "Updated Book", "author": "Updated Author"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Book")
        self.assertEqual(self.book1.author, "Updated Author")

    def test_delete_destroy(self):
        url = reverse("book-detail", kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)