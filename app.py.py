import streamlit as st
import sqlite3
from datetime import datetime

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('personal_cases.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cases (
            cnr TEXT PRIMARY KEY,
            case_title TEXT,
            next_date TEXT,
            stage TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- APP UI DESIGN ---
st.title("⚖️ My Legal Case Tracker")
st.write("A personal tool to track your case hearings and updates.")

# Sidebar for adding cases
st.sidebar.header("Add New Case")
input_cnr = st.sidebar.text_input("16-Digit CNR Number")
input_title = st.sidebar.text_input("Case Title (e.g., Name vs Name)")

if st.sidebar.button("Add Case"):
    if len(input_cnr) == 16:
        conn = sqlite3.connect('personal_cases.db', check_same_thread=False)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT OR REPLACE INTO cases (cnr, case_title, next_date, stage) VALUES (?, ?, ?, ?)",
                           (input_cnr, input_title, "Not Updated", "Pending"))
            conn.commit()
            st.sidebar.success(f"Added {input_cnr} successfully!")
        except Exception as e:
            st.sidebar.error(f"Error: {e}")
        finally:
            conn.close()
    else:
        st.sidebar.warning("Please enter a valid 16-digit CNR number.")

# --- MAIN DASHBOARD ---
st.subheader("Your Tracked Cases")

conn = sqlite3.connect('personal_cases.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute("SELECT cnr, case_title, next_date, stage FROM cases")
rows = cursor.fetchall()
conn.close()

if not rows:
    st.info("No cases added yet. Use the sidebar to add your first case.")
else:
    for row in rows:
        cnr, title, next_date, stage = row
        with st.expander(f"📁 {title if title else cnr}"):
            st.write(f"**CNR Number:** `{cnr}`")
            st.write(f"**Next Hearing Date:** {next_date}")
            st.write(f"**Current Stage:** {stage}")
            
            # Delete button for each case
            if st.button(f"Remove {cnr}", key=cnr):
                conn = sqlite3.connect('personal_cases.db', check_same_thread=False)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM cases WHERE cnr = ?", (cnr,))
                conn.commit()
                conn.close()
                st.rerun()