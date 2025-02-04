from pymongo import MongoClient
from bson.objectid import ObjectId

# Step 1: Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI if needed
db = client["Courses"]
collection = db["Courses"]

# Function to Create a Course
def create_course():
    title = input("Enter course title: ")
    description = input("Enter course description: ")
    instructor = input("Enter instructor name: ")
    duration = int(input("Enter course duration (in days): "))

    course = {
        "title": title,
        "description": description,
        "instructor": instructor,
        "duration": duration
    }
    result = collection.insert_one(course)
    print(f"Course created successfully.")
    return result.inserted_id

# Function to Retrieve a Course (Admin sees IDs, General User does not)
def get_course(is_admin):
    course_id = input("Enter course ID to retrieve: ") if is_admin else None
    
    try:
        if is_admin:
            course = collection.find_one({"_id": ObjectId(course_id)})
        else:
            course_title = input("Enter course title to search: ")
            course = collection.find_one({"title": course_title})

        if course:
            print("\nCourse Details:")
            if is_admin:
                print(course)  # Admin sees everything
            else:
                print(f"Title: {course['title']}")
                print(f"Description: {course['description']}")
                print(f"Instructor: {course['instructor']}")
                print(f"Duration: {course['duration']} days")
        else:
            print("Course not found.")
    except Exception as e:
        print(f"Error: {e}")

# Function to Update a Course
def update_course():
    course_title = input("Enter course title to update: ")
    try:
        field = input("Enter field to update (description, instructor, duration): ").strip()
        if field not in ["description", "instructor", "duration"]:
            print("Invalid field. You can update only 'description', 'instructor', or 'duration'.")
            return

        new_value = input(f"Enter new value for {field}: ")
        if field == "duration":
            new_value = int(new_value)

        result = collection.update_one(
            {"title": course_title},
            {"$set": {field: new_value}}
        )
        if result.modified_count > 0:
            print("Course updated successfully.")
        else:
            print("No changes made or course not found.")
    except Exception as e:
        print(f"Error: {e}")

# Function to Delete a Course (Admin Only)
def delete_course():
    course_id = input("Enter course ID to delete: ")
    try:
        result = collection.delete_one({"_id": ObjectId(course_id)})
        if result.deleted_count > 0:
            print("Course deleted successfully.")
        else:
            print("Course not found.")
    except Exception as e:
        print(f"Error: {e}")

# Function to List All Courses (General Users don't see IDs)
def list_courses(is_admin):
    courses = collection.find()
    print("\nAll Courses:")
    for course in courses:
        if is_admin:
            print(course)  # Admin sees all details including ID
        else:
            print(f"- {course['title']} (Instructor: {course['instructor']}, Duration: {course['duration']} days)")

# User Authentication System
def main():
    print("Welcome to the Course Management System!")
    
    # Ask for user type
    user_type = input("Are you an Admin or General User? (admin/user): ").strip().lower()
    name = input("Enter your name: ").strip()  # Ask for user's name

    is_admin = user_type == "admin"

    if is_admin:
        password = input("Enter Admin Password: ")
        if password != "admin123":  # Set your own admin password
            print("Incorrect password! Exiting...")
            return

    print(f"\nHello {name}! 👋")
    print("Welcome to the Course Management Menu.")

    while True:
        print("\nCourse Management Menu:")
        print("1. Create a new course")
        print("2. Retrieve a course")
        print("3. Update a course")
        print("4. List all courses")
        
        if is_admin:
            print("5. Delete a course")
            print("6. Exit")
        else:
            print("5. Exit")

        choice = input(f"{name}, enter your choice: ")

        if choice == "1":
            create_course()
        elif choice == "2":
            get_course(is_admin)
        elif choice == "3":
            update_course()
        elif choice == "4":
            list_courses(is_admin)
        elif choice == "5" and is_admin:
            delete_course()
        elif choice == "5" and not is_admin or choice == "6":
            print(f"Goodbye, {name}! Have a great day! 😊")
            break
        else:
            print("Invalid choice, please try again.")

# Run the program
if __name__ == "__main__":
    main()
