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

# Premium CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%);
    }
    
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        animation: fadeInDown 0.8s ease-out;
    }
    
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.2rem;
        margin-bottom: 3rem;
        animation: fadeIn 1s ease-out;
    }
    
    .login-container {
        background: white;
        padding: 3rem;
        border-radius: 24px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .symptom-card {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.1);
        border: 2px solid #e8eef5;
        margin: 2rem 0;
        transition: all 0.3s ease;
    }
    
    .symptom-card:hover {
        box-shadow: 0 15px 50px rgba(102, 126, 234, 0.15);
        transform: translateY(-2px);
    }
    
    .result-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 2.5rem;
        border-radius: 20px;
        border-left: 6px solid #10b981;
        box-shadow: 0 10px 40px rgba(16, 185, 129, 0.1);
        margin-top: 2rem;
        animation: slideInUp 0.6s ease-out;
    }
    
    .warning-banner {
        background: linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%);
        padding: 1.5rem;
        border-radius: 16px;
        border-left: 6px solid #f59e0b;
        margin: 2rem 0;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.1);
    }
    
    .emergency-alert {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        padding: 1.5rem;
        border-radius: 16px;
        border-left: 6px solid #ef4444;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.15);
    }
    
    .user-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        text-align: center;
    }
    
    .tips-section {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        border: 2px solid #e8eef5;
        margin-top: 1rem;
    }
    
    .action-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        border: 2px solid #e8eef5;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .action-card:hover {
        border-color: #667eea;
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(102, 126, 234, 0.15);
    }
    
    .stat-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
    }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    h3 { color: #1e293b; font-weight: 600; }
    h4 { color: #334155; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# Main app header
st.markdown('<h1 class="main-header">🩺 AI Symptom Checker</h1>', unsafe_allow_html=True)

# Authentication section
if not st.session_state.token:
    st.markdown('<p class="subtitle">Your AI-Powered Health Companion</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>🔐</div>
            <h3 style='margin-bottom: 0.5rem;'>Welcome Back</h3>
            <p style='color: #64748b;'>Sign in to access your health analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        auth_choice = st.radio("", ["Login", "Register"], horizontal=True, label_visibility="collapsed")
        username = st.text_input("👤 Username", placeholder="Enter your username", key="auth_username")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password", key="auth_password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if auth_choice == "Login":
            if st.button("🚀 Sign In", use_container_width=True, type="primary"):
                if username and password:
                    if login(username, password):
                        st.rerun()
                else:
                    st.warning("Please enter both username and password.")
        else:
            if st.button("📝 Create Account", use_container_width=True, type="primary"):
                if username and password:
                    register(username, password)
                else:
                    st.warning("Please enter both username and password.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Feature highlights
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="action-card">
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>🤖</div>
            <h4>AI-Powered</h4>
            <p style='color: #64748b; font-size: 0.9rem;'>Advanced AI agents analyze your symptoms intelligently</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="action-card">
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>⚡</div>
            <h4>Instant Analysis</h4>
            <p style='color: #64748b; font-size: 0.9rem;'>Get rapid insights about your health concerns</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="action-card">
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>🔒</div>
            <h4>Secure & Private</h4>
            <p style='color: #64748b; font-size: 0.9rem;'>Your health data is protected and confidential</p>
        </div>
        """, unsafe_allow_html=True)

else:
    # User is logged in
    st.markdown('<p class="subtitle">Describe your symptoms for AI-powered analysis</p>', unsafe_allow_html=True)
    
    # Sidebar content
    st.sidebar.markdown(f"""
    <div class="user-badge">
        <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>👤</div>
        <h4 style='margin: 0; color: white;'>Welcome back!</h4>
        <p style='margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.9); font-size: 1.1rem;'>
            <strong>{st.session_state.username}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("🚪 Sign Out", use_container_width=True, type="secondary"):
        st.session_state.token = None
        st.session_state.username = None
        st.rerun()
    
    st.sidebar.markdown("""
    <div class="tips-section">
        <h4 style='margin-top: 0;'>💡 Tips for Better Analysis</h4>
        <ul style='color: #64748b; font-size: 0.9rem; line-height: 1.8;'>
            <li>Be specific about your symptoms</li>
            <li>Mention duration and severity</li>
            <li>Include any related factors</li>
            <li>Note recent health changes</li>
            <li>List any medications taken</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("""
    <div class="emergency-alert">
        <h4 style='margin-top: 0; color: #991b1b;'>🚨 Emergency Notice</h4>
        <p style='margin: 0; color: #7f1d1d; font-size: 0.9rem;'>
            <strong>If you're experiencing a medical emergency, call emergency services immediately.</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Main content - Warning disclaimer
    st.markdown("""
    <div class="warning-banner">
        <h4 style='margin-top: 0; color: #92400e;'>⚠️ Medical Disclaimer</h4>
        <p style='margin: 0; color: #78350f; font-size: 0.95rem;'>
            This AI symptom checker is for <strong>informational purposes only</strong> and does not replace 
            professional medical advice, diagnosis, or treatment. Always consult qualified healthcare providers 
            for medical concerns.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Symptom input card
    st.markdown('<div class="symptom-card">', unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <div style='font-size: 2.5rem; margin-bottom: 1rem;'>📝</div>
        <h3 style='margin: 0;'>Describe Your Symptoms</h3>
        <p style='color: #64748b; margin-top: 0.5rem;'>Provide detailed information for accurate analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    user_input = st.text_area(
        "Symptom Description",
        height=220,
        placeholder="Example: I've been experiencing a persistent headache for the past 3 days, mainly on the right side. It gets worse in the afternoon and I feel slightly nauseous. I've been more tired than usual and have had trouble sleeping...",
        help="Be as detailed as possible - include what you're feeling, when it started, severity, patterns, and any other relevant information",
        label_visibility="collapsed"
    )
    
    st.markdown("<p style='color: #64748b; font-size: 0.85rem; margin-bottom: 0.5rem;'>💭 Include details about:</p>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<span class="stat-badge">Duration</span>', unsafe_allow_html=True)
    with col2:
        st.markdown('<span class="stat-badge">Severity</span>', unsafe_allow_html=True)
    with col3:
        st.markdown('<span class="stat-badge">Frequency</span>', unsafe_allow_html=True)
    with col4:
        st.markdown('<span class="stat-badge">Location</span>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_clicked = st.button(
            "🔍 Analyze My Symptoms", 
            use_container_width=True,
            type="primary",
            disabled=not user_input.strip()
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if analyze_clicked and user_input:
        with st.spinner("🧠 AI agents are analyzing your symptoms... This may take a moment."):
            try:
                symptom_crew = create_symptom_crew(user_input)
                result = symptom_crew.kickoff()
                
                # Display results
                st.markdown("---")
                st.markdown('<div class="result-container">', unsafe_allow_html=True)
                
                st.markdown("""
                <div style='text-align: center; margin-bottom: 2rem;'>
                    <div style='font-size: 2.5rem; margin-bottom: 1rem;'>📊</div>
                    <h3 style='margin: 0;'>Your Analysis Results</h3>
                    <p style='color: #64748b; margin-top: 0.5rem;'>Based on AI-powered symptom evaluation</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(result)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Recommended next steps
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("""
                <div style='text-align: center; margin: 2rem 0 1rem 0;'>
                    <h3>🎯 Recommended Next Steps</h3>
                    <p style='color: #64748b;'>Consider these actions based on your symptoms</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("""
                    <div class="action-card">
                        <div style='font-size: 2.5rem; margin-bottom: 1rem;'>📋</div>
                        <h4>Monitor Symptoms</h4>
                        <p style='color: #64748b; font-size: 0.9rem;'>Keep track of any changes or progression</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div class="action-card">
                        <div style='font-size: 2.5rem; margin-bottom: 1rem;'>💊</div>
                        <h4>Self-Care</h4>
                        <p style='color: #64748b; font-size: 0.9rem;'>Consider rest, hydration, and over-the-counter relief</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown("""
                    <div class="action-card">
                        <div style='font-size: 2.5rem; margin-bottom: 1rem;'>🏥</div>
                        <h4>Professional Care</h4>
                        <p style='color: #64748b; font-size: 0.9rem;'>Consult a doctor if symptoms persist or worsen</p>
                    </div>
                    """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {e}")
                st.info("💡 Please try again or contact support if the problem persists.")
    
    elif analyze_clicked and not user_input.strip():
        st.warning("⚠️ Please describe your symptoms before analyzing.")

# Footer
st.markdown("""
<div style='text-align: center; color: #94a3b8; padding: 2rem 0; margin-top: 3rem; border-top: 2px solid #e2e8f0;'>
    <p style='font-size: 1.1rem; margin-bottom: 0.5rem;'>🩺 <strong>AI Symptom Checker</strong></p>
    <p style='font-size: 0.9rem;'>For informational purposes only | Always consult healthcare professionals for medical advice</p>
    <p style='font-size: 0.8rem; margin-top: 1rem;'>Powered by Advanced AI Technology</p>
</div>
""", unsafe_allow_html=True)