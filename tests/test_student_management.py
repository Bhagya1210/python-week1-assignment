"""Unit tests for Student Management System."""

from __future__ import annotations
import json
import os
import shutil
import sys
import tempfile
import unittest

# Ensure student_management_system directory is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SMS_DIR = os.path.join(PROJECT_ROOT, "student_management_system")
if SMS_DIR not in sys.path:
    sys.path.insert(0, SMS_DIR)

from models import Student, StudentManager


class TestStudentModel(unittest.TestCase):
    """Test Student entity model initialization and serialization."""

    def test_student_initialization(self) -> None:
        student = Student("101", "Neha", 20, "Python", 91.0)
        self.assertEqual(student.student_id, "101")
        self.assertEqual(student.name, "Neha")
        self.assertEqual(student.age, 20)
        self.assertEqual(student.course, "Python")
        self.assertEqual(student.marks, 91.0)

    def test_to_dict_and_from_dict(self) -> None:
        original = Student("102", "Arjun", 21, "Data Science", 85.5)
        data = original.to_dict()
        reconstructed = Student.from_dict(data)

        self.assertEqual(reconstructed.student_id, original.student_id)
        self.assertEqual(reconstructed.name, original.name)
        self.assertEqual(reconstructed.age, original.age)
        self.assertEqual(reconstructed.course, original.course)
        self.assertEqual(reconstructed.marks, original.marks)

    def test_string_representation(self) -> None:
        student = Student("101", "Neha", 20, "Python", 91.0)
        expected = "ID: 101 | Name: Neha | Age: 20 | Course: Python | Marks: 91.0"
        self.assertEqual(str(student), expected)


class TestStudentManagerCRUD(unittest.TestCase):
    """Test CRUD, search, sorting, and reporting logic in StudentManager."""

    def setUp(self) -> None:
        self.manager = StudentManager()
        self.s1 = Student("101", "Neha", 20, "Python", 91.0)
        self.s2 = Student("102", "Arjun", 21, "Data Science", 85.0)
        self.s3 = Student("103", "Ravi", 22, "Python", 95.0)
        self.manager.add_student(self.s1)
        self.manager.add_student(self.s2)
        self.manager.add_student(self.s3)

    def test_add_student_success(self) -> None:
        s4 = Student("104", "Priya", 20, "Web Dev", 92.0)
        success, msg = self.manager.add_student(s4)
        self.assertTrue(success)
        self.assertEqual(len(self.manager.get_all_students()), 4)

    def test_prevent_duplicate_student_id(self) -> None:
        duplicate = Student("101", "Duplicate Neha", 22, "Java", 70.0)
        success, msg = self.manager.add_student(duplicate)
        self.assertFalse(success)
        self.assertIn("already exists", msg)
        self.assertEqual(len(self.manager.get_all_students()), 3)

    def test_search_by_id(self) -> None:
        found = self.manager.search_by_id("102")
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "Arjun")  # type: ignore[union-attr]

        not_found = self.manager.search_by_id("999")
        self.assertIsNone(not_found)

    def test_search_by_name(self) -> None:
        results = self.manager.search_by_name("neha")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].student_id, "101")

        partial = self.manager.search_by_name("a")
        # Neha, Arjun, Ravi all contain 'a'
        self.assertEqual(len(partial), 3)

        empty_query = self.manager.search_by_name("")
        self.assertEqual(empty_query, [])

    def test_update_student(self) -> None:
        success, msg = self.manager.update_student(
            "101",
            name="Neha Sharma",
            marks=94.5,
        )
        self.assertTrue(success)
        updated = self.manager.search_by_id("101")
        self.assertIsNotNone(updated)
        self.assertEqual(updated.name, "Neha Sharma")  # type: ignore[union-attr]
        self.assertEqual(updated.marks, 94.5)  # type: ignore[union-attr]
        self.assertEqual(updated.age, 20)  # type: ignore[union-attr]

        fail_update, _ = self.manager.update_student("999", name="Ghost")
        self.assertFalse(fail_update)

    def test_delete_student(self) -> None:
        success, msg = self.manager.delete_student("102")
        self.assertTrue(success)
        self.assertEqual(len(self.manager.get_all_students()), 2)
        self.assertIsNone(self.manager.search_by_id("102"))

        fail_delete, _ = self.manager.delete_student("999")
        self.assertFalse(fail_delete)

    def test_sort_students_by_name(self) -> None:
        sorted_asc = self.manager.sort_students(by="name", reverse=False)
        names_asc = [s.name for s in sorted_asc]
        self.assertEqual(names_asc, ["Arjun", "Neha", "Ravi"])

        sorted_desc = self.manager.sort_students(by="name", reverse=True)
        names_desc = [s.name for s in sorted_desc]
        self.assertEqual(names_desc, ["Ravi", "Neha", "Arjun"])

    def test_sort_students_by_marks(self) -> None:
        sorted_marks = self.manager.sort_students(by="marks", reverse=True)
        marks_desc = [s.marks for s in sorted_marks]
        self.assertEqual(marks_desc, [95.0, 91.0, 85.0])

    def test_calculate_average_marks(self) -> None:
        # (91.0 + 85.0 + 95.0) / 3 = 271 / 3 = 90.33
        avg = self.manager.calculate_average_marks()
        self.assertAlmostEqual(avg, 90.33, places=2)

        empty_manager = StudentManager()
        self.assertEqual(empty_manager.calculate_average_marks(), 0.0)

    def test_get_top_performer(self) -> None:
        top_list = self.manager.get_top_performer()
        self.assertEqual(len(top_list), 1)
        self.assertEqual(top_list[0].student_id, "103")
        self.assertEqual(top_list[0].marks, 95.0)


class TestStudentManagerPersistence(unittest.TestCase):
    """Test JSON file save and reload operations."""

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp()
        self.json_path = os.path.join(self.test_dir, "test_students.json")

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_save_and_load_json(self) -> None:
        manager1 = StudentManager()
        manager1.add_student(Student("101", "Neha", 20, "Python", 91.0))
        manager1.add_student(Student("102", "Arjun", 21, "Data Science", 85.0))

        save_ok, _ = manager1.save_to_json(self.json_path)
        self.assertTrue(save_ok)
        self.assertTrue(os.path.exists(self.json_path))

        manager2 = StudentManager()
        load_ok, _ = manager2.load_from_json(self.json_path)
        self.assertTrue(load_ok)
        self.assertEqual(len(manager2.get_all_students()), 2)
        loaded_neha = manager2.search_by_id("101")
        self.assertIsNotNone(loaded_neha)
        self.assertEqual(loaded_neha.name, "Neha")  # type: ignore[union-attr]

    def test_load_nonexistent_file(self) -> None:
        manager = StudentManager()
        non_existent = os.path.join(self.test_dir, "missing.json")
        ok, msg = manager.load_from_json(non_existent)
        self.assertFalse(ok)
        self.assertEqual(len(manager.get_all_students()), 0)


if __name__ == "__main__":
    unittest.main()
