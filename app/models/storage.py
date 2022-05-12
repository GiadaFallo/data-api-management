from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List

@dataclass(frozen=True)
class CustomerInput:
    text: str
    language: str
    timestamp: date


@dataclass
class CustomerDialog:
    customer_id: int
    dialog_id: int
    data: List[CustomerInput] = field(default_factory=list, init=False)


class CustomerDialogStorage:
    storage: Dict[int, CustomerDialog] = {}

    def create_if_not_exist(self, customer_id: int, dialog_id: int) -> CustomerDialog:

        if dialog_id not in self.storage:
            self.storage[dialog_id] = CustomerDialog(customer_id, dialog_id)
 
        return self.storage[dialog_id]

    def get(self, dialog_id: int) -> (CustomerDialog | None):
        return self.storage.get(dialog_id)

    def delete(self, dialog_id):
        return self.storage.pop(dialog_id)


storage = CustomerDialogStorage()
