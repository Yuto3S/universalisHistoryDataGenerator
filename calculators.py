import json
import math

import requests

UNIVERSALIS_REQUEST_URL = f"https://universalis.app/api/v2/history/"


JSON_OUTPUT_KEYS = {
    "Item Name": "item_name",
    "Average Price": "average_price",
    "Total Market": "total_market",
    "Total Sold": "total_sold",
    "Average Quantity Sold": "average_quantity",
    "Stack of 99 Sold": "stack_of_99",
}

JSON_OUTPUT_EXTRA_KEYS = {
    "Id": "id",
}


def common_item_print(item_name, total_gil, total_quantity, entries, stack_of_99):
    average_price = math.floor(total_gil / total_quantity) if total_quantity > 0 else 0
    average_quantity_sold = math.floor(total_quantity / entries) if entries > 0 else 0

    output = f"{item_name}" \
             f";{average_price}" \
             f";{total_gil}" \
             f";{total_quantity}" \
             f";{average_quantity_sold}" \
             f";{stack_of_99}"

    return output


def common_item_json(item_name, total_gil, total_quantity, entries, stack_of_99):
    average_price = math.floor(total_gil / total_quantity) if total_quantity > 0 else 0
    average_quantity_sold = math.floor(total_quantity / entries) if entries > 0 else 0

    # TODO: move to const
    item_info = {
        "Item Name": item_name,
        "Average Price": average_price,
        "Total Market": total_gil,
        "Total Sold": total_quantity,
        # "Average Quantity Sold": average_quantity_sold,
        # "Stack of 99 Sold": stack_of_99,
    }

    return item_info


def calculate_item_info(item_id, server, timeframe_hours, only_hq=False):
    universalis_timeframe_seconds = timeframe_hours*60*60
    universalis_request = requests.get(f"{UNIVERSALIS_REQUEST_URL}/{server.value}/{item_id}?entriesWithin={universalis_timeframe_seconds}")

    if universalis_request.status_code == 200:
        result = json.loads(universalis_request.content)
    else:
        result = {}
        print(universalis_request.status_code)

    total_quantity_sold = 0
    total_price = 0
    stack_of_99 = 0

    if result.get("entries") is None:
        print(item_id)
        return 0, 0, 0, 0
    else:
        for entry in result["entries"]:
            if only_hq and not entry["hq"]:
                pass  # This entry doesn't fulfill our criteria
            else:
                total_price += entry["pricePerUnit"] * entry["quantity"]
                total_quantity_sold += entry["quantity"]
                if entry["quantity"] == 99:
                    stack_of_99 += 1

        return total_price, total_quantity_sold, len(result["entries"]), stack_of_99


def calculate_item_info_array(item_id, only_hq=False):
    print("request")
    universalis_request = requests.get(f"{UNIVERSALIS_TWINTANIA_REQUEST_URL}{item_id}?entriesWithin=604800")
    print("response")
    result = json.loads(universalis_request.content)

    quantities = []
    price_per_units = []
    stack_of_99 = 0

    if result.get("entries") is None:
        print(item_id)
        return 0, 0, 0, 0
    else:
        for entry in result["entries"]:
            if only_hq and not entry["hq"]:
                pass  # This entry doesn't fulfill our criteria
            else:
                price_per_units.append(entry["pricePerUnit"])
                quantities.append(entry["quantity"])
                if entry["quantity"] == 99:
                    stack_of_99 += 1

    price_per_units, quantities = remove_outliers(price_per_units, quantities)

    return 0, 0, len(result["entries"]), stack_of_99


def remove_outliers(price_per_units, quantities):
    if len(price_per_units) > 1:
        print(price_per_units)
        print(quantities)
        mean_price = sum(price_per_units) / len(price_per_units)
        differences = [(price - mean_price)**2 for price in price_per_units]
        standard_deviation = (sum(differences) / (len(price_per_units) - 1)) ** 0.5
        print(mean_price)
        print(standard_deviation)

        if standard_deviation > 0:
            zscores = [(price - mean_price) / standard_deviation for price in price_per_units]
            print(zscores)

    return 0, 0


def calculate_values(items, server, timeframe_hours):
    extra_attributes = set(items[list(items.keys())[0]].keys())
    extra_attributes = sorted(extra_attributes)

    # TODO: move those columns into CONSTS
    output = {
        "columns": [
            "Item Name",
            "Average Price",
            "Total Market",
            "Total Sold",
            # "Average Quantity Sold",
            # "Stack of 99 Sold",
        ],
        "items": [],
    }
    for extra_attribute in extra_attributes:
        output["columns"].append(extra_attribute)

    # TODO: move to helper function
    # CUSTOM LOGIC BASED ON COLUMNS BEGIN
    if "cost" in extra_attributes:
        output["columns"].append("Price/Cost")
    if "duration" in extra_attributes:
        output["columns"].append("Gil/Duration*Quantity")
    # CUSTOM LOGIC BASED ON COLUMNS END

    for item_name in items:
        print(item_name)
        item_id = items[item_name]["id"]
        total_gil, total_quantity_sold, entries, stack_of_99 = calculate_item_info(item_id, server, timeframe_hours)

        item_info = common_item_json(item_name, total_gil, total_quantity_sold, entries, stack_of_99)
        for extra_attribute in extra_attributes:
            item_info[extra_attribute] = items[item_name][extra_attribute]

        # TODO: move to helper function
        # CUSTOM LOGIC BASED ON COLUMNS BEGIN
        if "cost" in extra_attributes:
            item_info["Price/Cost"] = item_info["Average Price"] / item_info["cost"]
        if "duration" in extra_attributes:
            item_info["Gil/Duration*Quantity"] = item_info["Average Price"] / item_info["duration"] * item_info["quantity"]
        # CUSTOM LOGIC BASED ON COLUMNS END

        output["items"].append(item_info)

    return output
