import pytest
from utilities.logger_utility import _logger
# Initialize and collect Logger.
logger = _logger(__name__)

PRODUCT_SORTING_VALUES = ["az", "za", "lohi", "hilo"]


def test_add_item_to_cart(products_page_instance):
    logger.debug("TEST: Adding item to Cart")
    products_page_instance.add_item_to_cart("Sauce Labs Backpack")


@pytest.mark.parametrize("sort_value", PRODUCT_SORTING_VALUES)
def test_sorting(products_page_instance, sort_value: str):
    products_page_instance.items_filter.select_option(sort_value)
    sorted_names = products_page_instance.get_product_names()
    sorted_prices = products_page_instance.get_product_prices()
    logger.debug(f"TEST: Sorting items by value: {sort_value}")
    if sort_value == "az":
        assert sorted_names == sorted(sorted_names)
    elif sort_value == "za":
        assert sorted_names == sorted(sorted_names, reverse=True)
    elif sort_value == "lohi":
        assert sorted_prices == sorted(sorted_prices)
    elif sort_value == "hilo":
        assert sorted_prices == sorted(sorted_prices, reverse=True)
