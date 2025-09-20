import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent / "backend"))


import streamlit as st
import requests
from dotenv import load_dotenv
from backend.src.crew.agents import create_symptom_crew


load_dotenv()

st.set_page_config(page_title="Symptom Checker AI", layout="centered")

API_URL = "http://127.0.0.1:8000"

if 'token' not in st.session_state:
    st.session_state.token = None
if 'username' not in st.session_state:
    st.session_state.username = None

def login(username, password):
    try:
        response = requests.post(f"{API_URL}/token", json={"username": username, "password": password})
        if response.status_code == 200:
            st.session_state.token = response.json()['access_token']
            st.session_state.username = username
            return True
        else:
            st.error(f"Login failed: {response.json().get('detail')}")
            return False
    except requests.exceptions.ConnectionError:
        st.error("Connection failed. Is the API server running?")
        return False

def register(username, password):
    try:
        response = requests.post(f"{API_URL}/register/", json={"username": username, "password": password})
        if response.status_code == 200:
            st.success("Registration successful! Please log in.")
            return True
        else:
            st.error(f"Registration failed: {response.json().get('detail')}")
            return False
    except requests.exceptions.ConnectionError:
        st.error("Connection failed. Is the API server running?")
        return False

# --- UI ---
st.title("🩺 Agentic AI Symptom Checker")

if not st.session_state.token:
    st.sidebar.title("Login / Register")
    auth_choice = st.sidebar.radio("Choose Action", ["Login", "Register"])
    
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if auth_choice == "Login":
        if st.sidebar.button("Login"):
            if login(username, password):
                st.rerun()
    elif auth_choice == "Register":
        if st.sidebar.button("Register"):
            register(username, password)
else:
    st.sidebar.success(f"Logged in as **{st.session_state.username}**")
    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.username = None
        st.rerun()

    st.info("Describe your symptoms below. This tool is for informational purposes only and is not a substitute for professional medical advice.")
    user_input = st.text_area("How are you feeling?", height=150)

    if st.button("Analyze Symptoms"):
        if user_input:
            with st.spinner("Your AI agents are analyzing your symptoms..."):
                try:
                    symptom_crew = create_symptom_crew(user_input)
                    result = symptom_crew.kickoff()
                    st.markdown("---")
                    st.subheader("Analysis Results")
                    st.markdown(result)
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
        else:
            st.warning("Please describe your symptoms.")