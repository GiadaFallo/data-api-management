from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from fastapi import APIRouter
from app.models.storage import CustomerInput, storage

router = APIRouter()


class Message(BaseModel):
    text: str
    language: str

    def to_customer_input(self) -> CustomerInput:
        return CustomerInput(self.text, self.language, datetime.today())


class Consents(BaseModel):
    value: bool


@router.post("/data/{customer_id}/{dialog_id}", status_code=201)
async def send_message(customer_id: int, dialog_id: int, message: Message):
    """
        This endpoint push each customer input during his/her dialogue with the chatbot
    """
    dialog = storage.create_if_not_exist(customer_id, dialog_id)
    dialog.data.append(message.to_customer_input())


@router.post("/consents/{dialog_id}", status_code=201)
async def send_consent(dialog_id: int, consents: Consents):
    """
        This endpoint is called at the end of the dialogue when the customer is asked if he/she gives consent
        for us to store and use their data for further improving the chatbot.
        If false customer's data stored in-memory will be deleted
        If true customer's data will be stored in the database and deleted from the in-memory storage
    """
    pass


@router.get("/data/")
async def get_data(language: Optional[str] = None, customer_id: Optional[int] = None, page_number: int = 0, n_per_page: int = 0,
                   response_description="List all datapoints"):
    """
        Retrieve data to improve the chatbot it returns all the datapoints:
            * that match the query params (if any)
            * for which we have consent for
            * data are sorted by most recent data first and with pagination
        """
    pass