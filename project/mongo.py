from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps

import sys
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask, request, jsonify
from bson.json_util import dumps

# Connect to MongoDB
client = MongoClient("mongodb+srv://apatel2:AYUSH@cluster0.2oeoz.mongodb.net/?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true")
db = client["Courses"]
collection = db["Courses"]

# ---------------------- Flask API ----------------------
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the Course Management API!",
        "endpoints": {
            "GET /courses": "List all courses",
            "POST /courses": "Create a new course (Admin only)",
            "GET /courses/<course_id>": "Retrieve a specific course",
            "PUT /courses/<course_id>": "Update a specific course (Admin only)",
            "DELETE /courses/<course_id>": "Delete a specific course (Admin only)"
        }
    })

# Helper function to check admin access
def is_admin(request):
    return request.headers.get('X-Admin-Password') == 'admin123'

# Route to Create a Course
@app.route('/courses', methods=['POST'])
def create_course_api():
    if not is_admin(request):
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    course = {
        "title": data.get("title"),
        "description": data.get("description"),
        "instructor": data.get("instructor"),
        "duration": data.get("duration")
    }
    result = collection.insert_one(course)
    return jsonify({"message": "Course created successfully", "course_id": str(result.inserted_id)}), 201

# Route to Retrieve a Course
@app.route('/courses/<course_id>', methods=['GET'])
def get_course_api(course_id):
    try:
        course = collection.find_one({"_id": ObjectId(course_id)})
        if course:
            return dumps(course), 200
        else:
            return jsonify({"error": "Course not found"}), 404
    except:
        return jsonify({"error": "Invalid ID format"}), 400

# Route to Update a Course
@app.route('/courses/<course_id>', methods=['PUT'])
def update_course_api(course_id):
    if not is_admin(request):
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    valid_fields = ["description", "instructor", "duration"]
    updates = {k: v for k, v in data.items() if k in valid_fields}

    if not updates:
        return jsonify({"error": "No valid fields to update"}), 400

    result = collection.update_one(
        {"_id": ObjectId(course_id)},
        {"$set": updates}
    )
    if result.modified_count > 0:
        return jsonify({"message": "Course updated successfully"}), 200
    else:
        return jsonify({"error": "No changes made or course not found"}), 404

# Route to Delete a Course
@app.route('/courses/<course_id>', methods=['DELETE'])
def delete_course_api(course_id):
    if not is_admin(request):
        return jsonify({"error": "Unauthorized"}), 403

    try:
        result = collection.delete_one({"_id": ObjectId(course_id)})
        if result.deleted_count > 0:
            return jsonify({"message": "Course deleted successfully"}), 200
        else:
            return jsonify({"error": "Course not found"}), 404
    except:
        return jsonify({"error": "Invalid course ID format"}), 400

# Route to List All Courses
@app.route('/courses', methods=['GET'])
def list_courses_api():
    courses = list(collection.find())
    if courses:
        return dumps(courses), 200
    else:
        return jsonify({"message": "No courses available"}), 200

# ---------------------- CLI Mode ----------------------
def create_course_cli():
    title = input("Enter course title: ")
    description = input("Enter course description: ")
    instructor = input("Enter instructor name: ")
    duration = input("Enter course duration (e.g., '30 days', '4 weeks'): ")  

    course = {
        "title": title,
        "description": description,
        "instructor": instructor,
        "duration": duration
    }
    collection.insert_one(course)
    print("Course created successfully.")

def list_courses_cli():
    courses = collection.find()
    print("\nAll Courses:")
    for course in courses:
        print(f"- {course['title']} (Instructor: {course['instructor']}, Duration: {course['duration']})")

def main():
    print("Welcome to the Course Management System!")
    user_type = input("Are you an Admin or General User? (admin/user): ").strip().lower()

    if user_type == "admin":
        password = input("Enter Admin Password: ")
        if password != "admin123":
            print("Incorrect password! Exiting...")
            return

    print("\nOptions:")
    print("1. Create Course")
    print("2. List Courses")
    print("3. Exit")

    while True:
        choice = input("Enter your choice: ")
        if choice == "1":
            create_course_cli()
        elif choice == "2":
            list_courses_cli()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

# ---------------------- Running Mode ----------------------
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "cli":
        main()  # Run CLI mode
    else:
        app.run(port=5001, debug=True)  # Run Flask server
