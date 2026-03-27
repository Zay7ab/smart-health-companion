import streamlit as st
from groq import Groq

st.set_page_config(page_title="BMI & Vitals Calculator", page_icon="⚖️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: #f0f4f0 !important; }
[data-testid="stSidebar"] { background: #ffffff !important; border-right: 1px solid #e0ece0 !important; }
[data-testid="stSidebar"] * { color: #1a3a1a !important; }
[data-testid="stSidebarNav"] a[aria-current="page"] { background: linear-gradient(135deg,#eaf3de,#d4edbe) !important; color: #27500a !important; font-weight: 600 !important; }
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
.metrics-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 10px; margin-bottom: 1rem; }
.metric-card { border-radius: 14px; padding: 1.25rem; text-align: center; position: relative; overflow: hidden; }
.metric-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; }
.metric-label { font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px; }
.metric-value { font-size: 26px; font-weight: 700; letter-spacing: -0.5px; margin-bottom: 4px; }
.metric-status { font-size: 11px; font-weight: 600; }
.bmi-bar { background: #f0f4f0; border-radius: 10px; height: 12px; margin: 0.75rem 0; position: relative; overflow: hidden; }
.bmi-bar-fill { height: 100%; border-radius: 10px; transition: width 0.5s ease; }
.bmi-labels { display: flex; justify-content: space-between; font-size: 10px; color: #7a8f7a; margin-top: 4px; }
.ai-insight { background: white; border: 1px solid #e0ece0; border-radius: 12px; padding: 1rem; margin-top: 1rem; }
.ai-insight-header { display: flex; align-items: center; gap: 6px; font-size: 11px; font-weight: 600; color: #639922; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }
.ai-insight-text { font-size: 13px; color: #3a4a3a; line-height: 1.7; }
.disclaimer { background: #fff8e1; border: 1px solid #f0c040; border-radius: 10px; padding: 0.75rem 1rem; font-size: 11px; color: #7a6000; margin-top: 1rem; }
div[data-testid="stButton"] button { background: linear-gradient(135deg,#3b6d11,#639922) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; font-size: 13px !important; padding: 0.6rem 1.5rem !important; }
div[data-testid="stButton"] button:hover { background: linear-gradient(135deg,#27500a,#3b6d11) !important; box-shadow: 0 4px 15px rgba(99,153,34,0.3) !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="topbar">
    <div>
        <div class="topbar-title">⚖️ BMI & Vitals Calculator</div>
        <div class="topbar-sub">Calculate your health metrics with AI-powered insights</div>
    </div>
    <div class="ai-badge"><span class="ai-dot"></span> Groq AI Active</div>
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
    activity = st.selectbox("Activity Level", [
        "Sedentary (little/no exercise)",
        "Lightly active (1-3 days/week)",
        "Moderately active (3-5 days/week)",
        "Very active (6-7 days/week)",
        "Extra active (physical job)"
    ])
    goal = st.selectbox("Health Goal", ["Lose Weight", "Maintain Weight", "Gain Muscle"])

st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown('<div class="form-card"><div class="form-header"><h2>💓 Vital Signs</h2><span class="form-tag">Optional</span></div><div class="form-body">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    systolic = st.number_input("Systolic BP (mmHg)", min_value=50, max_value=250, value=120)
with col2:
    diastolic = st.number_input("Diastolic BP (mmHg)", min_value=30, max_value=150, value=80)
with col3:
    heart_rate = st.number_input("Heart Rate (bpm)", min_value=30, max_value=220, value=72)
with col4:
    temp = st.number_input("Body Temp (°C)", min_value=30.0, max_value=45.0, value=37.0)

st.markdown('</div></div>', unsafe_allow_html=True)

if st.button("⚡ Calculate & Get AI Insights"):
    # Calculations
    height_m = height / 100
    bmi = weight / (height_m ** 2)

    if bmi < 18.5:
        bmi_status = "Underweight"
        bmi_color = "#3b82f6"
        bmi_bg = "#eff6ff"
        bmi_pct = int((bmi / 40) * 100)
    elif bmi < 25:
        bmi_status = "Normal"
        bmi_color = "#27500a"
        bmi_bg = "#f0fff4"
        bmi_pct = int((bmi / 40) * 100)
    elif bmi < 30:
        bmi_status = "Overweight"
        bmi_color = "#d97706"
        bmi_bg = "#fffbeb"
        bmi_pct = int((bmi / 40) * 100)
    else:
        bmi_status = "Obese"
        bmi_color = "#c0392b"
        bmi_bg = "#fff0f0"
        bmi_pct = min(int((bmi / 40) * 100), 100)

    if gender == "Male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    activity_multipliers = {
        "Sedentary (little/no exercise)": 1.2,
        "Lightly active (1-3 days/week)": 1.375,
        "Moderately active (3-5 days/week)": 1.55,
        "Very active (6-7 days/week)": 1.725,
        "Extra active (physical job)": 1.9
    }
    tdee = bmr * activity_multipliers[activity]

    if gender == "Male":
        ideal_weight = 50 + 2.3 * ((height - 152.4) / 2.54)
    else:
        ideal_weight = 45.5 + 2.3 * ((height - 152.4) / 2.54)

    if systolic < 120 and diastolic < 80:
        bp_status = "Normal"
        bp_color = "#27500a"
    elif systolic < 130:
        bp_status = "Elevated"
        bp_color = "#d97706"
    elif systolic < 140:
        bp_status = "High Stage 1"
        bp_color = "#ea580c"
    else:
        bp_status = "High Stage 2"
        bp_color = "#c0392b"

    st.markdown("### 📊 Your Results")
    st.markdown(f"""
    <div class="metrics-grid">
        <div class="metric-card" style="background:{bmi_bg}; border:1px solid {bmi_color}40;">
            <div class="metric-card" style="position:absolute;top:0;left:0;right:0;height:3px;background:{bmi_color};border-radius:0;"></div>
            <div class="metric-label" style="color:{bmi_color}">BMI</div>
            <div class="metric-value" style="color:{bmi_color}">{bmi:.1f}</div>
            <div class="metric-status" style="color:{bmi_color}">{bmi_status}</div>
        </div>
        <div class="metric-card" style="background:#f0fff4; border:1px solid #97c45940;">
            <div class="metric-label" style="color:#27500a">Daily Calories</div>
            <div class="metric-value" style="color:#27500a">{tdee:.0f}</div>
            <div class="metric-status" style="color:#639922">kcal/day (TDEE)</div>
        </div>
        <div class="metric-card" style="background:#f0fff4; border:1px solid #97c45940;">
            <div class="metric-label" style="color:#27500a">Ideal Weight</div>
            <div class="metric-value" style="color:#27500a">{ideal_weight:.1f}</div>
            <div class="metric-status" style="color:#639922">kg for your height</div>
        </div>
        <div class="metric-card" style="background:#f8f8ff; border:1px solid {bp_color}40;">
            <div class="metric-label" style="color:{bp_color}">Blood Pressure</div>
            <div class="metric-value" style="color:{bp_color}; font-size:20px">{systolic}/{diastolic}</div>
            <div class="metric-status" style="color:{bp_color}">{bp_status}</div>
        </div>
    </div>
    <div style="background:white; border:1px solid #e0ece0; border-radius:12px; padding:1rem; margin-bottom:1rem;">
        <div style="font-size:12px; font-weight:600; color:#1a3a1a; margin-bottom:8px;">BMI Scale</div>
        <div class="bmi-bar">
            <div class="bmi-bar-fill" style="width:{bmi_pct}%; background:{bmi_color};"></div>
        </div>
        <div class="bmi-labels">
            <span>Underweight &lt;18.5</span>
            <span>Normal 18.5-24.9</span>
            <span>Overweight 25-29.9</span>
            <span>Obese &gt;30</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("🤖 Getting AI insights..."):
        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            prompt = f"""
            Patient health metrics:
            - BMI: {bmi:.1f} ({bmi_status})
            - Age: {age}, Gender: {gender}
            - Daily calorie needs (TDEE): {tdee:.0f} kcal
            - Ideal weight: {ideal_weight:.1f} kg (current: {weight} kg)
            - Blood pressure: {systolic}/{diastolic} ({bp_status})
            - Heart rate: {heart_rate} bpm
            - Health goal: {goal}
            - Activity level: {activity}

            Give a personalized 4-5 sentence health plan including:
            1. Assessment of their current health metrics
            2. Specific diet recommendations for their goal
            3. Exercise recommendations
            4. One key health warning if any metrics are concerning
            Be specific, practical and motivating.
            End with: Always consult a qualified doctor before starting any health program.
            """
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            )
            insight = response.choices[0].message.content
            st.markdown(f"""
            <div class="ai-insight">
                <div class="ai-insight-header">🤖 AI Personalized Health Plan</div>
                <div class="ai-insight-text">{insight}</div>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown('<div class="disclaimer">⚠️ For educational purposes only. Always consult a qualified doctor.</div>', unsafe_allow_html=True)
