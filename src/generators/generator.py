import os

from src.consts import FILE_PATH_GENERATED_ALL_ITEMS_NAMES_TO_ID
from src.consts import FILE_PATH_GENERATED_SHOPPING_LIST
from src.consts import FILE_PATH_MANUAL_SHOPPING_LIST
from src.generators.items import get_all_items_name_to_id
from src.generators.shopping_list import get_enriched_shopping_list
from src.utils.files import get_root_project_path
from src.utils.files import read_dict_from_file
from src.utils.files import write_dict_content_on_file


def generate_all_items_name_to_id():
    all_items_name_to_id = get_all_items_name_to_id()

    write_dict_content_on_file(
        all_items_name_to_id, FILE_PATH_GENERATED_ALL_ITEMS_NAMES_TO_ID
    )


def generate_enriched_shopping_lists():
    all_items_name_to_id = read_dict_from_file(
        FILE_PATH_GENERATED_ALL_ITEMS_NAMES_TO_ID
    )

    for shopping_list in os.listdir(
        f"{get_root_project_path()}{FILE_PATH_MANUAL_SHOPPING_LIST}"
    ):
        manual_shopping_list_dict = read_dict_from_file(
            f"{FILE_PATH_MANUAL_SHOPPING_LIST}{shopping_list}"
        )

        print(f"Enriching {shopping_list}...")
        items_infos = get_enriched_shopping_list(
            manual_shopping_list_dict, all_items_name_to_id
        )

        write_dict_content_on_file(
            items_infos, f"{FILE_PATH_GENERATED_SHOPPING_LIST}{shopping_list}"
        )
