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

/* Professional Vitals Row */
.vitals-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 1rem; }
.vital-card { background: #0d120d; border: 1px solid #1a2e1a; border-radius: 12px; padding: 0.75rem; text-align: center; }
.vital-label { font-size: 9px; color: #4ade80; text-transform: uppercase; font-weight: 700; margin-bottom: 4px; }
.vital-value { font-family: 'JetBrains Mono'; font-size: 16px; color: #ffffff; font-weight: 600; }

/* Chat Bubbles */
.bubble { padding: 1.25rem; border-radius: 14px; margin-bottom: 1rem; line-height: 1.7; font-size: 14px; max-width: 85%; }
.bubble-ai { background: #0d120d; border: 1px solid #1a2e1a; border-left: 4px solid #4ade80; color: rgba(255,255,255,0.8); }
.bubble-user { background: #0f1a0f; border: 1px solid #1a2e1a; margin-left: auto; border-right: 4px solid #58a6ff; color: #ffffff; }

/* Disclaimer */
.disclaimer { background: rgba(255,200,0,0.05); border: 1px solid rgba(255,200,0,0.15); border-radius: 10px; padding: 0.75rem; font-size: 11px; color: rgba(255,200,0,0.7); margin-top: 1rem; text-align: center; }

/* Inputs Fix */
div[data-testid="stChatInput"] { background-color: #0d120d !important; border: 1px solid #1a2e1a !important; }
label { color: #4ade80 !important; font-size: 12px !important; font-weight: 600; }
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
        # Injecting Vitals into the prompt for smarter AI responses
        context = f"[System Context: Patient BP: {vitals['bp']}, HR: {vitals['hr']}, SpO2: {vitals['ox']}] "
        full_msg = context + msg
        
        response = requests.post(
            f"{API_URL}/chat",
            json={"message": full_msg, "history": history, "api_key": st.secrets.get("GROQ_API_KEY", "")},
            timeout=30
        )
        return response.json().get("reply", "Clinical Intelligence Syncing...")
    except:
        return "⏱️ API Error. Check connectivity."

# --- UI Header ---
st.markdown(f"""
<div class="topbar">
    <div>
        <div class="topbar-title">🤖 AI Clinical Intelligence</div>
        <div style="font-size: 12px; color: rgba(255,255,255,0.4);">Advanced Diagnostic Assistant v3.0</div>
    </div>
    <div class="ai-badge"><span class="ai-dot"></span> FastAPI + Groq AI Active</div>
</div>
""", unsafe_allow_html=True)

# --- Feature 1: Clinical Data Inputs ---
with st.expander("📊 Patient Vitals & Lab Data", expanded=False):
    v1, v2, v3, v4 = st.columns(4)
    with v1:
        bp = st.text_input("Blood Pressure", value="120/80")
    with v2:
        hr = st.number_input("Heart Rate (BPM)", value=72)
    with v3:
        temp = st.number_input("Body Temp (°F)", value=98.6)
    with v4:
        ox = st.number_input("SpO2 (%)", value=98)
    
    st.session_state.patient_vitals = {"bp": bp, "hr": hr, "temp": temp, "ox": f"{ox}%"}
    
    st.file_uploader("📂 Upload Lab Reports (PDF/IMG) for Analysis", type=["pdf", "png", "jpg"])

# --- Feature 2: Live Vitals Display ---
st.markdown(f"""
<div class="vitals-grid">
    <div class="vital-card"><div class="vital-label">Blood Pressure</div><div class="vital-value">{st.session_state.patient_vitals['bp']}</div></div>
    <div class="vital-card"><div class="vital-label">Heart Rate</div><div class="vital-value">{st.session_state.patient_vitals['hr']} <small>BPM</small></div></div>
    <div class="vital-card"><div class="vital-label">Temp</div><div class="vital-value">{st.session_state.patient_vitals['temp']} <small>°F</small></div></div>
    <div class="vital-card"><div class="vital-label">SpO2</div><div class="vital-value">{st.session_state.patient_vitals['ox']}</div></div>
</div>
""", unsafe_allow_html=True)

# Chat Area
display_area = st.container()

with display_area:
    st.markdown("""
    <div class="bubble bubble-ai">
        <div style="font-size:11px; font-weight:700; color:#4ade80; margin-bottom:8px; text-transform:uppercase;">ClinIQ Intelligence</div>
        Clinical session active. Vitals are synced. Please describe your symptoms or provide medication names for interaction analysis.
    </div>
    """, unsafe_allow_html=True)

    for m in st.session_state.chat_history:
        is_user = m["role"] == "user"
        cls = "bubble-user" if is_user else "bubble-ai"
        lbl = "Patient Query" if is_user else "Clinical Insight"
        clr = "#58a6ff" if is_user else "#4ade80"
        
        st.markdown(f"""
        <div class="bubble {cls}">
            <div style="font-size:11px; font-weight:700; color:{clr}; margin-bottom:8px; text-transform:uppercase;">{lbl}</div>
            {m['content']}
        </div>
        """, unsafe_allow_html=True)

# --- Feature 3: Action Buttons ---
col_btn1, col_btn2 = st.columns([1, 1])
with col_btn1:
    if st.button("🗑️ Clear Clinical Session"):
        st.session_state.chat_history = []
        st.rerun()
with col_btn2:
    chat_txt = "\\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.chat_history])
    st.download_button("💾 Export Health Summary", data=chat_txt, file_name="health_summary.txt")

# Chat Input
query = st.chat_input("Enter clinical symptoms or drug names...")

if query:
    st.session_state.chat_history.append({"role": "user", "content": query})
    with st.spinner("🤖 Analyzing data..."):
        # Passing current vitals to the API call
        reply = get_clinical_response(query, st.session_state.chat_history[:-1], st.session_state.patient_vitals)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

st.markdown("""
<div class="disclaimer">
    ⚠️ <b>Clinical Disclaimer:</b> This tool is for informational support. In case of cardiac distress or emergency, call your local medical services (911/112) immediately.
</div>
""", unsafe_allow_html=True)
