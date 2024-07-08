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
                "title": "Fictional Reality",
                "author": "Alice Johnson",
                "published_date": "2024-02-10",
                "genre": "Fiction",
                "price": 22.99
            },
            {
                "title": "Adventures in the Unknown",
                "author": "Michael Brown",
                "published_date": "2023-03-07",
                "genre": "Adventure",
                "price": 17.25
            },
            {
                "title": "The Fictional Universe",
                "author": "Emily Davis",
                "published_date": "2022-11-11",
                "genre": "Fiction",
                "price": 20.00
            },
            {
                "title": "The Enchanted Forest",
                "author": "George Martin",
                "published_date": "2022-04-18",
                "genre": "Adventure",
                "price": 16.75
            },
            {
                "title": "Whispers of the Past",
                "author": "Laura Thompson",
                "published_date": "2022-09-29",
                "genre": "Fiction",
                "price": 19.85
            }
        ]

        for book in books:
            book_collection.insert_one(book)

        self.stdout.write(self.style.SUCCESS('Datos iniciales insertados correctamente.'))
