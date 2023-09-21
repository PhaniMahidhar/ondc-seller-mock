import datetime

import requests
from starlette.background import BackgroundTasks

from config.db import database
from mobility import mock_utils, search_model
from mobility.search_model import Status, OnStatus, OnCancel, Cancel, OnTrack
from ondc.context import Action
from schemas.order_model import Order

BPP_URI = "https://mobility-mockserver-00ab4bdaacc0.herokuapp.com/mobility/bpp/mock/"
BPP_ID = "seller-mock"


def send_on_status(url: str, on_status: OnStatus):
    return requests.post(url + "/on_status", json=on_status.model_dump())


def send_on_cancel(url: str, on_cancel: OnCancel):
    return requests.post(url + "/on_cancel", json=on_cancel.model_dump())


def send_on_track(url: str, on_track: OnTrack):
    return requests.post(url + "/on_track", json=on_track.model_dump())


class StatusService:

    def status_service(body: Status, background_task: BackgroundTasks):
        getCountAndUpdateStatus(body.message.order_id)
        order_collection = database['order']
        document = order_collection.find_one({"order_id": body.message.order_id})
        order_data = Order(**document)
        order = order_data.order
        order.context.transaction_id = body.context.transaction_id
        order.context.message_id = body.context.message_id
        order.context.timestamp = datetime.datetime.utcnow()
        order.context.action = Action.ON_STATUS
        print(order)
        background_task.add_task(send_on_status, body.context.bap_uri, order)
        json_response = {
            "domain": "ONDC:TRV10",
            "timestamp": f"{datetime.datetime.utcnow().isoformat()[:-3] + 'Z'}",
            "bap_id": f"{body.context.bap_id}",
            "transaction_id": f"{body.context.transaction_id}",
            "message_id": f"{body.context.message_id}",
            "city": "std:080",
            "core_version": "0.9.4",
            "action": "status",
            "bap_uri": f"{body.context.bap_uri}",
            "bpp_id": f"{BPP_ID}",
            "bpp_uri": f"{BPP_URI}",
        }
        return {"context": json_response, "message": {"ack": {"status": "ACK"}}}


def getCountAndUpdateStatus(ondc_order_id: str):
    order_collection = database['order']
    document = order_collection.find_one({"order_id": ondc_order_id})
    order = Order(**document)
    count = order.count
    update_query = {"$set": {}}

    if (order.order.message.order.fulfillment.state.descriptor.code != 'RIDE_CANCELLED') and (
            order.order.message.order.fulfillment.state.descriptor.code != 'RIDE_ENDED'):
        if count > 4:
            update_query["$set"]["count"] = 1
        elif count == 1:
            update_query["$set"]["count"] = count + 1
            update_query["$set"]["order.message.order.fulfillment.state.descriptor.code"] = 'DRIVER_EN_ROUTE_TO_PICKUP'
        elif count == 2:
            update_query["$set"]["count"] = count + 1
            update_query["$set"]["order.message.order.fulfillment.state.descriptor.code"] = 'DRIVER_AT_PICKUP'
        elif count == 3:
            update_query["$set"]["count"] = count + 1
            update_query["$set"]["order.message.order.fulfillment.state.descriptor.code"] = 'RIDE_STARTED'
        elif count == 4:
            update_query["$set"]["count"] = count + 1
            update_query["$set"]["order.message.order.fulfillment.state.descriptor.code"] = 'RIDE_ENDED'

    orders_collection = database["order"]
    orders_collection.update_one({"order_id": ondc_order_id}, update_query)


class CancelService:

    def cancel_service(body: Cancel, background_task: BackgroundTasks):
        order_collection = database['order']
        document = order_collection.find_one({"order_id": body.message.order_id})
        static_on_cancel: OnCancel = mock_utils.get_cancel_results()
        order_data = Order(**document)
        order = order_data.order
        update_query = {"$set": {}}
        update_query["$set"]["order.message.order.fulfillment.state.descriptor.code"] = 'RIDE_CANCELLED'
        order_collection.update_one({"order_id": order.message.order.id}, update_query)
        static_on_cancel.context.transaction_id = body.context.transaction_id
        static_on_cancel.context.message_id = body.context.message_id
        static_on_cancel.context.timestamp = datetime.datetime.utcnow()
        static_on_cancel.context.action = Action.ONCANCEL
        static_on_cancel.message.order.fulfillment.state.descriptor.code = 'RIDE_CANCELLED'
        static_on_cancel.message.order.id = body.message.order_id
        print(order)
        background_task.add_task(send_on_cancel, body.context.bap_uri, static_on_cancel)
        json_response = {
            "domain": "ONDC:TRV10",
            "timestamp": f"{datetime.datetime.utcnow().isoformat()[:-3] + 'Z'}",
            "bap_id": f"{body.context.bap_id}",
            "transaction_id": f"{body.context.transaction_id}",
            "message_id": f"{body.context.message_id}",
            "city": "std:080",
            "core_version": "0.9.4",
            "action": "status",
            "bap_uri": f"{body.context.bap_uri}",
            "bpp_id": f"{BPP_ID}",
            "bpp_uri": f"{BPP_URI}",
        }
        return {"context": json_response, "message": {"ack": {"status": "ACK"}}}


class TrackService:
    def track_service(body: search_model.Track, background_task: BackgroundTasks):
        static_on_track: OnTrack = mock_utils.get_track_results()
        print(static_on_track)
        static_on_track.context.transaction_id = body.context.transaction_id
        static_on_track.context.message_id = body.context.message_id
        static_on_track.context.timestamp = datetime.datetime.utcnow()
        background_task.add_task(send_on_track, body.context.bap_uri, static_on_track)
        json_response = {
            "domain": "ONDC:TRV10",
            "timestamp": f"{datetime.datetime.utcnow().isoformat()[:-3] + 'Z'}",
            "bap_id": f"{body.context.bap_id}",
            "transaction_id": f"{body.context.transaction_id}",
            "message_id": f"{body.context.message_id}",
            "city": "std:080",
            "core_version": "0.9.4",
            "action": "track",
            "bap_uri": f"{body.context.bap_uri}",
            "bpp_id": f"{BPP_ID}",
            "bpp_uri": f"{BPP_URI}",
        }
        return {"context": json_response, "message": {"ack": {"status": "ACK"}}}