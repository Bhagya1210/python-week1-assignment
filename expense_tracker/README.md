# Task 2: Expense Tracker

A console-based financial expense recording and reporting application developed in Python with persistent CSV storage. Part of the **WeIntern Pvt. Ltd. Python Development Internship (Week 1)**.

---

## 📌 Project Objective

The Expense Tracker enables users to record, review, categorize, and analyze daily personal expenses. The assignment emphasizes:
- Safe file handling using Python's standard `csv` module
- Date parsing and validation with the `datetime` module
- Graceful exception handling for missing files, invalid numbers, and edge cases
- Generating analytical financial summaries and exporting reports to files

---

## 🚀 Features

### Core Capabilities
- **Add Expense**: Records Date (`YYYY-MM-DD`), Category, Description, and Amount (`> 0.00`).
- **View All Expenses**: Displays all transactions in an organized, readable table.
- **Filter / Search by Category**: Quickly retrieves expenses matching a selected category.
- **Overall Financial Summary**: Computes total records, total expenditure, average expense, and the highest individual expense.
- **Persistent CSV Storage**: Loads records on startup and safely appends new entries without overwriting existing history.

### Advanced Enhancements
- **Category-wise Spending Breakdown**: Shows cumulative spend per category with percentage contribution.
- **Monthly Spending Summary**: Automatically aggregates transactions by month (`YYYY-MM`).
- **Sort by Amount**: Allows reviewing expenses from lowest-to-highest or highest-to-lowest.
- **Report Export**: Exports a detailed text summary report (`expense_summary_report.txt`) for archival or printing.

---

## 📁 File Structure

```
expense_tracker/
├── file_handler.py             # CSV reading, appending, and text report export
├── main.py                     # Menu interface and analytics flows
├── expenses.csv                # Persistent CSV storage file
├── expense_summary_report.txt  # Exported summary report (generated on demand)
└── README.md                   # Task documentation
```

### CSV Schema
`expenses.csv` uses a 4-column schema:
```csv
Date,Category,Description,Amount
2026-02-01,Food,Grocery shopping,1500.00
2026-02-03,Travel,Train tickets booking,1200.00
```

---

## 💻 How to Run

1. Open your terminal and navigate to `expense_tracker/`:
   ```bash
   cd expense_tracker
   ```
2. Run the application with Python 3:
   ```bash
   python main.py
   ```

---

## 📋 Sample Run & Outputs

### 1. Main Menu
```text
======================================
      ===== Expense Tracker =====
======================================
1. Add Expense
2. View All Expenses
3. Search / Filter by Category
4. Overall Expense Summary
5. Category-wise Spending Breakdown
6. Monthly Expense Summary
7. Sort Expenses by Amount
8. Export Summary Report to File
9. Exit
======================================
Enter your choice (1-9): 4
```

### 2. Overall Summary Report (Handbook Aligned)
```text
===== Expense Summary =====
Total Entries: 7
Total Spent:   5400.00
Average Expense: 771.43
Highest Expense: Travel - 1200.00 (Train tickets booking)
============================
```

### 3. Category-wise Breakdown
```text
--------------------------------------------------
Category             |   Amount Spent |  Share (%)
--------------------------------------------------
Food                 |        2150.00 |      39.8%
Travel               |        1200.00 |      22.2%
Utilities            |         750.00 |      13.9%
Health               |         500.00 |       9.3%
Education            |         450.00 |       8.3%
Entertainment        |         350.00 |       6.5%
--------------------------------------------------
Overall Total:       |        5400.00 |     100.0%
```

### 4. Monthly Expense Summary
```text
----------------------------------------
Month        | Transactions |    Total Spent
----------------------------------------
2026-02      |            7 |        5400.00
----------------------------------------
Grand Total: |            7 |        5400.00
```

---

## 🛡️ Exception Handling & Best Practices
- **Missing File on First Run**: Automatically creates `expenses.csv` with the correct column header row if the file does not exist.
- **Corrupted Records**: Safely skips blank or unparseable lines during CSV loading without halting the application.
- **Non-numeric & Negative Amounts**: Validates user inputs with descriptive error messages instead of raw crash tracebacks.
- **Date Format Checks**: Verifies `YYYY-MM-DD` conformance using `datetime.strptime`.
