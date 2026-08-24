import logging
import playwright.sync_api
from playwright.sync_api import expect
from configurations import config_loader
from page_object_models.basepage import BasePage
from page_object_models.checkout_info_page import CheckoutInformationPage

config = config_loader.ConfigLoader()


class CartPage(BasePage):
    def __init__(self, page: playwright.sync_api.Page, logger: logging.Logger):
        super().__init__(page, logger)

        self.PAGE_URL = config.cart_page_url()
        self.PAGE_INDICATOR = self.page.get_by_text("Your Cart", exact=True)

        # Page Elements
        self.product_list = self.page.locator("css=div.cart_list")
        self.checkout_button = self.page.get_by_role("button", name="Checkout", exact=True)
        self.continue_shopping_button = self.page.get_by_role("button", name="Go back Continue Shopping",
                                                              exact=True)
        self.quantity_header = self.page.get_by_text("QTY", exact=True)
        self.description_header = self.page.get_by_text("Description", exact=True)
        self.shopping_cart_quantity_counter = self.page.locator('[data-test="shopping-cart-badge"]')

    def should_show_critic_elements(self):
        self.logger.debug("Softly Validating Quantity Header is present")
        expect.soft(self.quantity_header).to_be_visible()
        self.logger.debug("Softly Validating Description Header is present")
        expect.soft(self.description_header).to_be_visible()
        self.logger.debug("Softly Validating Item List is present")
        expect.soft(self.product_list).to_be_visible()
        self.logger.debug("Validating Checkout Button is present")
        expect(self.checkout_button).to_be_visible()
        self.logger.debug("Validating Continue Shopping Button is present")
        expect(self.continue_shopping_button).to_be_visible()

    def validate_item_in_cart(self, item: str):
        self.logger.info(f"Validating {item} in cart")
        expect(self.product_list.filter(has_text=item)).to_be_visible()

    def validate_item_not_in_cart(self, item: str):
        self.logger.debug(f"Validating item: '{item}' is not on the list")
        expect(self.product_list.filter(has_text=item)).not_to_be_visible()

    def remove_item_from_cart(self, item: str):
        self.logger.info(f"Removing: '{item}' from cart")
        self.logger.debug("Clicking on the Remove button")
        self.product_list.filter(has_text=item).get_by_role("button", name="Remove").click()

    def navigate_to_checkout_page(self):
        self.checkout_button.click()
        checkout_page = CheckoutInformationPage(self.page, self.logger)
        return checkout_page
