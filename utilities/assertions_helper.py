import logging
import urllib.parse
from utilities.network import ResponseInfo

logger = logging.getLogger(__name__)

def is_first_party(url: str) ->  bool:
    hostname = urllib.parse.urlparse(url).hostname
    if hostname is None:
        return False
    return hostname == "saucedemo.com" or hostname.endswith(".saucedemo.com")

def traffic_errors(traffic_listener:list[ResponseInfo])->  list[ResponseInfo]:

    bad_entries  = [event for event in traffic_listener if
                    event.status >= 400 and
                    event.resource_type ==  "image" and
                    is_first_party(event.url)]

    return bad_entries