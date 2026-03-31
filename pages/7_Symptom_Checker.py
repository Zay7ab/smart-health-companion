import streamlit as st
import requests
import sys
sys.path.append('.')
from utils.sidebar import load_sidebar

st.set_page_config(page_title="Symptom Checker", page_icon="🔍", layout="wide")
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
.stNumberInput > div > div > input { background: #0f1a0f !important; border-color: #1a2e1a !important; color: white !important; }
.stTextInput > div > div > input { background: #0f1a0f !important; border-color: #1a2e1a !important; color: white !important; }
.stTextArea > div > div > textarea { background: #0f1a0f !important; border-color: #1a2e1a !important; color: white !important; }
div[data-testid="stCheckbox"] { background: #0f1a0f; border-radius: 8px; padding: 6px 10px; margin-bottom: 4px; border: 1px solid #1a2e1a; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="topbar">
    <div>
        <div class="topbar-title">🔍 Symptom Checker</div>
        <div class="topbar-sub">AI-powered symptom analysis via FastAPI</div>
    </div>
    <div class="ai-badge"><span class="ai-dot"></span> FastAPI + Groq AI Active</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="form-card"><div class="form-header"><h2>🩺 Patient Information</h2><span class="form-tag">AI Powered</span></div><div class="form-body">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    age = st.number_input("Age", min_value=1, max_value=120, value=30)
    gender = st.selectbox("Gender", ["Male","Female","Other"])
with col2:
    duration = st.selectbox("Duration of Symptoms", ["Less than 24 hours","1-3 days","3-7 days","1-2 weeks","More than 2 weeks"])
    severity = st.select_slider("Severity", options=["Mild","Moderate","Severe","Very Severe"])
with col3:
    existing = st.multiselect("Existing Conditions", ["Diabetes","Hypertension","Heart Disease","Asthma","None"], default=["None"])
    medications = st.text_input("Current Medications (optional)")
st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown('<div class="form-card"><div class="form-header"><h2>🤒 Select Your Symptoms</h2><span class="form-tag">Multiple Selection</span></div><div class="form-body">', unsafe_allow_html=True)
all_symptoms = ["Fever","Headache","Chest Pain","Shortness of Breath","Cough","Fatigue","Dizziness","Nausea","Vomiting","Abdominal Pain","Back Pain","Joint Pain","Muscle Pain","Sore Throat","Runny Nose","Loss of Appetite","Weight Loss","Night Sweats","Swollen Lymph Nodes","Skin Rash","Blurred Vision","Frequent Urination","Excessive Thirst","Numbness","Palpitations","Swollen Legs","Difficulty Swallowing"]
col1, col2, col3, col4 = st.columns(4)
selected_symptoms = []
for i, symptom in enumerate(all_symptoms):
    col = [col1, col2, col3, col4][i % 4]
    with col:
        if st.checkbox(symptom, key=f"sym_{i}"):
            selected_symptoms.append(symptom)
st.markdown('</div></div>', unsafe_allow_html=True)

additional = st.text_area("Any additional symptoms or details?", placeholder="Describe any other symptoms...")

if selected_symptoms:
    st.markdown(f'<div style="background:rgba(74,222,128,0.08);border:1px solid rgba(74,222,128,0.2);border-radius:10px;padding:0.6rem 1rem;margin-bottom:1rem;font-size:13px;color:#4ade80;"><b>{len(selected_symptoms)} symptom(s) selected:</b> {", ".join(selected_symptoms)}</div>', unsafe_allow_html=True)

if st.button("⚡ Analyze Symptoms with AI"):
    if not selected_symptoms:
        st.warning("⚠️ Please select at least one symptom.")
    else:
        with st.spinner("🤖 FastAPI analyzing symptoms..."):
            try:
                response = requests.post(f"{API_URL}/symptoms/check", json={"age": int(age), "gender": gender, "symptoms": selected_symptoms, "duration": duration, "severity": severity, "existing_conditions": existing, "medications": medications, "additional": additional, "api_key": st.secrets.get("GROQ_API_KEY", "")}, timeout=30)
                result = response.json()
                if "error" in result:
                    st.error(f"API Error: {result['error']}")
                else:
                    st.markdown(f'<div class="ai-insight"><div class="ai-insight-header">🤖 AI Symptom Analysis</div><div class="ai-insight-text">{result["analysis"].replace(chr(10), "<br>")}</div></div>', unsafe_allow_html=True)
                    if result.get("is_urgent"):
                        st.markdown('<div style="background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.2);border-radius:12px;padding:1rem 1.25rem;margin-top:1rem;"><div style="font-size:14px;font-weight:700;color:#ef4444;margin-bottom:4px;">🚨 Urgent Medical Attention Recommended</div><div style="font-size:12px;color:rgba(239,68,68,0.7);">Please visit your nearest emergency room immediately.</div></div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown('<div class="disclaimer">⚠️ For educational purposes only. Always consult a qualified doctor.</div>', unsafe_allow_html=True)
