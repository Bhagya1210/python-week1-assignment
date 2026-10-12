"""Unit tests for Expense Tracker application."""

from __future__ import annotations
import csv
import os
import shutil
import sys
import tempfile
import unittest

# Ensure expense_tracker directory is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ET_DIR = os.path.join(PROJECT_ROOT, "expense_tracker")
if ET_DIR not in sys.path:
    sys.path.insert(0, ET_DIR)

from file_handler import (
    ensure_data_file,
    export_summary,
    load_expenses,
    save_all_expenses,
    save_expense,
)
from main import calculate_overall_summary


class TestExpenseFileHandler(unittest.TestCase):
    """Test file operations including CSV initialization, append, and loading."""

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp()
        self.csv_path = os.path.join(self.test_dir, "test_expenses.csv")

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_ensure_data_file_creates_headers(self) -> None:
        ensure_data_file(self.csv_path)
        self.assertTrue(os.path.exists(self.csv_path))
        with open(self.csv_path, "r", encoding="utf-8") as f:
            header_line = f.readline().strip()
        self.assertEqual(header_line, "Date,Category,Description,Amount")

    def test_save_and_load_expense(self) -> None:
        record1 = {
            "date": "2026-02-01",
            "category": "Food",
            "description": "Lunch with team",
            "amount": 450.50,
        }
        record2 = {
            "date": "2026-02-02",
            "category": "Travel",
            "description": "Metro card recharge",
            "amount": 200.00,
        }

        save_expense(self.csv_path, record1)
        save_expense(self.csv_path, record2)

        loaded = load_expenses(self.csv_path)
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0]["category"], "Food")
        self.assertEqual(loaded[0]["amount"], 450.50)
        self.assertEqual(loaded[1]["category"], "Travel")
        self.assertEqual(loaded[1]["amount"], 200.00)

    def test_load_expenses_with_corrupted_line(self) -> None:
        ensure_data_file(self.csv_path)
        # Append a corrupted non-numeric line
        with open(self.csv_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["2026-02-05", "Shopping", "Shoes", "invalid_amount"])
            writer.writerow(["2026-02-06", "Books", "Python Guide", "500.00"])

        loaded = load_expenses(self.csv_path)
        # Should gracefully skip the corrupted line and load the valid one
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["amount"], 500.00)

    def test_export_summary(self) -> None:
        report_path = os.path.join(self.test_dir, "report.txt")
        content = "=== Test Summary Report ===\nTotal Spent: 1000.00"
        ok, msg = export_summary(report_path, content)
        self.assertTrue(ok)
        self.assertTrue(os.path.exists(report_path))
        with open(report_path, "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), content)


class TestExpenseAnalytics(unittest.TestCase):
    """Test expense calculation and analytical summary helpers."""

    def setUp(self) -> None:
        self.sample_expenses = [
            {"date": "2026-02-01", "category": "Food", "description": "Groceries", "amount": 1500.00},
            {"date": "2026-02-03", "category": "Travel", "description": "Flight ticket", "amount": 1200.00},
            {"date": "2026-02-05", "category": "Utilities", "description": "Electric bill", "amount": 750.00},
            {"date": "2026-02-12", "category": "Food", "description": "Dinner", "amount": 650.00},
        ]

    def test_overall_summary_calculation(self) -> None:
        report_text = calculate_overall_summary(self.sample_expenses)
        self.assertIn("Total Entries: 4", report_text)
        # Total: 1500 + 1200 + 750 + 650 = 4100.00
        self.assertIn("Total Spent:   4100.00", report_text)
        self.assertIn("Highest Expense: Food - 1500.00 (Groceries)", report_text)

    def test_empty_summary_calculation(self) -> None:
        report_text = calculate_overall_summary([])
        self.assertEqual(report_text, "No expense records available.")


if __name__ == "__main__":
    unittest.main()
