import os

from src.consts import FILE_PATH_GENERATED_ALL_ITEMS_NAMES_TO_ID
from src.consts import FILE_PATH_GENERATED_SHOPPING_LIST
from src.consts import FILE_PATH_MANUAL_SHOPPING_LIST
from src.utils.files import get_root_project_path
from src.utils.files import read_dict_from_file
from src.utils.files import write_dict_content_on_file


MANUAL_SHOPPING_LIST__EXTRA_FIELDS = "extra_fields"
MANUAL_SHOPPING_LIST__ITEMS = "items"

MANUAL_SHOPPING_LIST__IS_VENTURE_FILE = "is_venture_file"
MANUAL_SHOPPING_LIST__LEVEL = "level"
MANUAL_SHOPPING_LIST__DURATION = "duration"
MANUAL_SHOPPING_LIST__VENTURE_MIN_LEVEL = "venture_minimum_level"


def generate_enriched_shopping_lists():
    all_items_name_to_id = read_dict_from_file(
        FILE_PATH_GENERATED_ALL_ITEMS_NAMES_TO_ID
    )

    for shopping_list in os.listdir(
        f"{get_root_project_path()}/{FILE_PATH_MANUAL_SHOPPING_LIST}"
    ):
        enrich_shopping_list(shopping_list, all_items_name_to_id)
        print(f"{shopping_list} was enriched and generated.")


def enrich_shopping_list(shopping_list_name, all_items_name_to_id):
    manual_shopping_list_dict = read_dict_from_file(
        f"{FILE_PATH_MANUAL_SHOPPING_LIST}/{shopping_list_name}"
    )

    items_infos = get_enriched_shopping_list(
        manual_shopping_list_dict, all_items_name_to_id
    )

    write_dict_content_on_file(
        items_infos, f"{FILE_PATH_GENERATED_SHOPPING_LIST}/{shopping_list_name}"
    )


def get_enriched_shopping_list(manual_shopping_list_dict, all_items_name_to_id):
    extra_fields = manual_shopping_list_dict.get(MANUAL_SHOPPING_LIST__EXTRA_FIELDS, [])
    items_infos = {}

    for item in manual_shopping_list_dict[MANUAL_SHOPPING_LIST__ITEMS]:
        if should_skip_item(manual_shopping_list_dict, item):
            continue

        items_infos[item] = {
            "id": all_items_name_to_id[item],
        }

        for extra_field in extra_fields:
            items_infos[item][extra_field] = manual_shopping_list_dict[
                MANUAL_SHOPPING_LIST__ITEMS
            ][item][extra_field]

        if manual_shopping_list_dict.get(MANUAL_SHOPPING_LIST__IS_VENTURE_FILE):
            handle_venture_fields(manual_shopping_list_dict, items_infos, item)

    return items_infos


def should_skip_item(manual_shopping_list_dict, item):
    if is_venture_shopping_list(
        manual_shopping_list_dict
    ) and is_item_venture_level_too_low(manual_shopping_list_dict, item):
        return True

    return False


def is_venture_shopping_list(current_shopping_list):
    return current_shopping_list.get(MANUAL_SHOPPING_LIST__IS_VENTURE_FILE)


def is_item_venture_level_too_low(manual_shopping_list_dict, item):
    return manual_shopping_list_dict.get(
        MANUAL_SHOPPING_LIST__VENTURE_MIN_LEVEL, 0
    ) > manual_shopping_list_dict[MANUAL_SHOPPING_LIST__ITEMS][item].get(
        MANUAL_SHOPPING_LIST__LEVEL, 1
    )


def handle_venture_fields(manual_shopping_list_dict, items_infos, item):
    add_venture_duration(manual_shopping_list_dict, items_infos, item)


def add_venture_duration(manual_shopping_list_dict, items_infos, item):
    items_infos[item][MANUAL_SHOPPING_LIST__DURATION] = get_venture_duration(
        manual_shopping_list_dict[MANUAL_SHOPPING_LIST__ITEMS][item][
            MANUAL_SHOPPING_LIST__LEVEL
        ]
    )


def get_venture_duration(item_level):
    duration = 40
    if item_level >= 80:
        duration = 60
    elif item_level >= 70:
        duration = 50
    elif item_level > 90:
        raise Exception("WE HAVE REACHED EXPANSION 7.0 AND THIS LOGIC WAS NOT UPDATED")

    return duration
