import streamlit as st
import requests
import sys
sys.path.append('.')
from utils.sidebar import load_sidebar

st.set_page_config(page_title="Heart Disease Prediction", page_icon="🫀", layout="wide")
load_sidebar()

API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: #f0f4f0 !important; }
.topbar { background: white; border: 1px solid #e0ece0; border-radius: 16px; padding: 1.25rem 1.5rem; margin-bottom: 1.25rem; display: flex; align-items: center; justify-content: space-between; }
.topbar-title { font-size: 20px; font-weight: 700; color: #1a3a1a; }
.topbar-sub { font-size: 12px; color: #639922; margin-top: 2px; }
.ai-badge { display: inline-flex; align-items: center; gap: 6px; background: linear-gradient(135deg,#eaf3de,#d4edbe); border: 1px solid #97c459; border-radius: 20px; padding: 5px 12px; font-size: 11px; color: #27500a; font-weight: 600; }
.ai-dot { width: 6px; height: 6px; border-radius: 50%; background: #639922; display: inline-block; }
.stats-row { display: grid; grid-template-columns: repeat(3,1fr); gap: 10px; margin-bottom: 1.25rem; }
.stat-card { background: white; border: 1px solid #e0ece0; border-radius: 12px; padding: 1rem; position: relative; overflow: hidden; }
.stat-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg,#639922,#97c459); }
.stat-label { font-size: 10px; color: #7a8f7a; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500; margin-bottom: 4px; }
.stat-value { font-size: 20px; font-weight: 700; color: #1a3a1a; }
.stat-sub { font-size: 10px; color: #639922; margin-top: 2px; font-weight: 500; }
.form-card { background: white; border: 1px solid #e0ece0; border-radius: 16px; overflow: hidden; margin-bottom: 1rem; }
.form-header { padding: 1rem 1.25rem; background: linear-gradient(135deg,#f5f9f0,#eaf3de); border-bottom: 1px solid #e0ece0; display: flex; align-items: center; justify-content: space-between; }
.form-header h2 { font-size: 14px; font-weight: 600; color: #1a3a1a; }
.form-tag { font-size: 10px; color: #3b6d11; background: #d4edbe; padding: 2px 8px; border-radius: 20px; font-weight: 600; }
.result-high { background: linear-gradient(135deg,#fff0f0,#ffe0e0); border: 1px solid #ffb3b3; border-radius: 14px; padding: 1.25rem; margin-top: 1rem; }
.result-low { background: linear-gradient(135deg,#f0fff4,#e0ffe8); border: 1px solid #97c459; border-radius: 14px; padding: 1.25rem; margin-top: 1rem; }
.ai-insight { background: white; border: 1px solid #e0ece0; border-radius: 12px; padding: 1rem; margin-top: 1rem; }
.ai-insight-header { font-size: 11px; font-weight: 600; color: #639922; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }
.ai-insight-text { font-size: 13px; color: #3a4a3a; line-height: 1.7; }
.disclaimer { background: #fff8e1; border: 1px solid #f0c040; border-radius: 10px; padding: 0.75rem 1rem; font-size: 11px; color: #7a6000; margin-top: 1rem; }
div[data-testid="stButton"] button { background: linear-gradient(135deg,#3b6d11,#639922) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; font-size: 13px !important; padding: 0.6rem 1.5rem !important; }
label { color: #1a3a1a !important; }
p { color: #1a3a1a !important; }
</style>
""", unsafe_allow_html=True)

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
        <div class="stat-sub">+ SVM Ensemble</div>
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

col1, col2, col3 = st.columns(3)
with col1:
    id = st.number_input("Patient ID", value=1)
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

if st.button("⚡ Run AI Analysis"):
    with st.spinner("🤖 FastAPI processing..."):
        try:
            sex_val = 1 if sex == "Male" else 0
            response = requests.post(
                f"{API_URL}/predict/heart",
                json={
                    "id": float(id),
                    "age": float(age),
                    "sex": sex_val,
                    "dataset": int(dataset),
                    "cp": int(cp),
                    "trestbps": float(trestbps),
                    "chol": float(chol),
                    "fbs": int(fbs),
                    "restecg": int(restecg),
                    "thalach": float(thalach),
                    "exang": int(exang),
                    "oldpeak": float(oldpeak),
                    "slope": int(slope),
                    "ca": int(ca),
                    "thal": int(thal)
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
                        <div style="font-size:16px;font-weight:700;color:#c0392b">⚠️ High Risk Detected</div>
                        <div style="font-size:28px;font-weight:700;color:#c0392b">{probability*100:.1f}%</div>
                        <div style="font-size:12px;color:#7a3a3a;margin-top:4px">Probability of Heart Disease</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="result-low">
                        <div style="font-size:16px;font-weight:700;color:#27500a">✅ Low Risk</div>
                        <div style="font-size:28px;font-weight:700;color:#27500a">{(1-probability)*100:.1f}%</div>
                        <div style="font-size:12px;color:#3b6d11;margin-top:4px">Probability of Being Healthy</div>
                    </div>
                    """, unsafe_allow_html=True)

                if "ai_insight" in result:
                    st.markdown(f"""
                    <div class="ai-insight">
                        <div class="ai-insight-header">🤖 AI Medical Insight (via FastAPI)</div>
                        <div class="ai-insight-text">{result['ai_insight']}</div>
                    </div>
                    """, unsafe_allow_html=True)

        except requests.exceptions.Timeout:
            st.error("⏱️ API timeout — please try again")
        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown('<div class="disclaimer">⚠️ For educational purposes only. Always consult a qualified doctor.</div>', unsafe_allow_html=True)
