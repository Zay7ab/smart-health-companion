import streamlit as st
import requests
import datetime
import sys
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="ClinIQ | AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ClinIQ Professional Dark Theme CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Dark Background */
    .stApp {
        background-color: #050805 !important;
    }
    * {
        font-family: 'Inter', sans-serif;
        color: #e0e0e0 !important;
    }

    /* Sidebar Styling (Exactly as per Screenshot) */
    [data-testid="stSidebar"] {
        background-color: #050805 !important;
        border-right: 1px solid #1a1a1a !important;
    }
    
    .sidebar-brand {
        color: #2ecc71 !important;
        font-size: 1.6rem;
        font-weight: 700;
        padding-left: 1rem;
        margin-top: 1rem;
    }
    .sidebar-subtitle {
        color: #27ae60 !important;
        font-size: 0.7rem;
        font-weight: 600;
        padding-left: 1rem;
        margin-bottom: 2rem;
        letter-spacing: 1px;
    }

    .sidebar-label {
        font-size: 0.65rem;
        font-weight: 700;
        color: #444 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 1.5rem 0 0.8rem 1rem;
    }

    .nav-link {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 15px;
        margin: 2px 10px;
        border-radius: 8px;
        font-size: 0.9rem;
        color: #888 !important;
        transition: 0.3s;
        cursor: pointer;
    }
    .nav-active {
        background: #1a1a1a;
        color: #2ecc71 !important;
        border-right: 3px solid #2ecc71;
    }

    /* Top Navigation Bar */
    .chat-header {
        background: #0a0e0a;
        border: 1px solid #1a1a1a;
        border-radius: 12px;
        padding: 1.2rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }
    .status-badge {
        background: rgba(46, 204, 113, 0.05);
        color: #2ecc71 !important;
        border: 1px solid #2ecc71;
        border-radius: 20px;
        padding: 5px 15px;
        font-size: 0.75rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .pulse-dot {
        width: 7px; height: 7px; background-color: #2ecc71;
        border-radius: 50%; box-shadow: 0 0 10px #2ecc71;
    }

    /* Chat Bubbles Style */
    .chat-bubble {
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        line-height: 1.6;
        font-size: 0.95rem;
        max-width: 85%;
    }
    .bubble-ai {
        background: #0a0e0a;
        border: 1px solid #1a1a1a;
        border-left: 3px solid #2ecc71;
    }
    .bubble-user {
        background: #111;
        border: 1px solid #222;
        margin-left: auto;
        border-right: 3px solid #58a6ff;
    }
    
    .role-meta {
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 6px;
        letter-spacing: 0.5px;
    }

    /* Professional Warning */
    .warning-box {
        background: rgba(255, 193, 7, 0.02);
        border: 1px solid rgba(255, 193, 7, 0.15);
        padding: 15px;
        border-radius: 8px;
        color: #ffc107 !important;
        font-size: 0.8rem;
        text-align: center;
        margin-top: 2rem;
    }

    /* Input Area Overrides */
    div[data-testid="stChatInput"] {
        background-color: #0a0e0a !important;
        border: 1px solid #1a1a1a !important;
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar (Directly from Screenshot Style) ---
with st.sidebar:
    st.markdown('<div class="sidebar-brand">● ClinIQ</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">SMART COMPANION · 2026</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">EMERGENCY</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-link">🚨 Emergency SOS</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">DIAGNOSTICS</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-link">🏠 Home</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-link">🫀 Heart Disease</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-link">🫁 X-Ray Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-link">🔍 Symptom Checker</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">TOOLS</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-link nav-active">🤖 AI Chatbot</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-link">⚖️ BMI Calculator</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-link">📈 Risk Gauge</div>', unsafe_allow_html=True)

# --- Main Chat Page ---

# Header with Status
st.markdown(f"""
<div class="chat-header">
    <div style="display:flex; align-items:center; gap:15px;">
        <span style="font-size:1.8rem;">🤖</span>
        <div>
            <h2 style="margin:0; font-size:1.3rem;">Clinical AI Chatbot</h2>
            <p style="margin:0; font-size:0.75rem; color:#666 !important;">Powered by Llama 3.3 via Groq Systems</p>
        </div>
    </div>
    <div class="status-badge">
        <div class="pulse-dot"></div> FastAPI + Groq Active
    </div>
</div>
""", unsafe_allow_html=True)

# Chat Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat Interface
container = st.container()

with container:
    # Initial Assistant Greeting
    st.markdown("""
    <div class="chat-bubble bubble-ai">
        <div class="role-meta" style="color:#2ecc71;">ClinIQ AI Assistant</div>
        Hello. I am your specialized clinical AI. I can analyze symptoms, provide 
        information on medications, and explain complex diagnostic terms. 
        How can I assist your health query today?
    </div>
    """, unsafe_allow_html=True)

    # Rendering History
    for msg in st.session_state.chat_history:
        is_user = msg["role"] == "user"
        bubble_cls = "bubble-user" if is_user else "bubble-ai"
        role_label = "Patient Query" if is_user else "ClinIQ AI Insight"
        role_color = "#58a6ff" if is_user else "#2ecc71"
        
        st.markdown(f"""
        <div class="chat-bubble {bubble_cls}">
            <div class="role-meta" style="color:{role_color};">{role_label}</div>
            {msg['content']}
        </div>
        """, unsafe_allow_html=True)

# --- Chat Input & Logic ---
user_query = st.chat_input("Ask a medical question or describe symptoms...")

if user_query:
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    
    # API Call Simulation (Replace with your actual requests logic)
    with st.spinner("Processing clinical data..."):
        # Yahan aap apna actual API call dalain ge (FastAPI/Groq)
        # reply = get_ai_response(user_query, st.session_state.chat_history[:-1])
        reply = "Analyzing symptoms based on provided data... Please consult a physician for an official diagnosis."
        
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

# Professional Warning Footer
st.markdown("""
<div class="warning-box">
    ⚠️ <b>Disclaimer:</b> ClinIQ is an AI tool for informational purposes only. In case of medical 
    emergencies, please contact 911 or your local emergency number immediately.
</div>
<div style="text-align:center; margin-top:2rem; font-size:0.7rem; color:#444 !important;">
    © 2026 ClinIQ Intelligence Systems | Secure Data Processing
</div>
""", unsafe_allow_html=True)import streamlit as st
import requests
import datetime
import sys
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="ClinIQ | AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ClinIQ Professional Dark Theme CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Dark Background */
    .stApp {
        background-color: #050805 !important;
    }
    * {
        font-family: 'Inter', sans-serif;
        color: #e0e0e0 !important;
    }

    /* Sidebar Styling (Exactly as per Screenshot) */
    [data-testid="stSidebar"] {
        background-color: #050805 !important;
        border-right: 1px solid #1a1a1a !important;
    }
    
    .sidebar-brand {
        color: #2ecc71 !important;
        font-size: 1.6rem;
        font-weight: 700;
        padding-left: 1rem;
        margin-top: 1rem;
    }
    .sidebar-subtitle {
        color: #27ae60 !important;
        font-size: 0.7rem;
        font-weight: 600;
        padding-left: 1rem;
        margin-bottom: 2rem;
        letter-spacing: 1px;
    }

    .sidebar-label {
        font-size: 0.65rem;
        font-weight: 700;
        color: #444 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 1.5rem 0 0.8rem 1rem;
    }

    .nav-link {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 15px;
        margin: 2px 10px;
        border-radius: 8px;
        font-size: 0.9rem;
        color: #888 !important;
        transition: 0.3s;
        cursor: pointer;
    }
    .nav-active {
        background: #1a1a1a;
        color: #2ecc71 !important;
        border-right: 3px solid #2ecc71;
    }

    /* Top Navigation Bar */
    .chat-header {
        background: #0a0e0a;
        border: 1px solid #1a1a1a;
        border-radius: 12px;
        padding: 1.2rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }
    .status-badge {
        background: rgba(46, 204, 113, 0.05);
        color: #2ecc71 !important;
        border: 1px solid #2ecc71;
        border-radius: 20px;
        padding: 5px 15px;
        font-size: 0.75rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .pulse-dot {
        width: 7px; height: 7px; background-color: #2ecc71;
        border-radius: 50%; box-shadow: 0 0 10px #2ecc71;
    }

    /* Chat Bubbles Style */
    .chat-bubble {
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        line-height: 1.6;
        font-size: 0.95rem;
        max-width: 85%;
    }
    .bubble-ai {
        background: #0a0e0a;
        border: 1px solid #1a1a1a;
        border-left: 3px solid #2ecc71;
    }
    .bubble-user {
        background: #111;
        border: 1px solid #222;
        margin-left: auto;
        border-right: 3px solid #58a6ff;
    }
    
    .role-meta {
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 6px;
        letter-spacing: 0.5px;
    }

    /* Professional Warning */
    .warning-box {
        background: rgba(255, 193, 7, 0.02);
        border: 1px solid rgba(255, 193, 7, 0.15);
        padding: 15px;
        border-radius: 8px;
        color: #ffc107 !important;
        font-size: 0.8rem;
        text-align: center;
        margin-top: 2rem;
    }

    /* Input Area Overrides */
    div[data-testid="stChatInput"] {
        background-color: #0a0e0a !important;
        border: 1px solid #1a1a1a !important;
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar (Directly from Screenshot Style) ---
with st.sidebar:
    st.markdown('<div class="sidebar-brand">● ClinIQ</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">SMART COMPANION · 2026</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">EMERGENCY</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-link">🚨 Emergency SOS</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">DIAGNOSTICS</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-link">🏠 Home</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-link">🫀 Heart Disease</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-link">🫁 X-Ray Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-link">🔍 Symptom Checker</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">TOOLS</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-link nav-active">🤖 AI Chatbot</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-link">⚖️ BMI Calculator</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-link">📈 Risk Gauge</div>', unsafe_allow_html=True)

# --- Main Chat Page ---

# Header with Status
st.markdown(f"""
<div class="chat-header">
    <div style="display:flex; align-items:center; gap:15px;">
        <span style="font-size:1.8rem;">🤖</span>
        <div>
            <h2 style="margin:0; font-size:1.3rem;">Clinical AI Chatbot</h2>
            <p style="margin:0; font-size:0.75rem; color:#666 !important;">Powered by Llama 3.3 via Groq Systems</p>
        </div>
    </div>
    <div class="status-badge">
        <div class="pulse-dot"></div> FastAPI + Groq Active
    </div>
</div>
""", unsafe_allow_html=True)

# Chat Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat Interface
container = st.container()

with container:
    # Initial Assistant Greeting
    st.markdown("""
    <div class="chat-bubble bubble-ai">
        <div class="role-meta" style="color:#2ecc71;">ClinIQ AI Assistant</div>
        Hello. I am your specialized clinical AI. I can analyze symptoms, provide 
        information on medications, and explain complex diagnostic terms. 
        How can I assist your health query today?
    </div>
    """, unsafe_allow_html=True)

    # Rendering History
    for msg in st.session_state.chat_history:
        is_user = msg["role"] == "user"
        bubble_cls = "bubble-user" if is_user else "bubble-ai"
        role_label = "Patient Query" if is_user else "ClinIQ AI Insight"
        role_color = "#58a6ff" if is_user else "#2ecc71"
        
        st.markdown(f"""
        <div class="chat-bubble {bubble_cls}">
            <div class="role-meta" style="color:{role_color};">{role_label}</div>
            {msg['content']}
        </div>
        """, unsafe_allow_html=True)

# --- Chat Input & Logic ---
user_query = st.chat_input("Ask a medical question or describe symptoms...")

if user_query:
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    
    # API Call Simulation (Replace with your actual requests logic)
    with st.spinner("Processing clinical data..."):
        # Yahan aap apna actual API call dalain ge (FastAPI/Groq)
        # reply = get_ai_response(user_query, st.session_state.chat_history[:-1])
        reply = "Analyzing symptoms based on provided data... Please consult a physician for an official diagnosis."
        
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

# Professional Warning Footer
st.markdown("""
<div class="warning-box">
    ⚠️ <b>Disclaimer:</b> ClinIQ is an AI tool for informational purposes only. In case of medical 
    emergencies, please contact 911 or your local emergency number immediately.
</div>
<div style="text-align:center; margin-top:2rem; font-size:0.7rem; color:#444 !important;">
    © 2026 ClinIQ Intelligence Systems | Secure Data Processing
</div>
""", unsafe_allow_html=True)
