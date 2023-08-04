from typing import Any

from pydantic import BaseModel, Field


class Order(BaseModel):
    _id: str = Field(alias="order_id")  # Using alias to map "order_id" to _id
    order: Any
    message_id: str = Field(alias="message_id")
    transaction_id: str
    bap_uri: str
    bap_id: str
    confirm_message : Any
