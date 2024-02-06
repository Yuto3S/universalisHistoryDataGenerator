from src.calculators.calculators import calculate_item_info
from src.calculators.calculators import get_default_history
from src.calculators.calculators import get_universalis_response
from src.calculators.calculators import maybe_enrich_history
from src.calculators.calculators import maybe_enrich_item_info
from src.consts import ITEMS
from src.generators.items import get_items_id_to_name


def get_trends_history(items, server, timeframe_hours):
    extra_attributes = set(items[list(items.keys())[0]].keys())
    extra_attributes = sorted(extra_attributes)

    history = get_default_history(extra_attributes)
    maybe_enrich_history(history, extra_attributes)

    items_id_to_name = get_items_id_to_name(items)

    result = get_universalis_response(items_id_to_name, server, timeframe_hours)

    for item_id in result[ITEMS]:
        item_info = calculate_item_info(
            item_id, result, items, items_id_to_name, extra_attributes
        )
        maybe_enrich_item_info(item_info, extra_attributes)

        history[ITEMS].append(item_info)

    return history
