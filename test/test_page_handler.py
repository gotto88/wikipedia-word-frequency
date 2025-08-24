import pytest
from unittest.mock import Mock

from src.page_handler import PageHandler, RootPageNotFoundError
from src.wikipage_fetcher import WikiPageFetcher
from src.cache import WikiPageCache
from src.models import WikiPageInfo


class TestPageHandler:
    """Test cases for PageHandler class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.mock_wiki_fetcher = Mock(spec=WikiPageFetcher)
        self._mock_wiki_page_cache = Mock(spec=WikiPageCache)
        self._mock_wiki_page_cache.get.return_value = None
        self._mock_wiki_page_cache.set.return_value = None
        self.page_handler = PageHandler(
            self.mock_wiki_fetcher,
            self._mock_wiki_page_cache,
            use_cache=True
        )

    def test_calculate_word_frequency_root_page_not_found(self):
        """Test negative case: non-existing root page raises
        RootPageNotFoundError."""
        page_name = "NonExistentPage"
        self.mock_wiki_fetcher.fetch_page.return_value = None

        with pytest.raises(RootPageNotFoundError) as exc_info:
            self.page_handler.calculate_word_frequency(page_name, depth=1)
        assert str(exc_info.value) == "Root page NonExistentPage not found"
        self.mock_wiki_fetcher.fetch_page.assert_called_once_with(page_name)

    def test_calculate_word_frequency_depth_1_with_2_links(self):
        """Test case: depth 1 with 2 links, each page has one sentence
        content."""
        root_page_name = "Python"

        mock_root_page = Mock()
        mock_root_page.title = "Python"
        mock_root_page.text = "Python is a programming language."
        mock_root_page.links = {"Programming": None, "Language": None}

        mock_programming_page = Mock()
        mock_programming_page.title = "Programming"
        mock_programming_page.text = "Programming is writing code."
        mock_programming_page.links = {}

        mock_language_page = Mock()
        mock_language_page.title = "Language"
        mock_language_page.text = "Language is communication system."
        mock_language_page.links = {}

        def mock_fetch_page(page_name):
            if page_name == "Python":
                return mock_root_page
            elif page_name == "Programming":
                return mock_programming_page
            elif page_name == "Language":
                return mock_language_page
            return None
        self.mock_wiki_fetcher.fetch_page.side_effect = mock_fetch_page
        result = self.page_handler.calculate_word_frequency(
            page_name=root_page_name,
            depth=1
        )
        assert result is not None
        assert result["is"]["count"] == 3
        assert result["a"]["count"] == 1
        assert result["programming"]["count"] == 2
        assert result["language"]["count"] == 2
        assert result["code"]["count"] == 1
        assert result["communication"]["count"] == 1
        assert result["system"]["count"] == 1
        assert self.mock_wiki_fetcher.fetch_page.call_count == 3
        self.mock_wiki_fetcher.fetch_page.assert_any_call("Python")
        self.mock_wiki_fetcher.fetch_page.assert_any_call("Programming")
        self.mock_wiki_fetcher.fetch_page.assert_any_call("Language")

    def test_calculate_word_frequency_depth_2_with_multiple_links(self):
        """Test case: depth 2, each page has 2 links with one sentence
        content."""
        root_page_name = "Computer"
        mock_root_page = Mock()
        mock_root_page.title = "Computer"
        mock_root_page.text = "Computer is electronic device."
        mock_root_page.links = {"Hardware": None, "Software": None}
        mock_hardware_page = Mock()
        mock_hardware_page.title = "Hardware"
        mock_hardware_page.text = "Hardware is physical components."
        mock_hardware_page.links = {"CPU": None, "Memory": None}
        mock_software_page = Mock()
        mock_software_page.title = "Software"
        mock_software_page.text = "Software is computer programs."
        mock_software_page.links = {"Operating": None, "Application": None}

        mock_cpu_page = Mock()
        mock_cpu_page.title = "CPU"
        mock_cpu_page.text = "CPU is central processor."
        mock_cpu_page.links = {}
        mock_memory_page = Mock()
        mock_memory_page.title = "Memory"
        mock_memory_page.text = "Memory stores data."
        mock_memory_page.links = {}
        mock_operating_page = Mock()
        mock_operating_page.title = "Operating"
        mock_operating_page.text = "Operating system manages."
        mock_operating_page.links = {}
        mock_application_page = Mock()
        mock_application_page.title = "Application"
        mock_application_page.text = "Application runs tasks."
        mock_application_page.links = {}

        def mock_fetch_page(page_name):
            page_map = {
                "Computer": mock_root_page,
                "Hardware": mock_hardware_page,
                "Software": mock_software_page,
                "CPU": mock_cpu_page,
                "Memory": mock_memory_page,
                "Operating": mock_operating_page,
                "Application": mock_application_page
            }
            return page_map.get(page_name)
        self.mock_wiki_fetcher.fetch_page.side_effect = mock_fetch_page
        result = self.page_handler.calculate_word_frequency(
            page_name=root_page_name,
            depth=2
        )
        assert result is not None
        assert result["is"]["count"] == 4
        assert result["computer"]["count"] == 2
        assert result["hardware"]["count"] == 1
        assert result["software"]["count"] == 1
        assert result["cpu"]["count"] == 1
        assert result["memory"]["count"] == 1
        assert result["operating"]["count"] == 1
        assert result["application"]["count"] == 1
        assert result["electronic"]["count"] == 1
        assert result["physical"]["count"] == 1
        assert result["programs"]["count"] == 1
        assert result["central"]["count"] == 1
        assert result["processor"]["count"] == 1
        assert result["stores"]["count"] == 1
        assert result["data"]["count"] == 1
        assert result["system"]["count"] == 1
        assert result["manages"]["count"] == 1
        assert result["runs"]["count"] == 1
        assert result["tasks"]["count"] == 1
        assert self.mock_wiki_fetcher.fetch_page.call_count == 7
        self.mock_wiki_fetcher.fetch_page.assert_any_call("Computer")
        self.mock_wiki_fetcher.fetch_page.assert_any_call("Hardware")
        self.mock_wiki_fetcher.fetch_page.assert_any_call("Software")
        self.mock_wiki_fetcher.fetch_page.assert_any_call("CPU")
        self.mock_wiki_fetcher.fetch_page.assert_any_call("Memory")
        self.mock_wiki_fetcher.fetch_page.assert_any_call("Operating")
        self.mock_wiki_fetcher.fetch_page.assert_any_call("Application")

    def test_calculate_word_frequency_depth_2_same_links_appear(self):
        """Test case: depth 2, each page has 2 links with one sentence
        content."""
        root_page_name = "Computer"
        mock_root_page = Mock()
        mock_root_page.title = "Computer"
        mock_root_page.text = "Computer is electronic device."
        mock_root_page.links = {"Hardware": None, "Software": None}
        mock_hardware_page = Mock()
        mock_hardware_page.title = "Hardware"
        mock_hardware_page.text = "Hardware is physical components."
        mock_hardware_page.links = {"CPU": None, "Memory": None}
        mock_software_page = Mock()
        mock_software_page.title = "Software"
        mock_software_page.text = "Software is computer programs."
        mock_software_page.links = {"CPU": None, "Memory": None}

        mock_cpu_page = Mock()
        mock_cpu_page.title = "CPU"
        mock_cpu_page.text = "CPU is central processor."
        mock_cpu_page.links = {}
        mock_memory_page = Mock()
        mock_memory_page.title = "Memory"
        mock_memory_page.text = "Memory stores data."
        mock_memory_page.links = {}

        def mock_fetch_page(page_name):
            page_map = {
                "Computer": mock_root_page,
                "Hardware": mock_hardware_page,
                "Software": mock_software_page,
                "CPU": mock_cpu_page,
                "Memory": mock_memory_page
            }
            return page_map.get(page_name)
        self.mock_wiki_fetcher.fetch_page.side_effect = mock_fetch_page
        result = self.page_handler.calculate_word_frequency(
            page_name=root_page_name,
            depth=2
        )
        assert result is not None
        assert result["is"]["count"] == 4
        assert result["computer"]["count"] == 2
        assert result["hardware"]["count"] == 1
        assert result["software"]["count"] == 1
        assert result["cpu"]["count"] == 1
        assert result["memory"]["count"] == 1
        assert result["electronic"]["count"] == 1
        assert result["physical"]["count"] == 1
        assert result["programs"]["count"] == 1
        assert result["central"]["count"] == 1
        assert result["processor"]["count"] == 1
        assert result["stores"]["count"] == 1
        assert self.mock_wiki_fetcher.fetch_page.call_count == 5
        self.mock_wiki_fetcher.fetch_page.assert_any_call("Computer")
        self.mock_wiki_fetcher.fetch_page.assert_any_call("Hardware")
        self.mock_wiki_fetcher.fetch_page.assert_any_call("Software")
        self.mock_wiki_fetcher.fetch_page.assert_any_call("CPU")
        self.mock_wiki_fetcher.fetch_page.assert_any_call("Memory")

    def test_calculate_word_frequency_ignore_words(self):
        """Test case: ignore words in the ignore list."""
        root_page_name = "Python"

        mock_root_page = Mock()
        mock_root_page.title = "Python"
        mock_root_page.text = "Python is a programming language."
        mock_root_page.links = {"Programming": None, "Language": None}

        mock_programming_page = Mock()
        mock_programming_page.title = "Programming"
        mock_programming_page.text = "Programming is writing code."
        mock_programming_page.links = {}

        mock_language_page = Mock()
        mock_language_page.title = "Language"
        mock_language_page.text = "Language is communication system."
        mock_language_page.links = {}

        def mock_fetch_page(page_name):
            if page_name == "Python":
                return mock_root_page
            elif page_name == "Programming":
                return mock_programming_page
            elif page_name == "Language":
                return mock_language_page
            return None
        self.mock_wiki_fetcher.fetch_page.side_effect = mock_fetch_page
        result = self.page_handler.calculate_word_frequency(
            page_name=root_page_name,
            depth=1,
            ignore_list=["language", "programming"]
        )
        assert result is not None
        assert result["is"]["count"] == 3
        assert result["a"]["count"] == 1
        assert result["code"]["count"] == 1
        assert result["communication"]["count"] == 1
        assert result["system"]["count"] == 1
        assert "language" not in result
        assert "programming" not in result

    def test_use_cache_got_root_page_info(self):
        """Test case: get the cached page info if it exists."""
        root_page_name = "Test"
        self._mock_wiki_page_cache.get.side_effect = [
            WikiPageInfo(
                page_name="Test",
                world_freqs={
                    "test": 4,
                },
                links=["Test2", "Test3"]
            ),
            None,
            None
        ]
        self.mock_wiki_fetcher.fetch_page.return_value = None

        mock_test2_page = Mock()
        mock_test2_page.title = "Test2"
        mock_test2_page.text = "test2 test2"
        mock_test2_page.links = {}

        mock_test3_page = Mock()
        mock_test3_page.title = "Test3"
        mock_test3_page.text = "test3 test3"
        mock_test3_page.links = {}

        def mock_fetch_page(page_name):
            if page_name == "Test2":
                return mock_test2_page
            elif page_name == "Test3":
                return mock_test3_page
            return None
        self.mock_wiki_fetcher.fetch_page.side_effect = mock_fetch_page
        result = self.page_handler.calculate_word_frequency(
            page_name=root_page_name,
            depth=1
        )
        assert result is not None
        assert result["test"]["count"] == 4
        assert result["test2"]["count"] == 2
        assert result["test3"]["count"] == 2
