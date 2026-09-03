from utilities import assertions_helper
import pytest
from utilities.network import ResponseInfo, RequestInfo


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

CRAFTED_REQUESTS = [RequestInfo(url="Irrelevant",
                                method="Irrelevant",
                                resource_type="Irrelevant",
                                failure="NS_BINDING_ABORTED",
                                redirected_from=None),
                    # Should not be flagged: Expected.
                    RequestInfo(url="Irrelevant",
                                method="Irrelevant",
                                resource_type="Irrelevant",
                                failure="NS_ERROR_UNKNOWN_HOST",
                                redirected_from=None),
                    # Should be Flagged. Not Expected
                    RequestInfo(url="Irrelevant",
                                method="Irrelevant",
                                resource_type="Irrelevant",
                                failure=None,
                                redirected_from=None),
                    ]


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
    assert unexpected_failures == [CRAFTED_REQUESTS[1], CRAFTED_REQUESTS[2]]
