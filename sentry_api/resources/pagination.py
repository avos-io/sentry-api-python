from collections import deque
import json
from typing import NamedTuple, Type

from requests import Response

from sentry_api import api
from sentry_api.http import BaseHttp, RequestsHttp

class Link(NamedTuple):
    url: str
    rel: str
    results: bool
    cursor: str

class Pagination(NamedTuple):
    next: Link
    previous: Link

class SentryApiPage:
    def __init__(self, http_client: Type[BaseHttp], method, url):
        self.first_run = True
        self.http_client = http_client
        self.method = method
        self.initial_url = url

    def __iter__(self):
        return self

    def __next__(self) -> json:

        if self.first_run:
            self.first_run = False
            response: Response = self.http_client.make_a_call(self.method, self.initial_url)
            response_json = response.json()
            self.next_link = self.__parse_links(response.headers["link"]).next
            return response_json

        if self.next_link.results:
            response = self.http_client.make_a_full_url_call("get", self.next_link.url)
            self.response_json = response.json()
            self.next_link = self.__parse_links(response.headers["link"]).next
            return self.response_json

        raise StopIteration

    def __parse_links(self, links_header: str) -> Pagination:
        previous_link, next_link = links_header.split(",")

        return Pagination(
            next=self.__parse_link(next_link),
            previous=self.__parse_link(previous_link)
        )

    def __parse_link(self, link: str) -> Link:
        url, rel, results, cursor = link.split(";")

        results = results.split("=")[1].strip('"') == "true"

        return Link(
            url=url.strip(" <>"),
            rel=rel.split("=")[1].strip("\""),
            results=results,
            cursor=cursor.split("=")[1].strip("\"")
        )
