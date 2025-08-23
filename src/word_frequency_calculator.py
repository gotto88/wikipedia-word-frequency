from collections import Counter
import re


class WordFrequencyCalculator:

    @classmethod
    def calculate_word_frequency(self, text: str) -> Counter:
        """
        Calculate the frequency of each word in a given text.

        Args:
            text: The text to calculate the word frequency of.

        Returns:
            A Counter object containing the frequency of each word in the text.
        """
        cleaned = re.sub(r"[^a-zA-Z0-9\s]", " ", text.strip())
        words = re.findall(r'\b[A-Za-z]\w{0,}\b', cleaned)
        return Counter([word.lower() for word in words])
