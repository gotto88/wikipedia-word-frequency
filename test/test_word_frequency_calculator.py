from collections import Counter

from src.word_frequency_calculator import WordFrequencyCalculator


class TestWikiPageFetcher:
    """Test cases for WikiPageFetcher class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.calculator = WordFrequencyCalculator()

    def test_empty_string(self):
        """Test with empty string input."""
        result = self.calculator.calculate_word_frequency("")
        assert result == Counter()

    def test_one_word(self):
        """Test with one word."""
        result = self.calculator.calculate_word_frequency("test.")
        assert result == Counter({"test": 1})

    def test_two_same_words(self):
        """Test with two same words."""
        result = self.calculator.calculate_word_frequency("test test.")
        assert result == Counter({"test": 2})

    def test_two_words_not_proper_space(self):
        """Test with two words not proper space."""
        result = self.calculator.calculate_word_frequency("test.test2")
        assert result == Counter({"test": 1, "test2": 1})

    def test_two_different_words(self):
        """Test with two different words."""
        result = self.calculator.calculate_word_frequency("test test2.")
        assert result == Counter({"test": 1, "test2": 1})

    def test_100_same_words(self):
        """Test with input of 100 same words."""
        result = self.calculator.calculate_word_frequency("test " * 100)
        assert result == Counter({"test": 100})

    def test_omit_words_with_numbers(self):
        """Test omit numbers."""
        result = self.calculator.calculate_word_frequency("23 test 123.")
        assert result == Counter({"test": 1})
