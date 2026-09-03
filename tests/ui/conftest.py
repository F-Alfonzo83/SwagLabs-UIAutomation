import playwright.sync_api
import pytest
from playwright.sync_api import Playwright
from configurations import config_loader
from page_object_models.login_page import LoginPage
from utilities.logger_utility import _logger
from utilities.network import TrafficRecorder

# Import Configurations Loader
config = config_loader.ConfigLoader()


@pytest.fixture(scope="function")
def browser_instance(playwright: Playwright):
    '''Creates  a bare  browser instance.

    The Instance returned  is  clean, this allows to add, or not, a network traffic  listener

    Args:
        playwright: Playwright

    Returns:
    page: (Playwright.sync_api.Page): A page  Object
    '''
    # Set the Browser (Firefox, Chromium, etc)
    firefox = playwright.firefox
    # Launch the Browser
    browser = firefox.launch(headless=True)
    # Create a new Context.
    context = browser.new_context()
    # Create a new page within the context
    page = context.new_page()

    # Pass the Page to the test
    yield page

    # Upon completion: Close the Session
    context.close()
    # Close the Browser
    browser.close()


@pytest.fixture(scope="function")
def login_page(browser_instance: playwright.sync_api.Page):
    '''Receives the Browser  instance and navigates to login page.

    Args:
        browser_instance: Playwright.sync_api.Page

    Returns:
        login_page: (Playwright.sync_api.Page): A page  Object for  the Login page.
    '''
    browser_instance.goto(config.login_page_url())
    yield browser_instance


@pytest.fixture(scope="function")
def products_page(login_page: playwright.sync_api.Page, request):
    '''Returns a products page.

    Args:
        login_page: Playwright.sync_api.Page

    Returns:
        products_page: Playwright.sync_api.Page
    '''
    logger = _logger(request.module.__name__)
    login_page = LoginPage(login_page, logger)
    user = config.get_user(config_loader.UserRole.STANDARD_USER)
    login_page.should_be_healthy()
    login_page.fill_login_form(username=user.username,
                               password=user.password)

    products_page = login_page.submit_login()
    products_page.should_be_healthy()
    yield products_page


@pytest.fixture(scope="function")
def traffic_network_listener(browser_instance: playwright.sync_api.Page):

    traffic_record = TrafficRecorder()

    browser_instance.on("response", traffic_record._response)
    browser_instance.on("request", traffic_record._request)
    browser_instance.on("requestfailed", traffic_record._request_failure)

    yield traffic_record
    # On return
    browser_instance.remove_listener("response", traffic_record._response)
    browser_instance.remove_listener("request", traffic_record._request)
    browser_instance.remove_listener("requestfailed", traffic_record._request_failure)
