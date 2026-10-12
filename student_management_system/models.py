"""Student Management System - Data Models and Manager Class.

This module defines the Student class representing individual student records
and the StudentManager class handling CRUD operations, sorting, statistics,
and JSON file persistence.
"""

from __future__ import annotations
import json
import os
from typing import Any, Dict, List, Optional, Tuple


class Student:
    """Represents an individual student record.

    Attributes:
        student_id (str): Unique identifier for the student.
        name (str): Full name of the student.
        age (int): Age of the student (positive integer).
        course (str): Enrolled course or department.
        marks (float): Academic marks between 0.0 and 100.0.
    """

    def __init__(
        self,
        student_id: str,
        name: str,
        age: int,
        course: str,
        marks: float,
    ) -> None:
        self.student_id = str(student_id).strip()
        self.name = str(name).strip()
        self.age = int(age)
        self.course = str(course).strip()
        self.marks = round(float(marks), 2)

    def to_dict(self) -> Dict[str, Any]:
        """Convert Student instance to dictionary for JSON persistence."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "course": self.course,
            "marks": self.marks,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Student:
        """Create a Student instance from a dictionary."""
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            age=data["age"],
            course=data["course"],
            marks=data["marks"],
        )

    def __str__(self) -> str:
        """Return formatted string representation following WeIntern handbook style."""
        return (
            f"ID: {self.student_id} | Name: {self.name} | "
            f"Age: {self.age} | Course: {self.course} | Marks: {self.marks}"
        )

    def __repr__(self) -> str:
        return f"Student(id='{self.student_id}', name='{self.name}', marks={self.marks})"


class StudentManager:
    """Manages collections of students and provides CRUD operations and reporting."""

    def __init__(self) -> None:
        """Initialize with an empty list of students."""
        self.students: List[Student] = []

    def add_student(self, student: Student) -> Tuple[bool, str]:
        """Add a new student record.

        Args:
            student: Student object to add.

        Returns:
            Tuple of (success: bool, message: str).
        """
        if self.search_by_id(student.student_id) is not None:
            return False, f"Student with ID '{student.student_id}' already exists."

        self.students.append(student)
        return True, f"Student '{student.name}' added successfully."

    def get_all_students(self) -> List[Student]:
        """Return all student records."""
        return list(self.students)

    def search_by_id(self, student_id: str) -> Optional[Student]:
        """Search student by exact ID match."""
        target_id = str(student_id).strip().lower()
        for student in self.students:
            if student.student_id.lower() == target_id:
                return student
        return None

    def search_by_name(self, query: str) -> List[Student]:
        """Search students by partial or full name (case-insensitive)."""
        target_query = str(query).strip().lower()
        if not target_query:
            return []
        return [s for s in self.students if target_query in s.name.lower()]

    def update_student(
        self,
        student_id: str,
        name: Optional[str] = None,
        age: Optional[int] = None,
        course: Optional[str] = None,
        marks: Optional[float] = None,
    ) -> Tuple[bool, str]:
        """Update fields of an existing student.

        Returns:
            Tuple of (success: bool, message: str).
        """
        student = self.search_by_id(student_id)
        if not student:
            return False, f"Student with ID '{student_id}' not found."

        if name is not None and name.strip():
            student.name = name.strip()
        if age is not None:
            student.age = int(age)
        if course is not None and course.strip():
            student.course = course.strip()
        if marks is not None:
            student.marks = round(float(marks), 2)

        return True, f"Student ID '{student_id}' updated successfully."

    def delete_student(self, student_id: str) -> Tuple[bool, str]:
        """Delete student by ID.

        Returns:
            Tuple of (success: bool, message: str).
        """
        student = self.search_by_id(student_id)
        if not student:
            return False, f"Student with ID '{student_id}' not found."

        self.students.remove(student)
        return True, f"Student '{student.name}' (ID: {student_id}) deleted successfully."

    def sort_students(self, by: str = "name", reverse: bool = False) -> List[Student]:
        """Sort students by name or marks.

        Args:
            by: Criterion to sort by ('name' or 'marks').
            reverse: If True, sort in descending order.

        Returns:
            Sorted list of students.
        """
        if by.lower() == "marks":
            return sorted(self.students, key=lambda s: s.marks, reverse=reverse)
        # Default to name (case-insensitive)
        return sorted(self.students, key=lambda s: s.name.lower(), reverse=reverse)

    def calculate_average_marks(self) -> float:
        """Calculate average marks across all students.

        Returns:
            Average marks as float, or 0.0 if no students exist.
        """
        if not self.students:
            return 0.0
        total = sum(s.marks for s in self.students)
        return round(total / len(self.students), 2)

    def get_top_performer(self) -> List[Student]:
        """Return the student(s) with the highest marks.

        Returns:
            List of Student objects matching the highest marks.
        """
        if not self.students:
            return []
        highest = max(s.marks for s in self.students)
        return [s for s in self.students if s.marks == highest]

    def save_to_json(self, filepath: str) -> Tuple[bool, str]:
        """Save all student records to a JSON file.

        Args:
            filepath: Destination file path.

        Returns:
            Tuple of (success: bool, message: str).
        """
        try:
            dir_name = os.path.dirname(filepath)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)

            data = [s.to_dict() for s in self.students]
            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            return True, f"Saved {len(self.students)} records to '{filepath}'."
        except Exception as exc:
            return False, f"Error saving records to file: {exc}"

    def load_from_json(self, filepath: str) -> Tuple[bool, str]:
        """Load student records from a JSON file.

        Args:
            filepath: Source file path.

        Returns:
            Tuple of (success: bool, message: str).
        """
        if not os.path.exists(filepath):
            return False, f"File '{filepath}' does not exist. Starting with empty records."

        try:
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                return False, f"Invalid format in '{filepath}': expected a JSON list."

            loaded: List[Student] = []
            for item in data:
                if isinstance(item, dict) and "student_id" in item:
                    loaded.append(Student.from_dict(item))

            self.students = loaded
            return True, f"Loaded {len(self.students)} records from '{filepath}'."
        except json.JSONDecodeError:
            return False, f"File '{filepath}' contains invalid JSON. Starting with empty records."
        except Exception as exc:
            return False, f"Error loading records: {exc}"
