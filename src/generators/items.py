import multiprocessing as mp
from multiprocessing import Pool

import tqdm as tqdm

from src.consts import NON_BREAKING_SPACE
from src.generators.shopping_list import MANUAL_SHOPPING_LIST__FIELD_ID
from src.utils.api.lodestone import get_lodestone_items_for_page
from src.utils.api.lodestone import get_lodestone_items_number_of_pages
from src.utils.api.xivapi import get_xiv_api_response
from src.utils.api.xivapi import protect_rate_limit_xiv_api
from src.utils.api.xivapi import XIV_API_FIRST_PAGE
from src.utils.api.xivapi import XIV_API_ITEM_ID
from src.utils.api.xivapi import XIV_API_NAME_EN
from src.utils.api.xivapi import XIV_API_PAGINATION
from src.utils.api.xivapi import XIV_API_PAGINATION_NEXT
from src.utils.api.xivapi import XIV_API_PAGINATION_TOTAL
from src.utils.api.xivapi import XIV_API_RESULTS


def get_all_items_name_to_id():
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


def get_all_items_name_to_lodestone_id():
    all_items_name_to_lodestone_id = {}
    number_of_pages = get_lodestone_items_number_of_pages() + 1

    with Pool(processes=mp.cpu_count()) as pool:
        # lodestone_items_pool_result = pool.map(
        #     get_lodestone_items_for_page, [page_index for page_index in range(number_of_pages + 1)]
        # )
        lodestone_items_pool_result = list(
            tqdm.tqdm(
                pool.imap(get_lodestone_items_for_page, range(1, number_of_pages)),
                total=number_of_pages,
            )
        )

    for pages_entries in lodestone_items_pool_result:
        all_items_name_to_lodestone_id.update(pages_entries)

    return all_items_name_to_lodestone_id


def maybe_sanitize_item_name(item_name):
    if NON_BREAKING_SPACE in item_name:
        item_name = item_name.replace(NON_BREAKING_SPACE, " ")
        print(f"{item_name} had NON_BREAKING_SPACE")

    return item_name


def get_items_id_to_name(items):
    item_ids_to_name = {}
    for item_name in items:
        item_ids_to_name[
            str(items[item_name][MANUAL_SHOPPING_LIST__FIELD_ID])
        ] = item_name

    return item_ids_to_name
