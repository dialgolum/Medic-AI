import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent / "backend"))

import streamlit as st
import requests
from dotenv import load_dotenv
from backend.src.crew.agents import create_symptom_crew

load_dotenv()

# Enhanced page configuration with wider layout and better theme
st.set_page_config(
    page_title="MediScan AI - Symptom Checker",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo',
        'Report a bug': "https://github.com/your-repo/issues",
        'About': "# MediScan AI\nAdvanced AI-powered symptom analysis and health insights."
    }
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

# Enhanced Custom CSS with modern healthcare theme
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary: #2563eb;
        --primary-dark: #1d4ed8;
        --secondary: #10b981;
        --accent: #f59e0b;
        --danger: #ef4444;
        --light-bg: #f8fafc;
        --card-bg: #ffffff;
        --text-dark: #1e293b;
        --text-light: #64748b;
    }
    
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: var(--text-light);
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 400;
    }
    
    .symptom-input {
        background: var(--card-bg);
        padding: 30px;
        border-radius: 20px;
        border-left: 6px solid var(--primary);
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin: 20px 0;
        border: 1px solid #e2e8f0;
    }
    
    .result-box {
        background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
        padding: 30px;
        border-radius: 20px;
        border-left: 6px solid var(--secondary);
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        margin-top: 20px;
        border: 1px solid #bae6fd;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fffbeb, #fef3c7);
        padding: 25px;
        border-radius: 15px;
        border-left: 6px solid var(--accent);
        box-shadow: 0 8px 20px rgba(0,0,0,0.05);
        margin: 25px 0;
        border: 1px solid #fcd34d;
    }
    
    .emergency-box {
        background: linear-gradient(135deg, #fef2f2, #fee2e2);
        padding: 20px;
        border-radius: 15px;
        border-left: 6px solid var(--danger);
        box-shadow: 0 8px 20px rgba(0,0,0,0.05);
        margin: 20px 0;
        border: 1px solid #fca5a5;
    }
    
    .login-box {
        background: var(--card-bg);
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
        margin: 20px auto;
        max-width: 500px;
    }
    
    .user-welcome {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 25px;
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.2);
    }
    
    .user-avatar-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    .stats-card {
        background: var(--card-bg);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        margin: 10px 0;
    }
    
    .quick-actions-card {
        background: var(--card-bg);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        margin: 15px 0;
    }
    
    .analyze-btn {
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        color: white;
        padding: 15px 40px;
        border: none;
        border-radius: 50px;
        font-size: 18px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(37, 99, 235, 0.3);
    }
    
    .analyze-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.4);
    }
    
    .secondary-btn {
        background: linear-gradient(135deg, var(--secondary), #0d9668);
        color: white;
        padding: 12px 30px;
        border: none;
        border-radius: 50px;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .logout-btn {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
        padding: 12px 30px;
        border: none;
        border-radius: 50px;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 10px;
    }
    
    /* Custom streamlit component overrides */
    .stTextInput input, .stTextArea textarea {
        border-radius: 12px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 12px 16px !important;
        font-size: 16px !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
    }
    
    .stRadio > div {
        background: var(--light-bg);
        padding: 15px;
        border-radius: 12px;
    }
    
    /* Loading animation */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .pulse-animation {
        animation: pulse 2s infinite;
    }
    
    /* Avatar styling */
    .avatar-large {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 15px;
        font-size: 30px;
        color: white;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Main app header with enhanced design
st.markdown('<h1 class="main-header">🏥 MediScan AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Advanced AI-Powered Symptom Analysis & Health Insights</p>', unsafe_allow_html=True)

# Authentication section with improved design
if not st.session_state.token:
    # Hero section for unauthenticated users
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; margin-bottom: 40px;'>
            <h3 style='color: var(--text-dark); margin-bottom: 15px;'>Your Personal Health Assistant</h3>
            <p style='color: var(--text-light); font-size: 18px; line-height: 1.6;'>
                Get instant, AI-powered insights about your health concerns. 
                Our advanced system analyzes your symptoms and provides helpful guidance.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Features grid
        feat_col1, feat_col2, feat_col3 = st.columns(3)
        with feat_col1:
            st.markdown("""
            <div class='stats-card'>
                <h3>🔍</h3>
                <h4>Smart Analysis</h4>
                <p>AI-powered symptom assessment</p>
            </div>
            """, unsafe_allow_html=True)
        with feat_col2:
            st.markdown("""
            <div class='stats-card'>
                <h3>⚡</h3>
                <h4>Instant Results</h4>
                <p>Quick health insights</p>
            </div>
            """, unsafe_allow_html=True)
        with feat_col3:
            st.markdown("""
            <div class='stats-card'>
                <h3>🛡️</h3>
                <h4>Secure & Private</h4>
                <p>Your data is protected</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Login/Register box
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        
        st.markdown("""
        <div style='text-align: center; margin-bottom: 30px;'>
            <h2 style='color: var(--text-dark); margin-bottom: 10px;'>Welcome Back</h2>
            <p style='color: var(--text-light);'>Sign in to access MediScan AI</p>
        </div>
        """, unsafe_allow_html=True)
        
        auth_choice = st.radio(
            "Choose Action",
            ["Login", "Register"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        username = st.text_input("👤 Username", placeholder="Enter your username")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
        
        if auth_choice == "Login":
            if st.button("🚀 Sign In to MediScan", use_container_width=True, type="primary"):
                if username and password:
                    if login(username, password):
                        st.success("Welcome back! 🎉")
                        st.rerun()
                else:
                    st.warning("Please enter both username and password.")
        else:
            if st.button("📝 Create Account", use_container_width=True, type="secondary"):
                if username and password:
                    if register(username, password):
                        st.rerun()
                else:
                    st.warning("Please enter both username and password.")
        
        st.markdown("""
        <div style='text-align: center; margin-top: 25px; padding-top: 20px; border-top: 1px solid #e2e8f0;'>
            <p style='color: var(--text-light); font-size: 14px;'>
                By continuing, you agree to our Terms of Service and Privacy Policy
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # User is logged in - Enhanced dashboard with better sidebar organization
    main_col, sidebar_col = st.columns([3, 1])
    
    with sidebar_col:
        # User Avatar Card - At the top of sidebar
        st.markdown(f"""
        <div class='user-avatar-card'>
            <div class='avatar-large'>
                {st.session_state.username[0].upper()}
            </div>
            <h3 style='margin: 10px 0 5px 0; color: white;'>{st.session_state.username}</h3>
            <p style='margin: 0; color: rgba(255,255,255,0.9); font-size: 14px;'>
                <span style='background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 20px;'>Active User</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Logout Button - Right below avatar
        if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
            st.session_state.token = None
            st.session_state.username = None
            st.success("Logged out successfully!")
            st.rerun()

        # Analysis Tips
        st.markdown("""
        <div class='quick-actions-card'>
            <h4 style='color: var(--text-dark); margin-bottom: 15px;'>💡 Analysis Tips</h4>
            <div style='background: var(--light-bg); padding: 15px; border-radius: 12px;'>
                <p style='margin: 8px 0; font-size: 14px;'>• Be specific about symptoms</p>
                <p style='margin: 8px 0; font-size: 14px;'>• Mention duration & severity</p>
                <p style='margin: 8px 0; font-size: 14px;'>• Include related factors</p>
                <p style='margin: 8px 0; font-size: 14px;'>• Note recent changes</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Emergency notice at the bottom of sidebar
        st.markdown("""
        <div class='emergency-box'>
            <h4 style='color: var(--danger); margin-bottom: 10px;'>🚨 Emergency</h4>
            <p style='font-size: 14px; margin: 0; color: var(--text-dark);'>
                If you're experiencing a medical emergency,
                <strong>Please Call emergency services immediately.</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with main_col:
        # Main symptom analysis section
        st.markdown(f"""
        <div class='user-welcome'>
            <h2 style='margin: 0; color: white;'>👋 Welcome back, {st.session_state.username}!</h2>
            <p style='margin: 10px 0 0 0; color: rgba(255,255,255,0.9); font-size: 16px;'>
                Ready to analyze your symptoms? We're here to help.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='text-align: center; margin-bottom: 30px;'>
            <h2 style='color: var(--text-dark); margin-bottom: 15px;'>Describe Your Symptoms</h2>
            <p style='color: var(--text-light); font-size: 18px; line-height: 1.6;'>
                Please provide detailed information about how you're feeling for the most accurate analysis. 
                The more specific you are, the better our AI can assist you.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Warning box
        st.markdown("""
        <div class='warning-box'>
            <div style='display: flex; align-items: flex-start; gap: 15px;'>
                <div style='font-size: 24px;'>⚠️</div>
                <div>
                    <h4 style='margin: 0 0 10px 0; color: var(--text-dark);'>Important Medical Disclaimer</h4>
                    <p style='margin: 0; color: var(--text-dark); line-height: 1.5; font-size: 15px;'>
                        MediScan AI is for <strong>informational purposes only</strong> and is not a substitute for professional medical advice, 
                        diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider 
                        with any questions you may have regarding a medical condition.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced symptom input area
        st.markdown('<div class="symptom-input">', unsafe_allow_html=True)
        
        st.markdown("""
        <h3 style='color: var(--text-dark); margin-bottom: 20px;'>
            📝 Tell Us About Your Symptoms
        </h3>
        """, unsafe_allow_html=True)
        
        # Symptom guidance in columns
        guide_col1, guide_col2 = st.columns(2)
        with guide_col1:
            st.markdown("""
            <div style='background: var(--light-bg); padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
                <h5 style='margin: 0 0 10px 0; color: var(--primary);'>✅ Include These Details:</h5>
                <ul style='margin: 0; padding-left: 20px; font-size: 14px; color: var(--text-dark);'>
                    <li>Main symptoms</li>
                    <li>When they started</li>
                    <li>Severity level (1-10)</li>
                    <li>Any patterns</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with guide_col2:
            st.markdown("""
            <div style='background: var(--light-bg); padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
                <h5 style='margin: 0 0 10px 0; color: var(--secondary);'>💡 Helpful Information:</h5>
                <ul style='margin: 0; padding-left: 20px; font-size: 14px; color: var(--text-dark);'>
                    <li>Triggers or relievers</li>
                    <li>Recent activities</li>
                    <li>Existing conditions</li>
                    <li>Medications taken</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        user_input = st.text_area(
            "Describe your symptoms in detail:",
            height=200,
            placeholder="Example: I've had a persistent headache for 3 days, rated 7/10 in severity. It's worse in the morning and improves slightly with rest. I've also noticed some sensitivity to light. No fever or other symptoms. I have a history of migraines.",
            help="Be as detailed as possible for the most accurate analysis",
            label_visibility="collapsed"
        )
        
        # Analysis button with enhanced styling
        st.markdown("""
        <div style='text-align: center; margin-top: 25px;'>
        """, unsafe_allow_html=True)
        
        analyze_clicked = st.button(
            "🔍 Analyze My Symptoms with AI", 
            use_container_width=True,
            type="primary",
            disabled=not user_input.strip(),
            key="analyze_main"
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Handle analysis - FIXED VERSION
        if analyze_clicked and user_input:
            with st.spinner(""):
                # Show custom loading message
                loading_placeholder = st.empty()
                with loading_placeholder.container():
                    st.markdown("""
                    <div class='pulse-animation' style='text-align: center; padding: 30px;'>
                        <h3 style='color: #2563eb; margin-bottom: 15px;'>🧠 AI Analysis in Progress</h3>
                        <p style='color: #64748b; margin: 0;'>
                            Our healthcare AI agents are carefully analyzing your symptoms...<br>
                            This may take a moment as we provide comprehensive insights.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                try:
                    symptom_crew = create_symptom_crew(user_input)
                    result = symptom_crew.kickoff()
                    
                    # Clear the loading animation immediately after analysis is done
                    loading_placeholder.empty()
                    
                    # Display results in enhanced format
                    st.markdown("---")
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    
                    st.markdown("""
                    <div style='text-align: center; margin-bottom: 25px;'>
                        <h2 style='color: var(--secondary); margin-bottom: 10px;'>📊 Analysis Complete</h2>
                        <p style='color: var(--text-light);'>Your AI-powered health assessment is ready</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(result)
                    
                    # Enhanced follow-up actions
                    st.markdown("---")
                    st.markdown("""
                    <div style='text-align: center; margin: 30px 0 15px 0;'>
                        <h3 style='color: var(--text-dark); margin-bottom: 20px;'>🎯 Recommended Next Steps</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    action_col1, action_col2, action_col3 = st.columns(3)
                    with action_col1:
                        st.markdown("""
                        <div style='text-align: center; padding: 20px; background: var(--light-bg); border-radius: 15px;'>
                            <div style='font-size: 40px; margin-bottom: 15px;'>📋</div>
                            <h4 style='margin: 0 0 10px 0; color: var(--text-dark);'>Monitor Symptoms</h4>
                            <p style='margin: 0; color: var(--text-light); font-size: 14px;'>
                                Keep track of any changes in your condition
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with action_col2:
                        st.markdown("""
                        <div style='text-align: center; padding: 20px; background: var(--light-bg); border-radius: 15px;'>
                            <div style='font-size: 40px; margin-bottom: 15px;'>💊</div>
                            <h4 style='margin: 0 0 10px 0; color: var(--text-dark);'>Self-Care</h4>
                            <p style='margin: 0; color: var(--text-light); font-size: 14px;'>
                                Consider rest, hydration, and OTC options
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with action_col3:
                        st.markdown("""
                        <div style='text-align: center; padding: 20px; background: var(--light-bg); border-radius: 15px;'>
                            <div style='font-size: 40px; margin-bottom: 15px;'>🏥</div>
                            <h4 style='margin: 0 0 10px 0; color: var(--text-dark);'>Professional Care</h4>
                            <p style='margin: 0; color: var(--text-light); font-size: 14px;'>
                                Consult a healthcare provider if needed
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Additional actions
                    st.markdown("""
                    <div style='text-align: center; margin-top: 25px;'>
                        <p style='color: var(--text-light); font-size: 15px;'>
                            <strong>Remember:</strong> This analysis is AI-generated and should be used for informational purposes only.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    # Also clear loading animation if there's an error
                    loading_placeholder.empty()
                    st.error(f"❌ An unexpected error occurred during analysis: {str(e)}")
                    st.info("""
                    **Troubleshooting tips:**
                    - Please try again in a few moments
                    - Check your internet connection
                    - Ensure the symptom description is clear and detailed
                    - Contact support if the problem persists
                    """)
        
        elif analyze_clicked and not user_input.strip():
            st.warning("""
            ⚠️ **Please describe your symptoms**  
            We need details about how you're feeling to provide an accurate analysis.
            """)

# Enhanced Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: var(--text-light); padding: 20px 0;'>
    <div style='display: flex; justify-content: center; gap: 30px; margin-bottom: 15px;'>
        <a href='#' style='color: var(--text-light); text-decoration: none;'>Privacy Policy</a>
        <a href='#' style='color: var(--text-light); text-decoration: none;'>Terms of Service</a>
        <a href='#' style='color: var(--text-light); text-decoration: none;'>Contact Support</a>
        <a href='#' style='color: var(--text-light); text-decoration: none;'>About MediScan AI</a>
    </div>
    <p style='margin: 0; font-size: 14px;'>
        🏥 MediScan AI | AI-Powered Health Insights | For informational purposes only | 
        Always consult healthcare professionals for medical advice
    </p>
    <p style='margin: 10px 0 0 0; font-size: 12px; color: var(--text-light); opacity: 0.7;'>
        © 2024 MediScan AI. All rights reserved.
    </p>
</div>
""", unsafe_allow_html=True)