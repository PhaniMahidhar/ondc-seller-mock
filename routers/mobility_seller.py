from fastapi import APIRouter
from starlette.background import BackgroundTasks

from mobility import search_model
from mobility.search_model import Confirm, Status, Support, Cancel, Track
from service import search_select_init_service, confirm_service, status_service, support_service

BPP_URI = "https://mobility-mockserver-00ab4bdaacc0.herokuapp.com/mobility/bpp/mock/"
BPP_ID = "seller-mock"

router = APIRouter(
    prefix="/mobility/bpp/mock",
    tags=["Mobility Seller"],
    responses={404: {"description": "This endpoint is not yet mocked."}},
)


@router.post("/search")
def get_catalogue(body: search_model.Search, background_task: BackgroundTasks):
    return search_select_init_service.SearchService.search_service(body, background_task)


@router.post("/select")
def get_select(body: search_model.Select, background_task: BackgroundTasks):
    return search_select_init_service.SelectService.select_service(body, background_task)


@router.post("/init")
def get_select(body: search_model.Init, background_task: BackgroundTasks):
    return search_select_init_service.InitService.init_service(body, background_task)


@router.post("/confirm")
def get_confirm(body: Confirm, background_task: BackgroundTasks):
    return confirm_service.ConfirmService.confirm_service(body, background_task)


@router.post("/status")
def get_status(body: Status, background_task: BackgroundTasks):
    return status_service.StatusService.status_service(body, background_task)


@router.post("/support")
def get_support(body: Support, background_task: BackgroundTasks):
    return support_service.SupportService.support_service(body, background_task)


@router.post("/cancel")
def get_cancel(body: Cancel, background_task: BackgroundTasks):
    return status_service.CancelService.cancel_service(body, background_task)


@router.post("/track")
def get_track(body: Track, background_task: BackgroundTasks):
    return status_service.TrackService.track_service(body, background_task)