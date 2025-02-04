from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb+srv://apatel2:AYUSH@cluster0.2oeoz.mongodb.net/?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true")
db = client["Courses"]
collection = db["Courses"]

# Root route
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
def create_course():
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
def get_course(course_id):
    try:
        course = collection.find_one({"_id": ObjectId(course_id)})
        if course:
            return dumps(course), 200
        else:
            return jsonify({"error": "Course not found"}), 404
    except Exception as e:
        return jsonify({"error": "Invalid ID format"}), 400

# Route to Update a Course
@app.route('/courses/<course_id>', methods=['PUT'])
def update_course(course_id):
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
def delete_course(course_id):
    if not is_admin(request):
        return jsonify({"error": "Unauthorized"}), 403

    try:
        result = collection.delete_one({"_id": ObjectId(course_id)})
        if result.deleted_count > 0:
            return jsonify({"message": "Course deleted successfully"}), 200
        else:
            return jsonify({"error": "Course not found"}), 404
    except Exception as e:
        return jsonify({"error": "Invalid course ID format"}), 400

# Route to List All Courses
@app.route('/courses', methods=['GET'])
def list_courses():
    courses = list(collection.find())
    if courses:
        return dumps(courses), 200
    else:
        return jsonify({"message": "No courses available"}), 200

if __name__ == '__main__':
    app.run(port=5001, debug=True)