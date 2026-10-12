"""Python Mini Challenges - Dictionary Operations.

This module implements solutions for core dictionary manipulation challenges:
1. Counting the frequency of each character in a string.
2. Merging two dictionaries with customizable conflict resolution strategies.
3. Calculating individual and overall student average marks from a marks dictionary.

Each solution includes robust input validation, clear algorithmic logic,
and sample demonstrations.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Union


def count_character_frequency(
    text: str,
    ignore_spaces: bool = True,
    case_sensitive: bool = False,
) -> Dict[str, int]:
    """Count the frequency of each character in a string.

    Uses dictionary key-value counting via `dict.get()`.

    Args:
        text: Input string.
        ignore_spaces: If True, whitespace characters are excluded from count.
        case_sensitive: If False, characters are lowercased before counting.

    Returns:
        Dictionary mapping characters to their integer occurrences.

    Raises:
        TypeError: If text is not a string.

    Example:
        >>> count_character_frequency("banana")
        {'b': 1, 'a': 3, 'n': 2}
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected a string, got {type(text).__name__}.")

    freq: Dict[str, int] = {}
    processed = text if case_sensitive else text.lower()

    for char in processed:
        if ignore_spaces and char.isspace():
            continue
        freq[char] = freq.get(char, 0) + 1

    return freq


def merge_dictionaries(
    dict1: Dict[Any, Any],
    dict2: Dict[Any, Any],
    conflict_mode: str = "override",
) -> Dict[Any, Any]:
    """Merge two dictionaries into a new combined dictionary.

    Args:
        dict1: The base dictionary.
        dict2: The secondary dictionary to merge in.
        conflict_mode: Strategy when a key exists in both dictionaries:
            - 'override': dict2 value overrides dict1 value.
            - 'sum_numeric': numeric values are summed; non-numeric values are overridden.
            - 'combine_lists': values are merged into a list.

    Returns:
        A new dictionary containing merged key-value pairs.

    Raises:
        TypeError: If either argument is not a dictionary.
        ValueError: If conflict_mode is unrecognized.

    Example:
        >>> merge_dictionaries({"a": 10, "b": 20}, {"b": 30, "c": 40}, conflict_mode="sum_numeric")
        {'a': 10, 'b': 50, 'c': 40}
    """
    if not isinstance(dict1, dict) or not isinstance(dict2, dict):
        raise TypeError("Both arguments must be dictionaries.")

    valid_modes = {"override", "sum_numeric", "combine_lists"}
    if conflict_mode not in valid_modes:
        raise ValueError(f"Unknown mode '{conflict_mode}'. Choose from: {valid_modes}")

    merged: Dict[Any, Any] = dict1.copy()

    for key, val in dict2.items():
        if key in merged:
            if conflict_mode == "override":
                merged[key] = val
            elif conflict_mode == "sum_numeric":
                v1, v2 = merged[key], val
                if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
                    merged[key] = v1 + v2
                else:
                    merged[key] = val
            elif conflict_mode == "combine_lists":
                v1 = merged[key]
                list1 = v1 if isinstance(v1, list) else [v1]
                list2 = val if isinstance(val, list) else [val]
                merged[key] = list1 + list2
        else:
            merged[key] = val

    return merged


def calculate_student_averages(
    records: Dict[str, List[Union[int, float]]],
) -> Dict[str, Any]:
    """Calculate individual student averages and class statistics.

    Args:
        records: Dictionary where key is student name and value is a list of marks.

    Returns:
        Dictionary containing:
            - 'student_averages': Dict mapping student name to rounded average marks.
            - 'overall_class_average': Overall average across all students.
            - 'top_student': Name of student with highest average.
            - 'top_average': Highest average marks.

    Raises:
        TypeError: If records is not a dictionary or contains invalid types.
        ValueError: If records is empty.

    Example:
        >>> calculate_student_averages({"Alice": [80, 90, 85], "Bob": [70, 75, 80]})
        {'student_averages': {'Alice': 85.0, 'Bob': 75.0}, 'overall_class_average': 80.0, ...}
    """
    if not isinstance(records, dict):
        raise TypeError("Student records must be provided as a dictionary.")

    if not records:
        raise ValueError("Cannot calculate averages for an empty dictionary of records.")

    student_averages: Dict[str, float] = {}

    for name, marks in records.items():
        if not isinstance(marks, (list, tuple)):
            raise TypeError(f"Marks for '{name}' must be a list/tuple of numbers.")
        if not marks:
            student_averages[name] = 0.0
            continue

        # Validate elements
        for m in marks:
            if not isinstance(m, (int, float)):
                raise TypeError(f"Mark value '{m}' for '{name}' is not numeric.")

        avg = sum(marks) / len(marks)
        student_averages[name] = round(avg, 2)

    all_avgs = list(student_averages.values())
    overall_avg = round(sum(all_avgs) / len(all_avgs), 2) if all_avgs else 0.0

    top_student = max(student_averages, key=student_averages.get)  # type: ignore[arg-type]
    top_avg = student_averages[top_student]

    return {
        "student_averages": student_averages,
        "overall_class_average": overall_avg,
        "top_student": top_student,
        "top_average": top_avg,
    }


def run_demonstration() -> None:
    """Execute demonstration examples with formatted console outputs."""
    print("=" * 60)
    print("    Python Mini Challenges - Dictionary Operations")
    print("=" * 60)

    # 1. Character Frequency
    print("\n--- Challenge 1: Count Character Frequency ---")
    sample_string = "banana"
    freq = count_character_frequency(sample_string)
    print(f"Input Text: '{sample_string}'")
    print(f"Character Frequencies: {freq}")

    phrase = "Python Programming"
    freq_phrase = count_character_frequency(phrase, ignore_spaces=True)
    print(f"\nInput Text: '{phrase}' (spaces ignored)")
    print(f"Character Frequencies: {freq_phrase}")

    # 2. Merge Dictionaries
    print("\n--- Challenge 2: Merge Two Dictionaries ---")
    d1 = {"Python": 85, "Java": 78, "SQL": 90}
    d2 = {"SQL": 5, "C++": 88, "Python": 10}
    print(f"Dictionary 1: {d1}")
    print(f"Dictionary 2: {d2}")

    merged_override = merge_dictionaries(d1, d2, conflict_mode="override")
    print(f"Merged (override mode):    {merged_override}")

    merged_sum = merge_dictionaries(d1, d2, conflict_mode="sum_numeric")
    print(f"Merged (sum_numeric mode): {merged_sum}")

    # 3. Student Marks & Averages
    print("\n--- Challenge 3: Student Marks and Averages ---")
    student_data = {
        "Neha": [90, 92, 91],
        "Arjun": [80, 85, 90],
        "Ravi": [88, 86, 90],
        "Priya": [95, 98, 94],
        "Amit": [75, 80, 82],
    }
    print(f"Student Marks Database:\n{student_data}")

    analysis = calculate_student_averages(student_data)
    print("\nStudent Average Marks:")
    for student, avg in analysis["student_averages"].items():
        print(f"  * {student:<10}: {avg:.2f}")

    print(f"\nOverall Class Average: {analysis['overall_class_average']:.2f}")
    print(f"Top Student:           {analysis['top_student']} ({analysis['top_average']:.2f}%)")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    run_demonstration()
