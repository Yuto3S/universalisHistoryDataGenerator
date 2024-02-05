import json
import time

import requests

from src.consts import FILE_PATH_GENERATED_ALL_ITEMS_NAMES_TO_ID
from src.utils.files import write_dict_content_on_file

XIV_API_FIRST_PAGE = 1
XIV_API_RATE_LIMIT_PER_SECOND = 20


def generate_all_items_name_to_id():
    """
    Using the API provided from https://xivapi.com/docs/Game-Data#content
    """
    all_items_name_to_id = {}
    page = XIV_API_FIRST_PAGE
    while page:
        # TODO: Use Name_de, Name_fr, Name_jp if required for multilingual support for shopping_list inputs
        xiv_api_request = requests.get(
            f"http://xivapi.com/item?page={page}&limit=3000,&columns=ID,Name_de,Name_en,Name_fr,Name_ja"
        )
        xiv_response_json = json.loads(xiv_api_request.content)
        for entry in xiv_response_json["Results"]:
            item_name_en = entry["Name_en"]
            if " " in item_name_en:
                item_name_en = item_name_en.replace(" ", " ")
                print(f"{entry} had NBSP")

            all_items_name_to_id[item_name_en] = entry["ID"]

        print(f"Page: {page}/{xiv_response_json['Pagination']['PageTotal']}")

        time.sleep(1 / XIV_API_RATE_LIMIT_PER_SECOND)
        page = xiv_response_json["Pagination"]["PageNext"]

    write_dict_content_on_file(
        all_items_name_to_id, FILE_PATH_GENERATED_ALL_ITEMS_NAMES_TO_ID
    )
