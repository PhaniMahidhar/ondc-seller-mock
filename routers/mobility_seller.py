import datetime

import requests
from fastapi import APIRouter
from mobility import search_model, mock_utils
from mobility.search_model import OnSearch
from starlette.background import BackgroundTasks

router = APIRouter(
    prefix="/mobility/bpp/mock",
    tags=["Mobility Seller"],
    responses={404: {"description": "This endpoint is not yet mocked."}},
)


def send_on_search(url: str, on_search: OnSearch):
    return requests.post(url + "/on_search", on_search)


@router.post("/search")
def get_catalogue(body: search_model.Search, background_task: BackgroundTasks):
    static_on_search: OnSearch = mock_utils.get_search_results()
    print(static_on_search)
    static_on_search.context.transaction_id = body.context.transaction_id
    static_on_search.context.message_id = body.context.message_id
    static_on_search.context.timestamp = datetime.datetime.utcnow()
    background_task.add_task(send_on_search, body.context.bap_uri, static_on_search)
    return {"message": {"ack": {"status": "ACK"}}}
