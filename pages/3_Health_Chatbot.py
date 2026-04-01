import streamlit as st
import requests
import datetime
import os
from fpdf import FPDF

# --- Page Configuration ---
st.set_page_config(
    page_title="ClinIQ | Clinical Intelligence",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Full Dark Neon CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono&display=swap');

* { font-family: 'Inter', sans-serif; }
.stApp { background: #0a0f0a !important; color: #e0e0e0; }

/* Navigation Styling */
[data-testid="stSidebarNav"] { display: none; } /* Hide default nav */

.nav-item {
    padding: 10px 15px;
    border-radius: 8px;
    color: #a0a0a0;
    text-decoration: none;
    display: block;
    margin-bottom: 5px;
    font-size: 14px;
    transition: 0.3s;
}
.nav-item:hover { background: rgba(255,255,255,0.05); color: #ffffff; }
.nav-active { background: #1e1e2e; color: #ffffff; border-left: 3px solid #4ade80; }

/* Status Cards */
.status-card {
    background: #0d120d; border: 1px solid #1a2e1a; border-radius: 12px; 
    padding: 20px; text-align: center; margin-bottom: 15px;
}
.sync-card {
    background: #0d120d; border-left: 4px solid #4ade80; border-radius: 8px;
    padding: 15px; margin-bottom: 20px;
}

/* Rest of UI components */
.topbar { background: #0d120d; border: 1px solid #1a2e1a; border-radius: 16px; padding: 1rem 1.5rem; margin-bottom: 1.5rem; display: flex; align-items: center; justify-content: space-between; }
.bubble { padding: 1.2rem; border-radius: 14px; margin-bottom: 1rem; font-size: 14px; max-width: 85%; }
.bubble-ai { background: #0d120d; border-left: 4px solid #4ade80; color: #d1d5db; }
.bubble-user { background: #0f1a0f; border-right: 4px solid #58a6ff; margin-left: auto; color: #ffffff; }
</style>
""", unsafe_allow_html=True)

# --- Sidebar Logic ---
with st.sidebar:
    st.caption("app")
    
    # Custom Navigation Menu based on your image
    st.markdown("""
    <a href="#" class="nav-item">🚨 Emergency</a>
    <a href="#" class="nav-item">Heart Disease</a>
    <a href="#" class="nav-item">Xray Analysis</a>
    <a href="#" class="nav-item nav-active">Health Chatbot</a>
    <a href="#" class="nav-item">BMI Calculator</a>
    <a href="#" class="nav-item">Health Tips</a>
    <a href="#" class="nav-item">Risk Gauge</a>
    <a href="#" class="nav-item">Symptom Checker</a>
    <a href="#" class="nav-item">Medical History</a>
    <a href="#" class="nav-item">Patient Report</a>
    <a href="#" class="nav-item">Find Doctor</a>
    <hr style="border-color: #1a2e1a; margin: 20px 0;">
    """, unsafe_allow_html=True)

    # Status Box from your image
    st.markdown(f"""
    <div class="status-card">
        <h3 style="color: #4ade80; margin:0; font-size: 18px;">📊 STATUS</h3>
        <p style="color: rgba(255,255,255,0.4); font-size: 12px; margin-top:10px;">Diagnostic Node Active</p>
    </div>
    """, unsafe_allow_html=True)

    # Sync Time Box from your image
    st.markdown(f"""
    <div class="sync-card">
        <div style="color: rgba(255,255,255,0.4); font-size: 10px; text-transform: uppercase;">Last Sync Time</div>
        <div style="color: white; font-size: 22px; font-weight: 700; font-family: 'JetBrains Mono';">
            {datetime.datetime.now().strftime('%H:%M:%S')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<h4 style='font-size:14px;'>🛠️ System Control</h4>", unsafe_allow_html=True)
    
    if st.button("🗑️ PURGE SESSION DATA", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown(f"""
    <div style="font-size: 10px; color: #4ade80; opacity: 0.5; margin-top: 20px;">
        CLINIQ OS v4.5.2 | STABLE_BUILD
    </div>
    """, unsafe_allow_html=True)

# --- Main Page Content ---
# (Yahan aapka purana main screen logic (tabs/chat) chalega)

st.markdown("""
<div class="topbar">
    <div>
        <div style="font-size: 20px; font-weight: 700; color: white;">🤖 ClinIQ Clinical Intelligence</div>
        <div style="font-size: 12px; color: rgba(255,255,255,0.4);">Advanced Diagnostic Node v4.5</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize chat if not exists
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Simple Chat Display
chat_box = st.container(height=500, border=False)
with chat_box:
    for m in st.session_state.chat_history:
        cls = "bubble-user" if m["role"] == "user" else "bubble-ai"
        st.markdown(f'<div class="bubble {cls}">{m["content"]}</div>', unsafe_allow_html=True)

query = st.chat_input("Kaise madad kar sakta hoon?")
if query:
    st.session_state.chat_history.append({"role": "user", "content": query})
    # AI logic yahan aayega (requests.post etc.)
    st.session_state.chat_history.append({"role": "assistant", "content": "Analyzing context..."})
    st.rerun()
