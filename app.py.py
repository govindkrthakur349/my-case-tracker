import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="Live eCourts Portal", page_icon="⚖️", layout="centered")

st.markdown("### 🏛️ Live eCourts Portal Lookup")
st.write("Search cases instantly using the official government database framework.")

# Direct embedded iframe or quick navigation to the official eCourts CNR search
ecourts_search_url = "https://services.ecourts.gov.in/ecourtindia_v6/?p=home/index&app_token=default"

st.markdown(
    f"""
    <div style="text-align: center; padding: 20px;">
        <p>Click below to open the official portal search interface directly inside your workflow:</p>
        <a href="{ecourts_search_url}" target="_blank" style="background-color: #4CAF50; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 16px;">Open Live eCourts Search</a>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")
st.markdown("### 📋 Quick Court Links")
col1, col2 = st.columns(2)
with col1:
    st.markdown("[Supreme Court Portal](https://main.sci.gov.in/)")
    st.markdown("[Patna High Court](https://patnahighcourt.gov.in/)")
with col2:
    st.markdown("[Darbhanga District Court](https://districts.ecourts.gov.in/darbhanga)")
    st.markdown("[eCourts Services App Web](https://services.ecourts.gov.in/)")
