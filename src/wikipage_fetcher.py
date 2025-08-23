import wikipediaapi
import structlog


logger = structlog.get_logger(__name__)


class WikiPageFetcher:
    def __init__(self, wiki_api: wikipediaapi.Wikipedia):
        """
        Initialize the WikiPageFetcher with a Wikipedia API instance.

        Args:
            wiki_api: A Wikipedia API instance.
        """
        self._wiki_api = wiki_api

    def fetch_page(self, page_name: str) -> wikipediaapi.WikipediaPage | None:
        """
        Fetch a Wikipedia page and return a WikiPageInfo object.

        Args:
            page_name: The name of the Wikipedia page to fetch.

        Returns:
            A WikiPageInfo object if fatch was successful and the page exists,
            otherwise None.
        """
        try:
            page = self._wiki_api.page(page_name)
        except Exception:
            logger.warning(
                "Error fetching page", page=page_name, exc_info=True
            )
            return None
        if not page.exists():
            logger.warning("Page does not exist", page=page_name)
            return None
        return page
