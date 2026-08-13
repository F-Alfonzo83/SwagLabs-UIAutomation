# PyTest Tests configuration File.
from dataclasses import dataclass

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
    # Set the Browser (Firefox, Chromium, etc)
    firefox = playwright.firefox
    # Launch the Browser
    browser = firefox.launch(headless=True)
    # Create a new Context.
    context = browser.new_context()
    # Create a new page within the context
    page = context.new_page()
    page.goto(config.login_page_url())

    # Pass the Page to the test
    yield page

    # Upon completion: Close the Session
    context.close()
    # Close the Browser
    browser.close()


@pytest.fixture(scope="function")
def products_page_instance(browser_instance: playwright.sync_api.Page, request):
    logger = _logger(request.module.__name__)
    login_page = LoginPage(browser_instance, logger)
    login_page.should_be_healthy()
    login_page.fill_login_form(username="standard_user", password="secret_sauce")
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

