from unittest.mock import Mock
import wikipediaapi

from src.wikipage_fetcher import WikiPageFetcher


class TestWikiPageFetcher:
    """Test cases for WikiPageFetcher class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.mock_wiki_api = Mock(spec=wikipediaapi.Wikipedia)
        self.fetcher = WikiPageFetcher(self.mock_wiki_api)

    def test_fetch_page_success(self):
        """Test successful page fetch with existing page."""
        page_name = "Python"
        mock_page = Mock(spec=wikipediaapi.WikipediaPage)
        mock_page.exists.return_value = True
        mock_page.title = "Python"
        mock_page.text = "Python is a programming language..."
        mock_page.links = {"Programming": None, "Language": None}
        self.mock_wiki_api.page.return_value = mock_page
        result = self.fetcher.fetch_page(page_name)
        assert result is not None
        assert result == mock_page
        assert result.title == page_name
        assert result.text == "Python is a programming language..."
        assert result.links == {"Programming": None, "Language": None}
        self.mock_wiki_api.page.assert_called_once_with(page_name)

    def test_fetch_page_not_exists(self):
        """Test page fetch when page does not exist."""
        page_name = "NonExistentPage12345"
        mock_page = Mock(spec=wikipediaapi.WikipediaPage)
        mock_page.exists.return_value = False
        self.mock_wiki_api.page.return_value = mock_page
        result = self.fetcher.fetch_page(page_name)
        assert result is None
        self.mock_wiki_api.page.assert_called_once_with(page_name)

    def test_fetch_page_exception(self):
        """Test page fetch when Wikipedia API raises an exception."""
        page_name = "ProblematicPage"
        self.mock_wiki_api.page.side_effect = Exception("API Error")
        result = self.fetcher.fetch_page(page_name)
        assert result is None
        self.mock_wiki_api.page.assert_called_once_with(page_name)

    def test_fetch_page_network_error(self):
        """Test page fetch when network error occurs."""
        page_name = "NetworkErrorPage"
        self.mock_wiki_api.page.side_effect = ConnectionError(
            "Network timeout"
        )
        result = self.fetcher.fetch_page(page_name)
        assert result is None
        self.mock_wiki_api.page.assert_called_once_with(page_name)

    def test_fetch_page_http_error(self):
        """Test page fetch when HTTP error occurs."""
        page_name = "HttpErrorPage"
        self.mock_wiki_api.page.side_effect = Exception(
            "HTTP 500 Internal Server Error"
        )
        result = self.fetcher.fetch_page(page_name)
        assert result is None
        self.mock_wiki_api.page.assert_called_once_with(page_name)

    def test_fetch_page_empty_string(self):
        """Test page fetch with empty page name."""
        page_name = ""
        mock_page = Mock(spec=wikipediaapi.WikipediaPage)
        mock_page.exists.return_value = False
        self.mock_wiki_api.page.return_value = mock_page
        result = self.fetcher.fetch_page(page_name)
        assert result is None
        self.mock_wiki_api.page.assert_called_once_with(page_name)

    def test_fetch_page_special_characters(self):
        """Test page fetch with page name containing special characters."""
        page_name = "C++ (programming language)"
        mock_page = Mock(spec=wikipediaapi.WikipediaPage)
        mock_page.exists.return_value = True
        mock_page.title = "C++ (programming language)"
        mock_page.text = "C++ is a programming language..."
        self.mock_wiki_api.page.return_value = mock_page
        result = self.fetcher.fetch_page(page_name)
        assert result is not None
        assert result.title == page_name
        self.mock_wiki_api.page.assert_called_once_with(page_name)

    def test_fetch_page_unicode_characters(self):
        """Test page fetch with page name containing unicode characters."""
        page_name = "Árvíztűrő tükörfúrógép"
        mock_page = Mock(spec=wikipediaapi.WikipediaPage)
        mock_page.exists.return_value = True
        mock_page.title = "Árvíztűrő tükörfúrógép"
        mock_page.text = "An árvíztűrő tükörfúrógép does not exist..."
        self.mock_wiki_api.page.return_value = mock_page
        result = self.fetcher.fetch_page(page_name)
        assert result is not None
        assert result.title == page_name
        self.mock_wiki_api.page.assert_called_once_with(page_name)

    def test_fetch_page_none_input(self):
        """Test page fetch with None as page name."""
        page_name = None
        self.mock_wiki_api.page.side_effect = TypeError(
            "page() argument 1 must be str, not NoneType"
        )
        result = self.fetcher.fetch_page(page_name)
        assert result is None
        self.mock_wiki_api.page.assert_called_once_with(page_name)

    def test_fetch_page_multiple_calls_same_page(self):
        """Test multiple calls to fetch the same page."""
        page_name = "Python"
        mock_page = Mock(spec=wikipediaapi.WikipediaPage)
        mock_page.exists.return_value = True
        mock_page.title = "Python"
        self.mock_wiki_api.page.return_value = mock_page
        result1 = self.fetcher.fetch_page(page_name)
        result2 = self.fetcher.fetch_page(page_name)
        assert result1 is not None
        assert result2 is not None
        assert result1 == result2
        assert self.mock_wiki_api.page.call_count == 2
        self.mock_wiki_api.page.assert_called_with(page_name)
