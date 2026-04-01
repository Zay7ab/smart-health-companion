import streamlit as st
import requests
import datetime
from fpdf import FPDF

# --- Optional Mic Recorder ---
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

# --- CSS for Dark Neon Theme ---
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
.bubble { padding: 1.25rem; border-radius: 14px; margin-bottom: 1rem; line-height: 1.7; font-size: 14px; max-width: 85%; }
.bubble-ai { background: #0d120d; border: 1px solid #1a2e1a; border-left: 4px solid #4ade80; color: rgba(255,255,255,0.8); }
.bubble-user { background: #0f1a0f; border: 1px solid #1a2e1a; margin-left: auto; border-right: 4px solid #58a6ff; color: #ffffff; }
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

vitals_defaults = {'bp': "120/80", 'hr': 72.0, 'temp': 98.6, 'ox': 98.0}
for key, val in vitals_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")

# --- PDF Export ---
def export_pdf(history, vitals):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "ClinIQ Health Summary Report", ln=True, align='C')
    pdf.ln(10)

    # Vitals
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Patient Vitals Observation:", ln=True)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, f"Blood Pressure: {vitals.get('bp')}", ln=True)
    pdf.cell(0, 8, f"Heart Rate: {vitals.get('hr')} BPM", ln=True)
    pdf.cell(0, 8, f"Body Temp: {vitals.get('temp')} F", ln=True)
    pdf.cell(0, 8, f"Oxygen Sat: {vitals.get('ox')}%", ln=True)
    pdf.ln(10)

    # Chat history
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Clinical Interaction Log:", ln=True)
    pdf.set_font("Arial", '', 10)
    for msg in history:
        role = "PATIENT" if msg["role"] == "user" else "AI ASSISTANT"
        clean_txt = msg["content"].encode("latin-1", "ignore").decode("latin-1")
        pdf.multi_cell(0, 8, f"{role}: {clean_txt}")
        pdf.ln(2)

    return pdf.output(dest='S').encode('latin-1')

# --- Topbar ---
st.markdown(f"""
<div class="topbar">
    <div>
        <div class="topbar-title">🤖 ClinIQ Clinical Intelligence</div>
        <div style="font-size: 12px; color: rgba(255,255,255,0.4);">Advanced Diagnostic Node v4.5</div>
    </div>
    <div class="ai-badge"><span class="ai-dot"></span> FastAPI + Groq AI Active</div>
</div>
""", unsafe_allow_html=True)

# --- Vitals Deck ---
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
                new_val = st.text_input(f"New {meta['label']}", value=str(st.session_state[meta['key']]))
            else:
                new_val = st.number_input(f"New {meta['label']}", value=float(st.session_state[meta['key']]))
            if st.button(f"Update {meta['key'].upper()}", key=f"btn_{meta['key']}"):
                st.session_state[meta['key']] = new_val
                st.rerun()

# --- Tabs ---
st.markdown('<div style="margin-top:2rem;"></div>', unsafe_allow_html=True)
tab_chat, tab_reports, tab_tools = st.tabs(["💬 Clinical Chat", "📄 Diagnostic Reports", "🛠️ Clinical Tools"])

# --- Chat Tab ---
with tab_chat:
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
            context = f"[Context: BP {st.session_state.bp}, HR {st.session_state.hr}, Temp {st.session_state.temp}] "
            try:
                res = requests.post(f"{API_URL}/chat", json={"message": context+query, "history": st.session_state.chat_history[:-1]}, timeout=20)
                res.raise_for_status()
                reply = res.json().get("reply", "Clinical Intelligence calibrating...")
            except Exception:
                reply = "⏱️ API Connection Issue. Check your internet or API status."
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

# --- Reports Tab ---
with tab_reports:
    st.markdown("### 📄 Diagnostic Report Hub")
    uploaded_file = st.file_uploader("Upload Lab Reports (PDF, PNG, JPG)", type=["pdf", "png", "jpg"])
    if st.button("Run AI Document Analysis"):
        if uploaded_file:
            st.info("Scanning report for diagnostic markers...")
            try:
                res = requests.post(f"{API_URL}/analyze-report", files={"file": uploaded_file}, timeout=30)
                res.raise_for_status()
                analysis = res.json().get("analysis", "No analysis found.")
                st.success("✅ Analysis Complete")
                st.json(analysis)
            except Exception as e:
                st.error(f"Report analysis failed: {e}")
        else:
            st.warning("Please upload a file first.")

# --- Tools Tab ---
with tab_tools:
    st.markdown("### 🛠️ Professional Utilities")
    c1, c2 = st.columns(2)
    with c1:
        st.button("📍 Find Nearest Hospital", on_click=lambda: st.experimental_set_query_params(open_map="1"))
    with c2:
        if st.button("📝 Generate Clinical Report"):
            pdf_bytes = export_pdf(st.session_state.chat_history, st.session_state)
            st.download_button(label="💾 Download PDF Summary", data=pdf_bytes, file_name=f"ClinIQ_Summary_{datetime.date.today()}.pdf", mime="application/pdf")

# --- Sidebar ---
with st.sidebar:
    st.header("📊 STATUS")
    st.info("Diagnostic Node Active")
    st.markdown("**Last Sync Time:**")
    st.write(datetime.datetime.now().strftime('%H:%M:%S'))
    st.markdown("---")
    st.header("🛠️ System Control")
    if st.button("🗑️ PURGE SESSION DATA"):
        st.session_state.chat_history = []
        for key, val in vitals_defaults.items():
            st.session_state[key] = val
        st.rerun()
    st.markdown("---")
    st.header("Node Info")
    st.markdown("- Model: Groq-Llama-3\n- Protocol: HTTPS/FastAPI\n- Encryption: AES-256")
    st.markdown("---")
    st.caption("CLINIQ-OS v4.5.2 | STABLE_BUILD")
    
