import streamlit as st
from groq import Groq
import plotly.graph_objects as go
import sys
sys.path.append('.')
from utils.sidebar import load_sidebar

st.set_page_config(page_title="Disease Risk Gauge", page_icon="📊", layout="wide")
load_sidebar()

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
.form-card { background: white; border: 1px solid #e0ece0; border-radius: 16px; overflow: hidden; margin-bottom: 1rem; }
.form-header { padding: 1rem 1.25rem; background: linear-gradient(135deg,#f5f9f0,#eaf3de); border-bottom: 1px solid #e0ece0; display: flex; align-items: center; justify-content: space-between; }
.form-header h2 { font-size: 14px; font-weight: 600; color: #1a3a1a; }
.form-tag { font-size: 10px; color: #3b6d11; background: #d4edbe; padding: 2px 8px; border-radius: 20px; font-weight: 600; }
.form-body { padding: 1.25rem; }
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
        <div class="topbar-title">📊 Disease Risk Gauge</div>
        <div class="topbar-sub">AI-powered cardiovascular risk assessment</div>
    </div>
    <div class="ai-badge"><span class="ai-dot"></span> Groq AI Active</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="form-card"><div class="form-header"><h2>🩺 Risk Factors</h2><span class="form-tag">9 Factors</span></div><div class="form-body">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    age = st.number_input("Age", min_value=1, max_value=120, value=45)
    smoking = st.selectbox("Smoking Status", ["Never", "Former", "Current"])
    diabetes = st.selectbox("Diabetes", ["No", "Yes"])
with col2:
    bp = st.selectbox("High Blood Pressure", ["No", "Yes"])
    cholesterol = st.selectbox("High Cholesterol", ["No", "Yes"])
    exercise = st.selectbox("Regular Exercise", ["Yes", "No"])
with col3:
    family_history = st.selectbox("Family History of Heart Disease", ["No", "Yes"])
    obesity = st.selectbox("Obesity (BMI > 30)", ["No", "Yes"])
    stress = st.selectbox("High Stress Level", ["No", "Yes"])

st.markdown('</div></div>', unsafe_allow_html=True)

if st.button("⚡ Calculate Risk & Get AI Plan"):
    score = 0
    factors = {}

    if age > 55: score += 25; factors["Age > 55"] = ("High Risk", "#c0392b", "#fff0f0")
    elif age > 45: score += 15; factors["Age 45-55"] = ("Moderate", "#d97706", "#fffbeb")
    else: factors[f"Age {age}"] = ("Low Risk", "#27500a", "#f0fff4")

    if smoking == "Current": score += 25; factors["Smoking"] = ("Current", "#c0392b", "#fff0f0")
    elif smoking == "Former": score += 10; factors["Smoking"] = ("Former", "#d97706", "#fffbeb")
    else: factors["Smoking"] = ("Non-Smoker", "#27500a", "#f0fff4")

    if diabetes == "Yes": score += 15; factors["Diabetes"] = ("Diabetic", "#c0392b", "#fff0f0")
    else: factors["Diabetes"] = ("No Diabetes", "#27500a", "#f0fff4")

    if bp == "Yes": score += 15; factors["Blood Pressure"] = ("High BP", "#c0392b", "#fff0f0")
    else: factors["Blood Pressure"] = ("Normal BP", "#27500a", "#f0fff4")

    if cholesterol == "Yes": score += 10; factors["Cholesterol"] = ("High", "#d97706", "#fffbeb")
    else: factors["Cholesterol"] = ("Normal", "#27500a", "#f0fff4")

    if exercise == "No": score += 10; factors["Exercise"] = ("Inactive", "#d97706", "#fffbeb")
    else: factors["Exercise"] = ("Active", "#27500a", "#f0fff4")

    if family_history == "Yes": score += 10; factors["Family History"] = ("Present", "#d97706", "#fffbeb")
    else: factors["Family History"] = ("None", "#27500a", "#f0fff4")

    if obesity == "Yes": score += 10; factors["Obesity"] = ("Obese", "#c0392b", "#fff0f0")
    else: factors["Obesity"] = ("Normal", "#27500a", "#f0fff4")

    if stress == "Yes": score += 5; factors["Stress"] = ("High", "#d97706", "#fffbeb")
    else: factors["Stress"] = ("Low", "#27500a", "#f0fff4")

    score = min(score, 100)

    if score < 20: risk_level, risk_color, risk_bg, risk_border = "Low Risk", "#27500a", "linear-gradient(135deg,#f0fff4,#e0ffe8)", "#97c459"
    elif score < 40: risk_level, risk_color, risk_bg, risk_border = "Moderate Risk", "#d97706", "linear-gradient(135deg,#fffbeb,#fef3c7)", "#fbbf24"
    elif score < 65: risk_level, risk_color, risk_bg, risk_border = "High Risk", "#ea580c", "linear-gradient(135deg,#fff7ed,#ffedd5)", "#fb923c"
    else: risk_level, risk_color, risk_bg, risk_border = "Very High Risk", "#c0392b", "linear-gradient(135deg,#fff0f0,#ffe0e0)", "#f87171"

    col1, col2 = st.columns([1, 1])
    with col1:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            title={'text': "Risk Score", 'font': {'color': '#1a3a1a', 'family': 'Inter', 'size': 14}},
            number={'font': {'color': risk_color, 'family': 'Inter', 'size': 48}, 'suffix': '%'},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': '#7a8f7a', 'tickfont': {'color': '#7a8f7a', 'size': 10}},
                'bar': {'color': risk_color, 'thickness': 0.3},
                'bgcolor': 'rgba(0,0,0,0)',
                'bordercolor': '#e0ece0',
                'steps': [
                    {'range': [0, 20], 'color': 'rgba(39,80,10,0.1)'},
                    {'range': [20, 40], 'color': 'rgba(217,119,6,0.1)'},
                    {'range': [40, 65], 'color': 'rgba(234,88,12,0.1)'},
                    {'range': [65, 100], 'color': 'rgba(192,57,43,0.1)'},
                ],
                'threshold': {'line': {'color': risk_color, 'width': 3}, 'thickness': 0.75, 'value': score}
            }
        ))
        fig.update_layout(paper_bgcolor='rgba(255,255,255,1)', plot_bgcolor='rgba(0,0,0,0)', font={'color': '#1a3a1a', 'family': 'Inter'}, height=280, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown(f"""
        <div style="background:{risk_bg};border:1px solid {risk_border};border-radius:16px;padding:1.5rem;text-align:center;margin-bottom:1rem;">
            <div style="font-size:11px;font-weight:600;color:{risk_color};text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">Overall Risk</div>
            <div style="font-size:3.5rem;font-weight:700;color:{risk_color};letter-spacing:-2px;">{score}%</div>
            <div style="font-size:16px;font-weight:600;color:{risk_color};margin-top:8px;">{risk_level}</div>
        </div>
        """, unsafe_allow_html=True)

        factors_html = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;">'
        for name, (status, color, bg) in list(factors.items())[:6]:
            factors_html += f'<div style="background:{bg};border:1px solid {color}40;border-radius:8px;padding:6px 10px;display:flex;align-items:center;justify-content:space-between;"><span style="font-size:11px;color:#3a4a3a;">{name}</span><span style="font-size:10px;color:{color};font-weight:600;">{status}</span></div>'
        factors_html += '</div>'
        st.markdown(factors_html, unsafe_allow_html=True)

    with st.spinner("🤖 Getting AI prevention plan..."):
        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            active_risks = [k for k, v in factors.items() if "High" in v[0] or "Current" in v[0] or "Diabetic" in v[0] or "Obese" in v[0]]
            prompt = f"""Cardiovascular risk: {score}% ({risk_level}), Age: {age}, Key risks: {', '.join(active_risks) if active_risks else 'None'}, Exercise: {exercise}, Smoking: {smoking}.
            Give 4-5 sentence personalized prevention plan with urgent lifestyle changes, screening tests and motivation.
            End with: Consult a cardiologist for comprehensive evaluation."""
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            )
            st.markdown(f"""
            <div class="ai-insight">
                <div class="ai-insight-header">🤖 AI Prevention Plan</div>
                <div class="ai-insight-text">{response.choices[0].message.content}</div>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown('<div class="disclaimer">⚠️ For educational purposes only. Always consult a qualified doctor.</div>', unsafe_allow_html=True)
