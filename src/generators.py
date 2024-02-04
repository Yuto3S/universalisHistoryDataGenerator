import json
import time

import requests

from src.consts import MateriaType

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
            all_items_name_to_id[entry["Name_en"]] = entry["ID"]

        print(f"Page: {page}/{xiv_response_json['Pagination']['PageTotal']}")

        time.sleep(1 / XIV_API_RATE_LIMIT_PER_SECOND)
        page = xiv_response_json["Pagination"]["PageNext"]

    with open("assets/generated/config/all_items_name_to_id.json", "w") as outfile:
        json.dump(all_items_name_to_id, outfile)


def get_venture_duration(item_level):
    duration = 40
    if item_level >= 80:
        duration = 60
    elif item_level >= 70:
        duration = 50

    return duration


def generate_json(file_name):
    with open("../assets/generated/config/all_items_name_to_id.json", "r") as all_items_name_to_id_json_file:
        all_items_name_to_id = json.load(all_items_name_to_id_json_file)
        with open(f"assets/manual_input/shopping_list/{file_name}", "r") as raw_json_file:
            raw_json_input = json.load(raw_json_file)

            if raw_json_input.get("use_materia_logic"):
                generate_materias_json(all_items_name_to_id, raw_json_input, file_name)
            else:
                extra_fields = raw_json_input.get("extra_fields", [])
                items_infos = {}

                for item in raw_json_input["items"]:
                    items_infos[item] = {
                        "id": all_items_name_to_id[item],
                    }

                    for extra_field in extra_fields:
                        items_infos[item][extra_field] = raw_json_input["items"][item][extra_field]

                    if raw_json_input.get("add_venture_duration"):
                        items_infos[item]["duration"] = get_venture_duration(raw_json_input["items"][item]["level"])

                    if raw_json_input.get("venture_minimum_level", 0) > raw_json_input["items"][item].get("level", 1):
                        items_infos.pop(item)

                with open(f"assets/generated/shopping_list/{file_name}", "w") as output_json_file:
                    json.dump(items_infos, output_json_file)


def generate_materias_json(all_items_name_to_id, raw_json_input, file_name_input):
    for materia_type in MateriaType:
        all_materias_info = {}

        for materia_name in raw_json_input[materia_type.value]:
            for materia_level in raw_json_input["levels"]:
                entry_name = f"{materia_name} Materia {materia_level}"
                all_materias_info[entry_name] = {
                    "id": all_items_name_to_id[entry_name],
                }

                for extra_field in raw_json_input["extra_fields"]:
                    all_materias_info[entry_name][extra_field] = raw_json_input[materia_level][materia_type.value][extra_field]

        with open(f"assets/generated/shopping_list/{materia_type.value}_{file_name_input}", "w") as output_materias_json_file:
            json.dump(all_materias_info, output_materias_json_file)