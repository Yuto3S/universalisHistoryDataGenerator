import json
import time

import requests

from src.consts import FILE_PATH_GENERATED_ALL_ITEMS_NAMES_TO_ID
from src.consts import NON_BREAKING_SPACE
from src.utils.files import write_dict_content_on_file


XIV_API_ITEM_ID = "ID"
XIV_API_NAME_EN = "Name_en"
XIV_API_RESULTS = "Results"
XIV_API_PAGINATION = "Pagination"
XIV_API_PAGINATION_NEXT = "PageNext"
XIV_API_PAGINATION_TOTAL = "PageTotal"

XIV_API_FIRST_PAGE = 1
XIV_API_RATE_LIMIT_PER_SECOND = 20
XIV_API_ITEM_URL = "http://xivapi.com/item"
XIV_API_ITEM_QUERY_PARAMETERS = "limit=3000,&columns=ID,Name_de,Name_en,Name_fr,Name_ja"


def generate_all_items_name_to_id():
    all_items_name_to_id = get_all_items_name_to_id()

    write_dict_content_on_file(
        all_items_name_to_id, FILE_PATH_GENERATED_ALL_ITEMS_NAMES_TO_ID
    )


def get_all_items_name_to_id():
    # This function relies on the API provided from https://xivapi.com/docs/Game-Data#content
    all_items_name_to_id = {}
    next_page = XIV_API_FIRST_PAGE

    while next_page is not None:
        # TODO: Use Name_de, Name_fr, Name_jp if required for multilingual support for shopping_list inputs
        xiv_api_request = requests.get(
            f"{XIV_API_ITEM_URL}?page={next_page}&{XIV_API_ITEM_QUERY_PARAMETERS}"
        )
        xiv_response_json = json.loads(xiv_api_request.content)

        for entry in xiv_response_json[XIV_API_RESULTS]:
            item_name_en = maybe_sanitize_item_name(entry[XIV_API_NAME_EN])
            all_items_name_to_id[item_name_en] = entry[XIV_API_ITEM_ID]

        print(
            f"Page: {next_page}/{xiv_response_json[XIV_API_PAGINATION][XIV_API_PAGINATION_TOTAL]}"
        )

        next_page = xiv_response_json[XIV_API_PAGINATION][XIV_API_PAGINATION_NEXT]
        prevent_rate_limit_xiv_api()

    return all_items_name_to_id


def maybe_sanitize_item_name(item_name):
    if NON_BREAKING_SPACE in item_name:
        item_name = item_name.replace(NON_BREAKING_SPACE, " ")
        print(f"{item_name} had NON_BREAKING_SPACE")

    return item_name


def prevent_rate_limit_xiv_api():
    time.sleep(1 / XIV_API_RATE_LIMIT_PER_SECOND)
