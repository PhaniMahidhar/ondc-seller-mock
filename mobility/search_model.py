from typing import Any

from pydantic import BaseModel

from mobility.order_model_message import OnConfirmMessage
from ondc.context import Context


class Search(BaseModel):
    context: Context
    message: Any


class OnSearch(BaseModel):
    context: Context
    message: Any


class Select(BaseModel):
    context: Context
    message: Any


class OnSelect(BaseModel):
    context: Context
    message: Any


class OnInit(BaseModel):
    context: Context
    message: Any


class Init(BaseModel):
    context: Context
    message: Any


class Confirm(BaseModel):
    context: Context
    message: Any


class OnConfirm(BaseModel):
    context: Context
    message: OnConfirmMessage
