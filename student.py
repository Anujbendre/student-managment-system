import os
import json
import hashlib

STUDENT_FILE = "students.json"
ADMIN_FILE = "admin.json"

def load_data(file_path, default_data):
    if not os.path.exists(file_path):
        return default_data
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        print(f"Error: Failed to load {file_path}. Resetting data.")
        return default_data

def save_data(file_path, data):
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"Error saving data to {file_path}: {e}")

def setup_admin():
    admin_data = load_data(ADMIN_FILE, {})
    if "password" not in admin_data:
        print("No admin found. Setting up admin account.")
        password = input("Set Admin Password: ").strip()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        admin_data["password"] = hashed_password
        save_data(ADMIN_FILE, admin_data)
        print("Admin account created successfully!")

def verify_admin():
    admin_data = load_data(ADMIN_FILE, {})
    if "password" not in admin_data:
        setup_admin()
    password = input("Enter Admin Password: ").strip()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if hashed_password == admin_data.get("password"):
        print("Admin login successful!\n")
        return True
    else:
        print("Incorrect password! Access denied.")
        return False

def add_student(students):
    student_id = input("Enter student ID: ").strip()
    if any(student['id'] == student_id for student in students):
        print("Error: Student ID already exists!")
        return
    name = input("Enter student name: ").strip()
    course = input("Enter student course: ").strip()
    while True:
        try:
            marks = int(input("Enter student marks (numeric): ").strip())
            break
        except ValueError:
            print("Invalid marks! Please enter a number.")
    students.append({"id": student_id, "name": name, "course": course, "marks": marks})
    save_data(STUDENT_FILE, students)
    print("Student added successfully!\n")

def display_students(students):
    if not students:
        print("No students found.")
        return
    print("\nStudent Records:")
    print("-" * 40)
    for student in students:
        print(f"ID: {student['id']}, Name: {student['name']}, Course: {student['course']}, Marks: {student['marks']}")
    print("-" * 40)

def search_student(students):
    query = input("Enter student ID or Name to search: ").strip().lower()
    found_students = [student for student in students if student['id'] == query or student['name'].lower() == query]
    if found_students:
        print("\nSearch Results:")
        for student in found_students:
            print(f"ID: {student['id']}, Name: {student['name']}, Course: {student['course']}, Marks: {student['marks']}")
    else:
        print("Student not found!")

def delete_student(students):
    student_id = input("Enter student ID to delete: ").strip()
    student = next((student for student in students if student['id'] == student_id), None)
    if not student:
        print("Error: Student not found!")
        return
    confirm = input(f"Are you sure you want to delete {student['name']} (ID: {student_id})? (yes/no): ").strip().lower()
    if confirm == 'yes':
        students.remove(student)
        save_data(STUDENT_FILE, students)
        print("Student deleted successfully!\n")
    else:
        print("Deletion cancelled.")

def update_student(students):
    student_id = input("Enter student ID to update: ").strip()
    student = next((student for student in students if student['id'] == student_id), None)
    if not student:
        print("Error: Student not found!")
        return
    print("\nLeave blank to keep the existing value.")
    name = input(f"Enter new name ({student['name']}): ").strip() or student['name']
    course = input(f"Enter new course ({student['course']}): ").strip() or student['course']
    while True:
        marks_input = input(f"Enter new marks ({student['marks']}): ").strip()
        if not marks_input:
            marks = student['marks']
            break
        try:
            marks = int(marks_input)
            break
        except ValueError:
            print("Invalid marks! Please enter a number.")
    student.update({"name": name, "course": course, "marks": marks})
    save_data(STUDENT_FILE, students)
    print("Student updated successfully!\n")

def admin_menu(students):
    actions = {
        "1": add_student,
        "2": display_students,
        "3": search_student,
        "4": delete_student,
        "5": update_student,
        "6": lambda _: print("Logging out...")
    }
    while True:
        print("\nAdmin Menu")
        print("1. Add Student")
        print("2. Display Students")
        print("3. Search Student")
        print("4. Delete Student")
        print("5. Update Student")
        print("6. Logout")
        choice = input("Enter your choice: ").strip()
        action = actions.get(choice)
        if action:
            action(students)
            if choice == "6":
                break
        else:
            print("Invalid choice, please try again.")

def user_menu(students):
    actions = {
        "1": display_students,
        "2": search_student,
        "3": lambda _: print("Exiting...")
    }
    while True:
        print("\nUser Menu")
        print("1. Display Students")
        print("2. Search Student")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()
        action = actions.get(choice)
        if action:
            action(students)
            if choice == "3":
                break
        else:
            print("Invalid choice, please try again.")

def main():
    setup_admin()
    students = load_data(STUDENT_FILE, [])
    print("\nWelcome to the Student Management System")
    print("1. Login as Admin")
    print("2. Continue as User")
    role = input("Enter your choice: ").strip()
    if role == "1" and verify_admin():
        admin_menu(students)
    elif role == "2":
        user_menu(students)
    else:
        print("Invalid selection! Exiting...")

if __name__ == "__main__":
    main()
