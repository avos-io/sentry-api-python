from urllib.parse import urljoin

import requests

from sentry_api.exceptions import (
    SentryApiBadInputException,
    SentryApiConflictException,
    SentryApiException,
    SentryApiForbiddenException,
    SentryApiResourceNotFoundException,
)


class BaseHttp:
    def __init__(self, endpoint_url: str, token: str) -> None:
        self.endpoint_url = endpoint_url
        self.token = token

    def make_a_call(self, http_method: str, endpoint: str, data: dict = None):
        raise NotImplementedError()


class RequestsHttp(BaseHttp):
    class BaseUrlSession(requests.Session):
        def __init__(self, base_url=None):
            super().__init__()
            self.base_url = base_url

        def request_full_url(self, method, url, *args, **kwargs):
            if "json" in kwargs and kwargs["json"]:
                kwargs["json"] = self.remove_empty(kwargs["json"])

            print(f"Requesting {method} {url}")
            return super().request(method, url, *args, **kwargs)

        def request(self, method, url, *args, **kwargs):
            joined_url = urljoin(self.base_url, url)
            return self.request_full_url(method, joined_url, *args, **kwargs)

        def remove_empty(self, params: dict):
            """
            This method removes any parameters that do not have value set.
            So e.g. if we would pass `None` for `slug` during update of project we would get 405 response
            """
            return {k: v for k, v in params.items() if v is not None}

    def __init__(self, endpoint_url: str, token: str) -> None:
        super().__init__(endpoint_url, token)
        self.session = RequestsHttp.BaseUrlSession(endpoint_url)
        self.session.headers.update({"authorization": "Bearer " + token})

    def __check_status_code(self, r):
        if r.status_code == 400:
            raise SentryApiBadInputException(r)

        if r.status_code == 403:
            raise SentryApiForbiddenException(r)

        if r.status_code == 404:
            raise SentryApiResourceNotFoundException(r)

        if r.status_code == 405:
            raise SentryApiException(r)

        if r.status_code == 409:
            raise SentryApiConflictException(r)

    def make_a_full_url_call(self, http_method: str, url: str, data: dict = None):
        r = self.session.request_full_url(http_method, url, json=data)
        self.__check_status_code(r)
        return r

    def make_a_call(self, http_method: str, endpoint: str, data: dict = None):
        r = self.session.request(http_method, endpoint, json=data)
        self.__check_status_code(r)
        return r
