from src.calculators.calculators import get_history_bulk_items
from src.consts import FILE_PATH_GENERATED_SHOPPING_LIST
from src.utils.files import get_all_file_names_in_dir
from src.utils.files import get_generated_shopping_lists_path
from src.utils.files import maybe_make_dir
from src.utils.files import read_dict_from_file
from src.utils.files import write_dict_content_on_file


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
        print(f"{maybe_specific_shopping_list}")
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
