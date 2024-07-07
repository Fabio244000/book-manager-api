from datetime import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from pymongo import MongoClient


class Command(BaseCommand):
    help = 'Insert initial data into MongoDB'

    def handle(self, *args, **kwargs):
        client = MongoClient('mongodb://db:27017/')
        db = client.book_db
        book_collection = db.books

        books = [
            {
                "title": "Book Title 1",
                "author": "Author Name 1",
                "published_date": datetime(2022, 1, 1),
                "genre": "Fiction",
                "price": float(Decimal("19.99"))
            },
            {
                "title": "Book Title 2",
                "author": "Author Name 2",
                "published_date": datetime(2022, 2, 2),
                "genre": "Non-Fiction",
                "price": float(Decimal("29.99"))
            },
            {
                "title": "Book Title 3",
                "author": "Author Name 3",
                "published_date": datetime(2023, 3, 3),
                "genre": "Science Fiction",
                "price": float(Decimal("39.99"))
            },
            {
                "title": "Book Title 4",
                "author": "Author Name 4",
                "published_date": datetime(2023, 4, 4),
                "genre": "Fantasy",
                "price": float(Decimal("49.99"))
            },
            {
                "title": "Book Title 5",
                "author": "Author Name 5",
                "published_date": datetime(2025, 5, 5),
                "genre": "Mystery",
                "price": float(Decimal("59.99"))
            }
        ]

        for book in books:
            book_collection.insert_one(book)

        self.stdout.write(self.style.SUCCESS('Datos iniciales insertados correctamente.'))
