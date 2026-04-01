import streamlit as st
import requests
import sys

# Page Configuration
st.set_page_config(page_title="Heart Disease Prediction", page_icon="🫀", layout="wide")

# --- SIDEBAR SECTION START ---
with st.sidebar:
    st.title("Settings & Info")
    st.info("Bhai, yahan aap model ki details ya app ki instructions de sakte hain.")
    
    st.markdown("---")
    st.subheader("Navigation")
    # Aap yahan options add kar sakte hain
    page = st.radio("Go to", ["Home", "About Model", "Source Code"])
    
    st.markdown("---")
    st.write("Developed with ❤️ by Health AI Team")
# --- SIDEBAR SECTION END ---

API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")

# CSS Styling
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
.stats-row { display: grid; grid-template-columns: repeat(3,1fr); gap: 10px; margin-bottom: 1.25rem; }
.stat-card { background: #0d120d; border: 1px solid #1a2e1a; border-radius: 12px; padding: 1rem; position: relative; overflow: hidden; }
.stat-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg,#4ade80,#22c55e); }
.stat-label { font-size: 10px; color: rgba(255,255,255,0.4); text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500; margin-bottom: 4px; }
.stat-value { font-size: 20px; font-weight: 700; color: #ffffff; }
.stat-sub { font-size: 10px; color: #4ade80; margin-top: 2px; font-weight: 500; }
.form-card { background: #0d120d; border: 1px solid #1a2e1a; border-radius: 16px; overflow: hidden; margin-bottom: 1rem; }
.form-header { padding: 1rem 1.25rem; background: #0f1a0f; border-bottom: 1px solid #1a2e1a; display: flex; align-items: center; justify-content: space-between; }
.form-header h2 { font-size: 14px; font-weight: 600; color: #ffffff; }
.form-tag { font-size: 10px; color: #4ade80; background: rgba(74,222,128,0.1); border: 1px solid rgba(74,222,128,0.2); padding: 2px 8px; border-radius: 20px; font-weight: 600; }
.result-high { background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.2); border-radius: 14px; padding: 1.25rem; margin-top: 1rem; }
.result-low { background: rgba(74,222,128,0.08); border: 1px solid rgba(74,222,128,0.2); border-radius: 14px; padding: 1.25rem; margin-top: 1rem; }
.ai-insight { background: #0d120d; border: 1px solid #1a2e1a; border-radius: 12px; padding: 1rem; margin-top: 1rem; }
.ai-insight-header { font-size: 11px; font-weight: 600; color: #4ade80; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }
.ai-insight-text { font-size: 13px; color: rgba(255,255,255,0.7); line-height: 1.7; }
.disclaimer { background: rgba(255,200,0,0.05); border: 1px solid rgba(255,200,0,0.15); border-radius: 10px; padding: 0.75rem 1rem; font-size: 11px; color: rgba(255,200,0,0.7); margin-top: 1rem; }
div[data-testid="stButton"] button { background: linear-gradient(135deg,#166534,#4ade80) !important; color: #0a0f0a !important; border: none !important; border-radius: 8px !important; font-weight: 700 !important; font-size: 13px !important; padding: 0.6rem 1.5rem !important; }
div[data-testid="stButton"] button:hover { background: linear-gradient(135deg,#15803d,#22c55e) !important; }
label { color: rgba(255,255,255,0.7) !important; }
p { color: rgba(255,255,255,0.5) !important; }
.stSelectbox > div > div { background: #0f1a0f !important; border-color: #1a2e1a !important; color: white !important; }
.stNumberInput > div > div > input { background: #0f1a0f !important; border-color: #1a2e1a !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# Main UI
st.markdown("""
<div class="topbar">
    <div>
        <div class="topbar-title">🫀 Heart Disease Prediction</div>
        <div class="topbar-sub">ML-powered cardiac risk analysis using Random Forest</div>
    </div>
    <div class="ai-badge"><span class="ai-dot"></span> FastAPI + Groq AI Active</div>
</div>
<div class="stats-row">
    <div class="stat-card">
        <div class="stat-label">Model</div>
        <div class="stat-value">Random Forest</div>
        <div class="stat-sub">ML Model</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">AUC Score</div>
        <div class="stat-value">92%</div>
        <div class="stat-sub">Excellent Performance</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Features</div>
        <div class="stat-value">15</div>
        <div class="stat-sub">Cardiac Indicators</div>
    </div>
</div>
<div class="form-card">
    <div class="form-header">
        <h2>Patient Health Data</h2>
        <span class="form-tag">15 Features</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Input Columns
col1, col2, col3 = st.columns(3)
with col1:
    pid = st.number_input("Patient ID", value=1)
    age = st.number_input("Age", min_value=1, max_value=120, value=50)
    sex = st.selectbox("Sex", ["Male", "Female"])
    dataset = st.selectbox("Dataset Source", [0, 1, 2, 3])
    cp = st.selectbox("Chest Pain Type", [0, 1, 2, 3])
with col2:
    trestbps = st.number_input("Resting Blood Pressure", value=120)
    chol = st.number_input("Cholesterol", value=200)
    fbs = st.selectbox("Fasting Blood Sugar > 120mg/dl", [0, 1])
    restecg = st.selectbox("Resting ECG", [0, 1, 2])
    thalach = st.number_input("Max Heart Rate", value=150)
with col3:
    exang = st.selectbox("Exercise Induced Angina", [0, 1])
    oldpeak = st.number_input("ST Depression", value=0.0)
    slope = st.selectbox("Slope", [0, 1, 2])
    ca = st.selectbox("Number of Major Vessels", [0, 1, 2, 3])
    thal = st.selectbox("Thal", [0, 1, 2, 3])

# Prediction Logic
if st.button("⚡ Run AI Analysis"):
    with st.spinner("🤖 FastAPI processing..."):
        try:
            sex_val = 1 if sex == "Male" else 0
            response = requests.post(
                f"{API_URL}/predict/heart",
                json={
                    "id": float(pid), "age": float(age), "sex": sex_val,
                    "dataset": int(dataset), "cp": int(cp),
                    "trestbps": float(trestbps), "chol": float(chol),
                    "fbs": int(fbs), "restecg": int(restecg),
                    "thalach": float(thalach), "exang": int(exang),
                    "oldpeak": float(oldpeak), "slope": int(slope),
                    "ca": int(ca), "thal": int(thal)
                },
                timeout=30
            )
            result = response.json()
            if "error" in result:
                st.error(f"API Error: {result['error']}")
            else:
                prediction = result["prediction"]
                probability = result["probability"]
                if prediction == 1:
                    st.markdown(f"""
                    <div class="result-high">
                        <div style="font-size:16px;font-weight:700;color:#ef4444;">⚠️ High Risk Detected</div>
                        <div style="font-size:32px;font-weight:800;color:#ef4444;">{probability*100:.1f}%</div>
                        <div style="font-size:12px;color:rgba(239,68,68,0.7);margin-top:4px;">Probability of Heart Disease</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="result-low">
                        <div style="font-size:16px;font-weight:700;color:#4ade80;">✅ Low Risk</div>
                        <div style="font-size:32px;font-weight:800;color:#4ade80;">{(1-probability)*100:.1f}%</div>
                        <div style="font-size:12px;color:rgba(74,222,128,0.7);margin-top:4px;">Probability of Being Healthy</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                if "ai_insight" in result:
                    st.markdown(f"""
                    <div class="ai-insight">
                        <div class="ai-insight-header">🤖 AI Medical Insight</div>
                        <div class="ai-insight-text">{result['ai_insight']}</div>
                    </div>
                    """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown('<div class="disclaimer">⚠️ For educational purposes only. Always consult a qualified doctor.</div>', unsafe_allow_html=True)
