import urllib.parse
from utilities.network import ResponseInfo, RequestInfo

# Module Constants
EXPECTED_FAILURES = ["NS_BINDING_ABORTED"]
# NS_BINDING_ABORTED is a specific Firefox  vocabulary for an error.
# On Chrome  it would raise the alert,since  the error has  not been  added  as expected.
# In case it is  ran on Chrome, add the appropriate exception to the list.


def is_first_party(url: str) -> bool:
    '''Check if the provided url is from first party or external service.

    Args:
        url: string.
    Returns:
        bool: If the provided url is from first party or external service.

    Note:
        endwith(.saucedemo.com) adds an extra layer of protection covering cases like
        evilsaucedemo.com, where it ends with saucedemo, but having an altered hostname.
    '''
    hostname = urllib.parse.urlparse(url).hostname
    if hostname is None:
        return False
    return hostname == "saucedemo.com" or hostname.endswith(".saucedemo.com")


def traffic_errors(traffic_listener: list[ResponseInfo]) -> list[ResponseInfo]:
    '''Retrieves Traffic errors stored on the Traffic Listener.

        Will look for events that fail to load images  from first party urls.

    Args:
        traffic_listener: A list of  ResponseInfo objects.

    Returns:
        bad_entries: A list of ResponseInfo objects.

    Notes:
        It will not catch errors affecting other resource types that are not images.
        This is by Design and intentional.
        For example, it will catch if the page has no images, but will not catch if it has no  style.
    '''
    bad_entries = [event for event in traffic_listener if
                   event.status >= 400 and
                   event.resource_type == "image" and
                   is_first_party(event.url)]

    return bad_entries


def unexpected_failure(traffic_listener: list[RequestInfo]) -> list[RequestInfo]:
    '''Retrieves a  list of RequestFailures stored on the Traffic Listener in  case  there are any.

    Args:
        traffic_listener: A List of  RequestInfo objects.

    Returns:
        bad_entries: A list of RequestInfo objects.

    Notes:
        This method will catch if  the RequestInfo has a "failure=None". This is by Design and intentional.
        It is verified and expected on the unit test for this method.
        Will catch if someone passes "request_record" instead of "failed_response_record"
    '''

    bad_entries = [event for event in traffic_listener if
                   event.failure not in EXPECTED_FAILURES]

    return bad_entries
