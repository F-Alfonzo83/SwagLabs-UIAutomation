import logging
import playwright.sync_api
from playwright.sync_api import expect
from configurations.config_loader import ConfigLoader
from page_object_models.basepage import BasePage

config = ConfigLoader()


class CheckoutCompletePage(BasePage):
    def __init__(self, page: playwright.sync_api.Page, logger: logging.Logger):
        super().__init__(page, logger)

        self.PAGE_URL = config.checkout_complete_page_url()
        self.PAGE_INDICATOR = self.page.locator('[data-test="title"]')

        # Locators:

        self.order_complete_header = self.page.get_by_role(role="heading", name="Thank you for your order!")
        self.success_message = self.page.locator('[data-test="complete-text"]')
        self.back_home_button = self.page.get_by_role(role="button", name="Back Home")

    def should_show_critic_elements(self):
        expect.soft(self.order_complete_header).to_be_visible()
        expect.soft(self.success_message).to_be_visible()
        expect.soft(self.back_home_button).to_be_visible()

    def navigate_back_home(self):
        from page_object_models.products_page import ProductsPage
        self.back_home_button.click()
        product_page = ProductsPage(self.page, self.logger)
        return product_page
