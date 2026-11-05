"""
Task 1 - Streamlit front-end for the Student Management API.
Run the Flask API first (python app.py), then:  streamlit run streamlit_app.py
"""
import os

import pandas as pd
import requests
import streamlit as st

API_URL = os.environ.get("API_URL", "http://127.0.0.1:5000").rstrip("/")
TIMEOUT = 5

st.set_page_config(page_title="Student Management", page_icon="🎓", layout="wide")
st.title("🎓 Student Management System")
st.caption(f"Streamlit front-end  →  Flask API at {API_URL}")


# --------------------------------------------------------------------------
# API helpers
# --------------------------------------------------------------------------
def api(method, path, **kwargs):
    """Call the API; return (ok, payload_or_error_message)."""
    try:
        resp = requests.request(method, f"{API_URL}{path}", timeout=TIMEOUT, **kwargs)
    except requests.exceptions.RequestException as exc:
        return False, f"Cannot reach the API ({exc.__class__.__name__}). Is Flask running?"
    try:
        body = resp.json()
    except ValueError:
        body = {}
    if resp.ok:
        return True, body
    return False, body.get("error", f"HTTP {resp.status_code}")


def fetch_students():
    ok, data = api("GET", "/students")
    if not ok:
        st.error(data)
        return []
    return data


def flash():
    """Show a one-time success message stored before st.rerun()."""
    msg = st.session_state.pop("flash", None)
    if msg:
        st.success(msg)


def done(message):
    st.session_state["flash"] = message
    st.rerun()  # refresh the displayed records after every successful operation


# --------------------------------------------------------------------------
# Page
# --------------------------------------------------------------------------
flash()
students = fetch_students()

st.subheader("All Students")
if students:
    df = pd.DataFrame(students).rename(
        columns={"id": "ID", "name": "Name", "department": "Department", "email": "Email"}
    )
    st.dataframe(df, width="stretch", hide_index=True)
    st.caption(f"{len(df)} student(s)")
else:
    st.info("No students yet. Add one using the form below.")

add_tab, edit_tab, delete_tab = st.tabs(["➕ Add Student", "✏️ Update Student", "🗑️ Delete Student"])

# ---- Add -------------------------------------------------------------------
with add_tab:
    with st.form("add_form", clear_on_submit=True):
        name = st.text_input("Name")
        department = st.text_input("Department")
        email = st.text_input("Email")
        if st.form_submit_button("Add student", type="primary"):
            ok, res = api("POST", "/students", json={"name": name, "department": department, "email": email})
            if ok:
                done(f"Added student '{res['name']}' (ID {res['id']}).")
            else:
                st.error(res)

# ---- Update ----------------------------------------------------------------
with edit_tab:
    if not students:
        st.info("Nothing to update yet.")
    else:
        by_id = {s["id"]: s for s in students}
        sel = st.selectbox(
            "Select a student",
            options=list(by_id),
            format_func=lambda i: f"{i} - {by_id[i]['name']}",
            key="edit_select",
        )
        cur = by_id[sel]
        # key includes the id so the fields reset when another student is selected
        with st.form(f"edit_form_{sel}"):
            new_name = st.text_input("Name", value=cur["name"])
            new_dept = st.text_input("Department", value=cur["department"])
            new_email = st.text_input("Email", value=cur["email"])
            if st.form_submit_button("Save changes", type="primary"):
                ok, res = api(
                    "PUT",
                    f"/students/{sel}",
                    json={"name": new_name, "department": new_dept, "email": new_email},
                )
                if ok:
                    done(f"Updated student ID {sel}.")
                else:
                    st.error(res)

# ---- Delete ----------------------------------------------------------------
with delete_tab:
    if not students:
        st.info("Nothing to delete.")
    else:
        by_id = {s["id"]: s for s in students}
        sel_del = st.selectbox(
            "Select a student to delete",
            options=list(by_id),
            format_func=lambda i: f"{i} - {by_id[i]['name']} ({by_id[i]['email']})",
            key="delete_select",
        )
        confirm = st.checkbox("I confirm I want to delete this student", key=f"confirm_{sel_del}")
        if st.button("Delete student", type="primary", disabled=not confirm):
            ok, res = api("DELETE", f"/students/{sel_del}")
            if ok:
                done(res.get("message", "Student deleted."))
            else:
                st.error(res)

st.divider()
if st.button("🔄 Refresh"):
    st.rerun()
