import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent / "backend"))

import streamlit as st
from dotenv import load_dotenv

# Import frontend pages
from frontend.login_ui import login_page
from frontend.register_ui import register_page
from frontend.main_ui import main_ui
from frontend.edit_profile_ui import edit_profile_ui

load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="Symptom Checker AI",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'token' not in st.session_state:
    st.session_state.token = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = "Login"  # Default 
if 'page' not in st.session_state:
    st.session_state.page = "main" 


# Global header
st.markdown('<h1 style="text-align:center; color:#1f77b4;">🩺 AI Symptom Checker</h1>', unsafe_allow_html=True)

# Navigation
if not st.session_state.token:
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h3>Welcome to AI-Powered Symptom Analysis</h3>
        <p>Get instant insights about your health concerns. Please login or register to continue.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        mode = st.radio("Choose Action", ["Login", "Register"], horizontal=True)
        st.session_state.auth_mode = mode

        if mode == "Login":
            login_page()
        else:
            register_page()

else:
    # If logged in, go to main app UI
    if st.session_state.page == "main":
        main_ui()
    elif st.session_state.page == "edit_profile":
            edit_profile_ui()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6c757d;'>
    <p>🩺 AI Symptom Checker | For informational purposes only | Always consult healthcare professionals for medical advice</p>
</div>
""", unsafe_allow_html=True)
