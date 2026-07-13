import logging
from abc import ABC, abstractmethod

import playwright.sync_api
from playwright.sync_api import expect


class BasePage(ABC):
    """Abstract Base Class (ABC) for all Page Classes.

    Attributes:
        self.page (playwright.sync_api.Page): Page object.
        self.logger (logging.Logger): Logger object.
        self.PAGE_URL (str): Page URL obtained from config
        self.PAGE_INDICATOR (playwright.sync_api.PageIndicator): Page Indicator)
    """

    def __init__(self, page: playwright.sync_api.Page, logger: logging.Logger):
        self.page = page
        self.logger = logger

        self.PAGE_URL = None  # Holder
        self.PAGE_INDICATOR = None  # Holder

    def should_be_open(self):
        self.logger.info(f"Validating {type(self).__name__} is open")
        self.logger.debug("Validating URL")
        expect(self.page).to_have_url(self.PAGE_URL)
        self.logger.debug("Validating Page Header")
        expect(self.PAGE_INDICATOR).to_be_visible()

    @abstractmethod
    def should_show_critic_elements(self):
        pass

    def should_be_healthy(self):
        self.logger.info("Validating Open Elements")
        self.should_be_open()
        self.logger.info("Validating Critic Elements")
        self.should_show_critic_elements()
