from pymongo import MongoClient
from bson.objectid import ObjectId

# Step 1: Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI if remote
db = client["Courses"]
collection = db["Courses"]

# Step 2: Insert a Document
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
    print(f"Course created with ID: {result.inserted_id}")
    return result.inserted_id

# Step 3: Retrieve a Document
def get_course():
    course_id = input("Enter course ID to retrieve: ")
    try:
        course = collection.find_one({"_id": ObjectId(course_id)})
        if course:
            print("Course found:", course)
        else:
            print("Course not found.")
    except Exception as e:
        print(f"Error: {e}")

# Step 4: Update a Document
def update_course():
    course_id = input("Enter course ID to update: ")
    try:
        field = input("Enter field to update (title, description, instructor, duration): ").strip()
        new_value = input(f"Enter new value for {field}: ")

        # Convert duration to int if updating duration
        if field == "duration":
            new_value = int(new_value)

        result = collection.update_one(
            {"_id": ObjectId(course_id)},
            {"$set": {field: new_value}}
        )
        if result.modified_count > 0:
            print("Course updated successfully.")
        else:
            print("No changes made or course not found.")
    except Exception as e:
        print(f"Error: {e}")

# Step 5: Delete a Document
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

# Step 6: List All Documents
def list_courses():
    courses = collection.find()
    for course in courses:
        print(course)

# User Menu
if __name__ == "__main__":
    while True:
        print("\nCourse Management System")
        print("1. Create a new course")
        print("2. Retrieve a course")
        print("3. Update a course")
        print("4. Delete a course")
        print("5. List all courses")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_course()
        elif choice == "2":
            get_course()
        elif choice == "3":
            update_course()
        elif choice == "4":
            delete_course()
        elif choice == "5":
            list_courses()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")
