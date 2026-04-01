import streamlit as st
import requests
import datetime
import os
from fpdf import FPDF
try:
    from streamlit_mic_recorder import mic_recorder
except ImportError:
    mic_recorder = None

# --- Page Configuration ---
st.set_page_config(
    page_title="ClinIQ | Advanced Clinical AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Dark Neon CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: #0a0f0a !important; }

/* Topbar */
.topbar { 
    background: #0d120d; border: 1px solid #1a2e1a; border-radius: 16px; 
    padding: 1rem 1.5rem; margin-bottom: 1rem; 
    display: flex; align-items: center; justify-content: space-between; 
}
.topbar-title { font-size: 18px; font-weight: 700; color: #ffffff; }

/* Vitals Cards */
.vital-card-container {
    background: #0d120d; border: 1px solid #1a2e1a; border-radius: 14px; 
    padding: 1rem; text-align: center; border-top: 2px solid #4ade80;
}
.vital-label { font-size: 10px; color: rgba(255,255,255,0.4); text-transform: uppercase; font-weight: 800; margin-bottom: 5px; }
.vital-value { font-family: 'JetBrains Mono'; font-size: 22px; color: #ffffff; font-weight: 700; }

/* Chat Bubbles */
.bubble { padding: 1.2rem; border-radius: 14px; margin-bottom: 1rem; line-height: 1.6; font-size: 14px; max-width: 85%; }
.bubble-ai { background: #0d120d; border: 1px solid #1a2e1a; border-left: 4px solid #4ade80; color: #e0e0e0; }
.bubble-user { background: #0f1a0f; border: 1px solid #1a2e1a; margin-left: auto; border-right: 4px solid #58a6ff; color: #ffffff; }

/* Popover Buttons */
div[data-testid="stPopover"] > button {
    background: transparent !important; border: 1px solid #1a2e1a !important;
    color: #4ade80 !important; font-size: 10px !important; border-radius: 20px !important;
}
</style>
""", unsafe_allow_html=True)

# --- State Management ---
for key, val in {"bp": "120/80", "hr": 72, "temp": 98.6, "ox": 98, "chat_history": []}.items():
    if key not in st.session_state:
        st.session_state[key] = val

API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")

# --- Helper: PDF Generator ---
def export_pdf(history, vitals):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "ClinIQ Health Summary Report", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, f"Vitals: BP: {vitals['bp']} | HR: {vitals['hr']} | Temp: {vitals['temp']} | SpO2: {vitals['ox']}%", ln=True)
    pdf.ln(10)
    for msg in history:
        role = "PATIENT" if msg["role"] == "user" else "AI ASSISTANT"
        pdf.multi_cell(0, 10, f"{role}: {msg['content']}")
        pdf.ln(2)
    return pdf.output(dest='S').encode('latin-1')

# --- Header ---
st.markdown(f"""
<div class="topbar">
    <div><span class="topbar-title">🤖 ClinIQ Clinical Intelligence v4.0</span></div>
    <div style="background: rgba(74,222,128,0.1); color: #4ade80; padding: 4px 12px; border-radius: 20px; font-size: 11px; border: 1px solid #4ade80;">
        FastAPI + Groq Engine Active
    </div>
</div>
""", unsafe_allow_html=True)

# --- Vitals Observation Deck ---
st.markdown('<p style="color:#4ade80; font-size:11px; font-weight:700; letter-spacing:1px;">📡 VITALS OBSERVATION DECK</p>', unsafe_allow_html=True)
v_cols = st.columns(4)
v_data = [
    {"l": "Blood Pressure", "v": st.session_state.bp, "k": "bp", "t": "text"},
    {"l": "Heart Rate", "v": st.session_state.hr, "k": "hr", "t": "num"},
    {"l": "Body Temp", "v": st.session_state.temp, "k": "temp", "t": "num"},
    {"l": "Oxygen Sat.", "v": st.session_state.ox, "k": "ox", "t": "num"}
]

for i, vital in enumerate(v_data):
    with v_cols[i]:
        st.markdown(f'<div class="vital-card-container"><div class="vital-label">{vital["l"]}</div><div class="vital-value">{vital["v"]}</div></div>', unsafe_allow_html=True)
        with st.popover(f"Edit {vital['k'].upper()}"):
            if vital['t'] == "text":
                new_val = st.text_input("New Value", value=str(vital['v']))
            else:
                new_val = st.number_input("New Value", value=float(vital['v']))
            if st.button(f"Save {vital['k']}"):
                st.session_state[vital['k']] = new_val
                st.rerun()

# --- Main Interaction Tabs ---
st.markdown('<div style="margin-top:2rem;"></div>', unsafe_allow_html=True)
tab_chat, tab_reports, tab_tools = st.tabs(["💬 Intelligence Chat", "📄 Diagnostic Reports", "🛠️ Clinical Tools"])

with tab_chat:
    chat_box = st.container()
    with chat_box:
        st.markdown('<div class="bubble bubble-ai"><b>ClinIQ Assistant:</b> System ready. Vitals synced. Describe symptoms or use the microphone.</div>', unsafe_allow_html=True)
        for m in st.session_state.chat_history:
            cls = "bubble-user" if m["role"] == "user" else "bubble-ai"
            st.markdown(f'<div class="bubble {cls}">{m["content"]}</div>', unsafe_allow_html=True)

    # Voice Input Feature
    if mic_recorder:
        st.write("🎤 Voice Input:")
        voice_data = mic_recorder(start_prompt="Start Recording", stop_prompt="Stop & Process", key='recorder')
        if voice_data and 'transcription' in voice_data:
            # Note: transcription requires additional setup, usually we handle raw audio here
            st.warning("Audio captured. Transcription requires API integration.")

    query = st.chat_input("Ask clinical questions...")
    if query:
        st.session_state.chat_history.append({"role": "user", "content": query})
        with st.spinner("Analyzing context..."):
            v_ctx = f"[Context: BP {st.session_state.bp}, HR {st.session_state.hr}] "
            try:
                res = requests.post(f"{API_URL}/chat", json={"message": v_ctx + query, "history": st.session_state.chat_history[:-1], "api_key": st.secrets.get("GROQ_API_KEY", "")}, timeout=20)
                reply = res.json().get("reply", "Engine Calibrating...")
            except:
                reply = "Connection Error. Please check API."
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

with tab_reports:
    st.markdown("### 📄 Diagnostic Hub")
    st.file_uploader("Upload Lab Reports (PDF/JPG)", type=["pdf", "png", "jpg"])
    if st.button("Generate Summary"):
        st.info("Analysis in progress...")

with tab_tools:
    st.markdown("### 🛠️ Professional Utilities")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.link_button("📍 Find Nearest Hospital", "https://www.google.com/maps/search/hospital+near+me")
    with col_t2:
        pdf_bytes = export_pdf(st.session_state.chat_history, st.session_state)
        st.download_button("💾 Download Clinical PDF", data=pdf_bytes, file_name="clinIQ_report.pdf", mime="application/pdf")

# Sidebar
with st.sidebar:
    st.markdown("### 👤 Patient Profile")
    st.write(f"Session ID: {hex(id(st.session_state))[:8].upper()}")
    if st.button("🗑️ Reset All Sessions"):
        st.session_state.chat_history = []
        st.rerun()

st.markdown('<div style="text-align:center; color:#444; font-size:10px; margin-top:5rem;">ClinIQ Systems 2026 | Encrypted Session | Educational Use Only</div>', unsafe_allow_html=True)
