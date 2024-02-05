import json
import math
import time
from unittest.mock import patch

import requests

from src.consts import COLUMNS
from src.consts import COST
from src.consts import DURATION
from src.consts import GIL_PER_CURRENCY
from src.consts import GIL_PER_VENTURE
from src.consts import HISTORY_INFO_AVERAGE_PRICE
from src.consts import HISTORY_INFO_NAME
from src.consts import HISTORY_INFO_TOTAL_MARKET
from src.consts import HISTORY_INFO_TOTAL_QUANTITY
from src.consts import ID
from src.consts import ITEMS
from src.consts import MAX_IDS_PER_REQUEST_UNIVERSALIS
from src.consts import PROCESSES
from src.consts import QUANTITY
from src.consts import UNIVERSALIS_API_RATE_LIMIT_PER_SECOND
from src.consts import UNIVERSALIS_REQUEST_URL
from src.consts import UNIVERSALIS_RESPONSE_ENTRIES
from src.consts import UNIVERSALIS_RESPONSE_PRICE
from src.consts import UNIVERSALIS_RESPONSE_QUANTITY
from src.utils.ipv4 import getaddrinfoIPv4


def get_default_history(extra_attributes):
    history = {
        COLUMNS: [
            HISTORY_INFO_NAME,
            HISTORY_INFO_AVERAGE_PRICE,
            HISTORY_INFO_TOTAL_MARKET,
            HISTORY_INFO_TOTAL_QUANTITY,
        ],
        ITEMS: [],
    }
    for extra_attribute in extra_attributes:
        history[COLUMNS].append(extra_attribute)

    return history


def maybe_enrich_history(history, extra_attributes):
    if COST in extra_attributes:
        history[COLUMNS].append(GIL_PER_CURRENCY)
    if DURATION in extra_attributes:
        history[COLUMNS].append(GIL_PER_VENTURE)


def get_items_id_to_name(items):
    item_ids_to_name = {}
    for item_name in items:
        item_ids_to_name[str(items[item_name][ID])] = item_name

    return item_ids_to_name


def get_universalis_response(items_id_to_name, server, timeframe_hours):
    time.sleep(PROCESSES / UNIVERSALIS_API_RATE_LIMIT_PER_SECOND)
    ids_in_url = list(items_id_to_name.keys())

    combined_items_result = {}

    for i in range(0, len(ids_in_url), MAX_IDS_PER_REQUEST_UNIVERSALIS):
        ids_chunk = ids_in_url[i : i + MAX_IDS_PER_REQUEST_UNIVERSALIS]

        ids_in_url_as_string = ""
        for item_id in list(ids_chunk):
            ids_in_url_as_string += f"{str(item_id)},"

        """
            Under the hood, the logic that does the request starts by opening a socket to validate the connection.
            This would sometimes hang until timeout, which took up to 2 mins.

            After debugging, I noticed that this only happened when the socket opened using IPv6, and was always fine
            when we did it using IPv4. It was flaky, sometimes worked for IPV6 and sometimes did not.

            To avoid unecessary failures and spending more time debugging this issue which might be on the API's side,
            I decided to mock the function opening the socket to force it to use IPv4.
        """
        with patch("socket.getaddrinfo", side_effect=getaddrinfoIPv4):
            universalis_request = requests.get(
                f"{UNIVERSALIS_REQUEST_URL}"
                f"{server.value}/"
                f"{ids_in_url_as_string}"
                f"?entriesWithin={timeframe_hours * 60 * 60}",
            )

        if universalis_request.status_code != 200:
            # TODO(): Handle retry if status_code is 5XX
            print(
                f"Failed to get requested items with error code {universalis_request.status_code}, "
                f"{universalis_request.url}, "
                f"{universalis_request.content}, "
                f"{universalis_request.text}"
            )
        else:
            result = json.loads(universalis_request.content)
            combined_items_result = combined_items_result | result[ITEMS]

    return {ITEMS: combined_items_result}


def calculate_item_info(item_id, result, items, items_id_to_name, extra_attributes):
    total_gil = 0
    total_quantity = 0

    if result[ITEMS][item_id].get(UNIVERSALIS_RESPONSE_ENTRIES) is None:
        pass  # Do nothing, this item wasn't sold in the selected time frame
    else:
        for entry in result[ITEMS][item_id][UNIVERSALIS_RESPONSE_ENTRIES]:
            total_gil += (
                entry[UNIVERSALIS_RESPONSE_PRICE] * entry[UNIVERSALIS_RESPONSE_QUANTITY]
            )
            total_quantity += entry[UNIVERSALIS_RESPONSE_QUANTITY]

    item_info = get_default_item_info(
        items, items_id_to_name[item_id], total_gil, total_quantity, extra_attributes
    )
    return item_info


def get_default_item_info(
    items, item_name, total_gil, total_quantity, extra_attributes
):
    average_price = math.floor(total_gil / total_quantity) if total_quantity > 0 else 0

    item_info = {
        HISTORY_INFO_NAME: item_name,
        HISTORY_INFO_AVERAGE_PRICE: average_price,
        HISTORY_INFO_TOTAL_MARKET: total_gil,
        HISTORY_INFO_TOTAL_QUANTITY: total_quantity,
    }

    for extra_attribute in extra_attributes:
        item_info[extra_attribute] = items[item_name][extra_attribute]

    return item_info


def maybe_enrich_item_info(item_info, extra_attributes):
    if COST in extra_attributes:
        item_info[GIL_PER_CURRENCY] = (
            item_info[HISTORY_INFO_AVERAGE_PRICE] / item_info[COST]
        )
    if DURATION in extra_attributes:
        item_info[GIL_PER_VENTURE] = (
            item_info[HISTORY_INFO_AVERAGE_PRICE] * item_info[QUANTITY]
        )


def get_history_bulk_items(items, server, timeframe_hours):
    extra_attributes = set(items[list(items.keys())[0]].keys())
    extra_attributes = sorted(extra_attributes)

    history = get_default_history(extra_attributes)
    maybe_enrich_history(history, extra_attributes)

    items_id_to_name = get_items_id_to_name(items)

    result = get_universalis_response(items_id_to_name, server, timeframe_hours)

    for item_id in result[ITEMS]:
        item_info = calculate_item_info(
            item_id, result, items, items_id_to_name, extra_attributes
        )
        maybe_enrich_item_info(item_info, extra_attributes)

        history[ITEMS].append(item_info)

    return history
