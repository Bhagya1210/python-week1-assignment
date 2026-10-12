"""Python Mini Challenges - String Manipulation Problems.

This module implements solutions for core string manipulation challenges:
1. Reversing a string (handling empty strings and multi-word phrases)
2. Counting vowels in a sentence (total count and per-vowel breakdown)
3. Palindrome checking (case-insensitive, whitespace-agnostic)

Each solution includes input validation, comprehensive docstrings, and
sample demonstrations.
"""

from __future__ import annotations
from typing import Any, Dict


def reverse_string(text: str) -> str:
    """Reverse a string using Python slicing.

    Args:
        text (str): The input string to reverse.

    Returns:
        str: The reversed string. Returns empty string if input is empty.

    Raises:
        TypeError: If input is not a string.

    Example:
        >>> reverse_string("python internship")
        'pihsnretni nohtyp'
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected a string, but received {type(text).__name__}.")

    if not text:
        return ""

    # Efficient and Pythonic slice reversal
    return text[::-1]


def count_vowels(sentence: str) -> Dict[str, Any]:
    """Count vowels (A, E, I, O, U) in a sentence case-insensitively.

    Args:
        sentence (str): Input text or sentence.

    Returns:
        dict: A dictionary containing:
            - 'total': Total count of vowels.
            - 'breakdown': Dictionary mapping each vowel ('a', 'e', 'i', 'o', 'u')
              to its occurrence count.

    Raises:
        TypeError: If input is not a string.

    Example:
        >>> count_vowels("Hello World")
        {'total': 3, 'breakdown': {'a': 0, 'e': 1, 'i': 0, 'o': 2, 'u': 0}}
    """
    if not isinstance(sentence, str):
        raise TypeError(f"Expected a string, but received {type(sentence).__name__}.")

    vowels = {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}
    total = 0

    for char in sentence.lower():
        if char in vowels:
            vowels[char] += 1
            total += 1

    return {
        "total": total,
        "breakdown": vowels,
    }


def is_palindrome(text: str, ignore_spaces: bool = True) -> bool:
    """Check whether a given string is a palindrome.

    A palindrome reads the same forwards and backwards. This function is
    case-insensitive and optionally ignores spaces and punctuation.

    Args:
        text (str): The string to test.
        ignore_spaces (bool): If True, strips spaces and checks alphanumeric chars.

    Returns:
        bool: True if text is a palindrome, False otherwise.

    Raises:
        TypeError: If input is not a string.

    Example:
        >>> is_palindrome("Madam")
        True
        >>> is_palindrome("race car")
        True
        >>> is_palindrome("python")
        False
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected a string, but received {type(text).__name__}.")

    if not text:
        return True  # An empty string reads the same in both directions

    if ignore_spaces:
        cleaned = "".join(ch.lower() for ch in text if ch.isalnum())
    else:
        cleaned = text.lower()

    return cleaned == cleaned[::-1]


def run_demonstration() -> None:
    """Execute demonstration examples with formatted console outputs."""
    print("=" * 60)
    print("      Python Mini Challenges - String Operations")
    print("=" * 60)

    # 1. Reverse String Demonstration
    print("\n--- Challenge 1: Reverse a String ---")
    sample_text = "python internship"
    result_rev = reverse_string(sample_text)
    print(f"Original Text: '{sample_text}'")
    print(f"Reversed Text: '{result_rev}'")
    print(f"Empty String Test: '{reverse_string('')}' (length: {len(reverse_string(''))})")

    # 2. Count Vowels Demonstration
    print("\n--- Challenge 2: Count Vowels in a Sentence ---")
    sample_sentence = "WeIntern Python Development Internship"
    vowel_info = count_vowels(sample_sentence)
    print(f"Sentence: '{sample_sentence}'")
    print(f"Total Vowels Found: {vowel_info['total']}")
    print("Vowel Breakdown:")
    for v, count in vowel_info["breakdown"].items():
        print(f"  '{v}': {count}")

    # 3. Palindrome Check Demonstration
    print("\n--- Challenge 3: Palindrome Check ---")
    test_cases = [
        "Madam",
        "race car",
        "A man, a plan, a canal: Panama",
        "Hello Python",
        "",
    ]
    for case in test_cases:
        res = is_palindrome(case)
        print(f"Is '{case}' a palindrome? -> {res}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    run_demonstration()
