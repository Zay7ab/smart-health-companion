import streamlit as st
import requests
import datetime
import os
import sys
from fpdf import FPDF

# --- Import Mic Recorder (Optional Feature) ---
try:
    from streamlit_mic_recorder import mic_recorder
except ImportError:
    mic_recorder = None

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
.stApp { background: #0a0f0a !important; }

/* Topbar */
.topbar { 
    background: #0d120d; border: 1px solid #1a2e1a; border-radius: 16px; 
    padding: 1rem 1.5rem; margin-bottom: 1.5rem; 
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

/* Section Headers */
.section-header {
    font-size: 11px; font-weight: 700; color: #4ade80; 
    text-transform: uppercase; letter-spacing: 1.5px; 
    margin-bottom: 1rem; margin-top: 1rem;
    display: flex; align-items: center; gap: 8px;
}
.section-line { height: 1px; background: #1a2e1a; flex-grow: 1; }

/* Vitals Cards */
.vital-card-container {
    background: #0d120d; border: 1px solid #1a2e1a; border-radius: 14px; 
    padding: 1.2rem; text-align: center; border-top: 2px solid #4ade80;
}
.vital-label { font-size: 10px; color: rgba(255,255,255,0.4); text-transform: uppercase; font-weight: 800; margin-bottom: 8px; }
.vital-value { font-family: 'JetBrains Mono'; font-size: 24px; color: #ffffff; font-weight: 700; }
.vital-unit { font-size: 14px; color: #ffffff; font-weight: 500; margin-left: 4px; }

/* Popover Buttons */
div[data-testid="stPopover"] > button {
    background: transparent !important; border: 1px solid #1a2e1a !important;
    color: #4ade80 !important; font-size: 10px !important; 
    border-radius: 20px !important; margin-top: 10px !important; width: 100%;
}

/* Chat Bubbles */
.bubble { padding: 1.25rem; border-radius: 14px; margin-bottom: 1rem; line-height: 1.7; font-size: 14px; max-width: 85%; }
.bubble-ai { background: #0d120d; border: 1px solid #1a2e1a; border-left: 4px solid #4ade80; color: rgba(255,255,255,0.8); }
.bubble-user { background: #0f1a0f; border: 1px solid #1a2e1a; margin-left: auto; border-right: 4px solid #58a6ff; color: #ffffff; }

/* Disclaimer */
.disclaimer { background: rgba(255,200,0,0.05); border: 1px solid rgba(255,200,0,0.15); border-radius: 10px; padding: 0.75rem; font-size: 11px; color: rgba(255,200,0,0.7); margin-top: 2rem; text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- Initialize Session State ---
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

vitals_defaults = {'bp': "120/80", 'hr': 72.0, 'temp': 98.6, 'ox': 98.0}
for key, val in vitals_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")

# --- Helper: PDF Generator (Fixed for Streamlit) ---
def export_pdf(history, vitals):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "ClinIQ Health Summary Report", ln=True, align='C')
    pdf.ln(10)
    
    # Vitals Section
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Patient Vitals Observation:", ln=True)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, f"Blood Pressure: {vitals['bp']}", ln=True)
    pdf.cell(0, 8, f"Heart Rate: {vitals['hr']} BPM", ln=True)
    pdf.cell(0, 8, f"Body Temp: {vitals['temp']} F", ln=True)
    pdf.cell(0, 8, f"Oxygen Sat: {vitals['ox']}%", ln=True)
    pdf.ln(10)
    
    # Conversation Section
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Clinical Interaction Log:", ln=True)
    pdf.set_font("Arial", '', 10)
    
    for msg in history:
        role = "PATIENT" if msg["role"] == "user" else "AI ASSISTANT"
        # FPDF standard fonts don't support UTF-8 (emojis/special chars). 
        # We strip non-Latin-1 characters to prevent crashes.
        clean_txt = msg['content'].encode('latin-1', 'ignore').decode('latin-1')
        txt = f"{role}: {clean_txt}"
        pdf.multi_cell(0, 8, txt)
        pdf.ln(2)
    
    # IMPORTANT: Convert bytearray to bytes for Streamlit download
    return bytes(pdf.output())

# --- UI Header ---
st.markdown(f"""
<div class="topbar">
    <div>
        <div class="topbar-title">🤖 ClinIQ Clinical Intelligence</div>
        <div style="font-size: 12px; color: rgba(255,255,255,0.4);">Advanced Diagnostic Node v4.5</div>
    </div>
    <div class="ai-badge"><span class="ai-dot"></span> FastAPI + Groq AI Active</div>
</div>
""", unsafe_allow_html=True)

# --- Vitals Observation Deck ---
st.markdown('<div class="section-header">📡 Vitals Observation Deck <div class="section-line"></div></div>', unsafe_allow_html=True)
v_cols = st.columns(4)
v_meta = [
    {"label": "Blood Pressure", "key": "bp", "unit": ""},
    {"label": "Heart Rate", "key": "hr", "unit": "BPM"},
    {"label": "Body Temp", "key": "temp", "unit": "°F"},
    {"label": "Oxygen Sat.", "key": "ox", "unit": "%"}
]

for i, meta in enumerate(v_meta):
    with v_cols[i]:
        st.markdown(f"""<div class="vital-card-container">
            <div class="vital-label">{meta['label']}</div>
            <div class="vital-value">{st.session_state[meta['key']]} <span class="vital-unit">{meta['unit']}</span></div>
        </div>""", unsafe_allow_html=True)
        with st.popover(f"Edit {meta['key'].upper()}"):
            if meta['key'] == 'bp':
                st.session_state[meta['key']] = st.text_input(f"New {meta['label']}", value=str(st.session_state[meta['key']]))
            else:
                st.session_state[meta['key']] = st.number_input(f"New {meta['label']}", value=float(st.session_state[meta['key']]))
            if st.button(f"Update {meta['key']}", key=f"upd_{meta['key']}"): 
                st.rerun()

# --- Intelligence Tabs ---
st.markdown('<div style="margin-top:2rem;"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">🧠 Intelligence & Diagnostics <div class="section-line"></div></div>', unsafe_allow_html=True)

tab_chat, tab_reports, tab_tools = st.tabs(["💬 Clinical Chat", "📄 Diagnostic Reports", "🛠️ Clinical Tools"])

with tab_chat:
    chat_box = st.container()
    with chat_box:
        st.markdown('<div class="bubble bubble-ai"><b>ClinIQ Assistant:</b> Environment ready. Vitals synced. How can I assist you?</div>', unsafe_allow_html=True)
        for m in st.session_state.chat_history:
            cls = "bubble-user" if m["role"] == "user" else "bubble-ai"
            st.markdown(f'<div class="bubble {cls}">{m["content"]}</div>', unsafe_allow_html=True)

    if mic_recorder:
        st.write("🎤 Voice Triage (Beta):")
        mic_recorder(start_prompt="Record Symptoms", stop_prompt="Stop Recording", key='recorder')

    query = st.chat_input("Describe symptoms or ask about medications...")
    if query:
        st.session_state.chat_history.append({"role": "user", "content": query})
        with st.spinner("🤖 Analyzing clinical context..."):
            context = f"[Context: BP {st.session_state.bp}, HR {st.session_state.hr}] "
            try:
                res = requests.post(
                    f"{API_URL}/chat", 
                    json={
                        "message": context + query, 
                        "history": st.session_state.chat_history[:-1],
                        "api_key": st.secrets.get("GROQ_API_KEY", "")
                    }, 
                    timeout=20
                )
                res.raise_for_status()
                reply = res.json().get("reply", "Clinical Intelligence calibrating...")
            except Exception as e:
                reply = "⏱️ API Connection Issue. Check your internet or API status."
                
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

with tab_reports:
    st.markdown("### 📄 Diagnostic Report Hub")
    st.file_uploader("Upload Lab Reports (PDF, PNG, JPG)", type=["pdf", "png", "jpg"])
    if st.button("Run AI Document Analysis"):
        st.info("Scanning for diagnostic markers...")

with tab_tools:
    st.markdown("### 🛠️ Professional Utilities")
    c1, c2 = st.columns(2)
    with c1:
        st.link_button("📍 Find Nearest Hospital", "https://www.google.com/maps/search/hospital+near+me")
    with c2:
        if st.button("📝 Generate Clinical Report"):
            try:
                pdf_bytes = export_pdf(st.session_state.chat_history, st.session_state)
                st.download_button(
                    label="💾 Download PDF Summary",
                    data=pdf_bytes,
                    file_name=f"ClinIQ_Summary_{datetime.date.today()}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error generating PDF: {e}")

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Session Status")
    st.write(f"Vitals Updated: {datetime.datetime.now().strftime('%H:%M')}")
    if st.button("🗑️ Reset All Sessions"):
        st.session_state.chat_history = []
        st.rerun()

st.markdown("""
<div class="disclaimer">
    ⚠️ <b>Clinical Disclaimer:</b> ClinIQ is an AI tool for informational purposes. In emergency cases, contact your local medical services immediately.
</div>
""", unsafe_allow_html=True)import streamlit as st
import requests
import datetime
import os
import sys
from fpdf import FPDF

# --- Import Mic Recorder (Optional Feature) ---
try:
    from streamlit_mic_recorder import mic_recorder
except ImportError:
    mic_recorder = None

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
.stApp { background: #0a0f0a !important; }
.topbar { background: #0d120d; border: 1px solid #1a2e1a; border-radius: 16px; padding: 1rem 1.5rem; margin-bottom: 1.5rem; display: flex; align-items: center; justify-content: space-between; }
.topbar-title { font-size: 20px; font-weight: 700; color: #ffffff; }
.ai-badge { display: inline-flex; align-items: center; gap: 6px; background: rgba(74,222,128,0.1); border: 1px solid rgba(74,222,128,0.2); border-radius: 20px; padding: 5px 12px; font-size: 11px; color: #4ade80; font-weight: 600; }
.ai-dot { width: 6px; height: 6px; border-radius: 50%; background: #4ade80; display: inline-block; animation: blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }
.section-header { font-size: 11px; font-weight: 700; color: #4ade80; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 1rem; margin-top: 1rem; display: flex; align-items: center; gap: 8px; }
.section-line { height: 1px; background: #1a2e1a; flex-grow: 1; }
.vital-card-container { background: #0d120d; border: 1px solid #1a2e1a; border-radius: 14px; padding: 1.2rem; text-align: center; border-top: 2px solid #4ade80; }
.vital-label { font-size: 10px; color: rgba(255,255,255,0.4); text-transform: uppercase; font-weight: 800; margin-bottom: 8px; }
.vital-value { font-family: 'JetBrains Mono'; font-size: 24px; color: #ffffff; font-weight: 700; }
.vital-unit { font-size: 14px; color: #ffffff; font-weight: 500; margin-left: 4px; }
div[data-testid="stPopover"] > button { background: transparent !important; border: 1px solid #1a2e1a !important; color: #4ade80 !important; font-size: 10px !important; border-radius: 20px !important; margin-top: 10px !important; width: 100%; }
.bubble { padding: 1.25rem; border-radius: 14px; margin-bottom: 1rem; line-height: 1.7; font-size: 14px; max-width: 85%; }
.bubble-ai { background: #0d120d; border: 1px solid #1a2e1a; border-left: 4px solid #4ade80; color: rgba(255,255,255,0.8); }
.bubble-user { background: #0f1a0f; border: 1px solid #1a2e1a; margin-left: auto; border-right: 4px solid #58a6ff; color: #ffffff; }
.disclaimer { background: rgba(255,200,0,0.05); border: 1px solid rgba(255,200,0,0.15); border-radius: 10px; padding: 0.75rem; font-size: 11px; color: rgba(255,200,0,0.7); margin-top: 2rem; text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- Initialize Session State ---
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'bp' not in st.session_state:
    st.session_state.update({'bp': "120/80", 'hr': 72.0, 'temp': 98.6, 'ox': 98.0})

API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")

# --- Helper: Fixed PDF Generator ---
def export_pdf(history, vitals):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "ClinIQ Health Summary Report", ln=True, align='C')
    pdf.ln(10)
    
    # Vitals Section
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Patient Vitals Observation:", ln=True)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, f"Blood Pressure: {vitals.get('bp', 'N/A')}", ln=True)
    pdf.cell(0, 8, f"Heart Rate: {vitals.get('hr', 'N/A')} BPM", ln=True)
    pdf.cell(0, 8, f"Body Temp: {vitals.get('temp', 'N/A')} F", ln=True)
    pdf.cell(0, 8, f"Oxygen Sat: {vitals.get('ox', 'N/A')}%", ln=True)
    pdf.ln(10)
    
    # Conversation Section
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Clinical Interaction Log:", ln=True)
    pdf.set_font("Arial", '', 10)
    for msg in history:
        role = "PATIENT" if msg["role"] == "user" else "AI ASSISTANT"
        # Sanitize for Latin-1 encoding
        clean_text = msg['content'].encode('ascii', 'ignore').decode('ascii')
        pdf.multi_cell(0, 8, f"{role}: {clean_text}")
        pdf.ln(2)
    
    return pdf.output() # In fpdf2, this returns bytes if no dest provided

# --- UI Header ---
st.markdown(f"""
<div class="topbar">
    <div>
        <div class="topbar-title">🤖 ClinIQ Clinical Intelligence</div>
        <div style="font-size: 12px; color: rgba(255,255,255,0.4);">Advanced Diagnostic Node v4.5</div>
    </div>
    <div class="ai-badge"><span class="ai-dot"></span> FastAPI + Groq AI Active</div>
</div>
""", unsafe_allow_html=True)

# --- Vitals Observation Deck ---
st.markdown('<div class="section-header">📡 Vitals Observation Deck <div class="section-line"></div></div>', unsafe_allow_html=True)
v_cols = st.columns(4)
v_meta = [
    {"label": "Blood Pressure", "key": "bp", "unit": ""},
    {"label": "Heart Rate", "key": "hr", "unit": "BPM"},
    {"label": "Body Temp", "key": "temp", "unit": "°F"},
    {"label": "Oxygen Sat.", "key": "ox", "unit": "%"}
]

for i, meta in enumerate(v_meta):
    with v_cols[i]:
        st.markdown(f"""<div class="vital-card-container">
            <div class="vital-label">{meta['label']}</div>
            <div class="vital-value">{st.session_state[meta['key']]} <span class="vital-unit">{meta['unit']}</span></div>
        </div>""", unsafe_allow_html=True)
        with st.popover(f"Edit {meta['key'].upper()}"):
            if meta['key'] == 'bp':
                st.session_state[meta['key']] = st.text_input(f"New {meta['label']}", value=str(st.session_state[meta['key']]))
            else:
                st.session_state[meta['key']] = st.number_input(f"New {meta['label']}", value=float(st.session_state[meta['key']]))
            if st.button(f"Update {meta['key']}", key=f"btn_{meta['key']}"): 
                st.rerun()

# --- Intelligence Tabs ---
st.markdown('<div style="margin-top:2rem;"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">🧠 Intelligence & Diagnostics <div class="section-line"></div></div>', unsafe_allow_html=True)

tab_chat, tab_reports, tab_tools = st.tabs(["💬 Clinical Chat", "📄 Diagnostic Reports", "🛠️ Clinical Tools"])

with tab_chat:
    chat_box = st.container()
    with chat_box:
        st.markdown('<div class="bubble bubble-ai"><b>ClinIQ Assistant:</b> Environment ready. Vitals synced. How can I assist you?</div>', unsafe_allow_html=True)
        for m in st.session_state.chat_history:
            cls = "bubble-user" if m["role"] == "user" else "bubble-ai"
            st.markdown(f'<div class="bubble {cls}">{m["content"]}</div>', unsafe_allow_html=True)

    if mic_recorder:
        st.write("🎤 Voice Triage (Beta):")
        mic_recorder(start_prompt="Record Symptoms", stop_prompt="Stop Recording", key='recorder')

    query = st.chat_input("Describe symptoms or ask about medications...")
    if query:
        st.session_state.chat_history.append({"role": "user", "content": query})
        with st.spinner("🤖 Analyzing clinical context..."):
            context = f"[Context: BP {st.session_state.bp}, HR {st.session_state.hr}] "
            try:
                # Optimized payload and error handling
                payload = {
                    "message": context + query, 
                    "history": st.session_state.chat_history[:-1],
                    "api_key": st.secrets.get("GROQ_API_KEY", "")
                }
                res = requests.post(f"{API_URL}/chat", json=payload, timeout=20)
                res.raise_for_status()
                reply = res.json().get("reply", "Clinical Intelligence calibrating...")
            except Exception as e:
                reply = f"⏱️ Connection Error: {str(e)}"
            
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

with tab_reports:
    st.markdown("### 📄 Diagnostic Report Hub")
    st.file_uploader("Upload Lab Reports (PDF, PNG, JPG)", type=["pdf", "png", "jpg"])
    if st.button("Run AI Document Analysis"):
        st.info("Scanning for diagnostic markers...")

with tab_tools:
    st.markdown("### 🛠️ Professional Utilities")
    c1, c2 = st.columns(2)
    with c1:
        st.link_button("📍 Find Nearest Hospital", "https://www.google.com/maps/search/hospital+near+me")
    with c2:
        if st.button("📝 Prepare Clinical Report"):
            try:
                pdf_bytes = export_pdf(st.session_state.chat_history, st.session_state)
                st.download_button(
                    label="💾 Download PDF Summary",
                    data=pdf_bytes,
                    file_name=f"ClinIQ_Report_{datetime.datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error generating PDF: {e}")

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Session Status")
    st.write(f"Vitals Updated: {datetime.datetime.now().strftime('%H:%M')}")
    if st.button("🗑️ Reset All Sessions"):
        st.session_state.chat_history = []
        st.rerun()

st.markdown("""
<div class="disclaimer">
    ⚠️ <b>Clinical Disclaimer:</b> ClinIQ is an AI tool for informational purposes. In emergency cases, contact your local medical services immediately.
</div>
""", unsafe_allow_html=True)
