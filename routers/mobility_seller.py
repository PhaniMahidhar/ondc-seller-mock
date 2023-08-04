import datetime
from typing import Any
from uuid import uuid4

import requests
from fastapi import APIRouter
from starlette.background import BackgroundTasks

from config.db import database
from mobility import search_model, mock_utils
from mobility.search_model import OnSearch, OnSelect, OnInit, Confirm, OnConfirm
from schemas.order_model import Order

BPP_URI = "https://mobility-mockserver-00ab4bdaacc0.herokuapp.com/mobility/bpp/mock/"
BPP_ID = "seller-mock"

router = APIRouter(
    prefix="/mobility/bpp/mock",
    tags=["Mobility Seller"],
    responses={404: {"description": "This endpoint is not yet mocked."}},
)


def send_on_search(url: str, on_search: OnSearch):
    return requests.post(url + "/on_search", json=on_search.model_dump())


def send_on_select(url: str, on_select: OnSelect):
    return requests.post(url + "/on_select", json=on_select.model_dump())


def send_on_init(url: str, on_init: OnInit):
    return requests.post(url + "/on_init", json=on_init.model_dump())


def send_on_confirm(url: str, on_confirm: OnConfirm):
    return requests.post(url + "/on_confirm", json=on_confirm.model_dump())


@router.post("/search")
def get_catalogue(body: search_model.Search, background_task: BackgroundTasks):
    static_on_search: OnSearch = mock_utils.get_search_results()
    print(static_on_search)
    static_on_search.context.transaction_id = body.context.transaction_id
    static_on_search.context.message_id = body.context.message_id
    static_on_search.context.timestamp = datetime.datetime.utcnow()
    background_task.add_task(send_on_search, body.context.bap_uri, static_on_search)
    json_response = {
        "domain": "ONDC:TRV10",
        "timestamp": f"{datetime.datetime.utcnow().isoformat()[:-3] + 'Z'}",
        "bap_id": f"{body.context.bap_id}",
        "transaction_id": f"{body.context.transaction_id}",
        "message_id": f"{body.context.message_id}",
        "city": "std:080",
        "core_version": "0.9.4",
        "action": "search",
        "bap_uri": f"{body.context.bap_uri}",
        "bpp_id": f"{BPP_ID}",
        "bpp_uri": f"{BPP_URI}",
    }
    return {"context": json_response, "message": {"ack": {"status": "ACK"}}}


@router.post("/select")
def get_select(body: search_model.Select, background_task: BackgroundTasks):
    static_on_select: OnSelect = mock_utils.get_select_results()
    print(static_on_select)
    static_on_select.context.transaction_id = body.context.transaction_id
    static_on_select.context.message_id = body.context.message_id
    static_on_select.context.timestamp = datetime.datetime.utcnow()
    background_task.add_task(send_on_select, body.context.bap_uri, static_on_select)
    json_response = {
        "domain": "ONDC:TRV10",
        "timestamp": f"{datetime.datetime.utcnow().isoformat()[:-3] + 'Z'}",
        "bap_id": f"{body.context.bap_id}",
        "transaction_id": f"{body.context.transaction_id}",
        "message_id": f"{body.context.message_id}",
        "bpp_id": f"{BPP_ID}",
        "bpp_uri": f"{BPP_URI}",
        "city": "std:080",
        "core_version": "0.9.4",
        "action": f"{body.context.action}",
        "bap_uri": f"{body.context.bap_uri}",
    }
    return {"context": json_response, "message": {"ack": {"status": "ACK"}}}


@router.post("/init")
def get_select(body: search_model.Init, background_task: BackgroundTasks):
    static_on_init: OnSelect = mock_utils.get_init_results()
    print(static_on_init)
    static_on_init.context.transaction_id = body.context.transaction_id
    static_on_init.context.message_id = body.context.message_id
    static_on_init.context.timestamp = datetime.datetime.utcnow()
    background_task.add_task(send_on_init, body.context.bap_uri, static_on_init)
    json_response = {
        "domain": "ONDC:TRV10",
        "timestamp": f"{datetime.datetime.utcnow().isoformat()[:-3] + 'Z'}",
        "bap_id": f"{body.context.bap_id}",
        "transaction_id": f"{body.context.transaction_id}",
        "message_id": f"{body.context.message_id}",
        "bpp_id": f"{BPP_ID}",
        "bpp_uri": f"{BPP_URI}",
        "city": "std:080",
        "core_version": "0.9.4",
        "action": f"{body.context.action}",
        "bap_uri": f"{body.context.bap_uri}",
    }
    return {"context": json_response, "message": {"ack": {"status": "ACK"}}}


@router.post("/confirm", response_model=None)
def get_confirm(body: Confirm, background_task: BackgroundTasks):
    static_on_confirm: OnConfirm = mock_utils.get_confirm_results()
    print(static_on_confirm)
    order_id = str(uuid4())
    static_on_confirm.context.transaction_id = body.context.transaction_id
    static_on_confirm.context.message_id = body.context.message_id
    static_on_confirm.context.timestamp = datetime.datetime.utcnow()
    static_on_confirm.message.order.id = order_id
    background_task.add_task(send_on_confirm, body.context.bap_uri, static_on_confirm)
    get_and_save_order(static_on_confirm, static_on_confirm.context.transaction_id,
                       static_on_confirm.context.message_id, order_id, body.context.bap_uri, body.context.bap_id,
                       body.message)
    json_response = {
        "domain": "ONDC:TRV10",
        "timestamp": f"{datetime.datetime.utcnow().isoformat()[:-3] + 'Z'}",
        "bap_id": f"{body.context.bap_id}",
        "transaction_id": f"{body.context.transaction_id}",
        "message_id": f"{body.context.message_id}",
        "bpp_id": f"{BPP_ID}",
        "bpp_uri": f"{BPP_URI}",
        "city": "std:080",
        "core_version": "0.9.4",
        "action": f"{body.context.action}",
        "bap_uri": f"{body.context.bap_uri}",
    }
    return {"context": json_response, "message": {"ack": {"status": "ACK"}}}


def get_and_save_order(message: OnConfirm, transaction_id: str, message_id: str, order_id: str, bap_uri: str,
                       bap_id: str, confirm_message: Any):
    confirm_data = message.message
    # Now create an instance of Order
    order = Order(_id=order_id, order=confirm_data, message_id=message_id, transaction_id=transaction_id,
                  bap_uri=bap_uri, bap_id=bap_id, confirm_message=confirm_message)
    order_data = order.dict()
    print(order_data)
    orders_collection = database["order"]
    insert_result = orders_collection.insert_one(order_data)
