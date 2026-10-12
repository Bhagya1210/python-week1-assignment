"""Student Management System - Main Application Entrypoint.

Provides a clean, menu-driven console interface for managing student records
using Object-Oriented Programming (OOP) principles.
"""

from __future__ import annotations
import os
import sys

# Ensure local imports work regardless of working directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from models import Student, StudentManager
from utils import (
    display_header,
    display_students_table,
    get_confirmation,
    get_valid_float,
    get_valid_int,
    get_valid_menu_choice,
    get_valid_string,
)

DATA_FILE = os.path.join(CURRENT_DIR, "students.json")


def add_student_flow(manager: StudentManager) -> None:
    """Prompt user for student details and add record."""
    display_header("Add New Student")
    student_id = get_valid_string("Enter Student ID: ")

    if manager.search_by_id(student_id) is not None:
        print(f"[!] Error: A student with ID '{student_id}' already exists!")
        return

    name = get_valid_string("Enter Full Name: ")
    age = get_valid_int("Enter Age (5-120): ", min_val=5, max_val=120)
    course = get_valid_string("Enter Course / Stream: ")
    marks = get_valid_float("Enter Marks (0-100): ", min_val=0.0, max_val=100.0)

    student = Student(
        student_id=student_id,
        name=name,
        age=age,  # type: ignore[arg-type]
        course=course,
        marks=marks,  # type: ignore[arg-type]
    )

    success, message = manager.add_student(student)
    if success:
        print(f"[+] Success: {message}")
        manager.save_to_json(DATA_FILE)
    else:
        print(f"[!] Error: {message}")


def view_students_flow(manager: StudentManager) -> None:
    """Display all registered students."""
    display_header("Registered Student Records")
    students = manager.get_all_students()
    display_students_table(students)


def search_student_flow(manager: StudentManager) -> None:
    """Search for students by ID or Name."""
    display_header("Search Student")
    print("1. Search by Student ID")
    print("2. Search by Student Name")
    choice = get_valid_menu_choice("Enter choice (1-2): ", ["1", "2"])

    if choice == "1":
        student_id = get_valid_string("Enter Student ID to search: ")
        student = manager.search_by_id(student_id)
        if student:
            print("\n[+] Record Found:")
            display_students_table([student])
        else:
            print(f"[!] No student found with ID '{student_id}'.")
    else:
        query = get_valid_string("Enter Name or partial name: ")
        results = manager.search_by_name(query)
        if results:
            print(f"\n[+] Found {len(results)} matching record(s):")
            display_students_table(results)
        else:
            print(f"[!] No students found matching '{query}'.")


def update_student_flow(manager: StudentManager) -> None:
    """Modify details of an existing student record."""
    display_header("Update Student Details")
    student_id = get_valid_string("Enter Student ID to update: ")
    student = manager.search_by_id(student_id)

    if not student:
        print(f"[!] No student found with ID '{student_id}'.")
        return

    print("\nCurrent Student Details:")
    display_students_table([student])
    print("[Tip] Leave input blank to keep the current value.\n")

    new_name = get_valid_string(
        f"Enter new Name [{student.name}]: ",
        allow_empty=True,
    )
    new_age = get_valid_int(
        f"Enter new Age [{student.age}]: ",
        min_val=5,
        max_val=120,
        allow_empty=True,
    )
    new_course = get_valid_string(
        f"Enter new Course [{student.course}]: ",
        allow_empty=True,
    )
    new_marks = get_valid_float(
        f"Enter new Marks [{student.marks}]: ",
        min_val=0.0,
        max_val=100.0,
        allow_empty=True,
    )

    success, message = manager.update_student(
        student_id=student.student_id,
        name=new_name if new_name else None,
        age=new_age,
        course=new_course if new_course else None,
        marks=new_marks,
    )

    if success:
        print(f"[+] Success: {message}")
        manager.save_to_json(DATA_FILE)
    else:
        print(f"[!] Update failed: {message}")


def delete_student_flow(manager: StudentManager) -> None:
    """Delete a student record with confirmation."""
    display_header("Delete Student Record")
    student_id = get_valid_string("Enter Student ID to delete: ")
    student = manager.search_by_id(student_id)

    if not student:
        print(f"[!] No student found with ID '{student_id}'.")
        return

    print("\nRecord to be deleted:")
    display_students_table([student])

    if get_confirmation(f"Are you sure you want to permanently delete '{student.name}'?"):
        success, message = manager.delete_student(student_id)
        if success:
            print(f"[+] Success: {message}")
            manager.save_to_json(DATA_FILE)
        else:
            print(f"[!] Error: {message}")
    else:
        print("[-] Deletion cancelled.")


def sort_students_flow(manager: StudentManager) -> None:
    """Sort and display student records by name or marks."""
    display_header("Sort Student Records")
    print("1. Sort by Name (A -> Z)")
    print("2. Sort by Name (Z -> A)")
    print("3. Sort by Marks (Low -> High)")
    print("4. Sort by Marks (High -> Low)")
    choice = get_valid_menu_choice("Choose sorting option (1-4): ", ["1", "2", "3", "4"])

    if choice == "1":
        sorted_list = manager.sort_students(by="name", reverse=False)
    elif choice == "2":
        sorted_list = manager.sort_students(by="name", reverse=True)
    elif choice == "3":
        sorted_list = manager.sort_students(by="marks", reverse=False)
    else:
        sorted_list = manager.sort_students(by="marks", reverse=True)

    display_students_table(sorted_list)


def statistics_flow(manager: StudentManager) -> None:
    """Display overall academic performance statistics."""
    display_header("Academic Performance Statistics")
    students = manager.get_all_students()

    if not students:
        print("  [No student records available to calculate statistics.]")
        return

    avg_marks = manager.calculate_average_marks()
    top_performers = manager.get_top_performer()

    print(f"Total Enrolled Students: {len(students)}")
    print(f"Class Average Marks:     {avg_marks:.2f} / 100")
    print("\nTop Performing Student(s):")
    display_students_table(top_performers)


def print_main_menu() -> None:
    """Display the primary menu choices."""
    print("\n" + "=" * 40)
    print("   ===== Student Management System =====")
    print("=" * 40)
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Sort Students")
    print("7. Performance Statistics")
    print("8. Exit")
    print("=" * 40)


def main() -> None:
    """Main execution loop."""
    manager = StudentManager()

    # Automatically load data on startup
    if os.path.exists(DATA_FILE):
        success, msg = manager.load_from_json(DATA_FILE)
        print(f"[Info] {msg}")
    else:
        print("[Info] No existing database found. Starting with empty records.")

    valid_choices = ["1", "2", "3", "4", "5", "6", "7", "8"]

    while True:
        try:
            print_main_menu()
            choice = get_valid_menu_choice("Enter your choice (1-8): ", valid_choices)

            if choice == "1":
                add_student_flow(manager)
            elif choice == "2":
                view_students_flow(manager)
            elif choice == "3":
                search_student_flow(manager)
            elif choice == "4":
                update_student_flow(manager)
            elif choice == "5":
                delete_student_flow(manager)
            elif choice == "6":
                sort_students_flow(manager)
            elif choice == "7":
                statistics_flow(manager)
            elif choice == "8":
                manager.save_to_json(DATA_FILE)
                print("\n[+] Data saved successfully. Exiting Student Management System. Goodbye!")
                break

            input("\nPress [Enter] to return to the main menu...")
        except (KeyboardInterrupt, EOFError):
            print("\n\n[!] Interrupted. Saving changes before exit...")
            manager.save_to_json(DATA_FILE)
            print("[+] Saved. Goodbye!")
            break


if __name__ == "__main__":
    main()
