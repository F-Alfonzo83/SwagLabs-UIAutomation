from typing import NamedTuple

from faker import Faker
from playwright.sync_api import expect

from page_object_models.checkout_overview_page import CheckoutOverviewPage
from page_object_models.products_page import ProductsPage
from utilities.assertions_helper import is_first_party
from utilities.logger_utility import _logger

faker = Faker()
logger = _logger(__name__)


class CheckoutFlow(NamedTuple):
    overview_page: CheckoutOverviewPage
    item_name: str


def perform_checkout_flow(products_page: ProductsPage, faker: Faker):
    products_page.should_be_healthy()
    products = products_page.get_products()
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

    flow_result = CheckoutFlow(overview_page=checkout_overview_page,
                               item_name=item_name)
    return flow_result


def test_checkout_flow_single_item(products_page):

    flow_result = perform_checkout_flow(products_page, faker)
    checkout_overview_page = flow_result.overview_page
    item_name = flow_result.item_name

    expect(checkout_overview_page.cart_items_container).to_contain_text(item_name)
    checkout_complete_page = checkout_overview_page.finish_checkout()
    checkout_complete_page.should_be_healthy()
    expect(checkout_complete_page.order_complete_header).to_be_visible()


def test_checkout_flow_single_item_with_blocked_images_success(blocked_images_products_page, image_request_blocker):
    flow_result = perform_checkout_flow(blocked_images_products_page, faker)
    checkout_overview_page = flow_result.overview_page
    item_name = flow_result.item_name

    expect(checkout_overview_page.cart_items_container).to_contain_text(item_name)
    checkout_complete_page = checkout_overview_page.finish_checkout()
    checkout_complete_page.should_be_healthy()
    expect(checkout_complete_page.order_complete_header).to_be_visible()

    matched_blocked_images = [url for url in image_request_blocker.matched_urls
                              if is_first_party(url)
                              and "/assets/" in url]

    assert matched_blocked_images
