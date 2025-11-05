import csv
import time
import statistics
from linkedList import LinkedList
import hashlib

class Student:
    def __init__(self, filename = "student.csv"):
        self.filename = filename
        self.student_list = LinkedList()
        self.load_students()

    def load_students(self):
        with open(self.filename, mode="r", newline="") as file:
            reader = csv.reader(file)
            next(reader, None) # skips the header
            for row in reader:
                self.student_list.add_last(tuple(row))

    def save_students(self):
        with open(self.filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["email", "firstname", "lastname", "course_id", "grades", "marks"]) # rewrite the header
            current = self.student_list.head
            while current:
                writer.writerow(current.data)
                current = current.next

    def student_menu(self, email):
        self.professor = Professor()
        self.course = Course()
        self.grades = Grades()
        self.login = LoginUser()
        
        while True:
            print("\nStudent View--------------")
            print("\n1. Check Grades\n2. Check Marks \n3. Grade Report\n4. Course Details By Course\n5. Course Details By Professor\n6. Course Statistics\n7. Sort Students\n8. Change Password\n9. Logout\n10. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.check_my_grades(email)
            elif choice == "2":
                self.check_my_marks(email)
            elif choice == "3":
                self.grades.display_grade_report(email)
            elif choice == "4":
                course_id = input("Enter a course ID: ")
                self.course.display_course(course_id)
            elif choice == "5":
                email = input("Enter professor email: ")
                self.professor.show_course_details_by_professor(email)
            elif choice == "6":
                course_id = input("Enter a course ID: ")
                self.get_avg_median(course_id)
            elif choice == "7":
                sort_by = input("Sort by 'email', 'grade', or 'marks': ")
                order = input("Sort order ('A' for ascending, 'D' for descending): ")
                reverse = True if order == 'D' else False
                self.sort_students(sort_by, reverse)
            elif choice == "8":
                self.login.change_password(email)
            elif choice == "9":
                print("Logging out")
                break               
            elif choice == "10":
                print("Exiting")
                exit()
            else:
                print("Invalid input")

    def add_new_student(self, email, first_name, last_name, course_id, grade, marks):
        if not email or not course_id: 
            print("Email and course ID cannot be empty")
            return False
        
        current = self.student_list.head
        while current:
            #  check if student email is unique rather than using student id
             if current.data[0] == email:
                 print("Student with this email already exists")
                 return False
             current = current.next
        
        student = (email, first_name, last_name, course_id, grade, marks)
        self.student_list.add_last(student)
        self.save_students()
        print("Student added successfully")
        return True

    def delete_new_student(self, email):
        current = self.student_list.head
        while current:
            if current.data[0].strip().lower() == email.strip().lower():
                self.student_list.delete_node(current.data)
                self.save_students()
                login = LoginUser()
                login.delete_login_user(email)
                print("Student deleted successfully")
                return True
            current = current.next
        print("Student not found")
        return False

    def check_my_grades(self, email):
        start_time = time.time()
        current = self.student_list.head
        while current:
            # get rid of extra whitespace or it does not run
            if current.data[0].strip().lower() == email.strip().lower():
                print(f"Grade in {current.data[3]}: {current.data[4]}")
                # print timing of searching records
                print(f"Search time: {time.time() - start_time} seconds")
                return current.data
            current = current.next
        print("Student not found")
        return None
    
    def check_my_marks(self, email):
        start_time = time.time()
        current = self.student_list.head
        while current:
            if current.data[0].strip().lower() == email.strip().lower():
                print(f"Marks in {current.data[3]}: {current.data[5]}")
                # print timing of searching records
                print(f"Search time: {time.time() - start_time} seconds")
                return current.data
            current = current.next
        print("Student not found")
        return None

    def update_student_record(self, email):
        current = self.student_list.head
        while current:
            if current.data[0] == email:
                first = input("Enter new first name: ") 
                last = input("Enter new last name:  ")
                course_id = input("Enter new course ID: ")
                grade = input("Enter new grade: ")
                marks = input("Enter new marks: ") 
                current.data = (email, first, last, course_id, grade, marks)
                self.save_students()
                return True
            current = current.next
        print("Student not found")
        return None

    def get_avg_median(self, course_id):
        valid_course_ids = set()

        with open('course.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                valid_course_ids.add(row[0].strip())  
        if course_id not in valid_course_ids:
            print("Invalid course ID")
            return False

        start_time = time.time()
        total_marks = []
        self.course = Course()
        current = self.student_list.head

        while current:
            if current.data[3] == course_id:
                total_marks.append(int(current.data[5]))
            current = current.next
        if not total_marks:
            print("No scores")
            return False

        print(f"Average of Marks: {sum(total_marks) / len(total_marks)}")
        print(f"Median of Marks: {statistics.median(total_marks)}")
        # print timing of searching records
        print(f"Search time: {time.time() - start_time} seconds")

    def sort_students(self, sort_by="email", reverse=False):
        """Sort students by email, grade, or marks."""
        students = []
        current = self.student_list.head

        while current:
            students.append(current.data)
            current = current.next

        if sort_by == "email":
            sorted = lambda x: x[0].lower()
        elif sort_by == "grade":
            sorted = lambda x: x[4] 
        elif sort_by == "marks":
            sorted = lambda x: int(x[5]) if str(x[5]).isdigit() else 0
        else:
            print("Invalid sort key. Please choose 'email', 'grade', or 'marks'.")
            return students

        # use built in sort func
        students.sort(key=sorted, reverse=reverse)

        self.student_list = LinkedList()
        for student in students:
            self.student_list.add_last(student)

        print(f"Students sorted successfully by {sort_by} ({'descending' if reverse else 'ascending'} order)")
        self.save_students()
        return students
    
    def course_grade_report(self, course_id):
        valid_course_ids = set()
        with open('course.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader, None)  # skip header
            for row in reader:
                valid_course_ids.add(row[0].strip())

        if course_id not in valid_course_ids:
            print("Invalid course ID")
            return False

        current = self.student_list.head
        course_students = []
        while current:
            if current.data[3] == course_id:
                course_students.append(current.data)
            current = current.next

        if not course_students:
            print(f"No students found for course ID: {course_id}")
            return False

        print(f"Students in the Course {course_id}")
        print("---------------------------------------------------------")
        for student in course_students:
            email, first, last, _, grade, marks = student
            print(f"{email}     {first + ' ' + last}    {grade}     {marks}")

        # reports average and mean for every report\ -- student, course and prof
        marks_list = [int(s[5]) for s in course_students if s[5].isdigit()]
        if marks_list:
            average = sum(marks_list) / len(marks_list)
            median = statistics.median(marks_list)
            print(f"Average Marks: {average:.2f}")
            print(f"Median Marks: {median:.2f}")
            
        return True
    

class Course:
    def __init__(self, filename = "course.csv"):
        self.filename = filename
        self.course_list = LinkedList()
        self.load_courses()

    def load_courses(self):
        with open(self.filename, mode='r', newline="") as file:
            reader = csv.reader(file)
            next(reader, None) # skip the header when loading in so its not part of the data
            for row in reader:
                self.course_list.add_last(tuple(row))

    def save_courses(self):
        with open(self.filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["course_id", "course_name", "description"])
            current = self.course_list.head
            while current:
                writer.writerow(current.data)
                current = current.next  

    def get_course_details(self, course_id):
        current = self.course_list.head
        while current:
            if current.data[0] == course_id:
                return current.data
            current = current.next  
        return None
    
    def display_course(self, course_id):
        self.professor = Professor()
        current = self.course_list.head
        while current:
            if current.data[0] == course_id:
                prof_email = self.professor.get_professor_email(course_id)
                if prof_email:
                    self.professor.show_course_details_by_professor(prof_email)
                else:
                    print("Professor not found")
                return
            current = current.next
        print("Course not found")
    
    def add_new_course(self, course_id, course_name, description):
        if not course_id: 
            print("Course ID cannot be empty")
            return False
        
        current = self.course_list.head
        while current:
            #  checks if courseID is new because it is unique
             if current.data[0] == course_id:
                 print("Course with this ID already exists")
                 return False
             current = current.next      
        
        course = (course_id, course_name, description)
        self.course_list.add_last(course)
        self.save_courses()
        print("Course added successfully")
        return True

    def delete_new_course(self, course_id):
        current = self.course_list.head
        while current:
            if current.data[0] == course_id:
                self.course_list.delete_node(current.data)
                self.save_courses()
                print("Course deleted successfully")
                return True
            current = current.next
        print("Course not found")
        return False
    
    def modify_course_details(self, course_id):
        current = self.course_list.head
        while current:
            if current.data[0] == course_id:
                course_id = input("Enter new course ID: ")
                name = input("Enter new course name: ")
                description = input("Enter new course description: ")

                current.data = (course_id, name, description)
                self.save_courses()
                return True
            current = current.next
        print("Course not found")
        return None
    
   

class Professor:
    def __init__(self, filename = "professor.csv"):
        self.filename = filename
        self.professor_list = LinkedList()
        self.load_professors()

    def load_professors(self):
        with open(self.filename, mode='r', newline="") as file:
            reader = csv.reader(file)
            next(reader, None) # skip the header
            for row in reader:
                self.professor_list.add_last(tuple(row))

    def save_professors(self):
        with open(self.filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["email_address", "firstname", "lastname", "rank", "course_id"]) # rewrite the header
            current = self.professor_list.head
            while current:
                writer.writerow(current.data)
                current = current.next

    def professor_menu(self, email):
        self.student = Student()
        self.course = Course()
        self.grades = Grades()
        self.login = LoginUser()

        while True:
            print("\nProfessor View--------------")
            print("\n1. Add Student\n2. Delete Student\n3. Update Student Record\n4. Add Course\n5. Delete Course\n6. Update Course Record\n7. Display Course\n8. Add Professor\n9. Delete Professor\n10. Update Professor Record\n11. Change Password\n12. Course Grade Report\n13. Professor Grade Report\n14. Delete Student Course Grade\n15. Add Student Course Grade\n16. Update Student Course Grade\n17. Logout\n18. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                first = input("First Name: ")
                last = input("Last Name: ")
                email = input("Email: ")
                course = input("Course ID: ")
                grade = input("Grade: ")
                marks = input("Marks: ")
                self.student.add_new_student(email, first, last, course, grade, marks)
            elif choice == "2":
                email = input("Enter email of student to delete: ")
                self.student.delete_new_student(email)
            elif choice == "3":
                email = input("Enter email of student to modify: ")
                self.student.update_student_record(email)
            elif choice == "4":
                course_id = input("Enter a course ID to add: ")
                course_name = input("Enter name of the course: ")
                course_description = input("Enter description of the course: ")
                self.course.add_new_course(course_id, course_name, course_description)
            elif choice == "5":
                course_id = input("Enter a course ID to delete: ")
                self.course.delete_new_course(course_id)
            elif choice == "6":
                course_id = input("Enter a course ID to modify: ")
                self.course.modify_course_details(course_id)            
            elif choice == "7":
                course_id = input("Enter a course ID to get course details: ")
                self.course.display_course(course_id)
            elif choice == "8":
                email = input("Enter professor email: ")
                first = input("Enter first name: ")
                last = input("Enter last name: ")
                rank = input("Enter rank: ")
                course_id = input("Enter course ID: ")
                self.add_new_professor(email, first, last, rank, course_id)
            elif choice == "9":
                email = input("Enter professor email to delete: ")
                self.delete_new_professor(email)
            elif choice == "10":
                email = input("Enter professor email to modify: ")
                self.modify_professor_details(email)
            elif choice == "11":
                self.login.change_password(email)
            elif choice == "12":
                course_id = input("Enter a course ID to get course grade report: ")
                self.student.course_grade_report(course_id)
            elif choice == "13":
                prof_email = input("Enter your professor email to generate grade report: ")
                self.professor_grade_report(prof_email)
            elif choice == "14":
                email = input("Enter student email: ")
                course_id = input("Enter course ID: ")
                self.grades.delete_course_grade(email, course_id)
            elif choice == "15":
                email = input("Enter student email: ")
                firstname = input("Enter first name: ")
                lastname = input("Enter last name: ")
                course_id = input("Enter course ID: ")
                grade = input("Enter grade: ")
                marks = input("Enter marks: ")
                self.grades.add_course_grade(email, firstname, lastname, course_id, grade, marks)
            elif choice == "16":
                email = input("Enter student email: ")
                course_id = input("Enter a course ID: ")
                new_grade = input("Enter a new grade: ")
                new_marks = input("Enter a new marks: ")
                self.grades.update_course_grade(email, course_id, new_grade, new_marks)
            elif choice == "17":
                print("Logging out")
                break               
            elif choice == "18":
                print("Exiting")
                exit()
            else:
                print("Invalid choice")

    def add_new_professor(self, email_address, first_name, last_name, rank, course_id):
        if not email_address or not course_id: 
            print("Email and course ID cannot be empty")
            return False
        
        current = self.professor_list.head
        while current:
            #  checks if professor email is unique because does not use professorid
             if current.data[0] == email_address:
                 print("Professor with this email already exists")
                 return False
             current = current.next       
        
        professor = (email_address, first_name, last_name, rank, course_id)
        self.professor_list.add_last(professor)
        self.save_professors()
        print("Professor added successfully")
        return True

    def delete_new_professor(self, email):
        current = self.professor_list.head
        while current:
            if current.data[0] == email:
                self.professor_list.delete_node(current.data)
                self.save_professors()
                login = LoginUser()
                login.delete_login_user(email)
                print("Professor deleted successfully")
                return True
            current = current.next
        print("Professor not found")
        return False

    def modify_professor_details(self, email):
        current = self.professor_list.head
        while current:
            if current.data[0] == email:
                first = input("Enter new first name: ")
                last = input("Enter new last name:  ")
                rank = input("Enter new rank: ")
                course_id = input("Enter new course ID: ")

                current.data = (email, first, last, rank, course_id)
                self.save_professors()
                return True
            current = current.next
        print("Professor not found")
        return False

    def show_course_details_by_professor(self, email):
        self.course = Course()
        start_time = time.time()
        current = self.professor_list.head
        while current:
            if current.data[0] == email:
                course_id = current.data[4]
                course_details = self.course.get_course_details(course_id)
                if course_details:
                    print(f"{current.data[1]} {current.data[2]}'s ({current.data[3]}) {current.data[4]} details: {course_details[2]}")
                    # print timing of searching records
                    print(f"Search time: {time.time() - start_time} seconds")
                    return current.data
                else:
                    print("Course not found")
                    return None
            current = current.next
        print("Professor not found")
        return None

    def get_professor_details(self, email):
        current = self.professor_list.head
        while current:
            if current.data[0] == email:
                return current.data
            current = current.next  
        return None

    def professor_display(self, course):
        current = self.professor_list.head
        while current:
            if current.data[4] == course:
                print(f"Course: {current.data[4]}\nProfessor: {current.data[1]} {current.data[2]}")
                return current.data
            current = current.next

    def get_professor_email(self, course_id):
        current = self.professor_list.head
        while current:
            if current.data[4] == course_id:
                return current.data[0]  
            current = current.next
        return None
    
    def professor_grade_report(self, professor_email):
        current = self.professor_list.head
        professor_courses = []

        while current:
            if current.data[0] == professor_email:
                professor_courses.append(current.data[4])
            current = current.next

        if not professor_courses:
            print(f"No courses found for {professor_email}")
            return False

        student_obj = Student()
        start_time = time.time()
        exists = False

        for course_id in professor_courses:
            current = student_obj.student_list.head
            course_students = []

            while current:
                if current.data[3] == course_id:
                    course_students.append(current.data)
                current = current.next

            if not course_students:
                print(f"\nNo students enrolled in {course_id} course")
                continue

            exists = True
            print(f"Professor's Courses")
            print("---------------------------------------------------------")
            for s in course_students:
                email, first, last, _, grade, marks = s
                print(f"{email}     {first + ' ' + last}     {grade}     {marks}")

            markss= []  # initialize an empty list

            for s in course_students:
                marks_str = str(s[5])
                if marks_str.isdigit():
                    markss.append(int(marks_str))
            if markss:
                avg = sum(markss) / len(markss)
                med = statistics.median(markss)
                print(f"Average Marks: {avg}")
                print(f"Median Marks: {med}")

        if not exists:
            print("No students found in any of the professor's courses.")
        else:
            print(f"\nReport generated in {time.time() - start_time:.2f} seconds")

        return True

class Grades:
    def __init__(self, filename = "student.csv"):
        self.filename = filename
        self.grade_list = LinkedList()
        self.load_students()

    def load_students(self):
        with open("student.csv", mode="r", newline="") as file:
            reader = csv.reader(file)
            next(reader, None) # skip the header
            for row in reader:
                self.grade_list.add_last(tuple(row))

    def save_grades(self):
        with open(self.filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["email", "firstname", "lastname", "course_id", "grades", "marks"])
            current = self.grade_list.head
            while current:
                writer.writerow(current.data)
                current = current.next
        
    def display_grade_report(self, email):
        self.professor = Professor()
        start_time = time.time()
        current = self.grade_list.head
        while current:
            if current.data[0] == email:
                self.professor.professor_display(current.data[3])                
                print(f"Grade: {current.data[4]}\nMarks: {current.data[5]}")
                # print timing of searching records
                print(f"Search time: {time.time() - start_time} seconds")                
                return current.data
            current = current.next
        print("Student not found")

    def add_course_grade(self, email, firstname, lastname, course_id, grade, marks):
        if not email or not course_id:
            print("Email and course ID cannot be empty")
            return False

        current = self.grade_list.head
        while current:
            if current.data[0] == email and current.data[3] == course_id:
                print("Grade record for this student and course already exists.")
                return False
            current = current.next

        new_grade_record = (email, firstname, lastname, course_id, grade, marks)
        self.grade_list.add_last(new_grade_record)

        self.save_grades()

        print(f"Grade record added successfully for {firstname} {lastname} in course {course_id}.")
        return True

    def delete_course_grade(self, email, course_id):
        current = self.grade_list.head
        while current:
            if current.data[0] == email and current.data[3] == course_id:
                print(f"Deleted for {current.data[1]} {current.data[2]} in {course_id}")
                current.data = (current.data[0], current.data[1], current.data[2], current.data[3], "N/A", "0")
                self.save_grades()
                return True
            current = current.next
        print("Grade record not found")
        return False

    def update_course_grade(self, email, course_id, new_grade=None, new_marks=None):
        start_time = time.time()
        exists = False

        current = self.grade_list.head
        while current:
            if current.data[0] == email and current.data[3] == course_id:
                exists = True
                updated_record = (current.data[0], current.data[1], current.data[2], current.data[3], new_grade, new_marks)
                current.data = updated_record
                self.save_grades()
                print(f"Update time: {time.time() - start_time} seconds")
                return True
            current = current.next
        if not exists:
            print("Student or course does not exist")
            return False

class LoginUser:
    def __init__(self, filename="login.csv"):
        self.filename = filename
        self.login_list = LinkedList()
        self.load_login()
        self.current_user = None

    def load_login(self):
        with open(self.filename, mode="r", newline="") as file:
            reader = csv.reader(file)
            next(reader, None)  # skip the header
            for row in reader:
                self.login_list.add_last(tuple(row))

    def save_login(self):
        with open(self.filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["user_id", "password", "role"])  # rewrite the header
            current = self.login_list.head
            while current:
                writer.writerow(current.data)
                current = current.next

    def delete_login_user(self, email):
        current = self.login_list.head
        while current:
            if current.data[0] == email:
                self.login_list.delete_node(current.data)
                self.save_login()
                return True
            current = current.next
        return False

    def register(self):
        email = input("Enter email: ")
        password = input("Enter password: ")
        encrypted_password = self.encrypt(password)
        
        current = self.login_list.head
        while current:
            if current.data[0] == email:
                print("Email already registered")
                return False
            current = current.next

        role = input("Enter role (professor/student): ")

        if role == "student":
            firstname = input("Enter First Name: ")
            lastname = input("Enter Last Name: ")
            course_id = input("Enter Course ID: ")
            grades = input("Enter Grade: ")
            marks = input("Enter Marks: ")

            self.login_list.add_last((email, encrypted_password, "student"))
            self.save_login()

            # append to csv file with new info
            with open("student.csv", "a") as file:
                file.write(f"{email},{firstname},{lastname},{course_id},{grades},{marks}\n")
  
            student = Student()
            student.load_students()

        elif role == "professor":
            firstname = input("Enter first name: ")
            lastname = input("Enter last name: ")
            rank = input("Enter professor rank: ")
            course_id = input("Enter course ID: ")

            self.login_list.add_last((email, encrypted_password, "professor"))
            self.save_login()

            with open("professor.csv", "a") as file:
                file.write(f"{email},{firstname},{lastname},{rank},{course_id}\n")

            professor = Professor()
            professor.load_professors()

        else:
            print("Invalid role")
            return False

        print("Registration successful!")
        return True
    
    def login(self, student, professor):
        email = input("Enter email: ")
        password = input("Enter password: ")
        encrypted_password = self.encrypt(password)
        
        current = self.login_list.head
        while current:
            if current.data[0] == email and current.data[1] == encrypted_password:
                self.current_user = (email, current.data[2])
                print(f"Login successful! Currently logged in as {current.data[2]}")
                if current.data[2] == "student":
                    student.student_menu(email)
                if current.data[2] == "professor":
                    professor.professor_menu(email)
                return email, current.data[2]
            current = current.next
        print("Invalid email or password")
        return None, None

    def logout(self):
        if self.current_user:
            self.current_user = None
            print("User logged out successfully")
            self.load_login()
            return True
        return False

    def change_password(self, email):
        current = self.login_list.head
        while current:
            if current.data[0] == email:
                new_password = input("Enter new password: ")
                encrypted = self.encrypt(new_password)
                # update data as list since it was loaded as tuple
                updated = list(current.data)
                updated[1] = encrypted
                current.data = tuple(updated)
                self.save_login()
                # do not reload because then duplicates login csv file entries, must restart prog to work
                # self.load_login()
                print("Password changed successfully. Eexit program to complete update")
                return True
            current = current.next
        print("Email not found")
        return False

    def encrypt(self, text):
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def decrypt(self, text):
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def verify_password(self, stored, password):
        return self.encrypt(password) == stored


def main():
    student = Student()
    professor = Professor()
    login = LoginUser()

    while True:
        print("\nCheckMyGrade---------------")
        print("\n1. Login\n2. Register\n3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            login.login(student, professor)
        elif choice == "2":
            login.register()
        elif choice == "3":
            print("Exiting")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
