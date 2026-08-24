from faker import Faker
from playwright.sync_api import expect

faker = Faker()

def test_checkout_flow_single_item(products_page):
    products_page.should_be_healthy()
    products:dict = products_page.get_products()
    # Get the Keys. Convert to a list. Get the 1st element (1st product name)
    item_name = list(products.keys())[0]
    products_page.add_item_to_cart(item_name)
    cart_page = products_page.navigate_to_shopping_cart()
    cart_page.should_be_healthy()
    cart_page.validate_item_in_cart(item_name)
    checkout_information_page = cart_page.navigate_to_checkout_page()
    checkout_information_page.should_be_healthy()
    checkout_information_page.fill_checkout_information_form(first_name=faker.first_name(),
                                                             last_name=faker.last_name(),
                                                             postal_code=faker.postalcode(),)
    checkout_overview_page = checkout_information_page.submit_checkout_information()
    checkout_overview_page.should_be_healthy()
    checkout_overview_page.get_subtotal()
    checkout_overview_page.get_tax()
    checkout_overview_page.get_total()

    expect(checkout_overview_page.cart_items_container).to_contain_text(item_name)
    checkout_complete_page = checkout_overview_page.finish_checkout()
    checkout_complete_page.should_be_healthy()
    expect(checkout_complete_page.order_complete_header).to_be_visible()







