import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def register(username, password):
    try:
        response = requests.post(f"{API_URL}/register/", json={"username": username, "password": password})
        if response.status_code == 200:
            st.success("🎉 Registration successful! Please log in.")
        else:
            st.error(f"Registration failed: {response.json().get('detail')}")
    except requests.exceptions.ConnectionError:
        st.error("Connection failed. Is the API server running?")

def register_page():
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.subheader("📝 Register")

    username = st.text_input("👤 Username", placeholder="Enter a username", key="register_username")
    password = st.text_input("🔒 Password", type="password", placeholder="Enter a password", key="register_password")

    if st.button("📝 Register", use_container_width=True):
        if username and password:
            register(username, password)
        else:
            st.warning("Please enter both username and password.")
    
    st.markdown('</div>', unsafe_allow_html=True)
