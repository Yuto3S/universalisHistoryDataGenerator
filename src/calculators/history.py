import math

from src.consts import COLUMNS
from src.consts import COST
from src.consts import DURATION
from src.consts import GIL_PER_CURRENCY
from src.consts import GIL_PER_VENTURE
from src.consts import HISTORY_INFO_AVERAGE_PRICE
from src.consts import HISTORY_INFO_NAME
from src.consts import HISTORY_INFO_TOTAL_MARKET
from src.consts import HISTORY_INFO_TOTAL_QUANTITY
from src.consts import ITEMS
from src.consts import QUANTITY
from src.generators.items import get_items_id_to_name
from src.utils.api.universalis import get_universalis_response
from src.utils.api.universalis import UNIVERSALIS_RESPONSE_ENTRIES
from src.utils.api.universalis import UNIVERSALIS_RESPONSE_PRICE
from src.utils.api.universalis import UNIVERSALIS_RESPONSE_QUANTITY


def get_trends_history(items, server, timeframe_hours):
    extra_columns = set(items[list(items.keys())[0]].keys())
    extra_columns = sorted(extra_columns)

    history = get_default_history(extra_columns)
    items_id_to_name = get_items_id_to_name(items)

    result = get_universalis_response(items_id_to_name, server, timeframe_hours)

    for item_id in result[ITEMS]:
        item_info = calculate_columns_for_item(
            item_id, result, items, items_id_to_name, extra_columns
        )

        history[ITEMS].append(item_info)

    return history


def get_default_history(extra_columns):
    default_columns = [
        HISTORY_INFO_NAME,
        HISTORY_INFO_AVERAGE_PRICE,
        HISTORY_INFO_TOTAL_MARKET,
        HISTORY_INFO_TOTAL_QUANTITY,
    ]

    history = {
        COLUMNS: default_columns,
        ITEMS: [],
    }
    for column in extra_columns:
        history[COLUMNS].append(column)

    maybe_add_extra_columns(history, extra_columns)

    return history


def maybe_add_extra_columns(history, extra_columns):
    if COST in extra_columns:
        history[COLUMNS].append(GIL_PER_CURRENCY)
    if DURATION in extra_columns:
        history[COLUMNS].append(GIL_PER_VENTURE)


def calculate_columns_for_item(item_id, result, items, items_id_to_name, extra_columns):
    total_gil, total_quantity = calculate_gil_and_quantity_for_item(result, item_id)
    # TODO Implement math logic to remove outliers, as the items sometimes used to transfer large sums of money.
    average_price = math.floor(total_gil / total_quantity) if total_quantity > 0 else 0

    item_info = {
        HISTORY_INFO_NAME: items_id_to_name[item_id],
        HISTORY_INFO_AVERAGE_PRICE: average_price,
        HISTORY_INFO_TOTAL_MARKET: total_gil,
        HISTORY_INFO_TOTAL_QUANTITY: total_quantity,
    }

    for column in extra_columns:
        item_info[column] = items[items_id_to_name[item_id]][column]

    maybe_add_extra_columns_for_item(item_info, extra_columns)

    return item_info


def calculate_gil_and_quantity_for_item(result, item_id):
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

    return total_gil, total_quantity


def maybe_add_extra_columns_for_item(item_info, extra_columns):
    if COST in extra_columns:
        item_info[GIL_PER_CURRENCY] = (
            item_info[HISTORY_INFO_AVERAGE_PRICE] / item_info[COST]
        )
    if DURATION in extra_columns:
        item_info[GIL_PER_VENTURE] = (
            item_info[HISTORY_INFO_AVERAGE_PRICE] * item_info[QUANTITY]
        )
