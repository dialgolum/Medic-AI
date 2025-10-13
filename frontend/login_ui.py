import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def login(username, password):
    try:
        response = requests.post(f"{API_URL}/token", json={"username": username, "password": password})
        if response.status_code == 200:
            st.session_state.token = response.json()['access_token']
            st.session_state.username = username
            st.success("✅ Login successful! Redirecting...")
            st.rerun()
        else:
            st.error(f"Login failed: {response.json().get('detail')}")
    except requests.exceptions.ConnectionError:
        st.error("Connection failed. Is the API server running?")

def login_page():
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.subheader("🔐 Login")

    username = st.text_input("👤 Username", placeholder="Enter your username", key="login_username")
    password = st.text_input("🔒 Password", type="password", placeholder="Enter your password", key="login_password")

    if st.button("🚀 Login", use_container_width=True):
        if username and password:
            login(username, password)
        else:
            st.warning("Please enter both username and password.")
    
    st.markdown('</div>', unsafe_allow_html=True)
