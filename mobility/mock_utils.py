import json

from mobility.search_model import OnSearch, OnSelect, OnConfirm, OnInit


def get_search_results() -> OnSearch:
    with open("mock-data/on_search.json") as on_search:
        parsed_json = json.load(on_search)
    return OnSearch(**parsed_json)


def get_select_results() -> OnSelect:
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
