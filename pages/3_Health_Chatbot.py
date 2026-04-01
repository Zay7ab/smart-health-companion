import streamlit as st
import requests
import datetime
import sys
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="ClinIQ | Smart Companion",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Full Custom CSS (Screenshot Style) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Overrides */
    .stApp {
        background-color: #050805 !important;
    }
    * {
        font-family: 'Inter', sans-serif;
        color: #e0e0e0 !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #050805 !important;
        border-right: 1px solid #1a1a1a !important;
    }
    
    .sidebar-brand {
        color: #2ecc71 !important;
        font-size: 1.6rem;
        font-weight: 700;
        padding-left: 1rem;
        margin-bottom: 0px;
    }
    .sidebar-subtitle {
        color: #27ae60 !important;
        font-size: 0.7rem;
        font-weight: 600;
        padding-left: 1rem;
        margin-bottom: 2rem;
        letter-spacing: 1px;
    }

    /* Sidebar Navigation Sections */
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
    }
    .nav-link:hover {
        background: #111;
        color: #2ecc71 !important;
    }
    .nav-active {
        background: #1a1a1a;
        color: #2ecc71 !important;
        border-right: 3px solid #2ecc71;
    }

    /* Main Header Styling */
    .main-header {
        background: #0a0e0a;
        border: 1px solid #1a1a1a;
        border-radius: 12px;
        padding: 1.2rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }
    .header-left {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    .header-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin: 0;
    }
    .header-desc {
        font-size: 0.8rem;
        color: #666 !important;
        margin: 0;
    }

    /* FastAPI + Groq Badge */
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
        width: 7px;
        height: 7px;
        background-color: #2ecc71;
        border-radius: 50%;
        box-shadow: 0 0 10px #2ecc71;
    }

    /* Feature Cards */
    .glass-card {
        background: #0a0e0a;
        border: 1px solid #1a1a1a;
        border-top: 2px solid #2ecc71;
        padding: 1.5rem;
        border-radius: 10px;
        height: 100%;
    }
    .card-label { font-size: 0.7rem; color: #555 !important; font-weight: 700; text-transform: uppercase; }
    .card-value { font-size: 1.3rem; font-weight: 700; color: #fff !important; margin: 5px 0; }
    .card-footer { font-size: 0.75rem; color: #2ecc71 !important; font-weight: 500; }

    /* File Upload Box */
    .upload-zone {
        border: 1px dashed #2ecc71;
        background: rgba(46, 204, 113, 0.02);
        border-radius: 15px;
        padding: 3rem;
        text-align: center;
        margin-top: 1rem;
    }
    
    /* Footer Warning */
    .warning-box {
        background: rgba(255, 193, 7, 0.03);
        border: 1px solid rgba(255, 193, 7, 0.2);
        padding: 12px;
        border-radius: 8px;
        color: #ffc107 !important;
        font-size: 0.75rem;
        text-align: left;
        margin-top: 3rem;
    }

    /* Input Customization */
    div[data-testid="stChatInput"] {
        background-color: #0a0e0a !important;
        border: 1px solid #1a1a1a !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar Content ---
with st.sidebar:
    st.markdown('<div class="sidebar-brand">● ClinIQ</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">SMART COMPANION · 2026</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">EMERGENCY</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-link">🚨 Emergency SOS</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">DIAGNOSTICS</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-link">🏠 Home</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-link">🫀 Heart Disease</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-link nav-active">🫁 X-Ray Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-link">🔍 Symptom Checker</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">TOOLS</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-link">🤖 AI Chatbot</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-link">⚖️ BMI Calculator</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-link">📈 Risk Gauge</div>', unsafe_allow_html=True)

# --- Main Dashboard ---

# Header with FastAPI Badge
st.markdown(f"""
<div class="main-header">
    <div class="header-left">
        <span style="font-size:2rem;">🫁</span>
        <div>
            <h2 class="header-title">X-Ray Analysis</h2>
            <p class="header-desc">Deep Learning CNN model for pneumonia detection</p>
        </div>
    </div>
    <div class="status-badge">
        <div class="pulse-dot"></div> FastAPI + Groq Active
    </div>
</div>
""", unsafe_allow_html=True)

# Feature Info Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""<div class="glass-card"><p class="card-label">MODEL</p><p class="card-value">CNN</p><p class="card-footer">Deep Learning</p></div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class="glass-card"><p class="card-label">TRAINING ACCURACY</p><p class="card-value">95%</p><p class="card-footer">5216 Images</p></div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class="glass-card"><p class="card-label">CLASSES</p><p class="card-value">2</p><p class="card-footer">Normal · Pneumonia</p></div>""", unsafe_allow_html=True)

# Upload Area
st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="upload-zone">
    <span style="font-size:3rem;">🫁</span>
    <h3 style="margin-top:1rem;">Upload Chest X-Ray</h3>
    <p style="color:#666 !important; font-size:0.85rem;">Supports JPG, JPEG, PNG formats</p>
</div>
""", unsafe_allow_html=True)

# File Uploader component
uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

# Simple AI Chat Integration
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown("### 🤖 Clinical AI Chat")
chat_container = st.container()

with chat_container:
    for msg in st.session_state.chat_history:
        color = "#2ecc71" if msg["role"] == "assistant" else "#58a6ff"
        st.markdown(f"""
        <div style="background:#0a0e0a; border:1px solid #1a1a1a; padding:1rem; border-radius:10px; margin-bottom:10px;">
            <p style="color:{color} !important; font-size:0.7rem; font-weight:700; text-transform:uppercase; margin-bottom:5px;">{msg['role']}</p>
            <p style="margin:0; font-size:0.95rem;">{msg['content']}</p>
        </div>
        """, unsafe_allow_html=True)

user_query = st.chat_input("Ask about diagnostic results...")

if user_query:
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    # Simulated response
    st.session_state.chat_history.append({"role": "assistant", "content": "Analyzing clinical context via Groq Llama 3... Scanning complete."})
    st.rerun()

# Disclaimer
st.markdown("""
<div class="warning-box">
    ⚠️ For educational purposes only. Always consult a qualified doctor.
</div>
""", unsafe_allow_html=True)
