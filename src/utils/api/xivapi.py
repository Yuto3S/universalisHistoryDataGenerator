import json
import time

import requests

XIV_API_ITEM_ID = "row_id"
XIV_API_RESULTS = "rows"
XIV_API_FIELDS = "fields"
XIV_API_ITEM_NAME = "Name"

XIV_API_FIRST_PAGE = 0
XIV_API_RATE_LIMIT_PER_SECOND = 20
XIV_API_ITEM_URL = "http://xivapi.com/item"
XIV_API_ITEM_URL_UPDATE = (
    "https://beta.xivapi.com/api/1/sheet/Item?limit=500&fields=Name,row.id&after="
)
# TODO: Use Name_de, Name_fr, Name_jp if required for multilingual support for shopping_list inputs
XIV_API_ITEM_QUERY_PARAMETERS = "limit=3000,&columns=ID,Name_de,Name_en,Name_fr,Name_ja"


def get_xiv_api_response(page):
    # This function relies on the API provided from https://xivapi.com/docs/Game-Data#content
    xiv_api_request = requests.get(f"{XIV_API_ITEM_URL_UPDATE}{page}")
    print(xiv_api_request.url)
    return json.loads(xiv_api_request.content)


def protect_rate_limit_xiv_api():
    time.sleep(1 / XIV_API_RATE_LIMIT_PER_SECOND)
