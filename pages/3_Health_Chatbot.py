import streamlit as st
import requests
import datetime
import sys
import os

# Ensure local utils can be found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from utils.sidebar import load_sidebar
except ImportError:
    def load_sidebar():
        pass

# --- Page Configuration ---
st.set_page_config(page_title="HealthAI | Clinical", page_icon="🏥", layout="wide")

# --- Claude-Inspired Minimalist CSS ---
# Using standard spaces only to avoid SyntaxErrors
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    :root {
        --bg-white: #ffffff;
        --sidebar-gray: #f9f9f9;
        --border-light: #e5e5e5;
        --text-dark: #1a1a1a;
        --text-muted: #666666;
        --clinical-blue: #2563eb;
    }

    .stApp { background-color: var(--bg-white); }
    
    * { font-family: 'Inter', sans-serif; color: var(--text-dark); }

    /* Clean Top Header */
    .nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 1.5rem;
        border-bottom: 1px solid var(--border-light);
        background: white;
        margin-bottom: 2rem;
    }
    .nav-title { font-weight: 600; font-size: 1.1rem; }
    .status-indicator { font-size: 0.7rem; color: #166534; background: #f0fdf4; padding: 2px 8px; border-radius: 4px; border: 1px solid #bbf7d0; }

    /* Chat Styling */
    .chat-wrapper { max-width: 850px; margin: 0 auto; }
    
    .bubble {
        padding: 1rem;
        border-radius: 8px;
        line-height: 1.6;
        margin-bottom: 1rem;
        font-size: 0.95rem;
    }
    .bubble-ai { background: white; border: 1px solid var(--border-light); }
    .bubble-user { background: #f4f4f5; border: 1px solid #e4e4e7; margin-left: 2rem; }
    
    .label-meta { font-size: 0.75rem; font-weight: 600; color: var(--text-muted); margin-bottom: 4px; display: block; }

    /* Sidebar Improvements */
    section[data-testid="stSidebar"] { background-color: var(--sidebar-gray); border-right: 1px solid var(--border-light); }
    .sidebar-header { font-size: 0.7rem; font-weight: 700; color: #888; text-transform: uppercase; margin: 1.5rem 0 0.5rem 0; }

    /* Source Citations */
    .citation-box {
        margin-top: 12px;
        padding: 8px 12px;
        border-left: 3px solid var(--clinical-blue);
        background: #f8fafc;
        font-size: 0.85rem;
        color: #334155;
    }
</style>
""", unsafe_allow_html=True)

# --- Logic & State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")

def call_health_api(user_query, history, lang="English"):
    try:
        payload = {
            "message": user_query,
            "history": history,
            "language": lang,
            "api_key": st.secrets.get("GROQ_API_KEY", "")
        }
        response = requests.post(f"{API_URL}/chat", json=payload, timeout=25)
        return response.json().get("reply", "The assistant is currently unavailable.")
    except Exception:
        return "Network timeout. Please check your connection and try again."

# --- UI Layout ---

# 1. Sidebar (Professional Features)
with st.sidebar:
    load_sidebar()
    st.markdown('<p class="sidebar-header">Patient Vitals</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.number_input("BP (Sys)", 80, 200, 120)
    with c2:
        st.number_input("BP (Dia)", 50, 120, 80)
    st.slider("Heart Rate (BPM)", 40, 160, 72)
    
    st.markdown('<p class="sidebar-header">Medical Documents</p>', unsafe_allow_html=True)
    st.file_uploader("Upload Lab Report (PDF/JPG)", type=["pdf", "png", "jpg"], help="Analyze bloodwork or imaging results.")

    st.markdown('<p class="sidebar-header">Settings</p>', unsafe_allow_html=True)
    selected_lang = st.selectbox("Language", ["English", "Arabic", "French", "Spanish", "Urdu"])
    
    if st.button("Clear Conversation"):
        st.session_state.chat_history = []
        st.rerun()

# 2. Main Header
st.markdown(f"""
<div class="nav-bar">
    <div class="nav-title">🏥 HealthAI <span style="font-weight:300; color:#999; margin-left:10px;">Clinical Intelligence</span></div>
    <div class="status-indicator">SECURE CONNECTION</div>
</div>
""", unsafe_allow_html=True)

# 3. Chat Display
chat_container = st.container()

with chat_container:
    # Default Welcome
    st.markdown("""
    <div class="chat-wrapper">
        <span class="label-meta">ASSISTANT</span>
        <div class="bubble bubble-ai">
            Hello. I am your clinical intelligence assistant. You can input symptoms, 
            ask about drug interactions, or upload lab results for a
