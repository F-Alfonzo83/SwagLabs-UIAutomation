from page_object_models.login_page import LoginPage
from utilities.assertions_helper import traffic_errors, unexpected_failure, is_first_party
from utilities.logger_utility import _logger
from configurations.config_loader import ConfigLoader, UserRole

logger = _logger(__name__)
config = ConfigLoader()


def test_network_traffic_to_shopping_cart(recorded_login_page, traffic_network_listener):
    user = config.get_user(UserRole.STANDARD_USER)

    login_page = LoginPage(recorded_login_page, logger)
    login_page.should_be_healthy()
    login_page.fill_login_form(username=user.username,
                               password=user.password)
    products_page = login_page.submit_login()
    products_page.should_be_open()
    products_page.get_products()
    shopping_cart_page = products_page.navigate_to_shopping_cart()
    shopping_cart_page.should_be_healthy()

    logger.debug(repr(traffic_network_listener))

    _traffic_errors = traffic_errors(traffic_network_listener.response_record)
    assert not _traffic_errors, f"Errors found: {_traffic_errors}"

    _unexpected_failures = unexpected_failure(traffic_network_listener.failed_response_record)
    assert not _unexpected_failures, f"Errors found: {_unexpected_failures}"


def test_wait_for_event(login_page):
    login_page = LoginPage(login_page, logger)
    user = config.get_user(UserRole.STANDARD_USER)
    login_page.fill_login_form(username=user.username,
                               password=user.password)
    # This is  the action that triggers the expected response.
    with login_page.page.expect_response(lambda response: response.status == 200 and
                                         "backpack" in response.url and
                                         response.request.resource_type == "image") as info:
        products_page = login_page.submit_login()
    response = info.value
    products_page.should_be_open()
    logger.debug(response)


def test_add_item_to_shopping_cart_issue_zero_request(recorded_login_page, traffic_network_listener):
    user = config.get_user(UserRole.STANDARD_USER)

    login_page = LoginPage(recorded_login_page, logger)
    login_page.should_be_open()
    login_page.should_be_healthy()
    login_page.fill_login_form(username=user.username,
                               password=user.password)
    products_page = login_page.submit_login()
    products_page.should_be_open()
    products_page.should_be_healthy()
    products = products_page.get_products()
    logger.debug("Capturing number of executed requests before adding item to shopping_cart.")
    products_page.page.wait_for_load_state("networkidle")
    current_requests_count = len(traffic_network_listener.request_record)
    products_page.add_item_to_cart(next(iter(products)))

    products_page.page.wait_for_load_state("networkidle")
    new_requests = traffic_network_listener.request_record[current_requests_count:]
    assert not new_requests, \
        (f"Traffic after request should match number of executed requests previous "
         f"to  adding item to the shopping_cart: "
         f"{new_requests}")


def test_inventory_page_product_image_count(traffic_network_listener, recorded_login_page):
    user = config.get_user(UserRole.STANDARD_USER)

    login_page = LoginPage(recorded_login_page, logger)
    login_page.should_be_open()
    login_page.should_be_healthy()
    login_page.fill_login_form(username=user.username,
                               password=user.password)
    products_page = login_page.submit_login()
    products_page.should_be_open()
    products_page.should_be_healthy()
    items_in_page = len(products_page.get_products())
    # Let page  load.
    products_page.page.wait_for_load_state("networkidle")
    product_image_response = [response for response in
                              traffic_network_listener.response_record if
                              response.resource_type == "image" and
                              "/assets/" in response.url and
                              response.status == 200 and
                              is_first_party(response.url)]
    assert items_in_page == len(product_image_response), ("The number of products on the page does not match "
                                                          "the images response requests")
