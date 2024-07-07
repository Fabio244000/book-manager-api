from pymongo import MongoClient


class MongoDBClient:
    _instance = None

    @staticmethod
    def get_instance():
        if MongoDBClient._instance is None:
            MongoDBClient()
        return MongoDBClient._instance

    def __init__(self):
        if MongoDBClient._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.client = MongoClient('mongodb://db:27017/')
            self.db = self.client.book_db
            self.book_collection = self.db.books
            MongoDBClient._instance = self
