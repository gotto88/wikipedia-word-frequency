from pydantic import BaseModel
from collections import Counter


class WikiPageInfo(BaseModel):
    """
    Model for storing information about a Wikipedia page.

    Args:
        page_name: The name of the Wikipedia page.
        world_freqs: A Counter object containing the frequency of each
                     word in the page.
        links: A list of links to other Wikipedia pages.
    """
    page_name: str
    world_freqs: Counter
    links: list[str]


class RequestCommon(BaseModel):
    article: str
    depth: int


class RequestPost(RequestCommon):
    ignore_list: list[str] | None = None
    percentile: int | None = None
