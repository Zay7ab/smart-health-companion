import streamlit as st
import math

st.set_page_config(page_title="BMI & Vitals Calculator", page_icon="⚖️", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');
    .stApp { background: linear-gradient(135deg, #0a0a1a 0%, #0d1b2a 40%, #1a0a2e 100%); font-family: 'Rajdhani', sans-serif; }
    .page-title { font-family: 'Orbitron', monospace; font-size: 2.5rem; font-weight: 900; background: linear-gradient(90deg, #00d4ff, #7b2ff7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; animation: glow 3s ease-in-out infinite alternate; }
    @keyframes glow { from { filter: drop-shadow(0 0 10px #00d4ff); } to { filter: drop-shadow(0 0 30px #7b2ff7); } }
    .glass-card { background: rgba(255,255,255,0.05); backdrop-filter: blur(20px); border: 1px solid rgba(0,212,255,0.2); border-radius: 20px; padding: 2rem; margin: 1rem 0; animation: slideUp 0.8s ease-out; }
    @keyframes slideUp { from { opacity: 0; transform: translateY(40px); } to { opacity: 1; transform: translateY(0); } }
    .metric-box { background: rgba(0,212,255,0.1); border: 1px solid rgba(0,212,255,0.3); border-radius: 15px; padding: 1.5rem; text-align: center; margin: 0.5rem; }
    .metric-value { font-family: 'Orbitron', monospace; font-size: 2.5rem; font-weight: 900; color: #00d4ff; }
    .metric-label { color: rgba(255,255,255,0.6); font-size: 0.9rem; letter-spacing: 2px; text-transform: uppercase; }
    .stButton > button { background: linear-gradient(90deg, #00d4ff, #7b2ff7) !important; color: white !important; border: none !important; border-radius: 12px !important; padding: 0.8rem 3rem !important; font-family: 'Orbitron', monospace !important; font-weight: 700 !important; width: 100% !important; margin-top: 1rem !important; }
    .stSlider label, .stNumberInput label, .stSelectbox label { color: #00d4ff !important; font-family: 'Rajdhani', sans-serif !important; letter-spacing: 1px !important; }
    [data-testid="stSidebar"] { background: rgba(10,10,26,0.95) !important; border-right: 1px solid rgba(0,212,255,0.2) !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    p, label { color: rgba(255,255,255,0.8) !important; }
</style>
<div class="page-title">⚖️ BMI & VITALS CALCULATOR</div>
<p style="color: #00d4ff; letter-spacing: 2px; text-transform: uppercase; font-size: 0.9rem;">Calculate your health metrics instantly</p>
""", unsafe_allow_html=True)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📏 Body Metrics")
    height = st.number_input("Height (cm)", min_value=50, max_value=250, value=170)
    weight = st.number_input("Weight (kg)", min_value=10, max_value=300, value=70)
    age = st.number_input("Age", min_value=1, max_value=120, value=25)
    gender = st.selectbox("Gender", ["Male", "Female"])

with col2:
    st.markdown("### 💓 Vital Signs")
    systolic = st.number_input("Systolic BP (mmHg)", min_value=50, max_value=250, value=120)
    diastolic = st.number_input("Diastolic BP (mmHg)", min_value=30, max_value=150, value=80)
    heart_rate = st.number_input("Heart Rate (bpm)", min_value=30, max_value=220, value=72)
    temp = st.number_input("Body Temperature (°C)", min_value=30.0, max_value=45.0, value=37.0)

st.markdown('</div>', unsafe_allow_html=True)

if st.button("⚡ CALCULATE METRICS"):
    # BMI
    height_m = height / 100
    bmi = weight / (height_m ** 2)

    if bmi < 18.5:
        bmi_status = "UNDERWEIGHT"
        bmi_color = "#00d4ff"
    elif bmi < 25:
        bmi_status = "NORMAL"
        bmi_color = "#00ff96"
    elif bmi < 30:
        bmi_status = "OVERWEIGHT"
        bmi_color = "#ffaa00"
    else:
        bmi_status = "OBESE"
        bmi_color = "#ff006e"

    # BMR
    if gender == "Male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    # BP Status
    if systolic < 120 and diastolic < 80:
        bp_status = "NORMAL"
        bp_color = "#00ff96"
    elif systolic < 130:
        bp_status = "ELEVATED"
        bp_color = "#ffaa00"
    elif systolic < 140:
        bp_status = "HIGH STAGE 1"
        bp_color = "#ff6600"
    else:
        bp_status = "HIGH STAGE 2"
        bp_color = "#ff006e"

    # Ideal Weight
    if gender == "Male":
        ideal_weight = 50 + 2.3 * ((height - 152.4) / 2.54)
    else:
        ideal_weight = 45.5 + 2.3 * ((height - 152.4) / 2.54)

    st.markdown("### 📊 Your Results")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value" style="color:{bmi_color}">{bmi:.1f}</div>
            <div class="metric-label">BMI</div>
            <div style="color:{bmi_color}; font-size:0.8rem; margin-top:0.5rem">{bmi_status}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{bmr:.0f}</div>
            <div class="metric-label">BMR (kcal/day)</div>
            <div style="color:rgba(255,255,255,0.5); font-size:0.8rem; margin-top:0.5rem">Base Metabolic Rate</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value" style="color:{bp_color}">{systolic}/{diastolic}</div>
            <div class="metric-label">Blood Pressure</div>
            <div style="color:{bp_color}; font-size:0.8rem; margin-top:0.5rem">{bp_status}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{ideal_weight:.1f}</div>
            <div class="metric-label">Ideal Weight (kg)</div>
            <div style="color:rgba(255,255,255,0.5); font-size:0.8rem; margin-top:0.5rem">Based on height</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; color:rgba(255,255,255,0.5); margin-top:1rem; font-size:0.8rem;">
        ⚕️ Always consult a qualified doctor for proper diagnosis
    </div>
    """, unsafe_allow_html=True)
