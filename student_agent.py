from flask import Flask, jsonify, request, render_template
import uuid
import os
import json
from datetime import datetime
from collections import Counter
import sqlite3
from flask_cors import CORS  # Step 1: Import CORS
import requests
import os
app = Flask(__name__)
CORS(app)

port = int(os.environ.get("PORT", 5001))
app.run(host="0.0.0.0", port=5001)


app = Flask(__name__)
CORS(app)  # Step 1: Enable CORS for cross-origin frontend API calls

AGENT_NAME = "student_agent"
PORT = 5001

DATA_DIR = os.path.join(os.getcwd(), "data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "student.db")

metadata = {
    "uuid": str(uuid.uuid4()),
    "agent_name": AGENT_NAME,
    "description": "Manages student profiles with CRUD endpoints",
    "version": "1.0"
}

DATA_LOG_PATH = "./student_agent_data_log.json"
METADATA_PATH = "./student_agent_metadata.json"

def save_metadata_to_json(metadata, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(metadata, f, indent=4)

save_metadata_to_json(metadata, METADATA_PATH)

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)  # Remove existing DB file to avoid uniqueness conflicts
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    with open('schema.sql') as f:
        cursor.executescript(f.read())
    with open('seed.sql') as f:
        cursor.executescript(f.read())
    conn.commit()
    conn.close()


def dict_from_row(row):
    d = dict(row)
    for field in ["education", "skills", "projects", "work", "links"]:
        value = d.get(field)
        # Check for None, empty, or invalid JSON before parsing
        if value is None or value == '' or value == 'null':
            d[field] = [] if field != "links" else {}
        else:
            try:
                d[field] = json.loads(value)
            except (json.JSONDecodeError, TypeError):
                # Fallback to empty structure if malformed
                d[field] = [] if field != "links" else {}
    return d


def get_student_profiles():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student_profile")
    rows = cursor.fetchall()
    conn.close()
    return [dict_from_row(row) for row in rows]

# Step 2: Serve dashboard at /central_app
@app.route('/central_app')
def central_dashboard():
    return render_template('student_dashboard.html')

from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "App is running!"


# Your existing CRUD API endpoints below...

@app.route("/student/create", methods=["POST"])
def create_profile():
    data = request.json
    student_id = str(uuid.uuid4())
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO student_profile (id, name, email, education, skills, projects, work, links)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        student_id,
        data.get("name"),
        data.get("email"),
        json.dumps(data.get("education", [])),
        json.dumps(data.get("skills", [])),
        json.dumps(data.get("projects", [])),
        json.dumps(data.get("work", [])),
        json.dumps(data.get("links", {}))
    ))
    conn.commit()
    conn.close()
    profile = {
        "id": student_id,
        "name": data.get("name"),
        "email": data.get("email"),
        "education": data.get("education", []),
        "skills": data.get("skills", []),
        "projects": data.get("projects", []),
        "work": data.get("work", []),
        "links": data.get("links", {})
    }
    return jsonify({"message": "Profile created", "profile": profile}), 201

@app.route("/student/<student_id>", methods=["GET"])
def get_profile(student_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student_profile WHERE id=?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Profile not found"}), 404
    return jsonify(dict_from_row(row)), 200

@app.route("/student/<student_id>", methods=["PUT"])
def update_profile(student_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student_profile WHERE id=?", (student_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "Profile not found"}), 404
    old_profile = dict_from_row(row)
    data = request.json
    new_profile = {
        "name": data.get("name", old_profile["name"]),
        "email": data.get("email", old_profile["email"]),
        "education": data.get("education", old_profile["education"]),
        "skills": data.get("skills", old_profile["skills"]),
        "projects": data.get("projects", old_profile["projects"]),
        "work": data.get("work", old_profile["work"]),
        "links": data.get("links", old_profile["links"]),
    }
    cursor.execute("""
        UPDATE student_profile SET name=?, email=?, education=?, skills=?, projects=?, work=?, links=?
        WHERE id=?
    """, (
        new_profile["name"],
        new_profile["email"],
        json.dumps(new_profile["education"]),
        json.dumps(new_profile["skills"]),
        json.dumps(new_profile["projects"]),
        json.dumps(new_profile["work"]),
        json.dumps(new_profile["links"]),
        student_id
    ))
    conn.commit()
    conn.close()
    new_profile["id"] = student_id
    return jsonify({"message": "Profile updated", "profile": new_profile}), 200

@app.route("/student/<student_id>", methods=["DELETE"])
def delete_profile(student_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student_profile WHERE id=?", (student_id,))
    if cursor.fetchone() is None:
        conn.close()
        return jsonify({"error": "Profile not found"}), 404
    cursor.execute("DELETE FROM student_profile WHERE id=?", (student_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Profile deleted"}), 200

@app.route("/student/all", methods=["GET"])
def list_profiles():
    profiles = get_student_profiles()
    return jsonify(profiles), 200

@app.route("/projects", methods=["GET"])
def get_projects_by_skill():
    skill = request.args.get("skill", "").lower()
    profiles = get_student_profiles()
    matched_projects = []
    for profile in profiles:
        if skill and any(skill == s.lower() for s in profile.get("skills", [])):
            matched_projects.extend(profile.get("projects", []))
    return jsonify(matched_projects), 200

@app.route("/skills/top", methods=["GET"])
def get_top_skills():
    profiles = get_student_profiles()
    all_skills = []
    for profile in profiles:
        all_skills.extend(profile.get("skills", []))
    from collections import Counter
    skill_counts = Counter(all_skills)
    top_skills = skill_counts.most_common(5)
    return jsonify(top_skills), 200

@app.route("/search", methods=["GET"])
def search_profiles():
    q = request.args.get("q", "").lower()
    profiles = get_student_profiles()
    results = []
    for profile in profiles:
        if (
            q in profile["name"].lower() or
            q in profile["email"].lower() or
            any(q in skill.lower() for skill in profile.get("skills", []))
        ):
            results.append(profile)
    return jsonify(results), 200

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5001)
