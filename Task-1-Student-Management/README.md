# Task 1 — Database-Driven Flask API with Streamlit Interface

A student management app: a Flask REST API backed by SQLite, and a Streamlit web UI that talks to it.

## Run

```bash
pip install -r requirements.txt
python app.py                      # terminal 1 -> API on http://127.0.0.1:5000
streamlit run streamlit_app.py     # terminal 2 -> UI  on http://localhost:8501
```

The SQLite file `students.db` and the `students` table are created automatically on first start.

## Database

```sql
CREATE TABLE students (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,   -- student ID
    name       TEXT NOT NULL,
    department TEXT NOT NULL,
    email      TEXT NOT NULL UNIQUE
);
```

## Endpoints

| Method | URL | Purpose | Success | Errors |
|---|---|---|---|---|
| GET | `/students` | all students | 200 | – |
| GET | `/students/<id>` | one student | 200 | 404 |
| POST | `/students` | add (`name`, `department`, `email`) | 201 | 400 invalid, 409 duplicate email |
| PUT | `/students/<id>` | update any of the fields | 200 | 400, 404, 409 |
| DELETE | `/students/<id>` | delete | 200 | 404 |

Run `./test_api.sh` (Git Bash / WSL / Linux / macOS) for a full cURL walkthrough.

## Streamlit features (all call the API; none touch the DB directly)

* Table of all students (refreshes after **every** successful add / update / delete)
* **Add** form (clears itself after success)
* **Update**: choose a student from a dropdown, the form is pre-filled, save changes
* **Delete**: choose a student, tick the confirmation box, delete
* Clear error messages if the API is down or validation fails

## Expected cURL output (excerpt)

```
POST /students      -> {"department":"Computer Science","email":"ali.khan@szabist.pk","id":1,"name":"Ali Khan"}   (201)
PUT  /students/1    -> {"department":"Artificial Intelligence", ... "id":1, ...}                                  (200)
DELETE /students/2  -> {"message":"Student 2 deleted"}                                                           (200)
GET  /students/999  -> {"error":"Student not found"}                                                              (404)
```
