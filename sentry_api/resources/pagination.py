from typing import NamedTuple

from requests import Response

class Link(NamedTuple):
    url: str
    rel: str
    results: bool
    cursor: str

class Pagination(NamedTuple):
    next: Link
    previous: Link

def __parse_links(links_header: str) -> Pagination:
    previous_link, next_link = links_header.split(",")

    return Pagination(
        next=__parse_link(next_link),
        previous=__parse_link(previous_link)
    )

def __parse_link(link: str) -> Link:
    url, rel, results, cursor = link.split(";")

    results = results.split("=")[1].strip('"') == "true"

    return Link(
        url=url.strip(" <>"),
        rel=rel.split("=")[1].strip("\""),
        results=results,
        cursor=cursor.split("=")[1].strip("\"")
    )

def get_all_pages(api, url, results = None):
    response: Response = api.http_client.make_a_full_url_call("get", url)
    if results is None:
        results = response.json()
    else:
        results.extend(response.json())

    next_link = __parse_links(response.headers["link"]).next
    if next_link.results:
        results.extend(get_all_pages(api, next_link.url, results))

    return results
