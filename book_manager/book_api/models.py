from datetime import datetime, date
from decimal import Decimal
from bson.objectid import ObjectId
from db.mongodb import MongoDBClient


class Book:
    """
    The Book class represents a book in the MongoDB collection.

    Attributes:
        title (str): The title of the book.
        author (str): The author of the book.
        published_date (date): The publication date of the book.
        genre (str): The genre of the book.
        price (Decimal): The price of the book.
        id (str, optional): The ID of the book in the database.
    """
    def __init__(self, title, author, published_date, genre, price, book_id = None):
        self.title = title
        self.author = author
        self.published_date = self.parse_date(published_date)
        self.genre = genre
        self.price = price
        self.id = str(book_id) if book_id else None

    def parse_date(self, date_str):
        if isinstance(date_str, str):
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        elif isinstance(date_str, datetime):
            return date_str.date()
        return date_str

    def to_dict(self):
        data = {
            "title": self.title,
            "author": self.author,
            "published_date": datetime.combine(self.published_date, datetime.min.time())
            if isinstance(self.published_date, date)
            else self.published_date,
            "genre": self.genre,
            "price": float(self.price) if isinstance(self.price, Decimal) else self.price
        }
        if self.id:
            data["_id"] = ObjectId(self.id)
        return data

    @staticmethod
    def from_dict(data):
        book = Book(
            title=data.get('title'),
            author=data.get('author'),
            published_date=data.get('published_date').date()
            if isinstance(data.get('published_date'), datetime)
            else data.get('published_date'),
            genre=data.get('genre'),
            price=Decimal(data.get('price'))
            if isinstance(data.get('price'), (int, float, str))
            else data.get('price'),
            book_id=data.get('_id')
        )
        return book

    def save(self):
        client = MongoDBClient.get_instance()
        result = client.book_collection.insert_one(self.to_dict())
        self.id = str(result.inserted_id)

    @staticmethod
    def get_all():
        client = MongoDBClient.get_instance()
        books = client.book_collection.find()
        book_list = [Book.from_dict(book) for book in books]
        return book_list

    @staticmethod
    def get_by_id(book_id):
        client = MongoDBClient.get_instance()
        book = client.book_collection.find_one({"_id": ObjectId(book_id)})
        if book:
            return Book.from_dict(book)
        return None

    @staticmethod
    def update(book_id, data):
        client = MongoDBClient.get_instance()
        updated_book = Book.from_dict(data)
        client.book_collection.update_one({"_id": ObjectId(book_id)}, {"$set": updated_book.to_dict()})
        updated_book.id = book_id
        return updated_book

    @staticmethod
    def delete(book_id):
        client = MongoDBClient.get_instance()
        client.book_collection.delete_one({"_id": ObjectId(book_id)})

    @staticmethod
    def get_average_price_by_year(year):
        """
        Calculates the average price of books published in a specific year.

        Args:
            year (int): The year for which to calculate the average price.

        Returns:
            float: The average price of books published in the specified year.
        """
        client = MongoDBClient.get_instance()
        pipeline = [
            {
                "$match": {
                    "published_date": {
                        "$gte": datetime(year, 1, 1),
                        "$lt": datetime(year + 1, 1, 1)
                    }
                }
            },
            {
                "$group": {
                    "_id": None,
                    "average_price": {"$avg": "$price"}
                }
            }
        ]
        result = list(client.book_collection.aggregate(pipeline))
        if result:
            return result[0]['average_price']
        return 0
