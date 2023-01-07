import json
from multiprocessing import Pool

from calculators import get_history_bulk_items
from datetime import date
import shutil

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


def calculate_shopping_lists(selected_server, timeframe_hours, specific_shopping_list):
    print(f"SELECTED SERVER: {selected_server}")
    folder_date = str(date.today())
    dir_path = f"assets/generated/history/{selected_server.value}/{timeframe_hours}/{folder_date}"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    for file_name in os.listdir("assets/generated/shopping_list/"):
        if specific_shopping_list and file_name != specific_shopping_list:
            pass    # Do nothing
        else:
            print(f"{selected_server} --> {file_name}")
            with open(f"assets/generated/shopping_list/{file_name}", "r") as input_calculate_json_file:
                items = json.load(input_calculate_json_file)
                history = get_history_bulk_items(items, selected_server, timeframe_hours)

            with open(f"{dir_path}/{file_name}", "w") as output_file:
                output_file.write(json.dumps(history))


def copy_and_push_to_git():
    # TODO: Copy files to front-end service and push new branch to git to deploy changes
    shutil.copytree("./assets/generated/history", "../my-app/src/assets/history", dirs_exist_ok=True)
    shutil.copytree("./assets/generated/history", "../my-app/docs/assets/history", dirs_exist_ok=True)
    shutil.copy("./assets/generated/history_tree.json", "../my-app/src/assets/history_tree.json")
    shutil.copy("./assets/generated/history_tree.json", "../my-app/docs/assets/history_tree.json")
    os.popen(f"cd .. && cd my-app/ && git add . && git commit -m \"New shopping list informations for {str(date.today())}\" && git push")


if __name__ == '__main__':
    should_fetch_new_items = False
    should_generate_new_shopping_lists = False
    should_calculate_shopping_lists = True
    should_copy_and_push_to_git = False
    specific_shopping_list = None
    servers = [server for server in FFXIVServers]
    timeframe_history_hours = HistoryTimeFrameHours.SEVEN_DAYS.value

    if should_fetch_new_items:
        fetch_items_data()

    if should_generate_new_shopping_lists:
        generate_files_from_manual_input()

    if should_calculate_shopping_lists:
        with Pool(processes=PROCESSES) as pool:
            result = pool.map(
                partial(
                    calculate_shopping_lists,
                    timeframe_hours=timeframe_history_hours,
                    specific_shopping_list=specific_shopping_list
                ),
                servers
            )

    files_tree = get_files_tree_starting_on_folder("assets/generated/history")
    with open(f"assets/generated/history_tree.json", "w") as latest_tree:
        latest_tree.write(json.dumps(files_tree))

    if should_copy_and_push_to_git:
        copy_and_push_to_git()
