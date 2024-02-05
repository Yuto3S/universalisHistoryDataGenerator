import json
import time

import requests

from src.consts import FILE_PATH_GENERATED_ALL_ITEMS_NAMES_TO_ID
from src.consts import FILE_PATH_GENERATED_SHOPPING_LIST
from src.consts import FILE_PATH_MANUAL_SHOPPING_LIST
from src.utils.files import read_dict_from_file
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


def get_venture_duration(item_level):
    duration = 40
    if item_level >= 80:
        duration = 60
    elif item_level >= 70:
        duration = 50

    return duration


def generate_json(file_name):
    all_items_name_to_id = read_dict_from_file(
        FILE_PATH_GENERATED_ALL_ITEMS_NAMES_TO_ID
    )
    raw_json_input = read_dict_from_file(
        f"{FILE_PATH_MANUAL_SHOPPING_LIST}/{file_name}"
    )

    extra_fields = raw_json_input.get("extra_fields", [])
    items_infos = {}

    for item in raw_json_input["items"]:
        items_infos[item] = {
            "id": all_items_name_to_id[item],
        }

        for extra_field in extra_fields:
            items_infos[item][extra_field] = raw_json_input["items"][item][extra_field]

        if raw_json_input.get("add_venture_duration"):
            items_infos[item]["duration"] = get_venture_duration(
                raw_json_input["items"][item]["level"]
            )

        if raw_json_input.get("venture_minimum_level", 0) > raw_json_input["items"][
            item
        ].get("level", 1):
            items_infos.pop(item)

    write_dict_content_on_file(
        items_infos, f"{FILE_PATH_GENERATED_SHOPPING_LIST}/{file_name}"
    )
