from playwright.sync_api import expect

from configurations import config_loader

config = config_loader.ConfigLoader()

class ProductsPage:
    def __init__(self, page, logger):
        self.page = page
        self.logger = logger

        self.PAGE_URL = config.products_page_url()
        self.PAGE_INDICATOR = self.page.get_by_text("Products", exact=True)

        #Page Elements
        self.menu_button = self.page.get_by_role("button", name="Menu")
        self.cart_button = self.page.get_by_role("link").locator(".shopping_cart_link")
        self.inventory_items = self.page.locator(".inventory_item")
        self.items_filter = self.page.get_by_role("combobox").locator("css=.product_sort_container")

    def should_be_open(self):
        self.logger.info(f"Validating: {type(self).__name__} is open")
        self.logger.debug("Validating URL")
        expect(self.page).to_have_url(self.PAGE_URL)
        self.logger.debug("Validating Page Header")
        expect(self.PAGE_INDICATOR).to_be_visible()

    def add_item_to_cart(self, item:str):
        add_item_to_cart_btn = self.inventory_items.filter(has_text=item).get_by_role("button", name="Add to cart")
        add_item_to_cart_btn.click()

        expect(self.inventory_items.filter(has_text=item).get_by_role("button", name="Remove")).to_be_visible()
