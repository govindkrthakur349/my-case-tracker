import streamlit as st
import sqlite3

# --- PAGE CONFIG ---
st.set_page_config(page_title="Case Lookup & Tracker", page_icon="⚖️", layout="centered")

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('my_legal_cases.db', check_same_thread=False)
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

st.markdown("### 🔍 Instant Case Lookup")
st.write("Enter any 16-digit CNR number to search your records or add a new case.")

# --- SEARCH INPUT ---
search_cnr = st.text_input("Enter 16-Digit CNR Number to Search...", "").strip()

if search_cnr:
    conn = sqlite3.connect('my_legal_cases.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT cnr, case_title, next_date, stage, notes FROM cases WHERE cnr = ?", (search_cnr,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        # Case found in personal records! Display details right on the page.
        cnr, title, next_date, stage, notes = result
        st.success(f"Case Found in Your Records!")
        
        with st.container():
            st.markdown(f"### 📁 {title if title else cnr}")
            st.markdown(f"**🔢 CNR Number:** `{cnr}`")
            st.markdown(f"**📅 Next Hearing Date:** `{next_date}`")
            st.markdown(f"**⚖️ Current Stage:** `{stage}`")
            st.markdown(f"**📝 Case Notes & Details:**\n> {notes}")
            
            col1, col2 = st.columns(2)
            with col1:
                ecourts_url = f"https://services.ecourts.gov.in/"
                st.markdown(f"[🌐 Verify on eCourts Portal]({ecourts_url})", unsafe_allow_html=True)
            with col2:
                if st.button("🗑️ Delete This Case"):
                    conn = sqlite3.connect('my_legal_cases.db', check_same_thread=False)
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM cases WHERE cnr = ?", (cnr,))
                    conn.commit()
                    conn.close()
                    st.success("Case deleted successfully!")
                    st.rerun()
    else:
        # Case not found, offer quick registration form
        st.warning(f"CNR `{search_cnr}` is not in your saved records yet. Fill out the details below to save it:")
        
        with st.form("add_new_searched_case"):
            new_title = st.text_input("Case Title (e.g., Party A vs Party B)")
            new_date = st.text_input("Next Hearing Date (e.g., 15-May-2026)")
            new_stage = st.text_input("Current Stage (e.g., Arguments)")
            new_notes = st.text_area("Case Remarks / Notes")
            
            save_btn = st.form_submit_button("Save Case to Database")
            if save_btn:
                if len(search_cnr) == 16:
                    conn = sqlite3.connect('my_legal_cases.db', check_same_thread=False)
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT OR REPLACE INTO cases (cnr, case_title, next_date, stage, notes) 
                        VALUES (?, ?, ?, ?, ?)
                    """, (search_cnr, new_title, new_date, new_stage, new_notes))
                    conn.commit()
                    conn.close()
                    st.success("Case saved successfully! You can now search it anytime.")
                    st.rerun()
                else:
                    st.error("Please ensure the CNR number is 16 digits.")

st.markdown("---")
st.markdown("### 📋 All Saved Cases List")

# Display all cases for quick reference
conn = sqlite3.connect('my_legal_cases.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute("SELECT cnr, case_title, next_date FROM cases")
all_rows = cursor.fetchall()
conn.close()

if not all_rows:
    st.info("No cases saved yet.")
else:
    for row in all_rows:
        c_cnr, c_title, c_date = row
        st.text(f"• {c_title if c_title else 'Case'} | CNR: {c_cnr} | Next Date: {c_date}")
