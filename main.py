import json
import os
import sys
from datetime import date
from datetime import datetime
from functools import partial
from multiprocessing import Pool

from src.calculators import get_history_bulk_items
from src.consts import HistoryTimeFrameHours
from src.consts import PROCESSES
from src.generators import generate_all_items_name_to_id
from src.generators import generate_json
from src.utils.files_manipulation import get_files_tree_starting_on_folder
from src.utils.system_arguments import parse_system_arguments

"""
    TODO:
    - One shopping file per:
        - white scrip crafter
        - purple scrip crafter
    - Update venture files with new gear values. Rename them to start with "venture_"
    - Description of the files that is being sent to the front-end
    - Add black for python formatting
    - Split logic to calculate values/average and writing it into a file
        (writing into files/reading from files should be done in its own logic parts as much as possible)
    - Tests
    - Working only_hq flag for pots/foods
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


def func_calculate_shopping_lists(
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

    path = os.getenv("PYTHON_UNIVERSALIS_SCRIPT_PATH")
    print(path)

    folder_date = str(date.today())

    (
        calculate_shopping_lists,
        fetch_new_items,
        generate_new_shopping_lists,
        push_to_git,
        servers,
        specific_shopping_list,
        timeframe_hours,
    ) = parse_system_arguments(argument_list)

    if timeframe_hours == HistoryTimeFrameHours.ONE_HOUR:
        now = datetime.now()
        folder_date += f"-{now.hour:02d}-{now.minute:02d}"

    if fetch_new_items:
        fetch_items_data()

    if generate_new_shopping_lists:
        generate_files_from_manual_input()

    if calculate_shopping_lists:
        if len(servers) == 1:
            func_calculate_shopping_lists(
                selected_server=servers[0],
                folder_date_func=folder_date,
                timeframe_hours=timeframe_hours,
                maybe_specific_shopping_list=specific_shopping_list,
                custom_path=path,
            )
        else:
            # TODO(): We can't use ipdb if we go through this flow. If you want to debug, please input only 1 server.
            with Pool(processes=PROCESSES) as pool:
                result = pool.map(
                    partial(
                        func_calculate_shopping_lists,
                        folder_date_func=folder_date,
                        timeframe_hours=timeframe_hours,
                        maybe_specific_shopping_list=specific_shopping_list,
                        custom_path=path,
                    ),
                    servers,
                )

    files_tree = get_files_tree_starting_on_folder(f"{path}assets/generated/history")
    with open(f"{path}assets/generated/history_tree.json", "w") as latest_tree:
        latest_tree.write(json.dumps(files_tree))

    if calculate_shopping_lists and push_to_git:
        print("Pushing to git...")
        push_to_git(folder_date, servers, timeframe_hours, path)

    print(" --- Done --- ")
