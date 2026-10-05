from typing import Literal, get_args

import playwright.sync_api

AbortErrorCode = Literal["aborted", "accessdenied", "addressunreachable", "blockedbyclient", "blockedbyresponse",
                         "connectionclosed", "connectionaborted", "connectionfailed", "connectionrefused",
                         "connectionreset", "internetdisconnected", "namenotresolved", "timedout", "failed"]


class RouterActions():
    """Defines the actions to be executed by the Playwright Router
    """

    def __init__(self, abort_error_code: AbortErrorCode = "failed"):
        """Initializes an instance of the RouterActions Class.

        Instance takes an  argument to define the abort error code.

        Args:
            abort_error_code (AbortErrorCode): Literal value that defines the Playwright abort error code
            for the routing.

        Raises:
            ValueError: If abort_error_code is not an AbortErrorCode.

        Examples
            abort_failed =  RouterActions(abort_error_code="failed")
        """
        if abort_error_code not in get_args(AbortErrorCode):
            raise ValueError(f"{abort_error_code!r} abort_error_code not valid. Must be one of {AbortErrorCode}")
        self.matched_urls: set[str] = set()
        self.abort_error_code = abort_error_code

    def block_images(self, route: playwright.sync_api.Route):
        """Record the request's URL in matched_urls, then abort it with abort_error_code.

        Every URL in matched_urls was aborted by this handler; unexpected_request_failures relies on that as
        proof of ownership.

        Args:
            route: the intercepted request, supplied by Playwright (not called directly).
        """
        self.matched_urls.add(route.request.url)
        route.abort(self.abort_error_code)
