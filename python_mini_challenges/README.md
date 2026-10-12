# Task 3: Python Mini Challenges

A collection of foundational Python problem-solving exercises focusing on string manipulation, list algorithms, and dictionary structures. Part of the **WeIntern Pvt. Ltd. Python Development Internship (Week 1)**.

---

## 📌 Project Objective

The goal of Task 3 is to reinforce core programming logic, data structures, and algorithmic thinking without relying on external libraries. The challenges emphasize:
- Meaningful variable and function naming
- Defensive input validation (type checking, handling empty collections)
- Algorithmic efficiency and clarity
- PEP 8 compliance and clean documentation

---

## 📂 Challenges Overview

```
python_mini_challenges/
├── strings.py        # 3 String manipulation problems
├── lists.py          # 3 List algorithms and operations
├── dictionaries.py   # 3 Key-value dictionary problems
└── README.md         # Task documentation
```

---

## 🧩 Challenge Details

### A. String Problems (`strings.py`)

1. **Reverse a String (`reverse_string`)**:
   - Reverses any string input using Pythonic slice syntax `[::-1]`.
   - Handles empty strings (`"" -> ""`), multi-word sentences, and preserves spacing.
2. **Count Vowels (`count_vowels`)**:
   - Case-insensitively counts occurrences of vowels (`A, E, I, O, U`).
   - Returns both total vowel count and a per-vowel breakdown dictionary.
3. **Palindrome Check (`is_palindrome`)**:
   - Determines whether a phrase reads the same backward as forward.
   - Cleans punctuation and whitespace to correctly evaluate phrases like `"race car"` or `"Madam"`.

---

### B. List Problems (`lists.py`)

1. **Find Largest and Smallest (`find_largest_and_smallest`)**:
   - Computes minimum and maximum elements in \(O(N)\) time through iterative comparison.
   - Raises descriptive `ValueError` on empty lists and validates numerical data types.
2. **Remove Duplicates Preserving Order (`remove_duplicates_preserve_order`)**:
   - Eliminates duplicate items while strictly preserving the initial insertion order.
   - Achieves \(O(N)\) time complexity using a tracking set (overcoming the unordered nature of `list(set())`).
3. **Count Even and Odd Numbers (`count_even_odd`)**:
   - Separates and tallies even and odd integers.
   - Properly handles negative integers and zero.

---

### C. Dictionary Problems (`dictionaries.py`)

1. **Count Character Frequency (`count_character_frequency`)**:
   - Computes letter frequencies using `dict.get(char, 0) + 1`.
   - Supports optional case sensitivity and whitespace ignoring.
2. **Merge Two Dictionaries (`merge_dictionaries`)**:
   - Combines two dictionaries with selectable conflict strategies:
     - `override`: Values in the second dictionary take precedence.
     - `sum_numeric`: Numeric values sharing the same key are added together.
     - `combine_lists`: Values are concatenated into lists.
3. **Student Marks and Averages (`calculate_student_averages`)**:
   - Takes a dictionary mapping student names to lists of marks.
   - Calculates individual averages, overall class average, and detects the top-ranking student.

---

## 💻 How to Run

Navigate to the `python_mini_challenges` folder and run each script independently:

```bash
# Run String Challenges
python strings.py

# Run List Challenges
python lists.py

# Run Dictionary Challenges
python dictionaries.py
```

---

## 📋 Sample Terminal Outputs

### `strings.py`
```text
============================================================
      Python Mini Challenges - String Operations
============================================================

--- Challenge 1: Reverse a String ---
Original Text: 'python internship'
Reversed Text: 'pihsnretni nohtyp'

--- Challenge 2: Count Vowels in a Sentence ---
Sentence: 'WeIntern Python Development Internship'
Total Vowels Found: 11
Vowel Breakdown:
  'a': 0
  'e': 5
  'i': 3
  'o': 2
  'u': 0

--- Challenge 3: Palindrome Check ---
Is 'Madam' a palindrome? -> True
Is 'race car' a palindrome? -> True
Is 'Hello Python' a palindrome? -> False
```

### `lists.py`
```text
============================================================
       Python Mini Challenges - List Operations
============================================================

--- Challenge 1: Find Largest and Smallest Numbers ---
Input List: [42, 17, 89, 5, 23, 99, -12, 0, 77]
Smallest Number: -12
Largest Number:  99

--- Challenge 2: Remove Duplicates Preserving Order ---
Original List:  [4, 7, 2, 7, 9, 2, 1, 4, 8, 7]
De-duplicated:  [4, 7, 2, 9, 1, 8]

--- Challenge 3: Count Even and Odd Numbers ---
Input List: [12, 7, 19, 24, 30, 31, 45, 60, -4, 0]
Even Count: 6 -> [12, 24, 30, 60, -4, 0]
Odd Count:  4 -> [7, 19, 31, 45]
```

### `dictionaries.py`
```text
============================================================
    Python Mini Challenges - Dictionary Operations
============================================================

--- Challenge 1: Count Character Frequency ---
Input Text: 'banana'
Character Frequencies: {'b': 1, 'a': 3, 'n': 2}

--- Challenge 2: Merge Two Dictionaries ---
Dictionary 1: {'Python': 85, 'Java': 78, 'SQL': 90}
Dictionary 2: {'SQL': 5, 'C++': 88, 'Python': 10}
Merged (sum_numeric mode): {'Python': 95, 'Java': 78, 'SQL': 95, 'C++': 88}

--- Challenge 3: Student Marks and Averages ---
Student Average Marks:
  * Neha     : 91.00
  * Arjun    : 85.00
  * Ravi     : 88.00
  * Priya    : 95.67
  * Amit     : 79.00

Overall Class Average: 87.73
Top Student:           Priya (95.67%)
```

---

## 🛡️ Edge Cases Handled
- Empty input strings return empty strings without raising errors.
- Palindromes ignore spaces and punctuation when requested.
- Empty lists in `find_largest_and_smallest` raise clear `ValueError` instead of unhandled exceptions.
- Non-integer elements in `count_even_odd` trigger informative `TypeError` messages.
- Dictionaries handle empty inputs and mismatched types predictably.
