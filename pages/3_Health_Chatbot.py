import streamlit as st
import requests
import datetime
import sys
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="ClinIQ | Clinical AI Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar Logic ---
sys.path.append('.')
try:
    from utils.sidebar import load_sidebar
    load_sidebar()
except Exception:
    pass

# --- Custom CSS (Exact Screenshot Style) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono&display=swap');

* { font-family: 'Inter', sans-serif; }
.stApp { background: #0a0f0a !important; }

/* Header Bar */
.topbar { 
    background: #0d120d; border: 1px solid #1a2e1a; border-radius: 16px; 
    padding: 1.25rem 1.5rem; margin-bottom: 1.5rem; 
    display: flex; align-items: center; justify-content: space-between; 
}
.topbar-title { font-size: 20px; font-weight: 700; color: #ffffff; }

/* AI Badge */
.ai-badge { 
    display: inline-flex; align-items: center; gap: 6px; 
    background: rgba(74,222,128,0.1); border: 1px solid rgba(74,222,128,0.2); 
    border-radius: 20px; padding: 5px 12px; font-size: 11px; color: #4ade80; font-weight: 600; 
}
.ai-dot { width: 6px; height: 6px; border-radius: 50%; background: #4ade80; display: inline-block; animation: blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* Vitals Cards (Matches Image) */
.vitals-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 2rem; }
.vital-card { 
    background: #0d120d; border: 1px solid #1a2e1a; border-radius: 14px; 
    padding: 1.5rem 1rem; text-align: center; border-top: 2px solid #4ade80;
    transition: 0.3s;
}
.vital-label { font-size: 10px; color: rgba(255,255,255,0.4); text-transform: uppercase; font-weight: 800; margin-bottom: 8px; letter-spacing: 0.5px; }
.vital-value { font-family: 'JetBrains Mono'; font-size: 22px; color: #ffffff; font-weight: 700; }
.vital-unit { font-size: 14px; color: #ffffff; font-weight: 500; margin-left: 4px; }

/* Chat Bubbles */
.bubble { padding: 1.25rem; border-radius: 14px; margin-bottom: 1rem; line-height: 1.7; font-size: 14px; max-width: 85%; }
.bubble-ai { background: #0d120d; border: 1px solid #1a2e1a; border-left: 4px solid #4ade80; color: rgba(255,255,255,0.8); }
.bubble-user { background: #0f1a0f; border: 1px solid #1a2e1a; margin-left: auto; border-right: 4px solid #58a6ff; color: #ffffff; }

/* Tabs Styling */
.stTabs [data-baseweb="tab-list"] { gap: 24px; background-color: transparent; }
.stTabs [data-baseweb="tab"] { color: rgba(255,255,255,0.5); font-weight: 600; }
.stTabs [aria-selected="true"] { color: #4ade80 !important; border-bottom: 2px solid #4ade80 !important; }

/* Inputs Overrides */
div[data-testid="stChatInput"] { background-color: #0d120d !important; border: 1px solid #1a2e1a !important; }
input { color: white !important; }
</style>
""", unsafe_allow_html=True)

# --- Session State Management ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Sidebar (Settings) ---
with st.sidebar:
    st.markdown("### ⚙️ Patient Vitals Settings")
    # Using specific keys to ensure session state updates
    st.session_state.sb_bp = st.text_input("Blood Pressure", value="120/80")
    st.session_state.sb_hr = st.number_input("Heart Rate (BPM)", value=72)
    st.session_state.sb_temp = st.number_input("Body Temp (°F)", value=98.6)
    st.session_state.sb_ox = st.number_input("Oxygen Sat (%)", value=98)
    
    if st.button("🗑️ Reset All Sessions"):
        st.session_state.chat_history = []
        st.rerun()

# --- UI Header ---
st.markdown(f"""
<div class="topbar">
    <div>
        <div class="topbar-title">🤖 ClinIQ Clinical Center</div>
        <div style="font-size: 12px; color: rgba(255,255,255,0.4);">Advanced Diagnostic Node v3.2</div>
    </div>
    <div class="ai-badge"><span class="ai-dot"></span> FastAPI + Groq AI Active</div>
</div>
""", unsafe_allow_html=True)

# --- Main Dashboard: Vitals (Instantly updating from Sidebar) ---
st.markdown(f"""
<div class="vitals-grid">
    <div class="vital-card">
        <div class="vital-label">Blood Pressure</div>
        <div class="vital-value">{st.session_state.sb_bp}</div>
    </div>
    <div class="vital-card">
        <div class="vital-label">Heart Rate</div>
        <div class="vital-value">{st.session_state.sb_hr} <span class="vital-unit">BPM</span></div>
    </div>
    <div class="vital-card">
        <div class="vital-label">Body Temp</div>
        <div class="vital-value">{st.session_state.sb_temp} <span class="vital-unit">°F</span></div>
    </div>
    <div class="vital-card">
        <div class="vital-label">Oxygen Sat.</div>
        <div class="vital-value">{st.session_state.sb_ox}%</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Tabs: Chat & Reports ---
tab_chat, tab_reports = st.tabs(["💬 Clinical Chat", "📄 Diagnostic Reports"])

with tab_chat:
    display_chat = st.container()
    with display_chat:
        st.markdown("""
        <div class="bubble bubble-ai">
            <div style="font-size:11px; font-weight:700; color:#4ade80; margin-bottom:8px; text-transform:uppercase;">ClinIQ Intelligence</div>
            Diagnostic environment initialized. Your current vitals are monitored. How can I assist you?
        </div>
        """, unsafe_allow_html=True)
        for m in st.session_state.chat_history:
            cls = "bubble-user" if m["role"] == "user" else "bubble-ai"
            lbl = "Patient" if m["role"] == "user" else "Clinical Insight"
            clr = "#58a6ff" if m["role"] == "user" else "#4ade80"
            st.markdown(f'<div class="bubble {cls}"><div style="font-size:11px; font-weight:700; color:{clr}; margin-bottom:8px;">{lbl.upper()}</div>{m["content"]}</div>', unsafe_allow_html=True)

    query = st.chat_input("Enter clinical symptoms...")
    if query:
        st.session_state.chat_history.append({"role": "user", "content": query})
        # AI call logic goes here (requests.post...)
        st.rerun()

with tab_reports:
    st.markdown("### 📄 Diagnostic Reports Center")
    uploaded_file = st.file_uploader("Upload Reports", type=["pdf", "png", "jpg"])
    if uploaded_file:
        st.info("Analysis of diagnostic report in progress...")
