import sys
import os

# Allow importing project app folder
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)


import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime


from app.web_register import register_student
from app.web_verify import verify_face


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Entrance Security System",
    page_icon="🔐",
    layout="wide"
)



# =========================
# DATABASE
# =========================

DB_PATH = "data/database.db"



def get_connection():

    return sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )



def get_students():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT
            student_id,
            name,
            department,
            year,
            section
        FROM students
        """,
        conn
    )

    conn.close()

    return df



def get_attendance():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT
            id,
            student_id,
            name,
            date,
            time,
            status
        FROM attendance
        ORDER BY id DESC
        """,
        conn
    )

    conn.close()

    return df




# =========================
# SIDEBAR
# =========================

st.sidebar.title(
    "🔐 AI Entrance System"
)


page = st.sidebar.radio(
    "Menu",
    [
        "Dashboard",
        "Register Student",
        "Verify Face"
    ]
)



# =========================
# REGISTER PAGE
# =========================

if page == "Register Student":

    register_student()

    st.stop()



# =========================
# VERIFY PAGE
# =========================

if page == "Verify Face":

    verify_face()

    st.stop()



# =========================
# DASHBOARD
# =========================


st.title(
    "🔐 AI Entrance Security System"
)


st.subheader(
    "Face Recognition Attendance Dashboard"
)



students = get_students()

attendance = get_attendance()



# =========================
# CARDS
# =========================

col1, col2, col3, col4 = st.columns(4)



with col1:

    st.metric(
        "Total Students",
        len(students)
    )



with col2:

    today = datetime.now().strftime(
        "%d-%m-%Y"
    )


    today_entries = len(
        attendance[
            attendance["date"] == today
        ]
    )


    st.metric(
        "Today's Entry",
        today_entries
    )



with col3:

    granted = len(
        attendance[
            attendance["status"] == "Granted"
        ]
    )


    st.metric(
        "Access Granted",
        granted
    )



with col4:

    denied = len(
        attendance[
            attendance["status"] == "Denied"
        ]
    )


    st.metric(
        "Access Denied",
        denied
    )



st.divider()



# =========================
# STUDENTS TABLE
# =========================

st.header(
    "👨‍🎓 Registered Students"
)


if len(students) > 0:

    st.dataframe(
        students,
        use_container_width=True
    )

else:

    st.warning(
        "No students registered"
    )



st.divider()



# =========================
# ATTENDANCE TABLE
# =========================

st.header(
    "📋 Attendance Records"
)



if len(attendance) > 0:

    st.dataframe(
        attendance,
        use_container_width=True
    )

else:

    st.warning(
        "No attendance records"
    )



st.caption(
    "Connected to AI Camera Recognition System"
)
