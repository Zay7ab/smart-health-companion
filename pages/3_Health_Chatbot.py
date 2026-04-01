import streamlit as st
import requests
import datetime
import sys
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="ClinIQ | Clinical Intelligence",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar Navigation ---
sys.path.append('.')
try:
    from utils.sidebar import load_sidebar
    load_sidebar()
except Exception:
    pass

# --- Advanced Dark Neon CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono&display=swap');

* { font-family: 'Inter', sans-serif; }
.stApp { background: #0a0f0a !important; }

/* Header Section */
.topbar { 
    background: #0d120d; border: 1px solid #1a2e1a; border-radius: 16px; 
    padding: 1.25rem 1.5rem; margin-bottom: 1.5rem; 
    display: flex; align-items: center; justify-content: space-between; 
}
.topbar-title { font-size: 20px; font-weight: 700; color: #ffffff; }

/* Section Labels */
.section-header {
    font-size: 11px; font-weight: 700; color: #4ade80; 
    text-transform: uppercase; letter-spacing: 1.5px; 
    margin-bottom: 1rem; margin-top: 1rem;
    display: flex; align-items: center; gap: 8px;
}
.section-line { height: 1px; background: #1a2e1a; flex-grow: 1; }

/* Vitals Observation Deck */
.vital-card-container {
    background: #0d120d; border: 1px solid #1a2e1a; border-radius: 14px; 
    padding: 1.2rem; text-align: center; border-top: 2px solid #4ade80;
    transition: 0.3s;
}
.vital-label { font-size: 10px; color: rgba(255,255,255,0.4); text-transform: uppercase; font-weight: 800; margin-bottom: 8px; }
.vital-value { font-family: 'JetBrains Mono'; font-size: 24px; color: #ffffff; font-weight: 700; }
.vital-unit { font-size: 14px; color: #ffffff; font-weight: 500; margin-left: 4px; }

/* Popover Button Styling */
div[data-testid="stPopover"] > button {
    background: transparent !important; border: 1px solid #1a2e1a !important;
    color: #4ade80 !important; font-size: 10px !important; 
    border-radius: 20px !important; margin-top: 10px !important;
}

/* Chat Styling */
.bubble { padding: 1.25rem; border-radius: 14px; margin-bottom: 1rem; line-height: 1.7; font-size: 14px; max-width: 85%; }
.bubble-ai { background: #0d120d; border: 1px solid #1a2e1a; border-left: 4px solid #4ade80; color: rgba(255,255,255,0.8); }
.bubble-user { background: #0f1a0f; border: 1px solid #1a2e1a; margin-left: auto; border-right: 4px solid #58a6ff; color: #ffffff; }

/* AI Badge */
.ai-badge { 
    display: inline-flex; align-items: center; gap: 6px; 
    background: rgba(74,222,128,0.1); border: 1px solid rgba(74,222,128,0.2); 
    border-radius: 20px; padding: 5px 12px; font-size: 11px; color: #4ade80; font-weight: 600; 
}
.ai-dot { width: 6px; height: 6px; border-radius: 50%; background: #4ade80; display: inline-block; animation: blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }
</style>
""", unsafe_allow_html=True)

# --- Initialize State ---
if 'bp' not in st.session_state: st.session_state.bp = "120/80"
if 'hr' not in st.session_state: st.session_state.hr = 72
if 'temp' not in st.session_state: st.session_state.temp = 98.6
if 'ox' not in st.session_state: st.session_state.ox = 98
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# --- 1. Global Header ---
st.markdown(f"""
<div class="topbar">
    <div>
        <div class="topbar-title">🤖 ClinIQ Clinical Center</div>
        <div style="font-size: 12px; color: rgba(255,255,255,0.4);">Diagnostic Interface v3.5</div>
    </div>
    <div class="ai-badge"><span class="ai-dot"></span> FastAPI + Groq AI Active</div>
</div>
""", unsafe_allow_html=True)

# --- 2. Vitals Observation Deck (The Different Section) ---
st.markdown('<div class="section-header">📡 Vitals Observation Deck <div class="section-line"></div></div>', unsafe_allow_html=True)

v_cols = st.columns(4)

vitals_data = [
    {"label": "Blood Pressure", "val": st.session_state.bp, "unit": "", "key": "bp", "type": "text"},
    {"label": "Heart Rate", "val": st.session_state.hr, "unit": "BPM", "key": "hr", "type": "num"},
    {"label": "Body Temp", "val": st.session_state.temp, "unit": "°F", "key": "temp", "type": "num"},
    {"label": "Oxygen Sat.", "val": st.session_state.ox, "unit": "%", "key": "ox", "type": "num"}
]

for i, vital in enumerate(vitals_data):
    with v_cols[i]:
        st.markdown(f"""<div class="vital-card-container">
            <div class="vital-label">{vital['label']}</div>
            <div class="vital-value">{vital['val']} <span class="vital-unit">{vital['unit']}</span></div>
        </div>""", unsafe_allow_html=True)
        
        with st.popover(f"Edit {vital['label']}"):
            if vital['type'] == "text":
                new_val = st.text_input(f"New {vital['label']}", value=vital['val'])
            else:
                new_val = st.number_input(f"New {vital['label']}", value=float(vital['val']), step=0.1 if vital['key']=='temp' else 1.0)
            
            if st.button(f"Update {vital['key'].upper()}"):
                st.session_state[vital['key']] = new_val
                st.rerun()

# --- 3. Intelligence & Diagnostics Section ---
st.markdown('<div style="margin-top:2rem;"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">🧠 Intelligence & Diagnostics <div class="section-line"></div></div>', unsafe_allow_html=True)

tab_chat, tab_reports = st.tabs(["💬 Clinical Chat", "📄 Diagnostic Reports"])

with tab_chat:
    chat_container = st.container()
    with chat_container:
        st.markdown("""
        <div class="bubble bubble-ai">
            <div style="font-size:11px; font-weight:700; color:#4ade80; margin-bottom:8px; text-transform:uppercase;">ClinIQ Intelligence</div>
            Patient vitals are currently synced from the Observation Deck. Please describe symptoms or clinical concerns.
        </div>
        """, unsafe_allow_html=True)
        
        for m in st.session_state.chat_history:
            cls = "bubble-user" if m["role"] == "user" else "bubble-ai"
            lbl = "Patient" if m["role"] == "user" else "AI Insight"
            clr = "#58a6ff" if m["role"] == "user" else "#4ade80"
            st.markdown(f'<div class="bubble {cls}"><div style="font-size:11px; font-weight:700; color:{clr}; margin-bottom:8px;">{lbl.upper()}</div>{m["content"]}</div>', unsafe_allow_html=True)

    query = st.chat_input("Enter symptoms or medication names...")
    if query:
        st.session_state.chat_history.append({"role": "user", "content": query})
        # AI logic would go here
        st.rerun()

with tab_reports:
    st.markdown("### 📄 Diagnostic Report Hub")
    st.file_uploader("Upload Medical Reports (PDF, PNG, JPG)", type=["pdf", "png", "jpg"])

# Sidebar Footer
with st.sidebar:
    st.markdown("### 📊 System Status")
    st.write(f"Vitals Synced: {datetime.datetime.now().strftime('%H:%M:%S')}")
    if st.button("Reset Session"):
        st.session_state.chat_history = []
        st.rerun()

st.markdown("""
<div style="margin-top: 4rem; padding: 1rem; border-top: 1px solid #1a2e1a; text-align: center; color: rgba(255,255,255,0.2); font-size: 10px;">
    ClinIQ Systems | Data Encrypted | Not a substitute for professional medical advice.
</div>
""", unsafe_allow_html=True)
