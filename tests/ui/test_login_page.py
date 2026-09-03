import playwright.sync_api
from page_object_models.login_page import LoginPage
from utilities.logger_utility import _logger
from configurations.config_loader import ConfigLoader, UserRole

# Initialize and collect Logger.
logger = _logger(__name__)
config = ConfigLoader()


def test_login_user_valid(login_page: playwright.sync_api.Page):
    user = config.get_user(UserRole.STANDARD_USER)

    login_page = LoginPage(login_page, logger)
    login_page.should_be_healthy()
    login_page.fill_login_form(username=user.username,
                               password=user.password)
    products_page = login_page.submit_login()
    products_page.should_be_open()
