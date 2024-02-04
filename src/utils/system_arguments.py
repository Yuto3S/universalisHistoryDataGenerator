import getopt
from enum import Enum

from src.consts import FFXIVServers
from src.consts import HistoryTimeFrameHours


class SystemArgument(Enum):
    CALCULATE_SHOPPING_LISTS = "calculate_shopping_lists"
    FETCH_NEW_ITEMS = "fetch_new_items"
    GENERATE_NEW_SHOPPING_LISTS = "generate_new_shopping_lists"
    PUSH_TO_GIT = "push_to_git"
    SERVER = "server"
    SPECIFIC_SHOPPING_LIST = "specific_shopping_list"
    TIMEFRAME_HOURS = "timeframe_hours"


def parse_system_arguments(argument_list):
    calculate_shopping_lists = False
    fetch_new_items = False
    generate_new_shopping_lists = False
    push_to_git = False
    servers = [server for server in FFXIVServers]
    specific_shopping_list = None
    timeframe_hours = HistoryTimeFrameHours.ONE_DAY

    long_options = [f"{system_argument.value}=" for system_argument in SystemArgument]

    try:
        # Parsing argument
        print(argument_list)
        arguments, values = getopt.getopt(argument_list, ":", long_options)
        # checking each argument
        for current_argument, current_value in arguments:
            current_argument = SystemArgument(current_argument.split("--")[1])
            print(current_argument, current_value)
            match current_argument:
                case SystemArgument.CALCULATE_SHOPPING_LISTS:
                    calculate_shopping_lists = (
                        True if current_value == "True" else False
                    )
                case SystemArgument.FETCH_NEW_ITEMS:
                    fetch_new_items = True if current_value == "True" else False
                case SystemArgument.GENERATE_NEW_SHOPPING_LISTS:
                    generate_new_shopping_lists = (
                        True if current_value == "True" else False
                    )
                case SystemArgument.PUSH_TO_GIT:
                    push_to_git = True if current_value == "True" else False
                case SystemArgument.SERVER:
                    servers = [
                        FFXIVServers(current_server)
                        for current_server in current_value.split(",")
                    ]
                case SystemArgument.SPECIFIC_SHOPPING_LIST:
                    specific_shopping_list = current_value
                case SystemArgument.TIMEFRAME_HOURS:
                    timeframe_hours = HistoryTimeFrameHours(int(current_value))
                case _:
                    raise Exception(
                        f"{current_argument} doesn't have any implementation."
                    )

    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))

    return (
        calculate_shopping_lists,
        fetch_new_items,
        generate_new_shopping_lists,
        push_to_git,
        servers,
        specific_shopping_list,
        timeframe_hours,
    )
