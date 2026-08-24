import playwright.sync_api
from page_object_models.login_page import LoginPage
from utilities.logger_utility import _logger

# Initialize and collect Logger.
logger = _logger(__name__)


def test_login_user_valid(login_page: playwright.sync_api.Page):
    login_page = LoginPage(login_page, logger)
    login_page.should_be_healthy()
    login_page.fill_login_form(username="standard_user", password="secret_sauce")
    products_page = login_page.submit_login()
    products_page.should_be_open()
