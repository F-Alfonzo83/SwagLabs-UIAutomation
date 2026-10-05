import pytest
from utilities.network import ResponseInfo, RequestInfo
from utilities import assertions_helper
from utilities.logger_utility import _logger


logger = _logger(__name__)

URL_LIST = [
    ("https://www.saucedemo.com/inventory.html", True),  # Should pass
    ("https://saucedemo.com/", True),  # Should Pass
    ("https://events.backtrace.io/api/", False),  # Should Fail
    ("https://evilsaucedemo.com/", False),  # Should Fail
    ("data:image/png;base64,iVBOR", False),  # Should Fail
    ("https://WWW.SAUCEDEMO.COM/", True),  # Should Pass
    ("https://saucedemo.com:443/", True)  # Should pass
]
CRAFTED_RESPONSES = [ResponseInfo(status=404,
                                  resource_type="image",
                                  url="https://www.saucedemo.com/inventory.html",
                                  redirect_from=None,
                                  method="GET",
                                  navigation_request=False),
                     # 404 + image + first-party → flagged
                     ResponseInfo(status=404,
                                  resource_type="image",
                                  url="https://events.backtrace.io/api/",
                                  redirect_from=None,
                                  method="GET",
                                  navigation_request=False),
                     # 404 + image + third-party → not flagged
                     ResponseInfo(status=404,
                                  resource_type="script",
                                  url="https://WWW.SAUCEDEMO.COM/",
                                  redirect_from=None,
                                  method="GET",
                                  navigation_request=False),
                     # 404 + script + first-party → not flagged
                     ResponseInfo(status=200,
                                  resource_type="image",
                                  url="https://WWW.SAUCEDEMO.COM/",
                                  redirect_from=None,
                                  method="GET",
                                  navigation_request=False),
                     # 200 + image + first-party → not flagged
                     ]

CRAFTED_REQUESTS = [RequestInfo(url="https://www.saucedemo.com/inventory.html",
                                method="DELETE",
                                resource_type="image",
                                failure="NS_BINDING_ABORTED",
                                redirected_from=None),
                    RequestInfo(url="https://www.saucedemo.com/inventory.html",
                                method="PUT",
                                resource_type="data",
                                failure="NS_ERROR_UNKNOWN_HOST",
                                redirected_from=None),
                    RequestInfo(url="https://events.backtrace.io/api/",
                                method="POST",
                                resource_type="data",
                                failure="NS_ERROR_FAILURE",
                                redirected_from=None),
                    RequestInfo(url="https://events.backtrace.io/api/",
                                method="GET",
                                resource_type="image",
                                failure="NS_BINDING_ABORTED",
                                redirected_from=None),
                    RequestInfo(url="https://www.saucedemo.com/assets/sauce-backpack-1200x1500-CjRW-Djj.jpg",
                                method="GET",
                                resource_type="image",
                                failure="NS_ERROR_FAILURE",
                                redirected_from=None),
                    RequestInfo(url="https://www.saucedemo.com/assets/sauce-labs-onesie-1200x1500-MISSING.jpg",
                                method="GET",
                                resource_type="image",
                                failure="NS_ERROR_FAILURE",
                                redirected_from=None),
                    RequestInfo(url="https://www.saucedemo.com/assets/sauce-backpack-1200x1500-CjRW-Djj.jpg",
                                method="GET",
                                resource_type="image",
                                failure="NS_BINDING_ABORTED",
                                redirected_from=None),

                    ]

# To be used with the test_unexpected_request_failures
IMAGE_URL_LIST = set(["https://www.saucedemo.com/assets/sauce-backpack-1200x1500-CjRW-Djj.jpg",
                      "https://www.saucedemo.com/assets/bike-light-1200x1500-DxcZRFOA.jpg",
                      "https://www.saucedemo.com/assets/bolt-shirt-1200x1500-mR0ldpVS.jpg",
                      "https://www.saucedemo.com/assets/red-onesie-1200x1500-BrSuq0ic.jpg",
                      "https://www.saucedemo.com/assets/red-tatt-1200x1500-E-qp6aYf.jpg",
                      "https://www.saucedemo.com/assets/sauce-pullover-1200x1500-BfbI-PSd.jpg"])


@pytest.mark.parametrize("hostname, expected",
                         URL_LIST)
def test_is_first_party(hostname, expected):
    assert assertions_helper.is_first_party(hostname) == expected, \
        "Issue Detected on is_first_party assertions_helper"


def test_traffic_errors():
    bad_entries = assertions_helper.traffic_errors(CRAFTED_RESPONSES)
    assert bad_entries == [CRAFTED_RESPONSES[0]]


def test_unexpected_failures():
    unexpected_failures = assertions_helper.unexpected_failure(CRAFTED_REQUESTS)
    assert unexpected_failures == [CRAFTED_REQUESTS[1], CRAFTED_REQUESTS[2], CRAFTED_REQUESTS[4],
                                   CRAFTED_REQUESTS[5]]


def test_unexpected_request_failures():
    unexpected = assertions_helper.unexpected_request_failures(CRAFTED_REQUESTS, IMAGE_URL_LIST)
    assert unexpected == [CRAFTED_REQUESTS[0], CRAFTED_REQUESTS[1], CRAFTED_REQUESTS[2], CRAFTED_REQUESTS[3],
                          CRAFTED_REQUESTS[5]]
