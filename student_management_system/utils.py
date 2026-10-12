"""Utility functions for user input validation and console formatting.

This module provides reusable helpers to validate strings, integers, floats,
and menu selections, as well as helpers to render clean, readable tables
for student records.
"""

from __future__ import annotations
from typing import List, Optional, Sequence


def display_header(title: str) -> None:
    """Print a clean section banner."""
    line = "=" * (len(title) + 10)
    print(f"\n{line}")
    print(f"    {title}")
    print(f"{line}")


def get_valid_string(
    prompt: str,
    allow_empty: bool = False,
    min_length: int = 1,
) -> str:
    """Prompt the user for a non-empty string with validation.

    Args:
        prompt: Display text for input prompt.
        allow_empty: Whether an empty response is permissible.
        min_length: Minimum number of characters.

    Returns:
        Validated string input.
    """
    while True:
        value = input(prompt).strip()
        if not value and allow_empty:
            return ""
        if len(value) < min_length:
            print(f"[!] Input cannot be empty. Please enter at least {min_length} character(s).")
            continue
        return value


def get_valid_int(
    prompt: str,
    min_val: Optional[int] = None,
    max_val: Optional[int] = None,
    allow_empty: bool = False,
) -> Optional[int]:
    """Prompt the user for an integer with bounds checking.

    Args:
        prompt: Display text for input prompt.
        min_val: Optional minimum permissible value (inclusive).
        max_val: Optional maximum permissible value (inclusive).
        allow_empty: If True and input is blank, returns None.

    Returns:
        Validated integer or None if empty and permitted.
    """
    while True:
        raw = input(prompt).strip()
        if allow_empty and not raw:
            return None
        try:
            val = int(raw)
            if min_val is not None and val < min_val:
                print(f"[!] Value must be at least {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"[!] Value must not exceed {max_val}.")
                continue
            return val
        except ValueError:
            print("[!] Invalid input. Please enter a valid whole number.")


def get_valid_float(
    prompt: str,
    min_val: Optional[float] = None,
    max_val: Optional[float] = None,
    allow_empty: bool = False,
) -> Optional[float]:
    """Prompt the user for a floating-point number with bounds checking.

    Args:
        prompt: Display text for input prompt.
        min_val: Optional minimum permissible value.
        max_val: Optional maximum permissible value.
        allow_empty: If True and input is blank, returns None.

    Returns:
        Validated float or None if empty and permitted.
    """
    while True:
        raw = input(prompt).strip()
        if allow_empty and not raw:
            return None
        try:
            val = float(raw)
            if min_val is not None and val < min_val:
                print(f"[!] Value must be at least {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"[!] Value must not exceed {max_val}.")
                continue
            return val
        except ValueError:
            print("[!] Invalid input. Please enter a valid numeric value.")


def get_valid_menu_choice(prompt: str, valid_choices: Sequence[str]) -> str:
    """Prompt the user until one of the valid menu choices is entered."""
    valid_set = {str(c).strip().lower() for c in valid_choices}
    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_set:
            return choice
        print(f"[!] Invalid choice '{choice}'. Please select from: {', '.join(valid_choices)}")


def get_confirmation(prompt: str) -> bool:
    """Prompt the user for a Yes/No confirmation. Defaults to No."""
    choice = input(f"{prompt} (y/N): ").strip().lower()
    return choice in ("y", "yes")


def display_students_table(students: Sequence[object]) -> None:
    """Display a list of Student instances in a formatted console table."""
    if not students:
        print("\n  [No student records found.]")
        return

    # Header and divider
    header = f"{'ID':<10} | {'Name':<22} | {'Age':<5} | {'Course':<20} | {'Marks':<7}"
    divider = "-" * len(header)
    print(f"\n{divider}")
    print(header)
    print(divider)

    for student in students:
        s_id = getattr(student, "student_id", "")
        name = getattr(student, "name", "")
        age = getattr(student, "age", "")
        course = getattr(student, "course", "")
        marks = getattr(student, "marks", 0.0)
        print(f"{s_id:<10} | {name:<22} | {age:<5} | {course:<20} | {marks:<7.2f}")

    print(divider)
    print(f"Total Records: {len(students)}\n")
