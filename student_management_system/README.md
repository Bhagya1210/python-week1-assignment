# Task 1: Student Management System

A menu-driven console application developed in Python using Object-Oriented Programming (OOP) principles. Part of the **WeIntern Pvt. Ltd. Python Development Internship (Week 1)**.

---

## 📌 Project Objective

The primary objective is to build a robust, structured console application to manage student academic records. The project demonstrates core software engineering practices:
- Object-Oriented Programming (Classes, Objects, Encapsulation)
- Full CRUD operations (Create, Read, Update, Delete)
- Defensive input validation to prevent crashes
- Persistent file storage with JSON auto-loading and auto-saving
- Data analysis features (sorting, class average, top performers)

---

## 🚀 Features

### Core Operations (CRUD)
- **Add Student**: Prompts for ID, Name, Age, Course, and Marks. Automatically validates inputs and rejects duplicate IDs.
- **View Students**: Displays all records in a formatted, aligned table.
- **Search Student**: Search by unique Student ID or partial match on Student Name.
- **Update Student**: Update individual fields (`Name`, `Age`, `Course`, `Marks`) without modifying unchanged attributes.
- **Delete Student**: Removes a student record with an explicit confirmation prompt to prevent accidental loss.

### Advanced Enhancements
- **Sorting**: Sort student records ascending or descending by Name or Marks.
- **Academic Analytics**:
  - Class average marks calculation.
  - Identification of top-performing student(s).
- **File Persistence**:
  - Automatically loads existing records from `students.json` on application startup.
  - Automatically writes updates back to `students.json` with clean indentation.
  - Handles missing or corrupt JSON files gracefully.

---

## 🏗️ OOP Architecture

The project cleanly separates data models, business logic, and user interface helpers:

```
student_management_system/
├── models.py       # Student and StudentManager classes
├── utils.py        # Input validation and console table formatting
├── main.py         # Menu-driven CLI flow and user interaction
├── students.json   # Persistent JSON data storage
└── README.md       # Task documentation
```

### Classes & Responsibilities
1. **`Student` (`models.py`)**:
   - Represents an entity with `student_id`, `name`, `age`, `course`, and `marks`.
   - Implements `to_dict()` and `from_dict()` for clean JSON serialization.
   - Implements `__str__()` for standardized output matching handbook standards:
     ```
     ID: 101 | Name: Neha | Age: 20 | Course: Python | Marks: 91.0
     ```
2. **`StudentManager` (`models.py`)**:
   - Maintains a list of `Student` objects in memory.
   - Provides methods: `add_student`, `get_all_students`, `search_by_id`, `search_by_name`, `update_student`, `delete_student`, `sort_students`, `calculate_average_marks`, `get_top_performer`, `save_to_json`, and `load_from_json`.
3. **`utils.py`**:
   - Input validators ensuring positive numbers, valid ranges, non-empty text, and menu choices.

---

## 💻 How to Run

1. Open your terminal and navigate to the project directory:
   ```bash
   cd student_management_system
   ```
2. Run the application with Python 3:
   ```bash
   python main.py
   ```

---

## 📋 Sample Run & Outputs

### 1. Main Menu
```text
========================================
   ===== Student Management System =====
========================================
1. Add Student
2. View Students
3. Search Student
4. Update Student
5. Delete Student
6. Sort Students
7. Performance Statistics
8. Exit
========================================
Enter your choice (1-8): 2
```

### 2. View All Students
```text
-------------------------------------------------------------------------
ID         | Name                   | Age   | Course               | Marks  
-------------------------------------------------------------------------
101        | Neha                   | 20    | Python               | 91.00  
102        | Arjun                  | 21    | Data Science         | 85.00  
103        | Ravi                   | 22    | Python               | 88.00  
104        | Priya                  | 20    | Web Development      | 95.50  
105        | Amit                   | 23    | Machine Learning     | 79.00  
-------------------------------------------------------------------------
Total Records: 5
```

### 3. Add Student with Validation
```text
=======================
    Add New Student
=======================
Enter Student ID: 106
Enter Full Name: Sneha Patel
Enter Age (5-120): 21
Enter Course / Stream: Artificial Intelligence
Enter Marks (0-100): 94.5
[+] Success: Student 'Sneha Patel' added successfully.
```

### 4. Performance Statistics
```text
=======================================
    Academic Performance Statistics
=======================================
Total Enrolled Students: 5
Class Average Marks:     87.70 / 100

Top Performing Student(s):
-------------------------------------------------------------------------
ID         | Name                   | Age   | Course               | Marks  
-------------------------------------------------------------------------
104        | Priya                  | 20    | Web Development      | 95.50  
-------------------------------------------------------------------------
```

---

## 🛡️ Error Handling
- **Duplicate ID**: If a user tries to add an ID that exists, the program warns the user without crashing.
- **Invalid Types**: Non-numeric age or marks are caught with helpful retry prompts.
- **Out of Range**: Marks outside `0-100` and ages outside `5-120` are rejected immediately.
- **Corrupt / Missing File**: Handled gracefully with fallback to empty state.
