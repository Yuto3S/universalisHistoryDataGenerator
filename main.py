# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import json

from calculators import calculate_values_bulk
from datetime import date
from datetime import datetime
# Press the green button in the gutter to run the script.
from consts import FFXIVServers, HistoryTimeFrameHours
from generators import generate_json, generate_all_items_name_to_id
import os
from distutils.dir_util import copy_tree

# TODO:
from src.utils import get_files_tree_starting_on_folder

"""
- Seeds
- Furnishing
- Add working only_hq flag for pots/foods
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


def calculate_shopping_lists(selected_server, timeframe_hours, specific_shopping_list):
    folder_date = str(date.today())
    dir_path = f"assets/generated/history/{selected_server.value}/{timeframe_hours}/{folder_date}"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    for file_name in os.listdir("assets/generated/shopping_list/"):
        if specific_shopping_list and file_name != specific_shopping_list:
            pass    # Do nothing
        else:
            print(file_name)
            with open(f"assets/generated/shopping_list/{file_name}", "r") as input_calculate_json_file:
                items = json.load(input_calculate_json_file)
                history = get_history_bulk_items(items, selected_server, timeframe_hours)

            with open(f"{dir_path}/{file_name}", "w") as output_file:
                output_file.write(json.dumps(history))


if __name__ == '__main__':
    should_fetch_new_items = False
    should_generate_new_shopping_lists = False
    should_calculate_shopping_lists = True
    specific_shopping_list = None
    servers = [server for server in FFXIVServers]
    timeframe_history_hours = HistoryTimeFrameHours.SEVEN_DAYS.value

    if should_fetch_new_items:
        fetch_items_data()

    if should_generate_new_shopping_lists:
        generate_files_from_manual_input()

    if should_calculate_shopping_lists:
        for server in servers:
            print(f"SERVER {server} SERVER")
            calculate_shopping_lists(server, timeframe_history_hours, specific_shopping_list)

    files_tree = get_files_tree_starting_on_folder("assets/generated/history")
    with open(f"assets/generated/history_tree.json", "w") as latest_tree:
        latest_tree.write(json.dumps(files_tree))

    # TODO: Copy files to front-end service and push new branch to git to deploy changes
    # copy_tree(
    #     "./assets/generated/history",
    #     "../my-app/src/assets",
    # )
