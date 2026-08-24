import logging
import urllib.parse
from utilities.network import ResponseInfo, RequestInfo

logger = logging.getLogger(__name__)

# Module Constants
EXPECTED_FAILURES = ["NS_BINDING_ABORTED"]
# NS_BINDING_ABORTED is a specific Firefox  vocabulary for an error. Applied here since tests run on Firefox.


def is_first_party(url: str) -> bool:
    hostname = urllib.parse.urlparse(url).hostname
    if hostname is None:
        return False
    return hostname == "saucedemo.com" or hostname.endswith(".saucedemo.com")


def traffic_errors(traffic_listener: list[ResponseInfo]) -> list[ResponseInfo]:

    bad_entries = [event for event in traffic_listener if
                   event.status >= 400 and
                   event.resource_type == "image" and
                   is_first_party(event.url)]

    return bad_entries


def unexpected_failure(traffic_listener: list[RequestInfo]) -> list[RequestInfo]:

    bad_entries = [event for event in traffic_listener if
                   event.failure not in EXPECTED_FAILURES]

    return bad_entries
