import urllib.parse
from page_object_models.login_page import LoginPage
from utilities.assertions_helper import traffic_errors
from utilities.logger_utility import _logger

logger = _logger(__name__)

def test_network_traffic(browser_instance,traffic_network_listener):

    login_page = LoginPage(browser_instance, logger)
    login_page.should_be_healthy()
    login_page.fill_login_form(username="standard_user", password="secret_sauce")
    products_page = login_page.submit_login()
    products_page.should_be_open()
    products_page.get_products()
    shopping_cart_page = products_page.navigate_to_shopping_cart()
    shopping_cart_page.should_be_healthy()
    shopping_cart_page.page.reload()

    logger.debug(repr(traffic_network_listener))

    _traffic_errors = traffic_errors(traffic_network_listener.response_record)
    assert not _traffic_errors, f"Errors found: {_traffic_errors}"
    assert not traffic_network_listener.failed_response_record, f"Errors found: {traffic_network_listener.failed_response_record}"








