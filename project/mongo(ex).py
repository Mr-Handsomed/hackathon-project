from pymongo import MongoClient
from bson.objectid import ObjectId

# Connect to MongoDB
client = MongoClient("mongodb+srv://apatel2:AYUSH@cluster0.2oeoz.mongodb.net/?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true")

db = client["Courses"]
collection = db["Courses"]

# Function to Create a Course
def create_course():
    title = input("Enter course title: ")
    description = input("Enter course description: ")
    instructor = input("Enter instructor name: ")
    duration = input("Enter course duration (e.g., '30 days', '4 weeks'): ")  # Store as string

    course = {
        "title": title,
        "description": description,
        "instructor": instructor,
        "duration": duration
    }
    result = collection.insert_one(course)
    print("Course created successfully.")

# Function to Retrieve a Course
def get_course(is_admin):
    try:
        if is_admin:
            course_id = input("Enter course ID to retrieve: ")
            course = collection.find_one({"_id": ObjectId(course_id)})
        else:
            course_title = input("Enter course title to search: ")
            course = collection.find_one({"title": course_title})

        if course:
            print("\nCourse Details:")
            if is_admin:
                print(course)
            else:
                print(f"Title: {course['title']}")
                print(f"Description: {course['description']}")
                print(f"Instructor: {course['instructor']}")
                print(f"Duration: {course['duration']}")
        else:
            print("Course not found.")
    except Exception:
        print("Invalid ID format or course not found.")

# Function to Update a Course
def update_course():
    course_title = input("Enter course title to update: ")
    valid_fields = ["description", "instructor", "duration"]
    field = input("Enter field to update (description, instructor, duration): ").strip()

    if field not in valid_fields:
        print("Invalid field. Please choose from 'description', 'instructor', or 'duration'.")
        return

    new_value = input(f"Enter new value for {field}: ")

    result = collection.update_one(
        {"title": course_title},
        {"$set": {field: new_value}}
    )
    print("Course updated successfully." if result.modified_count > 0 else "No changes made or course not found.")

# Function to Delete a Course
def delete_course():
    try:
        course_id = input("Enter course ID to delete: ")
        result = collection.delete_one({"_id": ObjectId(course_id)})
        print("Course deleted successfully." if result.deleted_count > 0 else "Course not found.")
    except Exception:
        print("Invalid course ID format.")

# Function to List All Courses
def list_courses(is_admin):
    courses = collection.find()
    found_any = False
    print("\nAll Courses:")
    
    for course in courses:
        found_any = True
        if is_admin:
            print(course)
        else:
            print(f"- {course['title']} (Instructor: {course['instructor']}, Duration: {course['duration']})")

    if not found_any:
        print("No courses available.")

# Main Function
def main():
    print("Welcome to the Course Management System!")
    user_type = input("Are you an Admin or General User? (admin/user): ").strip().lower()
    name = input("Enter your name: ").strip()

    is_admin = user_type == "admin"
    if is_admin:
        password = input("Enter Admin Password: ")
        if password != "admin123":
            print("Incorrect password! Exiting...")
            return

    print(f"\nHello {name}! 👋")
    while True:
        print("\n1. Create Course\n2. Retrieve Course\n3. Update Course\n4. List Courses")
        if is_admin:
            print("5. Delete Course\n6. Exit")
        else:
            print("5. Exit")

        choice = input(f"{name}, enter your choice: ")

        if choice == "1": create_course()
        elif choice == "2": get_course(is_admin)
        elif choice == "3": update_course()
        elif choice == "4": list_courses(is_admin)
        elif choice == "5" and is_admin: delete_course()
        elif choice in ["5", "6"]: print(f"Goodbye, {name}!"); break
        else: print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
