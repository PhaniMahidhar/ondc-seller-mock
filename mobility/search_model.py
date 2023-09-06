from typing import Any

from pydantic import BaseModel

from mobility.confirm_model_response import ConfirmMessage
from mobility.on_cancel_model import OnCancelMessage
from mobility.status_model import StatusMessage
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
    message: ConfirmMessage


class OnConfirm(BaseModel):
    context: Context
    message: OnConfirmMessage


class Status(BaseModel):
    context: Context
    message: StatusMessage


class OnStatus(BaseModel):
    context: Context
    message: OnConfirmMessage


class SupportMessage(BaseModel):
    ref_id: str


class Support(BaseModel):
    context: Context
    message: SupportMessage


class OnSupportMessage(BaseModel):
    phone: str
    email: str
    url: str


class OnSupport(BaseModel):
    context: Context
    message: OnSupportMessage


class CancelMessage(BaseModel):
    cancellation_reason_id: str
    order_id: str


class Cancel(BaseModel):
    context: Context
    message: CancelMessage


class OnCancel(BaseModel):
    context: Context
    message: OnCancelMessage


class Track(BaseModel):
    context: Context
    message: Any


class OnTrack(BaseModel):
    context: Context
    message: Any
