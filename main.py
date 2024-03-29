from src.calculators.calculator import calculate_history_trends
from src.generators.generator import generate_all_items_name_to_id
from src.generators.generator import generate_all_items_to_attributes
from src.generators.generator import generate_all_items_to_lodestone_id
from src.generators.generator import generate_enriched_shopping_lists
from src.utils.command_line_arguments import parse_command_line_arguments

"""
    TODO:
    - One shopping file per:
        - white scrip crafter
        - purple scrip crafter
    - Update venture files with new gear values. Rename them to start with "venture_"
    - Description of the files that is being sent to the front-end
    - Tests
    - Working only_hq flag for pots/foods
    - Handle maybe_specific_shopping_list for generating_enriched_shopping_list
        as it currently only works for calculating the trends
"""


if __name__ == "__main__":
    (
        calculate_shopping_lists,
        fetch_new_items,
        generate_new_shopping_lists,
        push_to_git,
        servers,
        specific_shopping_list,
        timeframe_hours,
    ) = parse_command_line_arguments()

    if fetch_new_items:
        generate_all_items_name_to_id()
        generate_all_items_to_lodestone_id()
        generate_all_items_to_attributes()

    if generate_new_shopping_lists:
        generate_enriched_shopping_lists()

    if calculate_shopping_lists:
        calculate_history_trends(
            servers, push_to_git, timeframe_hours, specific_shopping_list
        )

    print(" --- Done --- ")
