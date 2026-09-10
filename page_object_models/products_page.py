import logging

import playwright.sync_api
from playwright.sync_api import expect
from configurations import config_loader
from page_object_models.basepage import BasePage
from page_object_models.cart_page import CartPage

config = config_loader.ConfigLoader()


class ProductsPage(BasePage):
    def __init__(self, page: playwright.sync_api.Page, logger: logging.Logger):
        super().__init__(page, logger)

        self.PAGE_URL = config.products_page_url()
        self.PAGE_INDICATOR = self.page.get_by_text("Products", exact=True)

        # Page Elements
        self.menu_button = self.page.get_by_role("button", name="Menu")
        self.cart_button = self.page.locator('a.shopping_cart_link')
        self.inventory_items = self.page.locator('[data-test="inventory-item"]')
        self.items_filter = self.page.get_by_role("combobox")

    def should_show_critic_elements(self):
        expect(self.menu_button).to_be_visible()
        expect(self.cart_button).to_be_visible()
        expect(self.inventory_items).not_to_have_count(0)
        expect(self.items_filter).to_be_visible()

    def add_item_to_cart(self, item: str):
        self.logger.info(f"Adding: '{item}' to cart")
        add_item_to_cart_btn = self.inventory_items.filter(has_text=item).get_by_role("button", name="Add to cart")
        self.logger.debug("Clicking the 'Add to cart' button")
        add_item_to_cart_btn.click()
        expect(self.inventory_items.filter(has_text=item).get_by_role("button", name="Remove")).to_be_visible()

    def navigate_to_shopping_cart(self):
        self.logger.info("Navigating to shopping cart page")
        self.cart_button.click()
        cart_page = CartPage(self.page, self.logger)
        return cart_page

    def get_products(self) -> dict:
        expect(self.inventory_items).not_to_have_count(0)

        products = {}
        for item in self.inventory_items.all():
            item_name = item.locator("[data-test='inventory-item-name']").inner_text()
            item_price = item.locator("[data-test='inventory-item-price']").inner_text().lstrip("$")
            if not item_name:
                raise ValueError(f"Item name is required.  Obtained: {item_name!r}")
            if not item_price:
                raise ValueError(f"Item price is required. Obtained: {item_price!r}")
            if item_name in products:
                raise ValueError(f"Item name '{item_name}' is already taken")
            products[item_name] = float(item_price)
        return products
