import datetime

import requests
from starlette.background import BackgroundTasks

from config.db import database
from mobility.search_model import Status, OnStatus
from ondc.context import Action
from schemas.order_model import Order

BPP_URI = "https://mobility-mockserver-00ab4bdaacc0.herokuapp.com/mobility/bpp/mock/"
BPP_ID = "seller-mock"


def send_on_status(url: str, on_status: OnStatus):
    return requests.post(url + "/on_status", json=on_status.model_dump())


class StatusService:

    def status_service(body: Status, background_task: BackgroundTasks):
        order_collection = database['order']
        document = order_collection.find_one({"order_id": body.message.order_id})
        order_data = Order(**document)
        order = order_data.order
        order.context.transaction_id = body.context.transaction_id
        order.context.message_id = body.context.message_id
        order.context.timestamp = datetime.datetime.utcnow()
        order.context.action = Action.ON_STATUS
        order.message.order.fulfillment.state.descriptor.code = 'DRIVER_AT_PICKUP'
        order.message.order.fulfillment.state.descriptor.name = 'Driver Arrived at Pickup Location'
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
