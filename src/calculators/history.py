from functools import partial
from multiprocessing import Pool

from src.calculators.calculators import get_history_bulk_items
from src.consts import FILE_PATH_GENERATED_HISTORY
from src.consts import FILE_PATH_GENERATED_HISTORY_TREE
from src.consts import FILE_PATH_GENERATED_SHOPPING_LIST
from src.consts import PROCESSES
from src.utils.files import get_all_file_names_in_dir
from src.utils.files import get_files_tree_starting_on_folder
from src.utils.files import get_folder_date
from src.utils.files import get_generated_shopping_lists_path
from src.utils.files import get_root_project_path
from src.utils.files import maybe_make_dir
from src.utils.files import read_dict_from_file
from src.utils.files import write_dict_content_on_file
from src.utils.git import push_generated_to_git


def calculate_trends(servers, push_to_git, timeframe_hours, specific_shopping_list):
    folder_date = get_folder_date(timeframe_hours)

    # TODO(): Find a way to debug with ipdb through Pool/multiprocesses
    if len(servers) == 1:
        # It is currently only possible to debug using ipdb if you only have 1 server.
        func_calculate_shopping_lists(
            selected_server=servers[0],
            folder_date=folder_date,
            timeframe_hours=timeframe_hours,
            maybe_specific_shopping_list=specific_shopping_list,
        )
    else:
        with Pool(processes=PROCESSES) as pool:
            pool.map(
                partial(
                    func_calculate_shopping_lists,
                    folder_date=folder_date,
                    timeframe_hours=timeframe_hours,
                    maybe_specific_shopping_list=specific_shopping_list,
                ),
                servers,
            )

    update_history_tree()

    if push_to_git:
        print("Pushing to git...")
        push_generated_to_git(folder_date, servers, timeframe_hours)


def func_calculate_shopping_lists(
    selected_server,
    folder_date,
    timeframe_hours,
    maybe_specific_shopping_list,
):
    dir_path = get_generated_shopping_lists_path(
        selected_server, timeframe_hours, folder_date
    )
    maybe_make_dir(dir_path)

    for file_name in get_all_file_names_in_dir(f"{FILE_PATH_GENERATED_SHOPPING_LIST}"):
        if maybe_specific_shopping_list and file_name != maybe_specific_shopping_list:
            pass  # Do nothing
        else:
            print(f"{selected_server} --> {file_name}")
            items = read_dict_from_file(
                f"{FILE_PATH_GENERATED_SHOPPING_LIST}/{file_name}"
            )

            history = get_history_bulk_items(
                items, selected_server, timeframe_hours.value
            )
            write_dict_content_on_file(history, f"{dir_path}/{file_name}")

    print(f"{selected_server} --> Done")


def update_history_tree():
    # This file is used by the web UI and describes the available files to the front-end.
    files_tree = get_files_tree_starting_on_folder(
        f"{get_root_project_path()}{FILE_PATH_GENERATED_HISTORY}"
    )
    write_dict_content_on_file(files_tree, FILE_PATH_GENERATED_HISTORY_TREE)
