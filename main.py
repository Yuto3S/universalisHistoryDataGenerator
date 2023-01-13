import json
from multiprocessing import Pool

from calculators import get_history_bulk_items
from datetime import date, datetime
from git import Repo

from consts import FFXIVServers, HistoryTimeFrameHours, PROCESSES
from generators import generate_json, generate_all_items_name_to_id
import os
from functools import partial

from src.utils import get_files_tree_starting_on_folder

"""
    TODO:
    Working only_hq flag for pots/foods
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


def calculate_shopping_lists(selected_server, folder_date_func, timeframe_hours, maybe_specific_shopping_list):
    dir_path = f"assets/generated/history/{selected_server.value}/{timeframe_hours}/{folder_date_func}"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    for file_name in os.listdir("assets/generated/shopping_list/"):
        if maybe_specific_shopping_list and file_name != maybe_specific_shopping_list:
            pass    # Do nothing
        else:
            print(f"{selected_server} --> {file_name}")
            with open(f"assets/generated/shopping_list/{file_name}", "r") as input_calculate_json_file:
                items = json.load(input_calculate_json_file)
                history = get_history_bulk_items(items, selected_server, timeframe_hours)

            with open(f"{dir_path}/{file_name}", "w") as output_file:
                output_file.write(json.dumps(history))

    print(f"{selected_server} --> Done")


def push_to_git(folder_name, list_of_servers, timeframe_hours):
    try:
        repo = Repo("./")
        repo.git.add("assets/generated/history")
        repo.git.add("assets/generated/history_tree.json")
        repo.index.commit(
            f"New shopping list informations for {folder_name} - "
            f"{[server.value for server in list_of_servers]} - "
            f"over the last {timeframe_hours} hours. "
        )
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Some error occured while pushing the code')


if __name__ == '__main__':
    should_fetch_new_items = True
    should_generate_new_shopping_lists = True
    should_calculate_shopping_lists = False
    should_push_to_git = False
    specific_shopping_list = None
    servers = [server for server in FFXIVServers]
    # servers = [FFXIVServers.TWINTANIA]
    timeframe_history_hours = HistoryTimeFrameHours.ONE_DAY.value
    folder_date = str(date.today())

    if timeframe_history_hours == HistoryTimeFrameHours.ONE_HOUR.value:
        now = datetime.now()
        folder_date += f"-{now.hour:02d}-{now.minute:02d}"

    if should_fetch_new_items:
        fetch_items_data()

    if should_generate_new_shopping_lists:
        generate_files_from_manual_input()

    if should_calculate_shopping_lists:
        with Pool(processes=PROCESSES) as pool:
            result = pool.map(
                partial(
                    calculate_shopping_lists,
                    folder_date_func=folder_date,
                    timeframe_hours=timeframe_history_hours,
                    maybe_specific_shopping_list=specific_shopping_list
                ),
                servers
            )

    files_tree = get_files_tree_starting_on_folder("assets/generated/history")
    with open(f"assets/generated/history_tree.json", "w") as latest_tree:
        latest_tree.write(json.dumps(files_tree))

    if should_calculate_shopping_lists and should_push_to_git:
        push_to_git(folder_date, servers, timeframe_history_hours)
