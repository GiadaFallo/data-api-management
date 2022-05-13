from dataclasses import asdict, dataclass
from typing import List
from pymongo.mongo_client import MongoClient

from app.config import settings
from app.models.storage import CustomerDialog


@dataclass
class Result:
    customer_id: int
    dialog_id: int
    text: str
    language: str
    timestamp: str

    @staticmethod
    def from_db_document(doc):
        return Result(
            doc["customer_id"],
            doc["dialog_id"],
            doc["data"]["text"],
            doc["data"]["language"],
            doc["data"]["timestamp"].isoformat(),
        )

class Database:
    def __init__(self, db_url, db_name: str, collection_name: str):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.customer_dialogs_collection = self.db[collection_name]

    def store_data(self, customer_dialog: CustomerDialog):
        self.customer_dialogs_collection.insert_one(asdict(customer_dialog))

    def read_data(
        self, language=None, customer_id=None, skip=0, limit=10
    ) -> List[Result]:

        conditions = []
        if language:
            conditions.append({"data.language": language})

        if customer_id:
            conditions.append({"customer_id": customer_id})

        final_condition = {"$and": conditions} if len(conditions) > 0 else {}

        cursor = self.customer_dialogs_collection.aggregate(
            [
                {"$unwind": "$data"},
                {"$match": final_condition},
                {"$sort": {"data.timestamp": -1}},
                {"$skip": skip},
                {"$limit": limit},
            ]
        )

        return list(map(Result.from_db_document, cursor))


database = Database(settings.db_url, "chat", "customer_dialogs")
