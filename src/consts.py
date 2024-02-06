from enum import Enum


NON_BREAKING_SPACE = " "

ID = "id"


QUANTITY = "quantity"
COLUMNS = "columns"
ITEMS = "items"
COST = "cost"
CURRENCY = "currency"
DURATION = "duration"


GIL_PER_CURRENCY = "Price/Cost"
GIL_PER_VENTURE = "Gil/Venture"

HISTORY_INFO_NAME = "Name"
HISTORY_INFO_AVERAGE_PRICE = "Average Price"
HISTORY_INFO_TOTAL_MARKET = "Total Market"
HISTORY_INFO_TOTAL_QUANTITY = "Total Quantity"


FILE_PATH_MANUAL_SHOPPING_LIST = "assets/manual_input/shopping_list/"
FILE_PATH_GENERATED_SHOPPING_LIST = "assets/generated/shopping_list/"
FILE_PATH_GENERATED_HISTORY = "assets/generated/history/"
FILE_PATH_GENERATED_HISTORY_TREE = "assets/generated/history_tree.json"
FILE_PATH_GENERATED_ALL_ITEMS_NAMES_TO_ID = (
    "assets/generated/config/all_items_name_to_id.json"
)


class FFXIVServers(Enum):
    ALPHA = "Alpha"
    LICH = "Lich"
    ODIN = "Odin"
    PHOENIX = "Phoenix"
    RAIDEN = "Raiden"
    SHIVA = "Shiva"
    TWINTANIA = "Twintania"
    ZODIARK = "Zodiark"


class HistoryTimeFrameHours(Enum):
    SEVEN_DAYS = 168
    ONE_DAY = 24
    ONE_HOUR = 1


class VentureType(Enum):
    BOTANY = "botany"
    HUNTING = "hunting"
    MINING = "mining"


PROCESSES = len(FFXIVServers)
