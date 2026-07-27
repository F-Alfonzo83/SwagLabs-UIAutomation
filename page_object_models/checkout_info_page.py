import logging
import playwright.sync_api
from playwright.sync_api import expect
from configurations.config_loader import ConfigLoader
from page_object_models.basepage import BasePage
from page_object_models.checkout_overview_page import CheckoutOverviewPage

config = ConfigLoader()


class CheckoutInformationPage(BasePage):
    def __init__(self, page: playwright.sync_api.Page, logger: logging.Logger):
        super().__init__(page, logger)

        self.PAGE_URL = config.checkout_information_page_url()
        self.PAGE_INDICATOR = self.page.locator('[data-test="title"]')

        # Page Elements:
        self.first_name_field = self.page.locator('[data-test="firstName"]')
        self.last_name_field = self.page.locator('[data-test="lastName"]')
        self.postal_code_field = self.page.locator('[data-test="postalCode"]')

        self.cancel_button = self.page.get_by_role(role="button", name="Go back Cancel")
        self.continue_button = self.page.get_by_role(role="button", name="Continue")

    def should_show_critic_elements(self):
        self.logger.debug("Validating First Name field is present")
        expect.soft(self.first_name_field).to_be_visible()
        self.logger.debug("Validating Last Name field is present")
        expect.soft(self.last_name_field).to_be_visible()
        self.logger.debug("Validating Postal Code field is present")
        expect.soft(self.postal_code_field).to_be_visible()
        self.logger.debug("Validating Cancel button is present")
        expect.soft(self.cancel_button).to_be_visible()
        self.logger.debug("Validating Continue button is present")
        expect.soft(self.continue_button).to_be_visible()

    def fill_checkout_information_form(self,
                                       first_name: str | None = None,
                                       last_name: str | None = None,
                                       postal_code: str | None = None):
        self.first_name_field.fill(first_name)
        self.last_name_field.fill(last_name)
        self.postal_code_field.fill(postal_code)

    def submit_checkout_information(self):
        self.continue_button.click()
        checkout_overview_page = CheckoutOverviewPage(self.page, self.logger)
        return checkout_overview_page
