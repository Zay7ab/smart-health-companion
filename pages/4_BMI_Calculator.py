import streamlit as st
import requests
import sys
sys.path.append('.')
from utils.sidebar import load_sidebar

st.set_page_config(page_title="BMI Calculator", page_icon="⚖️", layout="wide")
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
.metrics-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 10px; margin-bottom: 1rem; }
.metric-card { border-radius: 14px; padding: 1.25rem; text-align: center; }
.ai-insight { background: #0d120d; border: 1px solid #1a2e1a; border-radius: 12px; padding: 1rem; margin-top: 1rem; }
.ai-insight-header { font-size: 11px; font-weight: 600; color: #4ade80; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }
.ai-insight-text { font-size: 13px; color: rgba(255,255,255,0.7); line-height: 1.7; }
.disclaimer { background: rgba(255,200,0,0.05); border: 1px solid rgba(255,200,0,0.15); border-radius: 10px; padding: 0.75rem 1rem; font-size: 11px; color: rgba(255,200,0,0.7); margin-top: 1rem; }
div[data-testid="stButton"] button { background: linear-gradient(135deg,#166534,#4ade80) !important; color: #0a0f0a !important; border: none !important; border-radius: 8px !important; font-weight: 700 !important; font-size: 13px !important; padding: 0.6rem 1.5rem !important; }
label { color: rgba(255,255,255,0.7) !important; }
p { color: rgba(255,255,255,0.5) !important; }
.stSelectbox > div > div { background: #0f1a0f !important; border-color: #1a2e1a !important; color: white !important; }
.stNumberInput > div > div > input { background: #0f1a0f !important; border-color: #1a2e1a !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="topbar">
    <div>
        <div class="topbar-title">⚖️ BMI & Vitals Calculator</div>
        <div class="topbar-sub">Calculate your health metrics with AI-powered insights</div>
    </div>
    <div class="ai-badge"><span class="ai-dot"></span> FastAPI + Groq AI Active</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="form-card"><div class="form-header"><h2>📏 Body Metrics</h2><span class="form-tag">AI Powered</span></div><div class="form-body">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    height = st.number_input("Height (cm)", min_value=50, max_value=250, value=170)
    weight = st.number_input("Weight (kg)", min_value=10, max_value=300, value=70)
with col2:
    age = st.number_input("Age", min_value=1, max_value=120, value=25)
    gender = st.selectbox("Gender", ["Male", "Female"])
with col3:
    activity = st.selectbox("Activity Level", ["Sedentary (little/no exercise)","Lightly active (1-3 days/week)","Moderately active (3-5 days/week)","Very active (6-7 days/week)","Extra active (physical job)"])
    goal = st.selectbox("Health Goal", ["Lose Weight","Maintain Weight","Gain Muscle"])
st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown('<div class="form-card"><div class="form-header"><h2>💓 Vital Signs</h2><span class="form-tag">Optional</span></div><div class="form-body">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    systolic = st.number_input("Systolic BP", min_value=50, max_value=250, value=120)
with col2:
    diastolic = st.number_input("Diastolic BP", min_value=30, max_value=150, value=80)
with col3:
    heart_rate = st.number_input("Heart Rate (bpm)", min_value=30, max_value=220, value=72)
with col4:
    temp = st.number_input("Body Temp (°C)", min_value=30.0, max_value=45.0, value=37.0)
st.markdown('</div></div>', unsafe_allow_html=True)

if st.button("⚡ Calculate & Get AI Insights"):
    with st.spinner("🤖 FastAPI processing..."):
        try:
            response = requests.post(f"{API_URL}/bmi", json={"height": float(height), "weight": float(weight), "age": int(age), "gender": gender, "activity": activity, "goal": goal, "systolic": int(systolic), "diastolic": int(diastolic), "heart_rate": int(heart_rate), "api_key": st.secrets.get("GROQ_API_KEY", "")}, timeout=30)
            result = response.json()
            if "error" in result:
                st.error(f"API Error: {result['error']}")
            else:
                bmi = result["bmi"]
                bmi_status = result["bmi_status"]
                tdee = result["tdee"]
                ideal_weight = result["ideal_weight"]
                bp_status = result["bp_status"]
                if bmi_status == "Underweight": c = "#3b82f6"; bg = "rgba(59,130,246,0.1)"
                elif bmi_status == "Normal": c = "#4ade80"; bg = "rgba(74,222,128,0.08)"
                elif bmi_status == "Overweight": c = "#f59e0b"; bg = "rgba(245,158,11,0.1)"
                else: c = "#ef4444"; bg = "rgba(239,68,68,0.1)"
                bp_c = "#4ade80" if bp_status == "Normal" else "#f59e0b" if bp_status == "Elevated" else "#ef4444"
                bmi_pct = min(int((bmi/40)*100), 100)
                st.markdown(f"""
                <div class="metrics-grid">
                    <div class="metric-card" style="background:{bg};border:1px solid {c}40;">
                        <div style="font-size:10px;color:{c};font-weight:600;text-transform:uppercase;margin-bottom:6px;">BMI</div>
                        <div style="font-size:26px;font-weight:800;color:{c}">{bmi}</div>
                        <div style="font-size:11px;font-weight:600;color:{c}">{bmi_status}</div>
                    </div>
                    <div class="metric-card" style="background:rgba(74,222,128,0.08);border:1px solid rgba(74,222,128,0.2);">
                        <div style="font-size:10px;color:#4ade80;font-weight:600;text-transform:uppercase;margin-bottom:6px;">Daily Calories</div>
                        <div style="font-size:26px;font-weight:800;color:#4ade80">{tdee}</div>
                        <div style="font-size:11px;font-weight:600;color:rgba(74,222,128,0.7)">kcal/day TDEE</div>
                    </div>
                    <div class="metric-card" style="background:rgba(74,222,128,0.08);border:1px solid rgba(74,222,128,0.2);">
                        <div style="font-size:10px;color:#4ade80;font-weight:600;text-transform:uppercase;margin-bottom:6px;">Ideal Weight</div>
                        <div style="font-size:26px;font-weight:800;color:#4ade80">{ideal_weight}</div>
                        <div style="font-size:11px;font-weight:600;color:rgba(74,222,128,0.7)">kg for height</div>
                    </div>
                    <div class="metric-card" style="background:rgba(59,130,246,0.08);border:1px solid {bp_c}40;">
                        <div style="font-size:10px;color:{bp_c};font-weight:600;text-transform:uppercase;margin-bottom:6px;">Blood Pressure</div>
                        <div style="font-size:22px;font-weight:800;color:{bp_c}">{systolic}/{diastolic}</div>
                        <div style="font-size:11px;font-weight:600;color:{bp_c}">{bp_status}</div>
                    </div>
                </div>
                <div style="background:#0d120d;border:1px solid #1a2e1a;border-radius:12px;padding:1rem;margin-bottom:1rem;">
                    <div style="font-size:12px;font-weight:600;color:#ffffff;margin-bottom:8px;">BMI Scale</div>
                    <div style="background:#1a2e1a;border-radius:10px;height:10px;overflow:hidden;">
                        <div style="width:{bmi_pct}%;height:100%;background:{c};border-radius:10px;"></div>
                    </div>
                    <div style="display:flex;justify-content:space-between;font-size:10px;color:rgba(255,255,255,0.3);margin-top:4px;">
                        <span>Underweight &lt;18.5</span><span>Normal 18.5-24.9</span><span>Overweight 25-29.9</span><span>Obese &gt;30</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if "ai_insight" in result:
                    st.markdown(f'<div class="ai-insight"><div class="ai-insight-header">🤖 AI Personalized Health Plan</div><div class="ai-insight-text">{result["ai_insight"]}</div></div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown('<div class="disclaimer">⚠️ For educational purposes only. Always consult a qualified doctor.</div>', unsafe_allow_html=True)
