import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def register(username, password, name, age, gender):
    try:
        payload = {
            "username": username,
            "password": password,
            "name": name,
            "age": age,
            "gender": gender
        }

        response = requests.post(f"{API_URL}/register/", json=payload)
        if response.status_code == 200:
            st.success("🎉 Registration successful! Please log in.")
        else:
            st.error(f"Registration failed: {response.json().get('detail')}")
    except requests.exceptions.ConnectionError:
        st.error("Connection failed. Is the API server running?")

def register_page():
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.subheader("📝 Register")

    name = st.text_input("🧑 Name", placeholder="Enter your full name", key="register_name")
    age = st.number_input("🎂 Age", min_value=1, max_value=120, step=1, key="register_age")
    gender = st.selectbox("⚧ Gender", ["Male", "Female", "Other"], key="register_gender")

    username = st.text_input("👤 Username", placeholder="Enter a username", key="register_username")
    password = st.text_input("🔒 Password", type="password", placeholder="Enter a password", key="register_password")

    if st.button("📝 Register", use_container_width=True):
        if username and password and name and age and gender:
            register(username, password, name, age, gender)
        else:
            st.warning("Please fill in all fields.")
    
    st.markdown('</div>', unsafe_allow_html=True)
