import json

from mobility.search_model import OnSearch


def get_search_results() -> OnSearch:
    with open("mock-data/on_search.json") as on_search:
        parsed_json = json.load(on_search)
    return OnSearch(**parsed_json)
