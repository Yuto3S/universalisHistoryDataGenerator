import json
import time

import requests

from src.consts import NON_BREAKING_SPACE
from src.generators.shopping_list import MANUAL_SHOPPING_LIST__FIELD_ID


XIV_API_ITEM_ID = "ID"
XIV_API_NAME_EN = "Name_en"
XIV_API_RESULTS = "Results"
XIV_API_PAGINATION = "Pagination"
XIV_API_PAGINATION_NEXT = "PageNext"
XIV_API_PAGINATION_TOTAL = "PageTotal"

XIV_API_FIRST_PAGE = 1
XIV_API_RATE_LIMIT_PER_SECOND = 20
XIV_API_ITEM_URL = "http://xivapi.com/item"
# TODO: Use Name_de, Name_fr, Name_jp if required for multilingual support for shopping_list inputs
XIV_API_ITEM_QUERY_PARAMETERS = "limit=3000,&columns=ID,Name_de,Name_en,Name_fr,Name_ja"


def get_all_items_name_to_id():
    # This function relies on the API provided from https://xivapi.com/docs/Game-Data#content
    all_items_name_to_id = {}
    next_page = XIV_API_FIRST_PAGE

    while next_page is not None:
        xiv_api_response = get_xiv_api_response(next_page)

        for entry in xiv_api_response[XIV_API_RESULTS]:
            item_name_en = maybe_sanitize_item_name(entry[XIV_API_NAME_EN])
            all_items_name_to_id[item_name_en] = entry[XIV_API_ITEM_ID]

        print(
            f"Page: {next_page}/{xiv_api_response[XIV_API_PAGINATION][XIV_API_PAGINATION_TOTAL]}"
        )

        next_page = xiv_api_response[XIV_API_PAGINATION][XIV_API_PAGINATION_NEXT]
        protect_rate_limit_xiv_api()

    return all_items_name_to_id


def get_xiv_api_response(page):
    xiv_api_request = requests.get(
        f"{XIV_API_ITEM_URL}?page={page}&{XIV_API_ITEM_QUERY_PARAMETERS}"
    )
    return json.loads(xiv_api_request.content)


def maybe_sanitize_item_name(item_name):
    if NON_BREAKING_SPACE in item_name:
        item_name = item_name.replace(NON_BREAKING_SPACE, " ")
        print(f"{item_name} had NON_BREAKING_SPACE")

    return item_name


def protect_rate_limit_xiv_api():
    time.sleep(1 / XIV_API_RATE_LIMIT_PER_SECOND)


def get_items_id_to_name(items):
    item_ids_to_name = {}
    for item_name in items:
        item_ids_to_name[
            str(items[item_name][MANUAL_SHOPPING_LIST__FIELD_ID])
        ] = item_name

    return item_ids_to_name
