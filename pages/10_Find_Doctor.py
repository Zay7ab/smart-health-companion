import streamlit as st
import requests
import sys
sys.path.append('.')
from utils.sidebar import load_sidebar

st.set_page_config(page_title="Find a Doctor", page_icon="👨‍⚕️", layout="wide")
load_sidebar()

API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: #0a0f0a !important; }
.topbar { background: #0d120d; border: 1px solid #1a2e1a; border-radius: 16px; padding: 1.25rem 1.5rem; margin-bottom: 1.25rem; display: flex; align-items: center; justify-content: space-between; }
.topbar-title { font-size: 20px; font-weight: 700; color: #ffffff; }
.topbar-sub { font-size: 12px; color: rgba(255,255,255,0.4); margin-top: 2px; }
.ai-badge { display: inline-flex; align-items: center; gap: 6px; background: rgba(74,222,128,0.1); border: 1px solid rgba(74,222,128,0.2); border-radius: 20px; padding: 5px 12px; font-size: 11px; color: #4ade80; font-weight: 600; }
.ai-dot { width: 6px; height: 6px; border-radius: 50%; background: #4ade80; display: inline-block; animation: blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }
.form-card { background: #0d120d; border: 1px solid #1a2e1a; border-radius: 16px; overflow: hidden; margin-bottom: 1rem; }
.form-header { padding: 1rem 1.25rem; background: #0f1a0f; border-bottom: 1px solid #1a2e1a; display: flex; align-items: center; justify-content: space-between; }
.form-header h2 { font-size: 14px; font-weight: 600; color: #ffffff; }
.form-tag { font-size: 10px; color: #4ade80; background: rgba(74,222,128,0.1); border: 1px solid rgba(74,222,128,0.2); padding: 2px 8px; border-radius: 20px; font-weight: 600; }
.form-body { padding: 1.25rem; }
.ai-insight { background: #0d120d; border: 1px solid #1a2e1a; border-radius: 12px; padding: 1rem; margin-top: 1rem; }
.ai-insight-header { font-size: 11px; font-weight: 600; color: #4ade80; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }
.ai-insight-text { font-size: 13px; color: rgba(255,255,255,0.7); line-height: 1.7; }
.disclaimer { background: rgba(255,200,0,0.05); border: 1px solid rgba(255,200,0,0.15); border-radius: 10px; padding: 0.75rem 1rem; font-size: 11px; color: rgba(255,200,0,0.7); margin-top: 1rem; }
div[data-testid="stButton"] button { background: linear-gradient(135deg,#166534,#4ade80) !important; color: #0a0f0a !important; border: none !important; border-radius: 8px !important; font-weight: 700 !important; font-size: 13px !important; padding: 0.6rem 1.5rem !important; }
label { color: rgba(255,255,255,0.7) !important; }
p { color: rgba(255,255,255,0.5) !important; }
.stSelectbox > div > div { background: #0f1a0f !important; border-color: #1a2e1a !important; color: white !important; }
.stTextInput > div > div > input { background: #0f1a0f !important; border-color: #1a2e1a !important; color: white !important; }
.stTextArea > div > div > textarea { background: #0f1a0f !important; border-color: #1a2e1a !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="topbar">
    <div>
        <div class="topbar-title">👨‍⚕️ Find a Doctor & Hospital</div>
        <div class="topbar-sub">AI-powered doctor recommendations via FastAPI</div>
    </div>
    <div class="ai-badge"><span class="ai-dot"></span> FastAPI + Groq AI Active</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="form-card"><div class="form-header"><h2>🔍 Search Criteria</h2><span class="form-tag">AI Powered</span></div><div class="form-body">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    condition = st.text_input("Health Condition", placeholder="e.g. Heart Disease, Pneumonia...")
    city = st.text_input("City / Country", placeholder="e.g. Dubai, London, Karachi...")
with col2:
    specialty = st.selectbox("Medical Specialty", ["Auto-detect from condition","Cardiologist","Pulmonologist","Neurologist","Oncologist","Orthopedic Surgeon","Gastroenterologist","Endocrinologist","General Physician","Pediatrician","Gynecologist","Dermatologist"])
    urgency = st.selectbox("Urgency", ["Routine (within weeks)","Soon (within days)","Urgent (within 24 hours)","Emergency"])
with col3:
    budget = st.selectbox("Budget Range", ["Any","Budget-friendly","Mid-range","Premium / Private"])
    insurance = st.selectbox("Insurance", ["Not specified","Private Insurance","Government/Public","No Insurance"])
    language = st.text_input("Preferred Language", placeholder="e.g. English, Arabic, Urdu...")
st.markdown('</div></div>', unsafe_allow_html=True)

additional_info = st.text_area("Any additional requirements?", placeholder="e.g. Female doctor preferred, wheelchair accessible...")

if st.button("⚡ Find Best Doctors & Hospitals"):
    if not condition:
        st.warning("⚠️ Please enter your health condition.")
    elif not city:
        st.warning("⚠️ Please enter your city.")
    else:
        with st.spinner("🤖 FastAPI finding best doctors..."):
            try:
                response = requests.post(f"{API_URL}/doctor/find", json={"condition": condition, "city": city, "specialty": specialty, "urgency": urgency, "budget": budget, "insurance": insurance, "language": language, "additional": additional_info, "api_key": st.secrets.get("GROQ_API_KEY", "")}, timeout=30)
                result = response.json()
                if "error" in result:
                    st.error(f"API Error: {result['error']}")
                else:
                    st.markdown(f'<div class="ai-insight"><div class="ai-insight-header">🤖 AI Doctor Recommendations — {condition} in {city}</div><div class="ai-insight-text">{result["recommendations"].replace(chr(10), "<br>")}</div></div>', unsafe_allow_html=True)
                    st.markdown("""
                    <div style="background:linear-gradient(135deg,#0d1f0d,#0f2510);border:1px solid #1a3a1a;border-radius:16px;padding:1.5rem;margin-top:1rem;">
                        <div style="font-size:11px;color:#4ade80;font-weight:600;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">⚡ Quick Action Steps</div>
                        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;">
                            <div style="background:rgba(255,255,255,0.05);border:1px solid rgba(74,222,128,0.1);border-radius:10px;padding:0.75rem;text-align:center;">
                                <div style="font-size:1.5rem;margin-bottom:4px;">📞</div>
                                <div style="font-size:11px;color:#ffffff;font-weight:600;">Call First</div>
                                <div style="font-size:10px;color:rgba(255,255,255,0.4);">Book before visiting</div>
                            </div>
                            <div style="background:rgba(255,255,255,0.05);border:1px solid rgba(74,222,128,0.1);border-radius:10px;padding:0.75rem;text-align:center;">
                                <div style="font-size:1.5rem;margin-bottom:4px;">📋</div>
                                <div style="font-size:11px;color:#ffffff;font-weight:600;">Bring Records</div>
                                <div style="font-size:10px;color:rgba(255,255,255,0.4);">Previous tests & meds</div>
                            </div>
                            <div style="background:rgba(255,255,255,0.05);border:1px solid rgba(74,222,128,0.1);border-radius:10px;padding:0.75rem;text-align:center;">
                                <div style="font-size:1.5rem;margin-bottom:4px;">⭐</div>
                                <div style="font-size:11px;color:#ffffff;font-weight:600;">Check Reviews</div>
                                <div style="font-size:10px;color:rgba(255,255,255,0.4);">Verify credentials</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown('<div class="disclaimer">⚠️ AI recommendations for guidance only. Always verify doctor credentials directly.</div>', unsafe_allow_html=True)
