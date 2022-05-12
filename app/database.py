from app.config import settings
from pymongo.mongo_client import MongoClient

class Database:

    def __init__(self, db_url, db_name: str, collection_name: str):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.customer_dialogs_collection = self.db[collection_name]

database = Database(settings.db_url, "chat", "customer_dialogs")
