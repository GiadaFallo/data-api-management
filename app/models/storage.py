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


storage = CustomerDialogStorage()
