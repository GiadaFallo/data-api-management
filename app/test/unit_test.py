import unittest
import pytest

from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.testclient import TestClient

from app.routers import api

class UnitTestCase(unittest.TestCase):

    client = TestClient(api.router)
 
    def test_send_message(self):
        message_payload = {
            "text": "Hi! I need help.",
            "language": "EN"
        }

        response = self.client.post("/data/10/10", json=message_payload)
        assert response.status_code == 201


    def test_send_message_empty_payload(self):
        client = TestClient(api.router)
        message_payload = {}

        with pytest.raises(RequestValidationError) as err:
            client.post("/data/10/10", json=message_payload)
            assert err.type == 404


    def test_send_consents_false(self):
        client = TestClient(api.router)
        message_payload = {
            "text": "Test message",
            "language": "EN"
        }

        client.post("/data/1/11", json=message_payload)
        response = client.post("/consents/11", json={"value": False})
        assert response.status_code == 200


    def test_send_consents_raise_exception(self):
        client = TestClient(api.router)
        with pytest.raises(HTTPException) as exc:
            client.post("/consents/2", json={"value": True})
        assert exc.value.status_code == 404
        assert exc.value.detail == "Item not found"

