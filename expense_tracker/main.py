"""Expense Tracker - Main Console Application.

Provides an interactive console interface for tracking expenses, analyzing
spending habits, and exporting financial summaries with CSV persistence.
"""

from __future__ import annotations
from datetime import datetime
import os
import sys
from typing import Any, Dict, List, Optional

# Ensure local imports work regardless of execution directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from file_handler import (
    export_summary,
    load_expenses,
    save_expense,
)

CSV_FILE = os.path.join(CURRENT_DIR, "expenses.csv")
REPORT_FILE = os.path.join(CURRENT_DIR, "expense_summary_report.txt")

COMMON_CATEGORIES = [
    "Food",
    "Travel",
    "Utilities",
    "Entertainment",
    "Education",
    "Health",
    "Shopping",
    "Other",
]


def display_header(title: str) -> None:
    """Print a clean section banner."""
    line = "=" * (len(title) + 10)
    print(f"\n{line}")
    print(f"    {title}")
    print(f"{line}")


def prompt_date() -> str:
    """Prompt user for a date in YYYY-MM-DD format or default to today."""
    today_str = datetime.today().strftime("%Y-%m-%d")
    while True:
        raw = input(f"Enter Date (YYYY-MM-DD) [Default: {today_str}]: ").strip()
        if not raw:
            return today_str
        try:
            parsed = datetime.strptime(raw, "%Y-%m-%d")
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            print("[!] Invalid date format. Please use YYYY-MM-DD (e.g., 2026-02-15).")


def prompt_category() -> str:
    """Prompt user to select a category from list or specify a custom one."""
    print("\nSelect Expense Category:")
    for idx, cat in enumerate(COMMON_CATEGORIES, start=1):
        print(f"  {idx}. {cat}")
    print(f"  {len(COMMON_CATEGORIES) + 1}. Custom Category")

    while True:
        choice = input(f"Choose option (1-{len(COMMON_CATEGORIES) + 1}): ").strip()
        if choice.isdigit():
            val = int(choice)
            if 1 <= val <= len(COMMON_CATEGORIES):
                return COMMON_CATEGORIES[val - 1]
            if val == len(COMMON_CATEGORIES) + 1:
                custom = input("Enter custom category name: ").strip()
                if custom:
                    return custom.title()
                print("[!] Category cannot be empty.")
                continue
        print(f"[!] Please select a number between 1 and {len(COMMON_CATEGORIES) + 1}.")


def prompt_amount() -> float:
    """Prompt user for a positive expense amount."""
    while True:
        raw = input("Enter Amount (e.g., 250.00): ").strip()
        try:
            val = float(raw)
            if val <= 0:
                print("[!] Expense amount must be greater than zero.")
                continue
            return round(val, 2)
        except ValueError:
            print("[!] Invalid amount. Please enter a numeric value.")


def display_expenses_table(expenses: List[Dict[str, Any]]) -> None:
    """Display expenses in a clean formatted console table."""
    if not expenses:
        print("\n  [No expense records found.]")
        return

    header = f"{'#':<4} | {'Date':<10} | {'Category':<15} | {'Description':<26} | {'Amount':>10}"
    divider = "-" * len(header)
    print(f"\n{divider}")
    print(header)
    print(divider)

    total = 0.0
    for idx, exp in enumerate(expenses, start=1):
        amt = exp["amount"]
        total += amt
        desc = exp["description"]
        if len(desc) > 26:
            desc = desc[:23] + "..."
        print(
            f"{idx:<4} | {exp['date']:<10} | {exp['category']:<15} | "
            f"{desc:<26} | {amt:>10.2f}"
        )

    print(divider)
    print(f"{'Total Spent:':<57} | {total:>10.2f}")
    print(f"Total Transactions: {len(expenses)}\n")


def add_expense_flow(expenses: List[Dict[str, Any]]) -> None:
    """Add new expense and append to CSV."""
    display_header("Add New Expense")
    date_str = prompt_date()
    category = prompt_category()

    while True:
        description = input("Enter Description: ").strip()
        if description:
            break
        print("[!] Description cannot be empty.")

    amount = prompt_amount()

    new_record = {
        "date": date_str,
        "category": category,
        "description": description,
        "amount": amount,
    }

    success, msg = save_expense(CSV_FILE, new_record)
    if success:
        expenses.append(new_record)
        print(f"\n[+] Success: Expense of Rs. {amount:.2f} ({category}) recorded successfully!")
    else:
        print(f"\n[!] Error saving expense: {msg}")


def view_all_expenses_flow(expenses: List[Dict[str, Any]]) -> None:
    """View all logged expenses."""
    display_header("All Expense Records")
    display_expenses_table(expenses)


def filter_by_category_flow(expenses: List[Dict[str, Any]]) -> None:
    """Filter expenses by category (case-insensitive)."""
    display_header("Filter / Search by Category")
    if not expenses:
        print("  [No expenses available to filter.]")
        return

    query = input("Enter category name to search: ").strip().lower()
    matches = [e for e in expenses if query in e["category"].lower()]

    if matches:
        print(f"\n[+] Found {len(matches)} record(s) matching '{query}':")
        display_expenses_table(matches)
    else:
        print(f"\n[!] No expenses found for category matching '{query}'.")


def calculate_overall_summary(expenses: List[Dict[str, Any]]) -> str:
    """Generate overall summary text matching the handbook report format."""
    if not expenses:
        return "No expense records available."

    total_entries = len(expenses)
    total_spent = sum(e["amount"] for e in expenses)
    highest_entry = max(expenses, key=lambda e: e["amount"])
    avg_spent = total_spent / total_entries

    lines = [
        "===== Expense Summary =====",
        f"Total Entries: {total_entries}",
        f"Total Spent:   {total_spent:.2f}",
        f"Average Expense: {avg_spent:.2f}",
        (
            f"Highest Expense: {highest_entry['category']} - "
            f"{highest_entry['amount']:.2f} ({highest_entry['description']})"
        ),
        "============================",
    ]
    return "\n".join(lines)


def summary_report_flow(expenses: List[Dict[str, Any]]) -> None:
    """Display overall financial summary."""
    display_header("Overall Expense Summary")
    if not expenses:
        print("  [No expense records found.]")
        return

    report = calculate_overall_summary(expenses)
    print(f"\n{report}")


def category_summary_flow(expenses: List[Dict[str, Any]]) -> None:
    """Display category-wise spending totals and percentages."""
    display_header("Category-wise Spending Breakdown")
    if not expenses:
        print("  [No expense records found.]")
        return

    total_spent = sum(e["amount"] for e in expenses)
    cat_totals: Dict[str, float] = {}

    for exp in expenses:
        cat = exp["category"]
        cat_totals[cat] = cat_totals.get(cat, 0.0) + exp["amount"]

    # Sort categories by total spent descending
    sorted_cats = sorted(cat_totals.items(), key=lambda x: x[1], reverse=True)

    header = f"{'Category':<20} | {'Amount Spent':>14} | {'Share (%)':>10}"
    divider = "-" * len(header)
    print(f"\n{divider}")
    print(header)
    print(divider)

    for cat, amt in sorted_cats:
        percentage = (amt / total_spent * 100.0) if total_spent > 0 else 0.0
        print(f"{cat:<20} | {amt:>14.2f} | {percentage:>9.1f}%")

    print(divider)
    print(f"{'Overall Total:':<20} | {total_spent:>14.2f} | {'100.0%':>10}\n")


def monthly_summary_flow(expenses: List[Dict[str, Any]]) -> None:
    """Display monthly spending summary grouped by YYYY-MM."""
    display_header("Monthly Expense Summary")
    if not expenses:
        print("  [No expense records found.]")
        return

    monthly_totals: Dict[str, float] = {}
    monthly_counts: Dict[str, int] = {}

    for exp in expenses:
        date_str = exp["date"]
        # Extract YYYY-MM
        month_key = date_str[:7] if len(date_str) >= 7 else "Unknown"
        monthly_totals[month_key] = monthly_totals.get(month_key, 0.0) + exp["amount"]
        monthly_counts[month_key] = monthly_counts.get(month_key, 0) + 1

    sorted_months = sorted(monthly_totals.keys())

    header = f"{'Month':<12} | {'Transactions':>12} | {'Total Spent':>14}"
    divider = "-" * len(header)
    print(f"\n{divider}")
    print(header)
    print(divider)

    grand_total = 0.0
    for month in sorted_months:
        amt = monthly_totals[month]
        grand_total += amt
        count = monthly_counts[month]
        print(f"{month:<12} | {count:>12} | {amt:>14.2f}")

    print(divider)
    print(f"{'Grand Total:':<12} | {len(expenses):>12} | {grand_total:>14.2f}\n")


def sort_expenses_flow(expenses: List[Dict[str, Any]]) -> None:
    """Sort and display expenses by amount."""
    display_header("Sort Expenses by Amount")
    if not expenses:
        print("  [No expense records found.]")
        return

    print("1. Sort Lowest to Highest")
    print("2. Sort Highest to Lowest")
    while True:
        choice = input("Enter choice (1-2): ").strip()
        if choice == "1":
            sorted_list = sorted(expenses, key=lambda e: e["amount"])
            break
        if choice == "2":
            sorted_list = sorted(expenses, key=lambda e: e["amount"], reverse=True)
            break
        print("[!] Please enter 1 or 2.")

    display_expenses_table(sorted_list)


def export_report_flow(expenses: List[Dict[str, Any]]) -> None:
    """Export complete financial summary report to a text file."""
    display_header("Export Summary Report")
    if not expenses:
        print("  [No expenses available to export.]")
        return

    total_spent = sum(e["amount"] for e in expenses)
    highest_entry = max(expenses, key=lambda e: e["amount"])

    # Prepare detailed report
    content_lines = [
        "============================================================",
        "             EXPENSE TRACKER - SUMMARY REPORT               ",
        "============================================================",
        f"Generated At:    {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Total Records:   {len(expenses)}",
        f"Total Amount:    Rs. {total_spent:.2f}",
        f"Highest Expense: Rs. {highest_entry['amount']:.2f} ({highest_entry['category']}: {highest_entry['description']})",
        "",
        "--- CATEGORY BREAKDOWN ---",
    ]

    cat_totals: Dict[str, float] = {}
    for exp in expenses:
        cat = exp["category"]
        cat_totals[cat] = cat_totals.get(cat, 0.0) + exp["amount"]

    for cat, amt in sorted(cat_totals.items(), key=lambda x: x[1], reverse=True):
        share = (amt / total_spent * 100.0) if total_spent > 0 else 0.0
        content_lines.append(f"  * {cat:<15}: Rs. {amt:>8.2f}  ({share:>5.1f}%)")

    content_lines.append("")
    content_lines.append("--- DETAILED LOGS ---")
    for exp in expenses:
        content_lines.append(
            f"  {exp['date']} | {exp['category']:<12} | {exp['description']:<24} | Rs. {exp['amount']:.2f}"
        )
    content_lines.append("============================================================")

    full_report = "\n".join(content_lines)

    dest = input(f"Enter export filename [Default: {REPORT_FILE}]: ").strip()
    target_path = dest if dest else REPORT_FILE

    success, msg = export_summary(target_path, full_report)
    if success:
        print(f"[+] Success: {msg}")
    else:
        print(f"[!] Error: {msg}")


def print_main_menu() -> None:
    """Print the primary menu banner."""
    print("\n" + "=" * 38)
    print("      ===== Expense Tracker =====")
    print("=" * 38)
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. Search / Filter by Category")
    print("4. Overall Expense Summary")
    print("5. Category-wise Spending Breakdown")
    print("6. Monthly Expense Summary")
    print("7. Sort Expenses by Amount")
    print("8. Export Summary Report to File")
    print("9. Exit")
    print("=" * 38)


def main() -> None:
    """Main execution loop for Expense Tracker."""
    print("\n[Info] Loading expense records from CSV...")
    expenses = load_expenses(CSV_FILE)
    print(f"[Info] Successfully loaded {len(expenses)} expense record(s).")

    while True:
        try:
            print_main_menu()
            choice = input("Enter your choice (1-9): ").strip()

            if choice == "1":
                add_expense_flow(expenses)
            elif choice == "2":
                view_all_expenses_flow(expenses)
            elif choice == "3":
                filter_by_category_flow(expenses)
            elif choice == "4":
                summary_report_flow(expenses)
            elif choice == "5":
                category_summary_flow(expenses)
            elif choice == "6":
                monthly_summary_flow(expenses)
            elif choice == "7":
                sort_expenses_flow(expenses)
            elif choice == "8":
                export_report_flow(expenses)
            elif choice == "9":
                print("\n[+] Exiting Expense Tracker. Have a great day!")
                break
            else:
                print(f"[!] Invalid option '{choice}'. Please select a number from 1 to 9.")

            input("\nPress [Enter] to return to menu...")
        except (KeyboardInterrupt, EOFError):
            print("\n\n[!] Session interrupted. Exiting safely. Goodbye!")
            break


if __name__ == "__main__":
    main()
