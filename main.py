import getopt
import json
import os
import sys
from datetime import date
from datetime import datetime
from functools import partial
from multiprocessing import Pool

from src.calculators import get_history_bulk_items
from src.consts import FFXIVServers
from src.consts import HistoryTimeFrameHours
from src.consts import PROCESSES
from src.generators import generate_all_items_name_to_id
from src.generators import generate_json
from src.utils.files_manipulation import get_files_tree_starting_on_folder
from src.utils.git import push_to_git

"""
    TODO:
    - One shopping file per:
        - white scrip crafter
        - purple scrip crafter
    - Remove "materias.json"
    - Update venture files with new gear values. Rename them to start with "venture_"
    - Description of the files that is being sent to the front-end
    - Add black for python formatting
    - Split logic to calculate values/average and writing it into a file
        (writing into files/reading from files should be done in its own logic parts as much as possible)
    - Tests
    - Working only_hq flag for pots/foods
    - Make function runnable from command line
    - Make the following variable parameters of the command line function:
        should_fetch_new_items
        should_generate_new_shopping_lists
        should_calculate_shopping_lists
        should_push_to_git
        specific_shopping_list
        servers
        timeframe_history_hours
"""


def fetch_items_data():
    """
    Run this logic when new items that can be sold on the MarketBoard are added into the game
    This is likely when a new patch happens (versions _.X)
    """
    generate_all_items_name_to_id()


def generate_files_from_manual_input():
    """
    Run after modifying files in assets/manual_input/
    """
    for file_name in os.listdir("assets/manual_input/shopping_list/"):
        generate_json(file_name)


def calculate_shopping_lists(
    selected_server,
    folder_date_func,
    timeframe_hours,
    maybe_specific_shopping_list,
    custom_path,
):
    if custom_path:
        print(custom_path)

    dir_path = (
        f"{custom_path}"
        f"assets/generated/history/"
        f"{selected_server.value}/"
        f"{timeframe_hours.value}/"
        f"{folder_date_func}"
    )

    print(dir_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    for file_name in os.listdir(f"{custom_path}assets/generated/shopping_list/"):
        if maybe_specific_shopping_list and file_name != maybe_specific_shopping_list:
            pass  # Do nothing
        else:
            print(f"{selected_server} --> {file_name}")
            with open(
                f"{custom_path}assets/generated/shopping_list/{file_name}", "r"
            ) as input_calculate_json_file:
                items = json.load(input_calculate_json_file)
                history = get_history_bulk_items(
                    items, selected_server, timeframe_hours.value
                )

            with open(f"{dir_path}/{file_name}", "w") as output_file:
                output_file.write(json.dumps(history))

    print(f"{selected_server} --> Done")


if __name__ == "__main__":
    argument_list = sys.argv[1:]
    long_options = [
        "timeframe_hours=",
        "server=",
        "specific_shopping_list=",
        "push_to_git=",
        "should_fetch_new_items=",
        "should_calculate_shopping_lists=",
        "should_generate_new_shopping_lists=",
    ]

    should_fetch_new_items = False
    should_generate_new_shopping_lists = False
    should_calculate_shopping_lists = False
    should_push_to_git = False
    specific_shopping_list = None
    servers = [server for server in FFXIVServers]
    timeframe_history_hours = HistoryTimeFrameHours.ONE_DAY
    path = os.getenv("PYTHON_UNIVERSALIS_SCRIPT_PATH")
    print(path)

    try:
        # Parsing argument
        print(argument_list)
        arguments, values = getopt.getopt(argument_list, ":", long_options)
        # checking each argument
        for current_argument, current_value in arguments:
            print(current_argument, current_value)
            if "should_fetch_new_items" in current_argument:
                should_fetch_new_items = True if current_value == "True" else False
            if "should_generate_new_shopping_lists" in current_argument:
                should_generate_new_shopping_lists = (
                    True if current_value == "True" else False
                )
            if "should_calculate_shopping_lists" in current_argument:
                should_calculate_shopping_lists = (
                    True if current_value == "True" else False
                )
            if "timeframe_hours" in current_argument:
                timeframe_history_hours = HistoryTimeFrameHours(int(current_value))
                print(f"Timeframe in hours selected: {timeframe_history_hours}")
            elif "server" in current_argument:
                servers = [FFXIVServers(current_value)]
                print(f"Specific server selected: {servers}")
            elif "specific_shopping_list" in current_argument:
                specific_shopping_list = current_value
                print(f"Specific shopping list selected: {specific_shopping_list}")
            elif "push_to_git" in current_argument:
                should_push_to_git = True if current_value == "True" else False
                print(f"Should push to git: {should_push_to_git}")

    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))

    folder_date = str(date.today())

    if timeframe_history_hours == HistoryTimeFrameHours.ONE_HOUR:
        now = datetime.now()
        folder_date += f"-{now.hour:02d}-{now.minute:02d}"

    if should_fetch_new_items:
        fetch_items_data()

    if should_generate_new_shopping_lists:
        generate_files_from_manual_input()

    if should_calculate_shopping_lists:
        if len(servers) == 1:
            calculate_shopping_lists(
                selected_server=servers[0],
                folder_date_func=folder_date,
                timeframe_hours=timeframe_history_hours,
                maybe_specific_shopping_list=specific_shopping_list,
                custom_path=path,
            )
        else:
            with Pool(processes=PROCESSES) as pool:
                result = pool.map(
                    partial(
                        calculate_shopping_lists,
                        folder_date_func=folder_date,
                        timeframe_hours=timeframe_history_hours,
                        maybe_specific_shopping_list=specific_shopping_list,
                        custom_path=path,
                    ),
                    servers,
                )

    files_tree = get_files_tree_starting_on_folder(f"{path}assets/generated/history")
    with open(f"{path}assets/generated/history_tree.json", "w") as latest_tree:
        latest_tree.write(json.dumps(files_tree))

    if should_calculate_shopping_lists and should_push_to_git:
        print("Pushing to git...")
        push_to_git(folder_date, servers, timeframe_history_hours, path)

    print(" --- Done --- ")
