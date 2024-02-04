from enum import Enum

# One process per server
PROCESSES = 8
UNIVERSALIS_API_RATE_LIMIT_PER_SECOND = 20


ID = "id"

UNIVERSALIS_REQUEST_URL = "https://universalis.app/api/v2/history/"
MAX_IDS_PER_REQUEST_UNIVERSALIS = 100
UNIVERSALIS_RESPONSE_PRICE = "pricePerUnit"
UNIVERSALIS_RESPONSE_QUANTITY = "quantity"
UNIVERSALIS_RESPONSE_ENTRIES = "entries"

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


class SystemArgument(Enum):
    TEST = "test"
    PUSH_TO_GIT = "push_to_git"
    SERVER = "server"
    SHOULD_CALCULATE_SHOPPING_LISTS = "should_calculate_shopping_lists"
    SHOULD_FETCH_NEW_ITEMS = "should_fetch_new_items"
    SHOULD_GENERATE_NEW_SHOPPING_LISTS = "should_generate_new_shopping_lists"
    SPECIFIC_SHOPPING_LIST = "specific_shopping_list"
    TIMEFRAME_HOURS = "timeframe_hours"
