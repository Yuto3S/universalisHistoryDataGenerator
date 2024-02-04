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
