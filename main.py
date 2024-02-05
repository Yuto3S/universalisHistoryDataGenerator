import os
from datetime import date
from datetime import datetime
from functools import partial
from multiprocessing import Pool

from src.calculators.history import func_calculate_shopping_lists
from src.consts import FILE_PATH_GENERATED_HISTORY
from src.consts import FILE_PATH_GENERATED_HISTORY_TREE
from src.consts import FILE_PATH_MANUAL_SHOPPING_LIST
from src.consts import HistoryTimeFrameHours
from src.consts import PROCESSES
from src.generators import generate_all_items_name_to_id
from src.generators import generate_json
from src.utils.command_line_arguments import parse_command_line_arguments
from src.utils.files import get_files_tree_starting_on_folder
from src.utils.files import get_root_project_path
from src.utils.files import write_dict_content_on_file
from src.utils.git import push_generated_to_git

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


if __name__ == "__main__":
    folder_date = str(date.today())

    (
        calculate_shopping_lists,
        fetch_new_items,
        generate_new_shopping_lists,
        push_to_git,
        servers,
        specific_shopping_list,
        timeframe_hours,
    ) = parse_command_line_arguments()

    if timeframe_hours == HistoryTimeFrameHours.ONE_HOUR:
        now = datetime.now()
        folder_date += f"-{now.hour:02d}-{now.minute:02d}"

    if fetch_new_items:
        generate_all_items_name_to_id()

    if generate_new_shopping_lists:
        for file_name in os.listdir(FILE_PATH_MANUAL_SHOPPING_LIST):
            print(file_name)
            generate_json(file_name)

    if calculate_shopping_lists:
        if len(servers) == 1:
            func_calculate_shopping_lists(
                selected_server=servers[0],
                folder_date=folder_date,
                timeframe_hours=timeframe_hours,
                maybe_specific_shopping_list=specific_shopping_list,
            )
        else:
            # TODO(): We can't use ipdb if we go through this flow. If you want to debug, please input only 1 server.
            with Pool(processes=PROCESSES) as pool:
                result = pool.map(
                    partial(
                        func_calculate_shopping_lists,
                        folder_date=folder_date,
                        timeframe_hours=timeframe_hours,
                        maybe_specific_shopping_list=specific_shopping_list,
                    ),
                    servers,
                )

    files_tree = get_files_tree_starting_on_folder(
        f"{get_root_project_path()}{FILE_PATH_GENERATED_HISTORY}"
    )
    write_dict_content_on_file(files_tree, FILE_PATH_GENERATED_HISTORY_TREE)

    if push_to_git:
        print("Pushing to git...")
        push_generated_to_git(folder_date, servers, timeframe_hours)

    print(" --- Done --- ")
