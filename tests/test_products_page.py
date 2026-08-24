import pytest
from utilities.logger_utility import _logger
# Initialize and collect Logger.
logger = _logger(__name__)

PRODUCT_SORTING_VALUES = ["az", "za", "lohi", "hilo"]


def test_add_item_to_cart(products_page):
    logger.debug("TEST: Adding item to Cart")
    products_page.add_item_to_cart("Sauce Labs Backpack")


@pytest.mark.parametrize("sort_value", PRODUCT_SORTING_VALUES)
def test_sorting(products_page, sort_value: str):
    products_page.items_filter.select_option(sort_value)
    sorted_products: dict = products_page.get_products()
    logger.debug(f"TEST: Sorting items by value: {sort_value}")

    if sort_value == "az":
        assert list(sorted_products.keys()) == sorted(sorted_products.keys())
    elif sort_value == "za":
        assert list(sorted_products.keys()) == sorted(sorted_products.keys(), reverse=True)
    elif sort_value == "lohi":
        assert list(sorted_products.values()) == sorted(sorted_products.values())
    elif sort_value == "hilo":
        assert list(sorted_products.values()) == sorted(sorted_products.values(), reverse=True)
    else:
        pytest.fail("Sort value not recognized")
