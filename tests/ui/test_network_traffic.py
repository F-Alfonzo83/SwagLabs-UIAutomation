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
    products_page.should_be_healthy()
    products_page.get_products()
    shopping_cart_page = products_page.navigate_to_shopping_cart()
    shopping_cart_page.should_be_healthy()

    logger.debug(repr(traffic_network_listener))

    _traffic_errors = traffic_errors(traffic_network_listener.response_record)
    assert not _traffic_errors, f"Errors found: {_traffic_errors}"

    _unexpected_failures = unexpected_failure(traffic_network_listener.failed_response_record)
    assert not _unexpected_failures, f"Errors found: {_unexpected_failures}"


def test_backpack_image_loads_on_products_page(login_page):
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
    """Validates that no new requests are executed when an item is added to the shopping cart.

    Only evaluates the time the item is added to the shopping cart.
    page.wait_for_load_state("networkidle") is used to make  sure traffic has stopped and nothing leaks.
    Keep it to prevents leaks  caused for in-flights unfinished traffic.
    It shows the action of adding an item to the cart will not generate traffic, but does not prove anything
    for before or after.

    Args:
        recorded_login_page: Fixture that yields a page with a traffic recorder attached to it.
        traffic_network_listener: Traffic recorder

    Returns:
        None
    """
    user = config.get_user(UserRole.STANDARD_USER)

    login_page = LoginPage(recorded_login_page, logger)
    login_page.should_be_healthy()
    login_page.fill_login_form(username=user.username,
                               password=user.password)
    products_page = login_page.submit_login()
    products_page.should_be_healthy()
    products = products_page.get_products()
    logger.debug("Capturing number of executed requests before adding item to shopping_cart.")
    products_page.page.wait_for_load_state("networkidle")
    current_requests_count = len(traffic_network_listener.request_record)
    products_page.add_item_to_cart(next(iter(products)))

    products_page.page.wait_for_load_state("networkidle")
    new_requests = traffic_network_listener.request_record[current_requests_count:]
    assert not new_requests, \
        (f"Traffic after request should be none. Detected leaked traffic. "
         f"Elements Leaked : {new_requests}")


def test_inventory_page_product_image_count(traffic_network_listener, recorded_login_page):
    """Validates the number of product images loaded match the number of products.

    Covers for cases of mismatches (More or less images loaded for the products)
    Adds '/assets/' in the url validator since all the images contain that path. Without it any first
    party url matches the filter. Makes use of'is_first_party' to validate the source url belongs to
    Swaglabs and not to a third party.
    items_in_page is derived directly from the page dynamically

    Args:
       recorded_login_page: Fixture that yields a page with a traffic recorder attached to it.
       traffic_network_listener: Traffic recorder

    Notes:
        The 200 assertion has not been exercised yet since nothing has given a 404 so far.
        It is planned to create a method or function to validate  this parameter.
        Until then do not delete the assertion nor this comment.

    Returns:
        None
    """
    user = config.get_user(UserRole.STANDARD_USER)

    login_page = LoginPage(recorded_login_page, logger)
    login_page.should_be_healthy()
    login_page.fill_login_form(username=user.username,
                               password=user.password)
    products_page = login_page.submit_login()
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
    matched_urls = [response.url for response in product_image_response]
    assert items_in_page == len(product_image_response), (f"The number of products on the page does not match "
                                                          f"the images response requests: "
                                                          f"{items_in_page} != {len(product_image_response)}\n"
                                                          f"{matched_urls}")
