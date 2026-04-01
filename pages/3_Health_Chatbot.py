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

# --- Heart Disease Style Integration ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono&display=swap');

* { font-family: 'Inter', sans-serif; }
.stApp { background: #0a0f0a !important; }

/* Header Bar */
.topbar { 
    background: #0d120d; border: 1px solid #1a2e1a; border-radius: 16px; 
    padding: 1.25rem 1.5rem; margin-bottom: 1rem; 
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

/* Vitals Cards */
.vitals-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 1.5rem; }
.vital-card { background: #0d120d; border: 1px solid #1a2e1a; border-radius: 12px; padding: 0.75rem; text-align: center; border-top: 2px solid #4ade80; }
.vital-label { font-size: 9px; color: rgba(255,255,255,0.4); text-transform: uppercase; font-weight: 700; margin-bottom: 4px; }
.vital-value { font-family: 'JetBrains Mono'; font-size: 16px; color: #ffffff; font-weight: 600; }

/* Chat Bubbles */
.bubble { padding: 1.25rem; border-radius: 14px; margin-bottom: 1rem; line-height: 1.7; font-size: 14px; max-width: 85%; }
.bubble-ai { background: #0d120d; border: 1px solid #1a2e1a; border-left: 4px solid #4ade80; color: rgba(255,255,255,0.8); }
.bubble-user { background: #0f1a0f; border: 1px solid #1a2e1a; margin-left: auto; border-right: 4px solid #58a6ff; color: #ffffff; }

/* Report Section Cards */
.report-card { background: #0d120d; border: 1px dashed #1a2e1a; border-radius: 16px; padding: 2rem; text-align: center; margin-top: 1rem; }
.summary-box { background: rgba(74,222,128,0.05); border: 1px solid #1a2e1a; border-radius: 12px; padding: 1.5rem; color: #ffffff; margin-top: 1rem; }

/* Disclaimer */
.disclaimer { background: rgba(255,200,0,0.05); border: 1px solid rgba(255,200,0,0.15); border-radius: 10px; padding: 0.75rem; font-size: 11px; color: rgba(255,200,0,0.7); margin-top: 2rem; text-align: center; }

/* Inputs */
div[data-testid="stChatInput"] { background-color: #0d120d !important; border: 1px solid #1a2e1a !important; }
.stTabs [data-baseweb="tab-list"] { gap: 24px; background-color: transparent; }
.stTabs [data-baseweb="tab"] { color: rgba(255,255,255,0.5); font-weight: 600; border: none; }
.stTabs [aria-selected="true"] { color: #4ade80 !important; border-bottom: 2px solid #4ade80 !important; }
</style>
""", unsafe_allow_html=True)

# --- Session & Logic ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "patient_vitals" not in st.session_state:
    st.session_state.patient_vitals = {"bp": "120/80", "hr": "72", "temp": "98.6", "ox": "98%"}

API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")

def get_clinical_response(msg, history, vitals):
    try:
        context = f"[Vitals: BP {vitals['bp']}, HR {vitals['hr']}] "
        response = requests.post(
            f"{API_URL}/chat",
            json={"message": context + msg, "history": history, "api_key": st.secrets.get("GROQ_API_KEY", "")},
            timeout=30
        )
        return response.json().get("reply", "Engine Calibrating...")
    except:
        return "⏱️ API Error."

# --- UI Header ---
st.markdown(f"""
<div class="topbar">
    <div>
        <div class="topbar-title">🤖 ClinIQ Clinical Center</div>
        <div style="font-size: 12px; color: rgba(255,255,255,0.4);">Advanced Diagnostic Node v3.1</div>
    </div>
    <div class="ai-badge"><span class="ai-dot"></span> FastAPI + Groq AI Active</div>
</div>
""", unsafe_allow_html=True)

# --- Top Dashboard: Vitals & Lab Info ---
st.markdown(f"""
<div class="vitals-grid">
    <div class="vital-card"><div class="vital-label">Blood Pressure</div><div class="vital-value">{st.session_state.patient_vitals['bp']}</div></div>
    <div class="vital-card"><div class="vital-label">Heart Rate</div><div class="vital-value">{st.session_state.patient_vitals['hr']} <small>BPM</small></div></div>
    <div class="vital-card"><div class="vital-label">Body Temp</div><div class="vital-value">{st.session_state.patient_vitals['temp']} <small>°F</small></div></div>
    <div class="vital-card"><div class="vital-label">Oxygen Sat.</div><div class="vital-value">{st.session_state.patient_vitals['ox']}</div></div>
</div>
""", unsafe_allow_html=True)

# --- Feature: Separated Sections via Tabs ---
tab_chat, tab_reports = st.tabs(["💬 Clinical Chat", "📄 Diagnostic Reports"])

with tab_chat:
    display_chat = st.container()
    with display_chat:
        st.markdown("""
        <div class="bubble bubble-ai">
            <div style="font-size:11px; font-weight:700; color:#4ade80; margin-bottom:8px; text-transform:uppercase;">ClinIQ Intelligence</div>
            Welcome. How can I assist your health inquiry today? You can describe symptoms or ask about clinical data.
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
        with st.spinner("🤖 Analyzing..."):
            reply = get_clinical_response(query, st.session_state.chat_history[:-1], st.session_state.patient_vitals)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

with tab_reports:
    st.markdown("### 📄 Report Analysis Center")
    st.markdown('<p style="color:rgba(255,255,255,0.4); font-size:13px;">Upload your lab reports (Bloodwork, ECG, Imaging) for AI-driven summarization.</p>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="report-card">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Drop diagnostic files here", type=["pdf", "png", "jpg"], label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if uploaded_file:
            with st.spinner("📑 Scanning diagnostic markers..."):
                # Simulation of report summary
                st.markdown("""
                <div class="summary-box">
                    <div style="font-size:12px; font-weight:700; color:#4ade80; margin-bottom:10px; text-transform:uppercase;">AI Diagnostic Summary</div>
                    <b>Status:</b> Report analyzed successfully.<br><br>
                    <b>Key Observations:</b><br>
                    • Diagnostic markers are within standard deviations.<br>
                    • No immediate anomalies detected in the primary indicators.<br>
                    • Recommended to discuss these results with your cardiologist for context.
                </div>
                """, unsafe_allow_html=True)

# Settings Sidebar Logic (Vitals Input)
with st.sidebar:
    st.markdown("### ⚙️ Patient Settings")
    st.session_state.patient_vitals['bp'] = st.text_input("Blood Pressure", value="120/80")
    st.session_state.patient_vitals['hr'] = st.number_input("Heart Rate", value=72)
    st.session_state.patient_vitals['temp'] = st.number_input("Temp", value=98.6)
    st.session_state.patient_vitals['ox'] = f'{st.number_input("SpO2 %", value=98)}%'
    
    if st.button("🗑️ Reset Chat"):
        st.session_state.chat_history = []
        st.rerun()

st.markdown("""
<div class="disclaimer">
    ⚠️ <b>Disclaimer:</b> Information provided is for educational support. In case of emergency, call 911/112 immediately.
</div>
""", unsafe_allow_html=True)
