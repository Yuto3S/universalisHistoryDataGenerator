from enum import Enum


class FFXIVServers(Enum):
    SHIVA = "Shiva"
    TWINTANIA = "Twintania"
    ZODIARK = "Zodiark"


class HistoryTimeFrameHours(Enum):
    SEVEN_DAYS = 168


class VentureType(Enum):
    BOTANY = "botany"
    HUNTING = "hunting"
    MINING = "mining"


class MateriaType(Enum):
    DISCIPLE_OF_WAR_OR_MAGIC__BATTLE = "dow_dom"
    DISCILPE_OF_THE_HAND__CRAFTER = "doh"
    DISCIPLE_OF_THE_LAND__GATHERER = "dol"

