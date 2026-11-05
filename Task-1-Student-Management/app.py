"""
Task 1 - Student Management REST API (Flask + SQLite)

Endpoints
---------
GET    /students          -> list all students
GET    /students/<id>     -> get one student
POST   /students          -> add a student
PUT    /students/<id>     -> update a student
DELETE /students/<id>     -> delete a student
"""
import os
import re
import sqlite3

from flask import Flask, g, jsonify, request

DB_PATH = os.environ.get(
    "STUDENT_DB", os.path.join(os.path.dirname(os.path.abspath(__file__)), "students.db")
)

app = Flask(__name__)

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
FIELDS = ("name", "department", "email")


# --------------------------------------------------------------------------
# Database helpers
# --------------------------------------------------------------------------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT NOT NULL,
                department TEXT NOT NULL,
                email      TEXT NOT NULL UNIQUE
            )
            """
        )


def row_to_dict(row):
    return {k: row[k] for k in row.keys()}


def validate(data, require_all=True):
    """Return (clean_dict, error_message)."""
    if not isinstance(data, dict):
        return None, "Request body must be a JSON object"
    clean = {}
    for field in FIELDS:
        value = data.get(field)
        if value is None:
            if require_all:
                return None, f"'{field}' is required"
            continue
        if not isinstance(value, str) or not value.strip():
            return None, f"'{field}' must be a non-empty string"
        clean[field] = value.strip()
    if "email" in clean and not EMAIL_RE.match(clean["email"]):
        return None, "'email' is not a valid email address"
    return clean, None


# --------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------
@app.get("/students")
def list_students():
    rows = get_db().execute("SELECT * FROM students ORDER BY id").fetchall()
    return jsonify([row_to_dict(r) for r in rows]), 200


@app.get("/students/<int:student_id>")
def get_student(student_id):
    row = get_db().execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if row is None:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(row_to_dict(row)), 200


@app.post("/students")
def add_student():
    data, err = validate(request.get_json(silent=True), require_all=True)
    if err:
        return jsonify({"error": err}), 400
    db = get_db()
    try:
        cur = db.execute(
            "INSERT INTO students (name, department, email) VALUES (?, ?, ?)",
            (data["name"], data["department"], data["email"]),
        )
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "A student with this email already exists"}), 409
    row = db.execute("SELECT * FROM students WHERE id = ?", (cur.lastrowid,)).fetchone()
    return jsonify(row_to_dict(row)), 201


@app.put("/students/<int:student_id>")
def update_student(student_id):
    data, err = validate(request.get_json(silent=True), require_all=False)
    if err:
        return jsonify({"error": err}), 400
    if not data:
        return jsonify({"error": "Provide at least one of: name, department, email"}), 400
    db = get_db()
    if db.execute("SELECT 1 FROM students WHERE id = ?", (student_id,)).fetchone() is None:
        return jsonify({"error": "Student not found"}), 404
    sets = ", ".join(f"{k} = ?" for k in data)  # keys come from the FIELDS whitelist only
    try:
        db.execute(f"UPDATE students SET {sets} WHERE id = ?", (*data.values(), student_id))
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "A student with this email already exists"}), 409
    row = db.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    return jsonify(row_to_dict(row)), 200


@app.delete("/students/<int:student_id>")
def delete_student(student_id):
    db = get_db()
    cur = db.execute("DELETE FROM students WHERE id = ?", (student_id,))
    db.commit()
    if cur.rowcount == 0:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({"message": f"Student {student_id} deleted"}), 200


@app.errorhandler(404)
def not_found(_e):
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(405)
def method_not_allowed(_e):
    return jsonify({"error": "Method not allowed"}), 405


init_db()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
