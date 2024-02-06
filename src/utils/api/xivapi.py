import json
import time

import requests

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


def get_xiv_api_response(page):
    # This function relies on the API provided from https://xivapi.com/docs/Game-Data#content
    xiv_api_request = requests.get(
        f"{XIV_API_ITEM_URL}?page={page}&{XIV_API_ITEM_QUERY_PARAMETERS}"
    )
    return json.loads(xiv_api_request.content)


def protect_rate_limit_xiv_api():
    time.sleep(1 / XIV_API_RATE_LIMIT_PER_SECOND)
