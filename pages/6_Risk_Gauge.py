import streamlit as st
import requests
import plotly.graph_objects as go
import sys
sys.path.append('.')
from utils.sidebar import load_sidebar

st.set_page_config(page_title="Risk Gauge", page_icon="📊", layout="wide")
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
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="topbar">
    <div>
        <div class="topbar-title">📊 Disease Risk Gauge</div>
        <div class="topbar-sub">AI-powered cardiovascular risk assessment via FastAPI</div>
    </div>
    <div class="ai-badge"><span class="ai-dot"></span> FastAPI + Groq AI Active</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="form-card"><div class="form-header"><h2>🩺 Risk Factors</h2><span class="form-tag">9 Factors</span></div><div class="form-body">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    age = st.number_input("Age", min_value=1, max_value=120, value=45)
    smoking = st.selectbox("Smoking Status", ["Never","Former","Current"])
    diabetes = st.selectbox("Diabetes", ["No","Yes"])
with col2:
    bp = st.selectbox("High Blood Pressure", ["No","Yes"])
    cholesterol = st.selectbox("High Cholesterol", ["No","Yes"])
    exercise = st.selectbox("Regular Exercise", ["Yes","No"])
with col3:
    family_history = st.selectbox("Family History of Heart Disease", ["No","Yes"])
    obesity = st.selectbox("Obesity (BMI > 30)", ["No","Yes"])
    stress = st.selectbox("High Stress Level", ["No","Yes"])
st.markdown('</div></div>', unsafe_allow_html=True)

if st.button("⚡ Calculate Risk & Get AI Plan"):
    with st.spinner("🤖 FastAPI calculating risk..."):
        try:
            response = requests.post(f"{API_URL}/risk", json={"age": int(age), "smoking": smoking, "diabetes": diabetes, "bp": bp, "cholesterol": cholesterol, "exercise": exercise, "family_history": family_history, "obesity": obesity, "stress": stress, "api_key": st.secrets.get("GROQ_API_KEY", "")}, timeout=30)
            result = response.json()
            if "error" in result:
                st.error(f"API Error: {result['error']}")
            else:
                score = result["score"]
                risk_level = result["risk_level"]
                factors = result["factors"]
                if score < 20: rc = "#4ade80"
                elif score < 40: rc = "#f59e0b"
                elif score < 65: rc = "#f97316"
                else: rc = "#ef4444"

                col1, col2 = st.columns([1,1])
                with col1:
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=score,
                        title={'text': "Risk Score", 'font': {'color': 'white', 'family': 'Inter', 'size': 14}},
                        number={'font': {'color': rc, 'family': 'Inter', 'size': 48}, 'suffix': '%'},
                        gauge={
                            'axis': {'range': [0,100], 'tickcolor': 'rgba(255,255,255,0.3)'},
                            'bar': {'color': rc, 'thickness': 0.3},
                            'bgcolor': 'rgba(0,0,0,0)',
                            'steps': [
                                {'range': [0,20], 'color': 'rgba(74,222,128,0.1)'},
                                {'range': [20,40], 'color': 'rgba(245,158,11,0.1)'},
                                {'range': [40,65], 'color': 'rgba(249,115,22,0.1)'},
                                {'range': [65,100], 'color': 'rgba(239,68,68,0.1)'},
                            ],
                            'threshold': {'line': {'color': rc, 'width': 3}, 'thickness': 0.75, 'value': score}
                        }
                    ))
                    fig.update_layout(paper_bgcolor='rgba(13,18,13,1)', font_color='white', height=280, margin=dict(l=20,r=20,t=40,b=20))
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    st.markdown(f"""
                    <div style="background:rgba(0,0,0,0.3);border:1px solid {rc}40;border-radius:16px;padding:1.5rem;text-align:center;margin-bottom:1rem;">
                        <div style="font-size:11px;font-weight:600;color:{rc};text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">Overall Risk</div>
                        <div style="font-size:3.5rem;font-weight:800;color:{rc};letter-spacing:-2px;">{score}%</div>
                        <div style="font-size:16px;font-weight:600;color:{rc};margin-top:8px;">{risk_level}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    factors_html = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;">'
                    for name, status in list(factors.items())[:6]:
                        fc = "#ef4444" if "High" in status or "Current" in status or "Diabetic" in status else "#4ade80"
                        factors_html += f'<div style="background:rgba(0,0,0,0.3);border:1px solid {fc}30;border-radius:8px;padding:6px 10px;"><span style="font-size:11px;color:rgba(255,255,255,0.6);">{name}</span><br/><span style="font-size:10px;color:{fc};font-weight:600;">{status}</span></div>'
                    factors_html += '</div>'
                    st.markdown(factors_html, unsafe_allow_html=True)

                if "ai_plan" in result:
                    st.markdown(f'<div class="ai-insight"><div class="ai-insight-header">🤖 AI Prevention Plan</div><div class="ai-insight-text">{result["ai_plan"]}</div></div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown('<div class="disclaimer">⚠️ For educational purposes only. Always consult a qualified doctor.</div>', unsafe_allow_html=True)
