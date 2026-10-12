"""Python Mini Challenges - List Operations.

This module implements solutions for core list manipulation challenges:
1. Finding the largest and smallest numbers in a list.
2. Removing duplicate elements while strictly preserving original order.
3. Counting even and odd numbers.

Each solution includes robust input validation, handling of empty sequences,
clean algorithmic implementations, and sample demonstrations.
"""

from __future__ import annotations
from typing import Any, Dict, List, Sequence, Tuple, Union

Number = Union[int, float]


def find_largest_and_smallest(numbers: Sequence[Number]) -> Tuple[Number, Number]:
    """Find the largest and smallest numbers in a sequence.

    Uses an iterative comparison approach to demonstrate algorithmic logic
    rather than purely calling built-in functions.

    Args:
        numbers: A sequence (list or tuple) of numbers.

    Returns:
        Tuple of (smallest, largest).

    Raises:
        ValueError: If the sequence is empty.
        TypeError: If elements are not numeric.

    Example:
        >>> find_largest_and_smallest([4, 7, 2, 9, 2, -5])
        (-5, 9)
    """
    if not isinstance(numbers, (list, tuple)):
        raise TypeError(f"Expected a list or tuple, got {type(numbers).__name__}.")

    if not numbers:
        raise ValueError("Cannot find min/max in an empty list.")

    # Validate first item
    first = numbers[0]
    if not isinstance(first, (int, float)):
        raise TypeError(f"List elements must be numeric, got {type(first).__name__}.")

    smallest: Number = first
    largest: Number = first

    for num in numbers[1:]:
        if not isinstance(num, (int, float)):
            raise TypeError(f"List elements must be numeric, got {type(num).__name__}.")
        if num < smallest:
            smallest = num
        if num > largest:
            largest = num

    return smallest, largest


def remove_duplicates_preserve_order(items: Sequence[Any]) -> List[Any]:
    """Remove duplicate items from a sequence while preserving original insertion order.

    Unlike `list(set(items))` which does not guarantee order preservation,
    this function uses a lookup set to achieve O(N) time complexity while
    maintaining the exact original sequence.

    Args:
        items: An iterable sequence with potential duplicates.

    Returns:
        List containing unique elements in their first-seen order.

    Raises:
        TypeError: If items is not a sequence.

    Example:
        >>> remove_duplicates_preserve_order([4, 7, 2, 7, 9, 2])
        [4, 7, 2, 9]
    """
    if not isinstance(items, (list, tuple)):
        raise TypeError(f"Expected a list or tuple, got {type(items).__name__}.")

    seen = set()
    unique_items: List[Any] = []

    for item in items:
        # Check membership in set (O(1) average lookup)
        if item not in seen:
            seen.add(item)
            unique_items.append(item)

    return unique_items


def count_even_odd(numbers: Sequence[int]) -> Dict[str, Any]:
    """Count even and odd integers in a list.

    Correctly handles negative numbers, zeros, and empty lists.

    Args:
        numbers: Sequence of integer values.

    Returns:
        Dictionary containing:
            - 'even_count': Total count of even numbers.
            - 'odd_count': Total count of odd numbers.
            - 'even_numbers': List of even numbers encountered.
            - 'odd_numbers': List of odd numbers encountered.

    Raises:
        TypeError: If sequence is not a list/tuple or contains non-integers.

    Example:
        >>> count_even_odd([1, 2, 3, 4, 5, 6])
        {'even_count': 3, 'odd_count': 3, 'even_numbers': [2, 4, 6], 'odd_numbers': [1, 3, 5]}
    """
    if not isinstance(numbers, (list, tuple)):
        raise TypeError(f"Expected a list or tuple, got {type(numbers).__name__}.")

    even_numbers: List[int] = []
    odd_numbers: List[int] = []

    for item in numbers:
        if not isinstance(item, int) or isinstance(item, bool):
            raise TypeError(f"Expected integer element, received {type(item).__name__} ({item}).")
        if item % 2 == 0:
            even_numbers.append(item)
        else:
            odd_numbers.append(item)

    return {
        "even_count": len(even_numbers),
        "odd_count": len(odd_numbers),
        "even_numbers": even_numbers,
        "odd_numbers": odd_numbers,
    }


def run_demonstration() -> None:
    """Execute demonstration examples with formatted console outputs."""
    print("=" * 60)
    print("       Python Mini Challenges - List Operations")
    print("=" * 60)

    # 1. Min / Max Demonstration
    print("\n--- Challenge 1: Find Largest and Smallest Numbers ---")
    num_list = [42, 17, 89, 5, 23, 99, -12, 0, 77]
    smallest, largest = find_largest_and_smallest(num_list)
    print(f"Input List: {num_list}")
    print(f"Smallest Number: {smallest}")
    print(f"Largest Number:  {largest}")

    # 2. Duplicate Removal Demonstration
    print("\n--- Challenge 2: Remove Duplicates Preserving Order ---")
    raw_list = [4, 7, 2, 7, 9, 2, 1, 4, 8, 7]
    deduped = remove_duplicates_preserve_order(raw_list)
    print(f"Original List:  {raw_list}")
    print(f"De-duplicated:  {deduped}")

    # 3. Even and Odd Count Demonstration
    print("\n--- Challenge 3: Count Even and Odd Numbers ---")
    mixed_nums = [12, 7, 19, 24, 30, 31, 45, 60, -4, 0]
    result = count_even_odd(mixed_nums)
    print(f"Input List: {mixed_nums}")
    print(f"Even Count: {result['even_count']} -> {result['even_numbers']}")
    print(f"Odd Count:  {result['odd_count']} -> {result['odd_numbers']}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    run_demonstration()
