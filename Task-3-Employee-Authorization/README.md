# Task 3 — Employee Authentication and Authorization in Flask API

## Project Description

This project is an Employee Management REST API developed using Python, Flask, SQLite, and JWT authentication.

It demonstrates how authentication verifies a user's identity and authorization controls which operations a user can perform.

The application supports two roles: **Administrator** and **Employee**.

## Technologies Used

- Python
- Flask
- SQLite
- PyJWT
- REST API
- JSON
- Werkzeug Password Hashing

## Features

- User login using username and password
- JWT token generation after successful login
- Role-based access control (RBAC)
- Employee records stored in SQLite
- Administrator can perform all CRUD operations
- Employee can view records only
- Passwords stored as hashes
- Missing, invalid, and expired token handling

## Authentication vs Authorization

| Authentication | Authorization |
|---|---|
| Verifies user identity | Checks user permissions |
| Answers "Who are you?" | Answers "What can you do?" |
| Uses login credentials and JWT | Uses roles stored inside JWT |
| Invalid or missing token returns HTTP 401 | Insufficient permission returns HTTP 403 |

## User Roles and Permissions

| Operation | Administrator | Employee |
|---|---|---|
| Login | Allowed | Allowed |
| GET employees | Allowed | Allowed |
| GET employee by ID | Allowed | Allowed |
| POST employee | Allowed | Forbidden |
| PUT employee | Allowed | Forbidden |
| DELETE employee | Allowed | Forbidden |

## Demo Accounts

The application creates these demonstration accounts on first startup:

| Username | Password | Role |
|---|---|---|
| admin | Admin@123 | Administrator |
| employee1 | Employee@123 | Employee |

These credentials are for classroom demonstration only and must not be used in production.

## How to Run

**Step 1 — Install dependencies**

```bash
pip install -r requirements.txt
```

**Step 2 — Start Flask**

```bash
python app.py
```

The API runs at:

`http://127.0.0.1:5002`

The SQLite database and demonstration accounts are created automatically.

For a stable JWT signing secret across server restarts, configure the `SECRET_KEY` environment variable before starting Flask.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/login` | Authenticate and generate JWT |
| GET | `/employees` | View employee records |
| GET | `/employees/<id>` | View a specific employee |
| POST | `/employees` | Add an employee (Admin only) |
| PUT | `/employees/<id>` | Update an employee (Admin only) |
| DELETE | `/employees/<id>` | Delete an employee (Admin only) |

## JWT Authentication

After successful login, the server generates a signed JWT token.

The token contains the username, user ID, role, issue time, and expiry time.

JWT tokens are valid for **30 minutes**.

Protected endpoints require the following HTTP header:

```text
Authorization: Bearer <TOKEN>
```

## API Testing

The project includes `test_curl.sh`, a Bash script that demonstrates authentication and authorization checks.

The testing covers:

- Incorrect login credentials — HTTP 401
- Missing JWT token — HTTP 401
- Invalid JWT token — HTTP 401
- Employee GET request — HTTP 200
- Employee POST, PUT and DELETE — HTTP 403
- Administrator POST — HTTP 201
- Administrator GET and PUT — HTTP 200
- Administrator DELETE — HTTP 200

To run the Bash test script after starting Flask:

```bash
bash test_curl.sh
```

The script assumes a fresh demonstration database for its example employee IDs. If records already exist, adjust the IDs used in the tests.

## Security Features

- Password hashing using Werkzeug
- Signed JWT tokens using the HS256 algorithm
- Role-based authorization
- Restricted access to protected routes
- Input validation
- SQLite database for employee records

## Demonstration Video

[Watch Task 3 — Employee Authentication and Authorization Demonstration](https://drive.google.com/file/d/1f-ltHW52GaWSlFq9hIw5LBaV7HS0wNMi/view?usp=sharing)

## Conclusion

This project demonstrates secure API authentication and authorization using Flask, JWT, SQLite, and role-based permissions. Administrators can manage employee records, while normal employees have read-only access.
