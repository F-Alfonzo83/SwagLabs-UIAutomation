import playwright.sync_api


class RouterActions:
    def __init__(self):
        self.matched_urls: set[str] = set()

    def block_images(self, route: playwright.sync_api.Route):
        """Captures the routed elements (images) and blocks them.

        Stores a set of matching urls.

        Args:
            route:

        Returns:
            None

        """
        self.matched_urls.add(route.request.url)
        route.abort()
