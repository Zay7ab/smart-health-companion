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

# --- Global CSS (Combined Styles) ---
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

/* Badges & Dots */
.ai-badge { 
    display: inline-flex; align-items: center; gap: 6px; 
    background: rgba(74,222,128,0.1); border: 1px solid rgba(74,222,128,0.2); 
    border-radius: 20px; padding: 5px 12px; font-size: 11px; color: #4ade80; font-weight: 600; 
}
.ai-dot { width: 6px; height: 6px; border-radius: 50%; background: #4ade80; display: inline-block; animation: blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* Cards & Sections */
.section-header { font-size: 11px; font-weight: 700; color: #4ade80; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 1rem; display: flex; align-items: center; gap: 8px; }
.section-line { height: 1px; background: #1a2e1a; flex-grow: 1; }
.vital-card-container, .stat-card { background: #0d120d; border: 1px solid #1a2e1a; border-radius: 14px; padding: 1.2rem; text-align: center; border-top: 2px solid #4ade80; }
.vital-label, .stat-label { font-size: 10px; color: rgba(255,255,255,0.4); text-transform: uppercase; font-weight: 800; margin-bottom: 8px; }
.vital-value, .stat-value { font-family: 'JetBrains Mono'; font-size: 24px; color: #ffffff; font-weight: 700; }

/* Chat Bubbles */
.bubble { padding: 1.25rem; border-radius: 14px; margin-bottom: 1rem; line-height: 1.7; font-size: 14px; max-width: 85%; }
.bubble-ai { background: #0d120d; border: 1px solid #1a2e1a; border-left: 4px solid #4ade80; color: rgba(255,255,255,0.8); }
.bubble-user { background: #0f1a0f; border: 1px solid #1a2e1a; margin-left: auto; border-right: 4px solid #58a6ff; color: #ffffff; }

/* Results */
.result-high { background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.2); border-radius: 14px; padding: 1.25rem; margin-top: 1rem; border-left: 5px solid #ef4444; }
.result-low { background: rgba(74,222,128,0.08); border: 1px solid rgba(74,222,128,0.2); border-radius: 14px; padding: 1.25rem; margin-top: 1rem; border-left: 5px solid #4ade80; }

.disclaimer { background: rgba(255,200,0,0.05); border: 1px solid rgba(255,200,0,0.15); border-radius: 10px; padding: 0.75rem; font-size: 11px; color: rgba(255,200,0,0.7); margin-top: 2rem; text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- Sidebar Navigation ---
with st.sidebar:
    st.title("🎛️ ClinIQ Control")
    page = st.radio("Navigation", ["Clinical Assistant", "Heart Risk Analysis"])
    st.divider()
    st.markdown("### 📊 Session Status")
    st.info(f"Last Sync: {datetime.datetime.now().strftime('%H:%M')}")
    if st.button("🗑️ Reset All Sessions"):
        st.session_state.clear()
        st.rerun()

# --- Shared State Initialization ---
if 'chat_history' not in st.session_state: st.session_state.chat_history = []
if 'bp' not in st.session_state:
    st.session_state.update({'bp': "120/80", 'hr': 72.0, 'temp': 98.6, 'ox': 98.0})

API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")

# --- Helper: PDF Generator ---
def export_pdf(history, vitals):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "ClinIQ Health Summary Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Current Vitals:", ln=True)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, f"BP: {vitals['bp']} | HR: {vitals['hr']} | Temp: {vitals['temp']}F", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Clinical History:", ln=True)
    pdf.set_font("Arial", '', 10)
    for msg in history:
        role = "PATIENT" if msg["role"] == "user" else "AI"
        clean_txt = msg['content'].encode('latin-1', 'ignore').decode('latin-1')
        pdf.multi_cell(0, 8, f"{role}: {clean_txt}")
    return bytes(pdf.output())

# --- Page 1: Clinical Assistant ---
if page == "Clinical Assistant":
    st.markdown("""<div class="topbar"><div class="topbar-title">🤖 ClinIQ Clinical Intelligence</div>
    <div class="ai-badge"><span class="ai-dot"></span> FastAPI + Groq AI Active</div></div>""", unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">📡 Vitals Observation Deck <div class="section-line"></div></div>', unsafe_allow_html=True)
    v_cols = st.columns(4)
    v_keys = [("Blood Pressure", "bp", ""), ("Heart Rate", "hr", "BPM"), ("Body Temp", "temp", "°F"), ("Oxygen Sat.", "ox", "%")]
    
    for i, (label, key, unit) in enumerate(v_keys):
        with v_cols[i]:
            st.markdown(f'<div class="vital-card-container"><div class="vital-label">{label}</div><div class="vital-value">{st.session_state[key]}<span style="font-size:12px;">{unit}</span></div></div>', unsafe_allow_html=True)
            with st.popover(f"Edit {key.upper()}"):
                st.session_state[key] = st.text_input(f"New {label}", value=str(st.session_state[key]))
                if st.button("Update", key=f"upd_{key}"): st.rerun()

    tab_chat, tab_tools = st.tabs(["💬 Clinical Chat", "🛠️ Clinical Tools"])
    
    with tab_chat:
        for m in st.session_state.chat_history:
            cls = "bubble-user" if m["role"] == "user" else "bubble-ai"
            st.markdown(f'<div class="bubble {cls}">{m["content"]}</div>', unsafe_allow_html=True)
        
        query = st.chat_input("Describe symptoms...")
        if query:
            st.session_state.chat_history.append({"role": "user", "content": query})
            with st.spinner("🤖 Analyzing..."):
                try:
                    ctx = f"[Vitals: BP {st.session_state.bp}, HR {st.session_state.hr}] "
                    res = requests.post(f"{API_URL}/chat", json={"message": ctx + query, "history": st.session_state.chat_history[:-1]}, timeout=20)
                    reply = res.json().get("reply", "Calibrating...")
                except: reply = "⏱️ API Connection Issue."
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.rerun()

    with tab_tools:
        if st.button("📝 Generate PDF Report"):
            pdf_data = export_pdf(st.session_state.chat_history, st.session_state)
            st.download_button("💾 Download Report", data=pdf_data, file_name="ClinIQ_Report.pdf", mime="application/pdf")

# --- Page 2: Heart Risk Analysis ---
elif page == "Heart Risk Analysis":
    st.markdown("""<div class="topbar"><div class="topbar-title">🫀 Heart Disease Risk Prediction</div>
    <div class="ai-badge"><span class="ai-dot"></span> Random Forest Active</div></div>""", unsafe_allow_html=True)
    
    cols = st.columns(3)
    with cols[0]:
        age = st.number_input("Age", 1, 120, 50)
        sex = st.selectbox("Sex", ["Male", "Female"])
        cp = st.selectbox("Chest Pain Type (0-3)", [0, 1, 2, 3])
    with cols[1]:
        trestbps = st.number_input("Resting BP", value=120)
        chol = st.number_input("Cholesterol", value=200)
        thalach = st.number_input("Max Heart Rate", value=150)
    with cols[2]:
        oldpeak = st.number_input("ST Depression", value=0.0)
        ca = st.selectbox("Major Vessels", [0, 1, 2, 3])
        thal = st.selectbox("Thal", [0, 1, 2, 3])

    if st.button("⚡ Run AI Prediction"):
        with st.spinner("Calculating cardiac risk..."):
            try:
                payload = {
                    "id": 1.0, "age": float(age), "sex": 1 if sex == "Male" else 0,
                    "dataset": 1, "cp": int(cp), "trestbps": float(trestbps),
                    "chol": float(chol), "fbs": 0, "restecg": 1, "thalach": float(thalach),
                    "exang": 0, "oldpeak": float(oldpeak), "slope": 1, "ca": int(ca), "thal": int(thal)
                }
                res = requests.post(f"{API_URL}/predict/heart", json=payload, timeout=25)
                data = res.json()
                
                prob = data.get("probability", 0)
                if data.get("prediction") == 1:
                    st.markdown(f'<div class="result-high">⚠️ <b>High Risk:</b> {prob*100:.1f}% probability detected.</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="result-low">✅ <b>Low Risk:</b> {(1-prob)*100:.1f}% probability of healthy status.</div>', unsafe_allow_html=True)
                
                if "ai_insight" in data:
                    st.info(f"🤖 AI Insight: {data['ai_insight']}")
            except Exception as e:
                st.error(f"Prediction Error: {e}")

st.markdown('<div class="disclaimer">⚠️ For informational purposes only. Consult a physician for medical advice.</div>', unsafe_allow_html=True)
