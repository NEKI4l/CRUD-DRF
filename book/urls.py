from django.urls import path

from book import views

urlpatterns = [
    path('', views.books_list, name='books_list'),
    path('<int:id>/', views.book_detail, name='book_detail')
]