import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Disease Risk Gauge", page_icon="📊", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');
    .stApp { background: linear-gradient(135deg, #0a0a1a 0%, #0d1b2a 40%, #1a0a2e 100%); font-family: 'Rajdhani', sans-serif; }
    .page-title { font-family: 'Orbitron', monospace; font-size: 2.5rem; font-weight: 900; background: linear-gradient(90deg, #00d4ff, #7b2ff7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; animation: glow 3s ease-in-out infinite alternate; }
    @keyframes glow { from { filter: drop-shadow(0 0 10px #00d4ff); } to { filter: drop-shadow(0 0 30px #7b2ff7); } }
    .glass-card { background: rgba(255,255,255,0.05); backdrop-filter: blur(20px); border: 1px solid rgba(0,212,255,0.2); border-radius: 20px; padding: 2rem; margin: 1rem 0; }
    .stButton > button { background: linear-gradient(90deg, #00d4ff, #7b2ff7) !important; color: white !important; border: none !important; border-radius: 12px !important; padding: 0.8rem 3rem !important; font-family: 'Orbitron', monospace !important; font-weight: 700 !important; width: 100% !important; margin-top: 1rem !important; }
    .stNumberInput label, .stSelectbox label, .stSlider label { color: #00d4ff !important; }
    [data-testid="stSidebar"] { background: rgba(10,10,26,0.95) !important; border-right: 1px solid rgba(0,212,255,0.2) !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    p, label { color: rgba(255,255,255,0.8) !important; }
</style>
<div class="page-title">📊 DISEASE RISK GAUGE</div>
<p style="color: #00d4ff; letter-spacing: 2px; text-transform: uppercase; font-size: 0.9rem;">Visualize your health risk levels</p>
""", unsafe_allow_html=True)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=1, max_value=120, value=45)
    smoking = st.selectbox("Smoking Status", ["Never", "Former", "Current"])
    diabetes = st.selectbox("Diabetes", ["No", "Yes"])
    bp = st.selectbox("High Blood Pressure", ["No", "Yes"])

with col2:
    cholesterol = st.selectbox("High Cholesterol", ["No", "Yes"])
    exercise = st.selectbox("Regular Exercise", ["Yes", "No"])
    family_history = st.selectbox("Family History of Heart Disease", ["No", "Yes"])
    obesity = st.selectbox("Obesity (BMI > 30)", ["No", "Yes"])

st.markdown('</div>', unsafe_allow_html=True)

if st.button("⚡ CALCULATE RISK"):
    # Calculate risk score
    score = 0
    if age > 45: score += 20
    elif age > 35: score += 10
    if smoking == "Current": score += 25
    elif smoking == "Former": score += 10
    if diabetes == "Yes": score += 15
    if bp == "Yes": score += 15
    if cholesterol == "Yes": score += 10
    if exercise == "No": score += 10
    if family_history == "Yes": score += 10
    if obesity == "Yes": score += 10
    score = min(score, 100)

    if score < 25:
        risk_level = "LOW RISK"
        color = "#00ff96"
    elif score < 50:
        risk_level = "MODERATE RISK"
        color = "#ffaa00"
    elif score < 75:
        risk_level = "HIGH RISK"
        color = "#ff6600"
    else:
        risk_level = "VERY HIGH RISK"
        color = "#ff006e"

    col1, col2 = st.columns([1, 1])

    with col1:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "RISK SCORE", 'font': {'color': 'white', 'family': 'Orbitron', 'size': 16}},
            number={'font': {'color': color, 'family': 'Orbitron', 'size': 40}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': 'white', 'tickfont': {'color': 'white'}},
                'bar': {'color': color},
                'bgcolor': 'rgba(0,0,0,0)',
                'bordercolor': 'rgba(0,212,255,0.3)',
                'steps': [
                    {'range': [0, 25], 'color': 'rgba(0,255,150,0.2)'},
                    {'range': [25, 50], 'color': 'rgba(255,170,0,0.2)'},
                    {'range': [50, 75], 'color': 'rgba(255,102,0,0.2)'},
                    {'range': [75, 100], 'color': 'rgba(255,0,110,0.2)'},
                ],
                'threshold': {'line': {'color': color, 'width': 4}, 'thickness': 0.75, 'value': score}
            }
        ))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': 'white'},
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); border: 1px solid {color};
        border-radius: 20px; padding: 2rem; text-align: center; margin-top: 1rem;">
            <div style="font-family: Orbitron; color: {color}; font-size: 1.5rem; font-weight: 900;">
                {risk_level}
            </div>
            <div style="font-family: Orbitron; color: {color}; font-size: 3rem; font-weight: 900; margin: 1rem 0;">
                {score}%
            </div>
            <div style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">
                Based on your risk factors
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; color:rgba(255,255,255,0.5); margin-top:1rem; font-size:0.8rem;">
        ⚕️ Always consult a qualified doctor for proper diagnosis
    </div>
    """, unsafe_allow_html=True)
