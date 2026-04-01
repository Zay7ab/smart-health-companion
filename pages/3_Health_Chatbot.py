import streamlit as st
import requests
import datetime
import os
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
.stApp { background: #0a0f0a !important; color: #e0e0e0; }

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
    transition: transform 0.3s ease;
}
.vital-card-container:hover { transform: translateY(-5px); border-color: #58a6ff; }
.vital-label { font-size: 10px; color: rgba(255,255,255,0.4); text-transform: uppercase; font-weight: 800; margin-bottom: 8px; }
.vital-value { font-family: 'JetBrains Mono'; font-size: 24px; color: #ffffff; font-weight: 700; }
.vital-unit { font-size: 14px; color: #ffffff; font-weight: 500; margin-left: 4px; }

/* Chat Bubbles */
.bubble { padding: 1.25rem; border-radius: 14px; margin-bottom: 1rem; line-height: 1.6; font-size: 14px; max-width: 85%; }
.bubble-ai { background: #0d120d; border: 1px solid #1a2e1a; border-left: 4px solid #4ade80; color: #d1d5db; }
.bubble-user { background: #0f1a0f; border: 1px solid #1a2e1a; margin-left: auto; border-right: 4px solid #58a6ff; color: #ffffff; }

/* Tabs Styling */
.stTabs [data-baseweb="tab-list"] { gap: 10px; }
.stTabs [data-baseweb="tab"] { 
    background-color: #0d120d; border-radius: 8px 8px 0 0; 
    padding: 10px 20px; color: #888; 
}
.stTabs [aria-selected="true"] { color: #4ade80 !important; border-bottom: 2px solid #4ade80 !important; }
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

# --- Helper: PDF Generator ---
def export_pdf(history, vitals):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "ClinIQ Health Summary Report", ln=True, align='C')
    pdf.ln(10)
    
    # Vitals Section
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 10, "Patient Vitals Observation:", ln=True, fill=True)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, f"Blood Pressure: {vitals['bp']}", ln=True)
    pdf.cell(0, 8, f"Heart Rate: {vitals['hr']} BPM", ln=True)
    pdf.cell(0, 8, f"Body Temp: {vitals['temp']} F", ln=True)
    pdf.cell(0, 8, f"Oxygen Sat: {vitals['ox']}%", ln=True)
    pdf.ln(10)
    
    # Conversation Section
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Clinical Interaction Log:", ln=True, fill=True)
    pdf.set_font("Arial", '', 10)
    
    for msg in history:
        role = "PATIENT" if msg["role"] == "user" else "AI ASSISTANT"
        # Remove characters that Arial can't handle
        clean_txt = msg['content'].encode('latin-1', 'ignore').decode('latin-1')
        pdf.set_font("Arial", 'B', 9)
        pdf.cell(0, 6, f"{role}:", ln=True)
        pdf.set_font("Arial", '', 10)
        pdf.multi_cell(0, 6, clean_txt)
        pdf.ln(2)
    
    return bytes(pdf.output())

# --- Main UI Header ---
st.markdown(f"""
<div class="topbar">
    <div>
        <div class="topbar-title">🤖 ClinIQ Clinical Intelligence</div>
        <div style="font-size: 12px; color: rgba(255,255,255,0.4);">Advanced Diagnostic Node v4.5</div>
    </div>
    <div class="ai-badge"><span class="ai-dot"></span> FastAPI + Groq AI Active</div>
</div>
""", unsafe_allow_html=True)

# --- Vitals Section ---
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
        with st.popover(f"Edit {meta['key'].upper()}", use_container_width=True):
            if meta['key'] == 'bp':
                new_val = st.text_input(f"New {meta['label']}", value=str(st.session_state[meta['key']]), key=f"in_{meta['key']}")
            else:
                new_val = st.number_input(f"New {meta['label']}", value=float(st.session_state[meta['key']]), key=f"in_{meta['key']}")
            
            if st.button(f"Update", key=f"btn_{meta['key']}", use_container_width=True):
                st.session_state[meta['key']] = new_val
                st.rerun()

# --- Content Tabs ---
st.markdown('<div class="section-header">🧠 Intelligence & Diagnostics <div class="section-line"></div></div>', unsafe_allow_html=True)
tab_chat, tab_reports, tab_tools = st.tabs(["💬 Clinical Chat", "📄 Diagnostic Reports", "🛠️ Clinical Tools"])

with tab_chat:
    chat_container = st.container(height=400, border=False)
    with chat_container:
        st.markdown('<div class="bubble bubble-ai"><b>ClinIQ Assistant:</b> Environment ready. Vitals synced. How can I assist you today?</div>', unsafe_allow_html=True)
        for m in st.session_state.chat_history:
            cls = "bubble-user" if m["role"] == "user" else "bubble-ai"
            st.markdown(f'<div class="bubble {cls}">{m["content"]}</div>', unsafe_allow_html=True)

    # Voice & Text Input
    col_input, col_voice = st.columns([0.85, 0.15])
    with col_voice:
        if mic_recorder:
            mic_recorder(start_prompt="🎤", stop_prompt="🛑", key='recorder')
    
    query = st.chat_input("Describe symptoms (e.g., 'Persistent headache since morning')...")
    
    if query:
        st.session_state.chat_history.append({"role": "user", "content": query})
        with st.spinner("🤖 Analyzing clinical context..."):
            context = f"[Context: BP {st.session_state.bp}, HR {st.session_state.hr}, Temp {st.session_state.temp}] "
            try:
                res = requests.post(
                    f"{API_URL}/chat", 
                    json={
                        "message": context + query, 
                        "history": st.session_state.chat_history[:-1],
                        "api_key": st.secrets.get("GROQ_API_KEY", "demo_key")
                    }, 
                    timeout=20
                )
                reply = res.json().get("reply", "Consulting medical database...")
            except:
                reply = "⚠️ Connection error. Please ensure the API endpoint is active."
                
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

with tab_reports:
    st.markdown("### 📄 Lab Report Analysis")
    uploaded_file = st.file_uploader("Upload Medical Reports", type=["pdf", "png", "jpg"])
    if uploaded_file and st.button("Process Document"):
        st.info("Extracting data from document...")

with tab_tools:
    st.markdown("### 🛠️ Utilities")
    c1, c2 = st.columns(2)
    with c1:
        st.link_button("📍 Locate Nearest ER", "https://www.google.com/maps/search/hospitals+near+me")
    with c2:
        if st.button("📝 Generate PDF Report", use_container_width=True):
            if not st.session_state.chat_history:
                st.warning("No conversation data to export.")
            else:
                pdf_data = export_pdf(st.session_state.chat_history, st.session_state)
                st.download_button("💾 Download Report", data=pdf_data, file_name="ClinIQ_Report.pdf", mime="application/pdf")

# --- Sidebar ---
with st.sidebar:
    st.markdown("### 📊 System Status")
    st.success("Network: Connected")
    st.write(f"**Sync Time:** {datetime.datetime.now().strftime('%H:%M:%S')}")
    
    st.divider()
    if st.button("🗑️ CLEAR SESSION", use_container_width=True, type="primary"):
        st.session_state.chat_history = []
        for key, val in vitals_defaults.items():
            st.session_state[key] = val
        st.rerun()
    
    st.info("**Model:** Llama-3-Groq\n\n**Note:** This is an AI assistant, not a doctor. In emergency, call 911.")
