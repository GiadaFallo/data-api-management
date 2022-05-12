from dataclasses import asdict
from app.config import settings
from pymongo.mongo_client import MongoClient

from app.models.storage import CustomerDialog


class Database:

    def __init__(self, db_url, db_name: str, collection_name: str):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.customer_dialogs_collection = self.db[collection_name]

    def store_data(self, customer_dialog: CustomerDialog):
        self.customer_dialogs_collection\
            .insert_one(asdict(customer_dialog))


database = Database(settings.db_url, "chat", "customer_dialogs")
