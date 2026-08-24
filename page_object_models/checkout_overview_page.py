import logging
import playwright.sync_api
from playwright.sync_api import expect
from configurations import config_loader
from page_object_models.basepage import BasePage
from page_object_models.checkout_complete_page import CheckoutCompletePage

config = config_loader.ConfigLoader()


class CheckoutOverviewPage(BasePage):
    def __init__(self, page: playwright.sync_api.Page, logger: logging.Logger):
        super().__init__(page, logger)

        self.PAGE_URL = config.checkout_overview_page_url()
        self.PAGE_INDICATOR = self.page.locator('[data-test="title"]')

        # Locators:
        self.cancel_button = self.page.get_by_role(role="button", name="Go back Cancel")
        self.finish_button = self.page.get_by_role(role="button", name="Finish")
        self.cart_items_container = self.page.locator('[data-test="cart-list"]')
        self.subtotal = self.page.locator('[data-test="subtotal-label"]')
        self.tax = self.page.locator('[data-test="tax-label"]')
        self.total = self.page.locator('[data-test="total-label"]')

    def should_show_critic_elements(self):
        self.logger.debug("Validating Cancel button is present")
        expect.soft(self.cancel_button).to_be_visible()
        self.logger.debug("Validating Finish button is present")
        expect.soft(self.finish_button).to_be_visible()
        self.logger.debug("Validating Cart Items container is present")
        expect.soft(self.cart_items_container).to_be_visible()
        expect.soft(self.cart_items_container).not_to_be_empty()
        self.logger.debug("Validating Subtotal container is present")
        expect.soft(self.subtotal).to_be_visible()
        expect.soft(self.subtotal).not_to_be_empty()
        self.logger.debug("Validating Tax container is present")
        expect.soft(self.tax).to_be_visible()
        expect.soft(self.tax).not_to_be_empty()
        self.logger.debug("Validating Total container is present")
        expect.soft(self.total).to_be_visible()
        expect.soft(self.total).not_to_be_empty()

    def finish_checkout(self):
        self.finish_button.click()
        checkout_complete_page = CheckoutCompletePage(self.page, self.logger)
        return checkout_complete_page

    def get_subtotal(self):
        return float(self.subtotal.inner_text().split("$")[-1])

    def get_tax(self):
        return float(self.tax.inner_text().split("$")[-1])

    def get_total(self):
        return float(self.total.inner_text().split("$")[-1])
