from collections import Counter

from src.word_frequency_calculator import WordFrequencyCalculator


class TestWikiPageFetcher:
    """Test cases for WikiPageFetcher class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.calculator = WordFrequencyCalculator()

    def test_empty_string(self):
        """Test empty string input."""
        result = self.calculator.calculate_word_frequency("")
        assert result == Counter()

    def test_one_word(self):
        """Test empty string input."""
        result = self.calculator.calculate_word_frequency("test.")
        assert result == Counter({"test": 1})

    def test_two_same_words(self):
        """Test empty string input."""
        result = self.calculator.calculate_word_frequency("test test.")
        assert result == Counter({"test": 2})

    def test_two_different_words(self):
        """Test empty string input."""
        result = self.calculator.calculate_word_frequency("test test2.")
        assert result == Counter({"test": 1, "test2": 1})

    def test_100_same_words(self):
        """Test empty string input."""
        result = self.calculator.calculate_word_frequency("test " * 100)
        assert result == Counter({"test": 100})
