#Utility file for the Network  Traffic Analyzer
from dataclasses import dataclass

#Collector Dataclasses:

@dataclass
class RequestInfo:
    url: str
    method: str
    resource_type: str
    failure: str | None
    redirected_from : str | None

@dataclass
class ResponseInfo:
    url: str
    status: int
    method: str
    resource_type: str
    navigation_request: bool
    redirect_from : str | None

## Traffic Observers:

class  TrafficRecorder():
    def __init__(self):
        self.request_record:list[RequestInfo] = []
        self.response_record:list[ResponseInfo] = []
        self.failed_response_record:list[RequestInfo] = []

    def _request(self, request):
        self.request_record.append(RequestInfo(
            url=request.url,
            method=request.method,
            failure=request.failure,
            resource_type=request.resource_type,
            redirected_from=request.redirected_from.url if request.redirected_from is not None else None,
        )
        )

    def _response(self, response):  # Response Event Handler
        self.response_record.append(ResponseInfo(
            url=response.url,
            status=response.status,
            method=response.request.method,
            resource_type=response.request.resource_type,
            navigation_request=response.request.is_navigation_request(),
            redirect_from=response.request.redirected_from.url if response.request.redirected_from is not None else None,
        ))

    # Failed Response:
    def _request_failure(self, request):
        self.failed_response_record.append(RequestInfo(
            url=request.url,
            method=request.method,
            failure=request.failure,
            resource_type=request.resource_type,
            redirected_from=request.redirected_from.url if request.redirected_from is not None else None,
        ))

    def __repr__(self):
        redirects_from_on_requests = [request for request in self.request_record if request.redirected_from is not None]
        redirects_from_on_response = [request for request in self.response_record if request.redirect_from is not None]

        return (f"Total Requests: {len(self.request_record)}\n"
                f"Redirected Requests: {redirects_from_on_requests}\n"
                f"Total Responses: {len(self.response_record)}\n"
                f"Redirected Responses: {redirects_from_on_response}\n"
                f"Failed Requests: {len(self.failed_response_record)}\n")



