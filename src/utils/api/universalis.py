import json
import time
from unittest.mock import patch

import requests

from src.consts import ITEMS
from src.consts import PROCESSES
from src.utils.ipv4 import getaddrinfoIPv4


UNIVERSALIS_API_RATE_LIMIT_PER_SECOND = 20

UNIVERSALIS_REQUEST_URL = "https://universalis.app/api/v2/history/"
MAX_IDS_PER_REQUEST_UNIVERSALIS = 100
UNIVERSALIS_RESPONSE_PRICE = "pricePerUnit"
UNIVERSALIS_RESPONSE_QUANTITY = "quantity"
UNIVERSALIS_RESPONSE_ENTRIES = "entries"


def get_universalis_response(items_id_to_name, server, timeframe_hours):
    time.sleep(PROCESSES / UNIVERSALIS_API_RATE_LIMIT_PER_SECOND)
    ids_in_url = list(items_id_to_name.keys())

    combined_items_result = {}

    for i in range(0, len(ids_in_url), MAX_IDS_PER_REQUEST_UNIVERSALIS):
        ids_chunk = ids_in_url[i : i + MAX_IDS_PER_REQUEST_UNIVERSALIS]

        ids_in_url_as_string = ""
        for item_id in list(ids_chunk):
            ids_in_url_as_string += f"{str(item_id)},"

        result = get_and_retry_universalis(
            f"{UNIVERSALIS_REQUEST_URL}"
            f"{server.value}/"
            f"{ids_in_url_as_string}"
            f"?entriesWithin={timeframe_hours * 60 * 60}",
        )
        combined_items_result = combined_items_result | result[ITEMS]

    return {ITEMS: combined_items_result}


def get_and_retry_universalis(url, retries=2):
    """
    Under the hood, the logic that does the request starts by opening a socket to validate the connection.
    This would sometimes hang until timeout, which took up to 2 mins.

    After debugging, I noticed that this only happened when the socket opened using IPv6, and was always fine
    when we did it using IPv4. It was flaky, sometimes worked for IPV6 and sometimes did not.

    To avoid unecessary failures and spending more time debugging this issue which might be on the API's side,
    I decided to mock the function opening the socket to force it to use IPv4.
    """
    for _ in range(0, retries):
        with patch("socket.getaddrinfo", side_effect=getaddrinfoIPv4):
            universalis_request = requests.get(url)

        if universalis_request.status_code != 200:
            pass
        else:
            return json.loads(universalis_request.content)

    print(
        f"Failed with error code {universalis_request.status_code} and {retries} retries to get url "
        f"{universalis_request.url}"
    )
    return {}
