# PyTest Tests configuration File.
import pytest
from playwright.sync_api import Playwright

from configurations import config_loader

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
    #Create a new page within the context
    page = context.new_page()
    page.goto(config.login_page_url())

    #Pass the Page to the test
    yield page

    # Upon completion: Close the Session
    context.close()
    # Close the Browser
    browser.close()

