import os
import structlog
from concurrent.futures import ThreadPoolExecutor, as_completed

from wikipediaapi import WikipediaPage

from src.models import WikiPageInfo
from src.wikipage_fetcher import WikiPageFetcher
from src.word_frequency_calculator import WordFrequencyCalculator


logger = structlog.get_logger(__name__)


class RootPageNotFoundError(Exception):
    pass


DEFAULT_MAX_THREADS = 10


class PageHandler:
    MAX_THREADS = int(os.environ.get(
        "MAX_FETCHING_THREADS", DEFAULT_MAX_THREADS)
    )

    def __init__(self, wikipage_fetcher: WikiPageFetcher) -> None:
        """
        Initialize the PageHandler with a WikiPageFetcher.

        Args:
            wikipage_fetcher: A WikiPageFetcher instance.
        """
        self._wikipage_fetcher = wikipage_fetcher

    def calculate_word_frequency(
        self,
        page_name: str,
        depth: int,
        ignore_list: list[str] | None = None,
        percentile: int | None = None
    ) -> dict[str, dict[str, int | float]]:
        """
        Calculate the word frequency of a page and its links
        up to a given depth.

        Args:
            page_name: The name of the root page.
            depth: The depth of the page to fetch.
            ignore_list: A list of words to ignore.
            percentile: The percentile limit to use for the word frequency.
        """
        fethed_pages: list[str] = []
        total_hits = 0
        root_page = self._wikipage_fetcher.fetch_page(page_name)
        if not root_page:
            logger.warning("Root page not found", page=page_name)
            raise RootPageNotFoundError(f"Root page {page_name} not found")

        fethed_pages.append(root_page.title)
        pages_to_fetch: list[str] = list(root_page.links.keys())
        aggregated_frequencies = WordFrequencyCalculator.calculate_word_frequency(
            root_page.text
        )
        total_hits += aggregated_frequencies.total()

        for level in range(1, depth + 1):
            logger.debug("Fetching next level", depth=level, max_depth=depth)
            logger.debug("Pages to fetch", number_of_pages=len(pages_to_fetch))
            with ThreadPoolExecutor(max_workers=self.MAX_THREADS) as executor:
                future_to_page = {
                    executor.submit(self._fetch_page_info, page_name): page_name
                    for page_name in pages_to_fetch
                }
                next_pages: list[str] = []
                for future in as_completed(future_to_page):
                    page_name = future_to_page[future]
                    try:
                        page_info = future.result()
                        fethed_pages.append(page_name)
                        if page_info:
                            aggregated_frequencies += page_info.world_freqs
                            total_hits += page_info.world_freqs.total()
                            next_pages.extend(page_info.links)
                            logger.debug("Fetched page", page=page_name)
                        else:
                            logger.warning("Page not found", page=page_name)
                    except Exception as e:
                        logger.error(
                            "Error fetching page", page=page_name, error=str(e)
                        )
                        continue
            next_pages = list(set(next_pages))
            pages_to_fetch = [page_name for page_name in next_pages if page_name not in fethed_pages]
        result = {name: {"count": count, "percent": count / total_hits * 100} for name, count in aggregated_frequencies.items()}
        if percentile:
            result = {name: stats for name, stats in result.items() if stats["percent"] >= percentile}
        if ignore_list:
            result = {name: stats for name, stats in result.items() if name not in ignore_list}
        return result

    def _fetch_page_info(self, page_name: str) -> WikiPageInfo | None:
        page: WikipediaPage | None = self._wikipage_fetcher.fetch_page(page_name)
        if not page:
            logger.warning("Page not found", page=page_name)
            return None
        return WikiPageInfo(
            page_name=page.title,
            world_freqs=WordFrequencyCalculator.calculate_word_frequency(page.text),
            links=list(page.links.keys())
        )
