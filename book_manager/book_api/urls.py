from django.urls import path
from .views import BookListCreateView, BookDetailView, AveragePriceView

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<str:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/average-price-per-year/<int:year>/', AveragePriceView.as_view(), name='average-price'),
]
