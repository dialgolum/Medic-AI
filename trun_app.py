import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent / "backend"))

import streamlit as st
import requests
from dotenv import load_dotenv
from backend.src.crew.agents import create_symptom_crew

load_dotenv()

# Enhanced page configuration
st.set_page_config(
    page_title="Symptom Checker AI",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="expanded"
)

API_URL = "http://127.0.0.1:8000"

# Initialize session state
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

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .symptom-input {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .result-box {
        background-color: #e8f4fd;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin-top: 20px;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
        margin: 20px 0;
    }
    .login-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #dee2e6;
    }
    .analyze-btn {
        background-color: #1f77b4;
        color: white;
        padding: 12px 30px;
        border: none;
        border-radius: 25px;
        font-size: 16px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Main app header
st.markdown('<h1 class="main-header">🩺 AI Symptom Checker</h1>', unsafe_allow_html=True)

# Authentication section
if not st.session_state.token:
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h3>Welcome to AI-Powered Symptom Analysis</h3>
        <p>Get instant insights about your health concerns. Please login or register to continue.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.subheader("🔐 Authentication")
        
        auth_choice = st.radio(
            "Choose Action",
            ["Login", "Register"],
            horizontal=True
        )
        
        username = st.text_input("👤 Username", placeholder="Enter your username")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
        
        if auth_choice == "Login":
            if st.button("🚀 Login", use_container_width=True):
                if username and password:
                    if login(username, password):
                        st.rerun()
                else:
                    st.warning("Please enter both username and password.")
        else:
            if st.button("📝 Register", use_container_width=True):
                if username and password:
                    register(username, password)
                else:
                    st.warning("Please enter both username and password.")
        
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # User is logged in
    st.sidebar.markdown(f"""
    <div style='background-color: #e8f4fd; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
        <h4>👋 Welcome back!</h4>
        <p><strong>{st.session_state.username}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.token = None
        st.session_state.username = None
        st.rerun()
    
    # Add quick tips in sidebar
    st.sidebar.markdown("""
    ### 💡 Tips for Better Analysis
    - Be specific about your symptoms
    - Mention duration and severity
    - Include any related factors
    - Note recent changes in health
    - Remember: This is not medical advice
    """)
    
    # Emergency notice
    st.sidebar.markdown("""
    <div style='background-color: #ffe6e6; padding: 15px; border-radius: 10px; border-left: 5px solid #dc3545;'>
        <h4>🚨 Emergency Notice</h4>
        <p>If you're experiencing a medical emergency, please call your local emergency number immediately.</p>
    </div>
    """, unsafe_allow_html=True)

    # Main content area
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h3>Describe Your Symptoms</h3>
        <p>Please provide detailed information about how you're feeling for the most accurate analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Warning box
    st.markdown("""
    <div class="warning-box">
        <h4>⚠️ Important Disclaimer</h4>
        <p>This AI symptom checker is for informational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Symptom input area
    st.markdown('<div class="symptom-input">', unsafe_allow_html=True)
    
    st.subheader("📝 Describe Your Symptoms")
    
    user_input = st.text_area(
        "How are you feeling?",
        height=200,
        placeholder="Please describe:\n• Your main symptoms\n• When they started\n• How severe they are\n• Any patterns you've noticed\n• Other relevant information",
        help="Be as detailed as possible for better analysis"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_clicked = st.button(
            "🔍 Analyze Symptoms", 
            use_container_width=True,
            type="primary",
            disabled=not user_input.strip()
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if analyze_clicked and user_input:
        with st.spinner("🧠 Your AI healthcare agents are analyzing your symptoms... This may take a moment."):
            try:
                symptom_crew = create_symptom_crew(user_input)
                result = symptom_crew.kickoff()
                
                # Display results in a nicely formatted box
                st.markdown("---")
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.subheader("📊 Analysis Results")
                st.markdown(result)
                
                # Add follow-up actions
                st.markdown("---")
                st.subheader("🎯 Recommended Next Steps")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.info("📋 **Monitor Symptoms**\n\nKeep track of any changes")
                with col2:
                    st.info("💊 **Self-Care**\n\nConsider rest and hydration")
                with col3:
                    st.info("🏥 **Professional Care**\n\nConsult a doctor if symptoms persist")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {e}")
                st.info("Please try again or contact support if the problem persists.")
    
    elif analyze_clicked and not user_input.strip():
        st.warning("⚠️ Please describe your symptoms before analyzing.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6c757d;'>
    <p>🩺 AI Symptom Checker | For informational purposes only | Always consult healthcare professionals for medical advice</p>
</div>
""", unsafe_allow_html=True)