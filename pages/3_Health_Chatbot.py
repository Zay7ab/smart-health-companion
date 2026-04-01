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

# --- Custom CSS (Exact Screenshot Style + Button Styling) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono&display=swap');

* { font-family: 'Inter', sans-serif; }
.stApp { background: #0a0f0a !important; }

/* Topbar Styling */
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

/* Vitals Card Styling */
.vital-card-container {
    background: #0d120d; border: 1px solid #1a2e1a; border-radius: 14px; 
    padding: 1rem; text-align: center; border-top: 2px solid #4ade80;
    height: 100%;
}
.vital-label { font-size: 10px; color: rgba(255,255,255,0.4); text-transform: uppercase; font-weight: 800; margin-bottom: 8px; letter-spacing: 0.5px; }
.vital-value { font-family: 'JetBrains Mono'; font-size: 22px; color: #ffffff; font-weight: 700; }
.vital-unit { font-size: 14px; color: #ffffff; font-weight: 500; margin-left: 4px; }

/* Edit Button Overrides */
div[data-testid="stPopover"] > button {
    background-color: transparent !important;
    border: 1px solid #1a2e1a !important;
    color: #4ade80 !important;
    font-size: 10px !important;
    padding: 2px 10px !important;
    margin-top: 10px !important;
    border-radius: 20px !important;
}
div[data-testid="stPopover"] > button:hover {
    border-color: #4ade80 !important;
    background: rgba(74,222,128,0.05) !important;
}

/* Chat Styling */
.bubble { padding: 1.25rem; border-radius: 14px; margin-bottom: 1rem; line-height: 1.7; font-size: 14px; max-width: 85%; }
.bubble-ai { background: #0d120d; border: 1px solid #1a2e1a; border-left: 4px solid #4ade80; color: rgba(255,255,255,0.8); }
.bubble-user { background: #0f1a0f; border: 1px solid #1a2e1a; margin-left: auto; border-right: 4px solid #58a6ff; color: #ffffff; }
</style>
""", unsafe_allow_html=True)

# --- Initialize Session State ---
if 'bp' not in st.session_state: st.session_state.bp = "120/80"
if 'hr' not in st.session_state: st.session_state.hr = 72
if 'temp' not in st.session_state: st.session_state.temp = 98.6
if 'ox' not in st.session_state: st.session_state.ox = 98
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# --- Header ---
st.markdown(f"""
<div class="topbar">
    <div>
        <div class="topbar-title">🤖 ClinIQ Clinical Center</div>
        <div style="font-size: 12px; color: rgba(255,255,255,0.4);">Click 'Edit' on cards to update vitals</div>
    </div>
    <div class="ai-badge"><span class="ai-dot"></span> FastAPI + Groq AI Active</div>
</div>
""", unsafe_allow_html=True)

# --- Vitals Display with Edit Buttons ---
cols = st.columns(4)

# 1. Blood Pressure Card
with cols[0]:
    st.markdown(f"""<div class="vital-card-container">
        <div class="vital-label">Blood Pressure</div>
        <div class="vital-value">{st.session_state.bp}</div>
    </div>""", unsafe_allow_html=True)
    with st.popover("Edit BP"):
        st.text_input("Update BP", value=st.session_state.bp, key="new_bp")
        if st.button("Save BP"):
            st.session_state.bp = st.session_state.new_bp
            st.rerun()

# 2. Heart Rate Card
with cols[1]:
    st.markdown(f"""<div class="vital-card-container">
        <div class="vital-label">Heart Rate</div>
        <div class="vital-value">{st.session_state.hr} <span class="vital-unit">BPM</span></div>
    </div>""", unsafe_allow_html=True)
    with st.popover("Edit HR"):
        st.number_input("Update HR", value=st.session_state.hr, key="new_hr")
        if st.button("Save HR"):
            st.session_state.hr = st.session_state.new_hr
            st.rerun()

# 3. Body Temp Card
with cols[2]:
    st.markdown(f"""<div class="vital-card-container">
        <div class="vital-label">Body Temp</div>
        <div class="vital-value">{st.session_state.temp} <span class="vital-unit">°F</span></div>
    </div>""", unsafe_allow_html=True)
    with st.popover("Edit Temp"):
        st.number_input("Update Temp", value=st.session_state.temp, format="%.1f", key="new_temp")
        if st.button("Save Temp"):
            st.session_state.temp = st.session_state.new_temp
            st.rerun()

# 4. Oxygen Sat Card
with cols[3]:
    st.markdown(f"""<div class="vital-card-container">
        <div class="vital-label">Oxygen Sat.</div>
        <div class="vital-value">{st.session_state.ox}%</div>
    </div>""", unsafe_allow_html=True)
    with st.popover("Edit SpO2"):
        st.number_input("Update Oxygen %", value=st.session_state.ox, key="new_ox")
        if st.button("Save SpO2"):
            st.session_state.ox = st.session_state.new_ox
            st.rerun()

# --- Tabs: Chat & Reports ---
tab_chat, tab_reports = st.tabs(["💬 Clinical Chat", "📄 Diagnostic Reports"])

with tab_chat:
    display_chat = st.container()
    with display_chat:
        st.markdown('<div class="bubble bubble-ai"><div style="font-size:11px; font-weight:700; color:#4ade80; margin-bottom:8px; text-transform:uppercase;">ClinIQ Intelligence</div>Assistant active. You can edit vitals directly above. How can I help?</div>', unsafe_allow_html=True)
        for m in st.session_state.chat_history:
            cls = "bubble-user" if m["role"] == "user" else "bubble-ai"
            st.markdown(f'<div class="bubble {cls}">{m["content"]}</div>', unsafe_allow_html=True)

    query = st.chat_input("Enter clinical symptoms...")
    if query:
        st.session_state.chat_history.append({"role": "user", "content": query})
        # AI Logic Call here...
        st.rerun()

with tab_reports:
    st.markdown("### 📄 Diagnostic Reports Center")
    st.file_uploader("Upload Lab Reports", type=["pdf", "png", "jpg"])

# Sidebar (Navigation and Background Info)
with st.sidebar:
    st.markdown("### 📊 System Status")
    st.write(f"Last Updated: {datetime.datetime.now().strftime('%H:%M:%S')}")
    if st.button("Reset Session"):
        st.session_state.chat_history = []
        st.rerun()
