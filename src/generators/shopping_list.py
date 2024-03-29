MANUAL_SHOPPING_LIST__EXTRA_FIELDS = "extra_fields"
MANUAL_SHOPPING_LIST__FIELD_ITEMS = "items"
MANUAL_SHOPPING_LIST__FIELD_ID = "id"

MANUAL_SHOPPING_LIST__IS_VENTURE_FILE = "is_venture_file"
MANUAL_SHOPPING_LIST__LEVEL = "level"
MANUAL_SHOPPING_LIST__DURATION = "duration"
MANUAL_SHOPPING_LIST__VENTURE_MIN_LEVEL = "venture_minimum_level"


def get_enriched_shopping_list(manual_shopping_list_dict, all_items_name_to_attributes):
    items_infos = {}
    extra_fields = manual_shopping_list_dict.get(MANUAL_SHOPPING_LIST__EXTRA_FIELDS, [])

    for item in manual_shopping_list_dict[MANUAL_SHOPPING_LIST__FIELD_ITEMS]:
        if should_skip_item(item, manual_shopping_list_dict):
            continue

        items_infos[item] = {
            "id": all_items_name_to_attributes[item]["id"],
        }
        items_infos[item]["lodestone_id"] = all_items_name_to_attributes[item][
            "lodestone_id"
        ]

        for extra_field in extra_fields:
            items_infos[item][extra_field] = manual_shopping_list_dict[
                MANUAL_SHOPPING_LIST__FIELD_ITEMS
            ][item][extra_field]

        if is_venture_shopping_list(manual_shopping_list_dict):
            handle_venture_fields(manual_shopping_list_dict, items_infos, item)

    return items_infos


def should_skip_item(item, manual_shopping_list_dict):
    if is_venture_shopping_list(
        manual_shopping_list_dict
    ) and is_item_venture_level_too_low(manual_shopping_list_dict, item):
        return True

    return False


def is_venture_shopping_list(current_shopping_list):
    return current_shopping_list.get(MANUAL_SHOPPING_LIST__IS_VENTURE_FILE)


def is_item_venture_level_too_low(manual_shopping_list_dict, item):
    return manual_shopping_list_dict.get(
        MANUAL_SHOPPING_LIST__VENTURE_MIN_LEVEL, 0
    ) > manual_shopping_list_dict[MANUAL_SHOPPING_LIST__FIELD_ITEMS][item].get(
        MANUAL_SHOPPING_LIST__LEVEL, 1
    )


def handle_venture_fields(manual_shopping_list_dict, items_infos, item):
    add_venture_duration(manual_shopping_list_dict, items_infos, item)


def add_venture_duration(manual_shopping_list_dict, items_infos, item):
    items_infos[item][MANUAL_SHOPPING_LIST__DURATION] = get_venture_duration(
        manual_shopping_list_dict[MANUAL_SHOPPING_LIST__FIELD_ITEMS][item][
            MANUAL_SHOPPING_LIST__LEVEL
        ]
    )


def get_venture_duration(item_level):
    duration = 40
    if item_level >= 80:
        duration = 60
    elif item_level >= 70:
        duration = 50
    elif item_level > 90:
        raise Exception("WE HAVE REACHED EXPANSION 7.0 AND THIS LOGIC WAS NOT UPDATED")

    return duration
