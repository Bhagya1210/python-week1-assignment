"""File handler for Expense Tracker.

Provides modular CSV persistence and summary report export logic using
Python's built-in csv and os libraries. Decouples storage operations
from console and UI logic.
"""

from __future__ import annotations
import csv
import os
from typing import Any, Dict, List, Tuple

CSV_HEADERS: List[str] = ["Date", "Category", "Description", "Amount"]


def ensure_data_file(filepath: str) -> None:
    """Ensure the CSV file and its parent folder exist with header row."""
    parent_dir = os.path.dirname(filepath)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    if not os.path.exists(filepath):
        with open(filepath, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADERS)


def load_expenses(filepath: str) -> List[Dict[str, Any]]:
    """Load expense entries from a CSV file.

    Args:
        filepath: Path to the CSV file.

    Returns:
        List of expense dictionaries:
        {'date': str, 'category': str, 'description': str, 'amount': float}
    """
    ensure_data_file(filepath)
    expenses: List[Dict[str, Any]] = []

    try:
        with open(filepath, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row_index, row in enumerate(reader, start=2):
                # Guard against empty or truncated rows
                if not row or not any(row.values()):
                    continue

                date_val = row.get("Date", "").strip()
                cat_val = row.get("Category", "").strip()
                desc_val = row.get("Description", "").strip()
                amount_str = row.get("Amount", "").strip()

                try:
                    amount_val = float(amount_str)
                except (ValueError, TypeError):
                    # Corrupted or malformed amount, skip gracefully
                    continue

                expenses.append({
                    "date": date_val,
                    "category": cat_val,
                    "description": desc_val,
                    "amount": round(amount_val, 2),
                })
    except Exception as exc:
        print(f"[!] Warning: Error reading expenses file: {exc}")

    return expenses


def save_expense(filepath: str, expense: Dict[str, Any]) -> Tuple[bool, str]:
    """Append a single expense entry to the CSV file.

    Args:
        filepath: Path to the CSV file.
        expense: Dict with keys ('date', 'category', 'description', 'amount').

    Returns:
        Tuple of (success: bool, message: str).
    """
    ensure_data_file(filepath)
    try:
        with open(filepath, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                expense["date"],
                expense["category"],
                expense["description"],
                f"{float(expense['amount']):.2f}",
            ])
        return True, "Expense record saved successfully."
    except Exception as exc:
        return False, f"Failed to append expense: {exc}"


def save_all_expenses(filepath: str, expenses: List[Dict[str, Any]]) -> Tuple[bool, str]:
    """Rewrite entire CSV with all expense records.

    Args:
        filepath: Path to the CSV file.
        expenses: List of expense dictionaries.

    Returns:
        Tuple of (success: bool, message: str).
    """
    parent_dir = os.path.dirname(filepath)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    try:
        with open(filepath, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADERS)
            for item in expenses:
                writer.writerow([
                    item["date"],
                    item["category"],
                    item["description"],
                    f"{float(item['amount']):.2f}",
                ])
        return True, f"Saved {len(expenses)} expense entries to '{filepath}'."
    except Exception as exc:
        return False, f"Failed to rewrite expenses: {exc}"


def export_summary(report_filepath: str, summary_content: str) -> Tuple[bool, str]:
    """Export formatted text summary report to a file.

    Args:
        report_filepath: Destination file path.
        summary_content: Formatted text to write.

    Returns:
        Tuple of (success: bool, message: str).
    """
    parent_dir = os.path.dirname(report_filepath)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    try:
        with open(report_filepath, "w", encoding="utf-8") as file:
            file.write(summary_content)
        return True, f"Summary report exported successfully to '{report_filepath}'."
    except Exception as exc:
        return False, f"Error exporting summary report: {exc}"
