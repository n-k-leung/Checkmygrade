import unittest
from unittest.mock import patch
import time
from checkmygrade import Student, Course, Professor  

class TestStudentRecords(unittest.TestCase):
    # test adding 1000 students
    def test_add_students(self):
        student = Student(filename="test_student.csv")
        
        # adding 1000 student records
        for i in range(1, 1001):
            email = f"student{i}@sjsu.edu"
            first_name = f"First{i}"
            last_name = f"Last{i}"
            course_id = f"DATA{200+i%100}"
            grade = "A" if i % 2 == 0 else "B"
            marks = 90 if i % 2 == 0 else 80
            
            self.assertTrue(student.add_new_student(email, first_name, last_name, course_id, grade, marks))
    
    # test deleting a student
    def test_delete_student(self):
        student = Student(filename="test_student.csv")
        student.add_new_student("news@gmail.com", "ne", "ws", "DATA200", "A", 90)
        self.assertTrue(student.delete_new_student("news@gmail.com"))
    
    # test modifying student records with input
    @patch('builtins.input', side_effect=["", "", "", "B", 80])
    def test_modify_student(self, input):
        student = Student(filename="test_student.csv")
        student.update_student_record("testing@gmail.com")
        modified_student = student.check_my_grades("testing@gmail.com")
        self.assertIsNotNone(modified_student)
        self.assertEqual(modified_student[4], "B")
        self.assertEqual(modified_student[5], 80)

    # test load data from CSV and search
    def test_load_and_search_students(self):
        start_time = time.time()
        student = Student(filename="test_student.csv")
        
        search_result = None
        current = student.student_list.head
        while current:
            if current.data[0] == "testing@gmail.com":  
                search_result = current.data
                print("Student from CSV file found")
                break
            current = current.next 

        self.assertIsNotNone(search_result)  
        print(f"Search took {time.time() - start_time} seconds.") 

    # test sorting student records (ascending by email)
    def test_sort_students_by_email(self):
        student = Student(filename="test_student.csv")
        start_time = time.time()
        sorted_students = student.sort_students(sort_by="email", reverse=False)

        self.assertTrue(sorted_students[0][0] <= sorted_students[-1][0])
        print(f"Sorting by ascending email took {time.time() - start_time} seconds.")

    # test sorting student records (descending by marks)
    def test_sort_students_by_marks(self):
        student = Student(filename="test_student.csv")
        start_time = time.time()
        sorted_students = student.sort_students(sort_by="marks", reverse=True)

        self.assertTrue(sorted_students[0][5] >= sorted_students[-1][5])
        print(f"Sorting by descending marks took {time.time() - start_time} seconds.")

class TestCourseOperations(unittest.TestCase):
    # test adding a course
    def test_add_course(self):
        course = Course(filename="test_course.csv")
        self.assertTrue(course.add_new_course("DATA203", "newnew", "descriptions"))
    
    # test deleting a course
    def test_delete_course(self):
        course = Course(filename="test_course.csv")
        course.add_new_course("DATA204", "aaaaaaa", "aaaaaaaaaaaaa")
        self.assertTrue(course.delete_new_course("DATA204"))
    
    # test modifying a course with input
    @patch('builtins.input', side_effect=["", "", "TBD"])
    def test_modify_course(self, input):
        course = Course(filename="test_course.csv")
        course.add_new_course("DATA206", "labs", "N/A")
        course.modify_course_details("DATA206")
        modified_course = course.get_course_details("DATA206")
        self.assertEqual(modified_course[2], "TBD")

class TestProfessorOperations(unittest.TestCase):
    # test adding a professor
    def test_add_professor(self):
        professor = Professor(filename="test_professor.csv")
        self.assertTrue(professor.add_new_professor("pprroff@example.com", "p", "r", "Senior", "DATA204"))

    # test modifying a professor with input
    @patch('builtins.input', side_effect=["", "", "Senior", ""])
    def test_modify_professor(self, input):
        professor = Professor(filename="test_professor.csv")
        professor.add_new_professor("newhire@sjsu.edu", "New", "Hire", "Junior", "DATA255")
        professor.modify_professor_details("newhire@sjsu.edu")
        modified_professor = professor.get_professor_details("newhire@sjsu.edu")
        self.assertEqual(modified_professor[3], "Senior")
     
    # test deleting a professor
    def test_delete_professor(self):
        professor = Professor(filename="test_professor.csv")
        professor.add_new_professor("pprroff@sjsu.edu", "p", "r", "Junior", "DATA204")
        self.assertTrue(professor.delete_new_professor("pprroff@sjsu.edu"))
    
    

if __name__ == "__main__":
    unittest.main()

# Student added successfully
# Student added successfully
# Student added successfully
# Student added successfully
# .Student added successfully
# Student deleted successfully
# .Student from CSV file found
# Search took 0.014000654220581055 seconds.
# .Grade in : B
# Search time: 0.0 seconds
# .Students sorted successfully by email (ascending order).
# Sorting by ascending email took 0.007998228073120117 seconds.
# .Students sorted successfully by marks (descending order).
# Sorting by descending marks took 0.009001016616821289 seconds.
# .
# ======================================================================
# ERROR: test_modify_course (__main__.TestCourseOperations.test_modify_course)
# ----------------------------------------------------------------------
# Traceback (most recent call last):
#   File "C:\msys64\ucrt64\lib\python3.12\unittest\mock.py", line 1395, in patched
#     return func(*newargs, **newkeywargs)
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "c:/Users/natal/Documents/Fall 2025/data 200/lab/lab1/testing.py", line 93, in test_modify_course
#     self.assertEqual(modified_course[2], "TBD")
#                      ~~~~~~~~~~~~~~~^^^
# TypeError: 'NoneType' object is not subscriptable

# ----------------------------------------------------------------------
# Ran 12 tests in 0.881s

# FAILED (errors=1)
