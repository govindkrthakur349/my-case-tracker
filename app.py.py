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
            stage TEXT,
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- APP UI DESIGN ---
st.title("⚖️ My Legal Case Tracker")
st.write("Search, manage, and track your case details easily.")

# Sidebar for adding new cases
st.sidebar.header("➕ Add New Case")
input_cnr = st.sidebar.text_input("16-Digit CNR Number")
input_title = st.sidebar.text_input("Case Title (e.g., Client vs Party)")
input_notes = st.sidebar.text_area("Initial Notes / Remarks")

if st.sidebar.button("Save Case"):
    if len(input_cnr.strip()) == 16:
        conn = sqlite3.connect('personal_cases.db', check_same_thread=False)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO cases (cnr, case_title, next_date, stage, notes) 
                VALUES (?, ?, ?, ?, ?)
            """, (input_cnr.strip(), input_title, "Check eCourts", "Active", input_notes))
            conn.commit()
            st.sidebar.success("Case saved successfully!")
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Error: {e}")
        finally:
            conn.close()
    else:
        st.sidebar.warning("Please enter a valid 16-digit CNR number.")

# --- SEARCH & FILTER DASHBOARD ---
st.subheader("🔍 Search Your Cases")
search_query = st.text_input("Search by CNR Number or Title...", "").lower()

conn = sqlite3.connect('personal_cases.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute("SELECT cnr, case_title, next_date, stage, notes FROM cases")
rows = cursor.fetchall()
conn.close()

# Filter rows based on search input
filtered_rows = [row for row in rows if search_query in row[0].lower() or search_query in row[1].lower()]

if not rows:
    st.info("No cases saved yet. Use the sidebar to add your first case.")
elif not filtered_rows:
    st.warning("No matching cases found.")
else:
    st.write(f"Showing {len(filtered_rows)} case(s):")
    for row in filtered_rows:
        cnr, title, next_date, stage, notes = row
        display_title = title if title else cnr
        
        with st.expander(f"📁 {display_title} (CNR: {cnr})"):
            st.write(f"**Next Hearing Date:** {next_date}")
            st.write(f"**Current Stage:** {stage}")
            st.write(f"**Notes:** {notes if notes else 'None'}")
            
            # Action buttons
            col1, col2 = st.columns(2)
            with col1:
                # Direct link button to search this specific CNR on the official eCourts website
                ecourts_url = f"https://services.ecourts.gov.in/ecourtindia_v6/?p=home/index&app_token=default"
                st.markdown(f"[🌐 Open on eCourts Portal]({ecourts_url})", unsafe_allow_html=True)
            
            with col2:
                if st.button(f"🗑️ Delete Case", key=f"del_{cnr}"):
                    conn = sqlite3.connect('personal_cases.db', check_same_thread=False)
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM cases WHERE cnr = ?", (cnr,))
                    conn.commit()
                    conn.close()
                    st.rerun()
