

def test_check_item_on_cart(products_page_instance):
    ITEM = "Sauce Labs Backpack"
    products_page_instance.add_item_to_cart(ITEM)
    cart_page = products_page_instance.navigate_to_shopping_cart()
    cart_page.should_be_healthy()
    cart_page.validate_item_in_cart(ITEM)


def test_remove_item_from_cart(products_page_instance):
    ITEM = "Sauce Labs Backpack"
    products_page_instance.add_item_to_cart(ITEM)
    cart_page = products_page_instance.navigate_to_shopping_cart()
    cart_page.should_be_healthy()
    cart_page.validate_item_in_cart(ITEM)
    cart_page.remove_item_from_cart(ITEM)
    cart_page.validate_item_not_in_cart(ITEM)
