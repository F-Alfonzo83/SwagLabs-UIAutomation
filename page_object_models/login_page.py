from configurations import config_loader
from playwright.sync_api import expect

from page_object_models.products_page import ProductsPage

config = config_loader.ConfigLoader()

class LoginPage:
    def __init__(self, page, logger) -> None:
        self.page = page
        self.logger = logger
        # Page constants
        self.PAGE_URL = config.login_page_url()
        self.PAGE_INDICATOR = self.page.get_by_text("Swag Labs")

        #Page interactive elements
        self.username_field = self.page.get_by_role("textbox", name="Username")
        self.password_field = self.page.get_by_role("textbox", name="Password")
        self.login_button = self.page.get_by_role("button", name="Login")

    def should_be_open(self):
        self.logger.info(f"Validating: {type(self).__name__} is open")
        self.logger.debug("Validating URL")
        expect(self.page).to_have_url(self.PAGE_URL)
        self.logger.debug("Validating Page Header")
        expect(self.PAGE_INDICATOR).to_be_visible()

    def should_show_critic_elements(self):
        self.logger.info(f"Validating: {type(self).__name__} is showing critic elements")
        self.logger.debug("Validating Username field is present")
        expect(self.username_field).to_be_visible()
        self.logger.debug("Validating Password field is present")
        expect(self.password_field).to_be_visible()
        self.logger.debug("Validating Login button is present")
        expect(self.login_button).to_be_visible()

    def should_be_healthy(self):
        self.should_be_open()
        self.should_show_critic_elements()

    def fill_login_form(self, username=None, password=None):
        self.logger.info(f"Filling username field: {username}")
        self.username_field.fill(username)
        self.logger.info(f"Filling password field")
        self.password_field.fill(password)

    def submit_login(self):
        self.logger.info(f"Submitting login info")
        self.login_button.click()
        products_page = ProductsPage(self.page, self.logger)
        return products_page
