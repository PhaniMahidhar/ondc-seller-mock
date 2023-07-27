import json

from mobility.search_model import OnSearch, OnSelect


def get_search_results() -> OnSearch:
    with open("mock-data/on_search.json") as on_search:
        parsed_json = json.load(on_search)
    return OnSearch(**parsed_json)


def get_select_results() -> OnSelect:
    with open("mock-data/on_select.json") as on_select:
        parsed_json = json.load(on_select)
    return OnSelect(**parsed_json)
