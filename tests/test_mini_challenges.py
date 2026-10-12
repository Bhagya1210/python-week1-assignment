"""Unit tests for Python Mini Challenges (strings, lists, dictionaries)."""

from __future__ import annotations
import os
import sys
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PMC_DIR = os.path.join(PROJECT_ROOT, "python_mini_challenges")
if PMC_DIR not in sys.path:
    sys.path.insert(0, PMC_DIR)

from dictionaries import (
    calculate_student_averages,
    count_character_frequency,
    merge_dictionaries,
)
from lists import (
    count_even_odd,
    find_largest_and_smallest,
    remove_duplicates_preserve_order,
)
from strings import (
    count_vowels,
    is_palindrome,
    reverse_string,
)


class TestStringChallenges(unittest.TestCase):
    """Test string manipulation functions."""

    def test_reverse_string_normal(self) -> None:
        self.assertEqual(reverse_string("python internship"), "pihsnretni nohtyp")
        self.assertEqual(reverse_string("hello"), "olleh")

    def test_reverse_string_empty(self) -> None:
        self.assertEqual(reverse_string(""), "")

    def test_reverse_string_type_error(self) -> None:
        with self.assertRaises(TypeError):
            reverse_string(123)  # type: ignore[arg-type]

    def test_count_vowels(self) -> None:
        result = count_vowels("Hello World")
        self.assertEqual(result["total"], 3)
        self.assertEqual(result["breakdown"]["e"], 1)
        self.assertEqual(result["breakdown"]["o"], 2)
        self.assertEqual(result["breakdown"]["a"], 0)

    def test_count_vowels_no_vowels(self) -> None:
        result = count_vowels("rhythm fly")
        self.assertEqual(result["total"], 0)

    def test_count_vowels_type_error(self) -> None:
        with self.assertRaises(TypeError):
            count_vowels(None)  # type: ignore[arg-type]

    def test_is_palindrome_true(self) -> None:
        self.assertTrue(is_palindrome("Madam"))
        self.assertTrue(is_palindrome("race car"))
        self.assertTrue(is_palindrome("A man, a plan, a canal: Panama"))
        self.assertTrue(is_palindrome(""))

    def test_is_palindrome_false(self) -> None:
        self.assertFalse(is_palindrome("Python"))
        self.assertFalse(is_palindrome("WeIntern"))


class TestListChallenges(unittest.TestCase):
    """Test list algorithms and operations."""

    def test_find_largest_and_smallest(self) -> None:
        smallest, largest = find_largest_and_smallest([42, 17, 89, 5, -12, 0])
        self.assertEqual(smallest, -12)
        self.assertEqual(largest, 89)

    def test_find_largest_and_smallest_single_element(self) -> None:
        smallest, largest = find_largest_and_smallest([7])
        self.assertEqual(smallest, 7)
        self.assertEqual(largest, 7)

    def test_find_largest_and_smallest_empty_error(self) -> None:
        with self.assertRaises(ValueError):
            find_largest_and_smallest([])

    def test_find_largest_and_smallest_type_error(self) -> None:
        with self.assertRaises(TypeError):
            find_largest_and_smallest([1, "two", 3])  # type: ignore[list-item]

    def test_remove_duplicates_preserve_order(self) -> None:
        input_data = [4, 7, 2, 7, 9, 2, 1, 4]
        result = remove_duplicates_preserve_order(input_data)
        self.assertEqual(result, [4, 7, 2, 9, 1])

    def test_remove_duplicates_empty(self) -> None:
        self.assertEqual(remove_duplicates_preserve_order([]), [])

    def test_count_even_odd(self) -> None:
        numbers = [12, 7, 19, 24, 30, 31, -4, 0]
        res = count_even_odd(numbers)
        # Even: 12, 24, 30, -4, 0 (5)
        # Odd: 7, 19, 31 (3)
        self.assertEqual(res["even_count"], 5)
        self.assertEqual(res["odd_count"], 3)
        self.assertEqual(res["even_numbers"], [12, 24, 30, -4, 0])
        self.assertEqual(res["odd_numbers"], [7, 19, 31])

    def test_count_even_odd_invalid_type(self) -> None:
        with self.assertRaises(TypeError):
            count_even_odd([1, 2, "three"])  # type: ignore[list-item]


class TestDictionaryChallenges(unittest.TestCase):
    """Test dictionary manipulation and data analysis functions."""

    def test_count_character_frequency(self) -> None:
        freq = count_character_frequency("banana")
        self.assertEqual(freq, {"b": 1, "a": 3, "n": 2})

    def test_count_character_frequency_with_spaces(self) -> None:
        freq = count_character_frequency("a b a", ignore_spaces=True)
        self.assertEqual(freq, {"a": 2, "b": 1})

    def test_merge_dictionaries_override(self) -> None:
        d1 = {"a": 1, "b": 2}
        d2 = {"b": 99, "c": 3}
        merged = merge_dictionaries(d1, d2, conflict_mode="override")
        self.assertEqual(merged, {"a": 1, "b": 99, "c": 3})

    def test_merge_dictionaries_sum_numeric(self) -> None:
        d1 = {"apple": 10, "banana": 20}
        d2 = {"banana": 30, "cherry": 40}
        merged = merge_dictionaries(d1, d2, conflict_mode="sum_numeric")
        self.assertEqual(merged, {"apple": 10, "banana": 50, "cherry": 40})

    def test_calculate_student_averages(self) -> None:
        records = {
            "Neha": [90, 92, 91],
            "Arjun": [80, 85, 90],
            "Priya": [95, 98, 94],
        }
        res = calculate_student_averages(records)
        self.assertEqual(res["student_averages"]["Neha"], 91.0)
        self.assertEqual(res["student_averages"]["Arjun"], 85.0)
        self.assertAlmostEqual(res["student_averages"]["Priya"], 95.67, places=2)
        self.assertEqual(res["top_student"], "Priya")
        self.assertAlmostEqual(res["overall_class_average"], 90.56, places=2)

    def test_calculate_student_averages_empty_error(self) -> None:
        with self.assertRaises(ValueError):
            calculate_student_averages({})


if __name__ == "__main__":
    unittest.main()
