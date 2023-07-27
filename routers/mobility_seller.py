import datetime
import json

import requests
from fastapi import APIRouter
from mobility import search_model, mock_utils
from mobility.search_model import OnSearch, OnSelect
from starlette.background import BackgroundTasks

BPP_URI= "https://mobility-mockserver-00ab4bdaacc0.herokuapp.com/mobility/bpp/mock/"
BPP_ID="seller-mock"

router = APIRouter(
    prefix="/mobility/bpp/mock",
    tags=["Mobility Seller"],
    responses={404: {"description": "This endpoint is not yet mocked."}},
)


def send_on_search(url: str, on_search: OnSearch):
    return requests.post(url + "/on_search", json=on_search.model_dump())


def send_on_select(url: str, on_select: OnSelect):
    return requests.post(url + "/on_select", data=on_select.model_dump())


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
        "timestamp": f"{datetime.datetime.utcnow().isoformat()[:-3]+'Z'}",
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
        "timestamp": f"{datetime.datetime.utcnow().isoformat()[:-3]+'Z'}",
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
