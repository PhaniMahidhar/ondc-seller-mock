import json

from mobility.search_model import OnSearch, OnSelect, OnConfirm, OnInit, OnStatus, OnSupport, OnCancel, OnTrack


def get_search_results() -> OnSearch:
    with open("mock-data/on_search.json") as on_search:
        parsed_json = json.load(on_search)
    return OnSearch(**parsed_json)


def get_search_results_uber() -> OnSearch:
    with open("mock-data/on_search_uber.json") as on_search:
        parsed_json = json.load(on_search)
    return OnSearch(**parsed_json)


def get_select_results() -> OnSelect:
    with open("mock-data/on_select.json") as on_select:
        parsed_json = json.load(on_select)
    return OnSelect(**parsed_json)


def get_select_results_uber() -> OnSelect:
    with open("mock-data/on_select.json") as on_select:
        parsed_json = json.load(on_select)
    return OnSelect(**parsed_json)



def get_select_results_ola() -> OnSelect:
    with open("mock-data/on_select.json") as on_select:
        parsed_json = json.load(on_select)
    return OnSelect(**parsed_json)


def get_init_results() -> OnInit:
    with open("mock-data/on_init.json") as on_init:
        parsed_json = json.load(on_init)
    return OnInit(**parsed_json)


def get_confirm_results() -> OnConfirm:
    with open("mock-data/on_confirm.json") as on_confirm:
        parsed_json = json.load(on_confirm)
    return OnConfirm(**parsed_json)


def get_status_results() -> OnStatus:
    with open("mock-data/on_status.json") as on_status:
        parsed_json = json.load(on_status)
    return OnStatus(**parsed_json)


def get_support_results() -> OnSupport:
    with open("mock-data/on_support.json") as on_support:
        parsed_json = json.load(on_support)
    return OnSupport(**parsed_json)


def get_cancel_results() -> OnCancel:
    with open("mock-data/on_cancel.json") as on_cancel:
        parsed_json = json.load(on_cancel)
    return OnCancel(**parsed_json)


def get_track_results() -> OnTrack:
    with open("mock-data/on_cancel.json") as on_track:
        parsed_json = json.load(on_track)
    return OnTrack(**parsed_json)
