from .models import Book
from bson.objectid import ObjectId
from .constants import BOOK_NOT_FOUND
from rest_framework.exceptions import NotFound
import logging

logger = logging.getLogger(__name__)


class BookService:

    @staticmethod
    def get_all_books():
        try:
            return Book.get_all()
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            raise

    @staticmethod
    def get_book_by_id(book_id):
        try:
            book = Book.get_by_id(ObjectId(book_id))
            if book is None:
                raise NotFound(detail=BOOK_NOT_FOUND)
            return book
        except NotFound:
            raise
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            raise

    @staticmethod
    def create_book(data):
        try:
            book = Book(**data)
            book.save()
            return book
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            raise

    @staticmethod
    def update_book(book_id, data):
        try:
            updated_book = Book.update(ObjectId(book_id), data)
            return updated_book
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            raise

    @staticmethod
    def delete_book(book_id):
        try:
            Book.delete(ObjectId(book_id))
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            raise

    @staticmethod
    def get_average_price_by_year(year):
        try:
            average_price = Book.get_average_price_by_year(year)
            formatted_price = "{:.2f}".format(average_price)
            return float(formatted_price)
        except Exception as e:
            logger.error(f"Error getting average price by year: {e}")
            raise
