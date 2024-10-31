import json

class Person:
    def __init__(self, name:str, age:int, address:str):
        self.name = name
        self.age = age
        self.address = address

    def display_person_info(self): 
        print(f'Name:{self.name}\nAge:{self.age}\nAddress: {self.address}')
        
class Student(Person):
    def __init__(self, name, age, address, student_id):
        super().__init__(name, age, address)
        self.student_id = student_id
        self.grades = {}
        self.courses = []

    def add_grade(self, subject, grade):
        self.grades[subject] = grade
        print(f"Grade {grade} added for {self.name} in {subject}.")

    def enroll_course(self, course):
        if course not in self.courses:
            self.courses.append(course)
            print(f"{self.name} enrolled in {course}.")
        else:
            print(f"{self.name} is already enrolled in {course}.")

    def display_student_info(self):
        super().display_person_info()  
        print(f'ID:{self.student_id}\nEnrolled Courses: {", ".join(self.courses)}\nGrades: {self.grades}')
      
class Course:
    def __init__(self, course_name, course_code, instructor):
        self.course_name = course_name
        self.course_code = course_code
        self.instructor = instructor
        self.students = []

    def add_student(self, student):
        if student not in self.students:
            self.students.append(student)
        else:
            print(f"Student {student.name} is already enrolled in {self.course_name}.")

    def display_course_info(self): 
        print(f'Course Naem:{self.course_name}\nCourse Code:{self.course_code}\nInstructor:{self.instructor}\nEnrolled Students:{", ".join(student.name for student in self.students)}')
         
         
class StudentManagementSystem:
    def __init__(self):
        self.students = {}
        self.courses = {}

    def add_student(self):
        try: 
            name = input("Enter Name: ")
            age = int(input("Enter Age: ")) 
            if age <= 0: 
                print('Age must be positive.') 
                return
            address = input("Enter Address: ")
            student_id = input("Enter Student ID: ")
            if student_id in self.students:
                print("Student ID already exists.")
            else:
                student = Student(name, age, address, student_id)
                self.students[student_id] = student
                print(f"Student {name} (ID: {student_id}) added successfully.") 
        except Exception as error: 
            print(f"An error occurred: {error}")

    def add_course(self):
        try: 
            course_name = input("Enter Course Name: ")
            course_code = input("Enter Course Code: ")
            instructor = input("Enter Instructor Name: ")
            if course_code in self.courses:
                print("Course code already exists.")
            else:
                course = Course(course_name, course_code, instructor)
                self.courses[course_code] = course
                print(f"Course {course_name} (Code: {course_code}) created with instructor {instructor}.") 
        except Exception as error: 
            print(f"An error occurred: {error}")

    def enroll_student_in_course(self):
        try: 
            student_id = input("Enter Student ID: ")
            course_code = input("Enter Course Code: ")
            student = self.students.get(student_id)
            course = self.courses.get(course_code)
            if student and course:
                student.enroll_course(course.course_name)
                course.add_student(student) 
                print(f"Student {student.name} (ID:{student_id}) enrolled in {course.course_name} (Code:{course_code}).")
            else:
                print("Invalid student ID or course code!!") 
        except Exception as error: 
            print(f"An error occurred during enrollment: {error}")
        

    def add_grade_for_student(self):
        try: 
            student_id = input("Enter Student ID: ")
            course_code = input("Enter Course Code: ")
            grade = input("Enter Grade: ")
            student = self.students.get(student_id)
            course = self.courses.get(course_code)
            if student and course and course.course_name in student.courses:
                student.add_grade(course.course_name, grade)
            else:
                print("Student is not enrolled in the specified course or invalid IDs.")
        except Exception as error:
            print(f"An error occurred while adding grade: {error}!!")


    def display_student_details(self):
        try: 
            student_id = input("Enter Student ID: ")
            student = self.students.get(student_id)
            if student: 
                print('Student Informaiton: ')
                student.display_student_info()
            else:
                print("Student not found.")
        except Exception as error: 
             print(f"An error occurred while displaying student details: {error}!!")
    def display_course_details(self):
        try: 
            course_code = input("Enter Course Code: ")
            course = self.courses.get(course_code)
            if course: 
                print('Course Information: ') 
                course.display_course_info()
            else:
                print("Course not found.") 
        except Exception as error: 
            print(f"An error occurred while displaying course details: {error}!!")


    def save_data(self):
        data = {
            "students": {
                sid: {
                    "name": s.name,
                    "age": s.age,
                    "address": s.address,
                    "student_id": s.student_id,
                    "grades": s.grades,
                    "courses": s.courses,
                }
                for sid, s in self.students.items()
            },
            "courses": {
                cc: {
                    "course_name": c.course_name,
                    "course_code": c.course_code,
                    "instructor": c.instructor,
                    "students": [student.student_id for student in c.students]
                }
                for cc, c in self.courses.items()
            },
        }
        with open("student_data.json", "w") as f:
            json.dump(data, f, indent=4)
        print("All student and course data saved successfully.")

    def load_data(self):
        try:
            with open("student_data.json", "r") as f:
                data = json.load(f)

           
            self.students = {
                sid: Student(
                    info["name"], info["age"], info["address"], info["student_id"]
                )
                for sid, info in data["students"].items()
            }
            for sid, info in data["students"].items():
                self.students[sid].grades = info["grades"]
                self.students[sid].courses = info["courses"]

           
            self.courses = {
                cc: Course(
                    info["course_name"], info["course_code"], info["instructor"]
                )
                for cc, info in data["courses"].items()
            }
            for cc, info in data["courses"].items():
                self.courses[cc].students = [
                    self.students[sid] for sid in info["students"] if sid in self.students
                ]

            print("Data loaded successfully.")
        except FileNotFoundError:
            print("No saved data found.")

        
    def main_menu(self):
        try: 
            while True:
                print("\n==== Student Management System ====")
                menus = ['1. add new student', '2. add new course', '3. enroll student in course', '4. add grade for student', '5. disply student details', '6. display course details', '7. save data to file', '8. load data from file', '0. exit']    
                for  menu in menus: 
                    print(menu.title()) 
                
                 
                choice = input("Select Option: ")
                 
                if choice == '1':
                    self.add_student()
                elif choice == '2':
                    self.add_course()
                elif choice == '3':
                    self.enroll_student_in_course()
                elif choice == '4':
                    self.add_grade_for_student()
                elif choice == '5':
                    self.display_student_details()
                elif choice == '6':
                    self.display_course_details()
                elif choice == '7':
                    self.save_data()
                elif choice == '8':
                    self.load_data()
                elif choice == '0':
                    print("Exiting Student Management System. Goodbye!")
                    break
                else:
                    print("Invalid option. Please try again.") 
        except Exception as error:  
            print(f"An unexpected error occurred: {error}")
            
 
 
if __name__ == "__main__":
    student = StudentManagementSystem()
    student.main_menu()
