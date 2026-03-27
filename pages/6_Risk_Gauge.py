import streamlit as st
from groq import Groq
import plotly.graph_objects as go

st.set_page_config(page_title="Disease Risk Gauge", page_icon="📊", layout="wide")

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
.risk-box { border-radius: 16px; padding: 1.5rem; text-align: center; margin-bottom: 1rem; }
.risk-label { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
.risk-value { font-size: 3.5rem; font-weight: 700; letter-spacing: -2px; line-height: 1; margin-bottom: 4px; }
.risk-status { font-size: 16px; font-weight: 600; margin-top: 8px; }
.factors-grid { display: grid; grid-template-columns: repeat(2,1fr); gap: 8px; margin-bottom: 1rem; }
.factor-item { background: white; border: 1px solid #e0ece0; border-radius: 10px; padding: 0.75rem 1rem; display: flex; align-items: center; justify-content: space-between; }
.factor-name { font-size: 12px; color: #3a4a3a; font-weight: 500; }
.factor-badge { font-size: 10px; padding: 2px 8px; border-radius: 20px; font-weight: 600; }
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
        <div class="topbar-title">📊 Disease Risk Gauge</div>
        <div class="topbar-sub">AI-powered cardiovascular risk assessment</div>
    </div>
    <div class="ai-badge"><span class="ai-dot"></span> Groq AI Active</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="form-card"><div class="form-header"><h2>🩺 Risk Factors</h2><span class="form-tag">8 Factors</span></div><div class="form-body">', unsafe_allow_html=True)

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
    # Risk calculation
    score = 0
    factors = {}

    if age > 55: score += 25; factors["Age > 55"] = ("High Risk", "#c0392b", "#fff0f0")
    elif age > 45: score += 15; factors["Age 45-55"] = ("Moderate Risk", "#d97706", "#fffbeb")
    elif age > 35: score += 8; factors["Age 35-45"] = ("Low Risk", "#27500a", "#f0fff4")
    else: factors["Age < 35"] = ("Minimal Risk", "#639922", "#f0fff4")

    if smoking == "Current": score += 25; factors["Smoking"] = ("Current Smoker", "#c0392b", "#fff0f0")
    elif smoking == "Former": score += 10; factors["Smoking"] = ("Former Smoker", "#d97706", "#fffbeb")
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
    else: factors["Obesity"] = ("Normal Weight", "#27500a", "#f0fff4")

    if stress == "Yes": score += 5; factors["Stress"] = ("High Stress", "#d97706", "#fffbeb")
    else: factors["Stress"] = ("Low Stress", "#27500a", "#f0fff4")

    score = min(score, 100)

    if score < 20:
        risk_level = "Low Risk"
        risk_color = "#27500a"
        risk_bg = "linear-gradient(135deg,#f0fff4,#e0ffe8)"
        risk_border = "#97c459"
    elif score < 40:
        risk_level = "Moderate Risk"
        risk_color = "#d97706"
        risk_bg = "linear-gradient(135deg,#fffbeb,#fef3c7)"
        risk_border = "#fbbf24"
    elif score < 65:
        risk_level = "High Risk"
        risk_color = "#ea580c"
        risk_bg = "linear-gradient(135deg,#fff7ed,#ffedd5)"
        risk_border = "#fb923c"
    else:
        risk_level = "Very High Risk"
        risk_color = "#c0392b"
        risk_bg = "linear-gradient(135deg,#fff0f0,#ffe0e0)"
        risk_border = "#f87171"

    col1, col2 = st.columns([1, 1])

    with col1:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Risk Score", 'font': {'color': '#1a3a1a', 'family': 'Inter', 'size': 14}},
            number={'font': {'color': risk_color, 'family': 'Inter', 'size': 48}, 'suffix': '%'},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': '#7a8f7a', 'tickfont': {'color': '#7a8f7a', 'size': 10}},
                'bar': {'color': risk_color, 'thickness': 0.3},
                'bgcolor': 'rgba(0,0,0,0)',
                'bordercolor': '#e0ece0',
                'borderwidth': 1,
                'steps': [
                    {'range': [0, 20], 'color': 'rgba(39,80,10,0.1)'},
                    {'range': [20, 40], 'color': 'rgba(217,119,6,0.1)'},
                    {'range': [40, 65], 'color': 'rgba(234,88,12,0.1)'},
                    {'range': [65, 100], 'color': 'rgba(192,57,43,0.1)'},
                ],
                'threshold': {
                    'line': {'color': risk_color, 'width': 3},
                    'thickness': 0.75,
                    'value': score
                }
            }
        ))
        fig.update_layout(
            paper_bgcolor='rgba(255,255,255,1)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#1a3a1a', 'family': 'Inter'},
            height=280,
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown(f"""
        <div class="risk-box" style="background:{risk_bg}; border:1px solid {risk_border};">
            <div class="risk-label" style="color:{risk_color}">Overall Risk Level</div>
            <div class="risk-value" style="color:{risk_color}">{score}%</div>
            <div class="risk-status" style="color:{risk_color}">{risk_level}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Risk Factor Summary:**")
        factors_html = '<div class="factors-grid">'
        for name, (status, color, bg) in list(factors.items())[:6]:
            factors_html += f"""
            <div class="factor-item" style="background:{bg};">
                <span class="factor-name">{name}</span>
                <span class="factor-badge" style="background:{bg};color:{color};border:1px solid {color}40">{status}</span>
            </div>
            """
        factors_html += '</div>'
        st.markdown(factors_html, unsafe_allow_html=True)

    with st.spinner("🤖 Getting AI prevention plan..."):
        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            active_risks = [k for k, v in factors.items() if "High" in v[0] or "Current" in v[0] or "Diabetic" in v[0] or "Obese" in v[0]]
            prompt = f"""
            Patient cardiovascular risk assessment:
            - Overall risk score: {score}% ({risk_level})
            - Age: {age}
            - Key risk factors present: {', '.join(active_risks) if active_risks else 'None significant'}
            - Exercise status: {exercise}
            - Smoking: {smoking}

            Provide a personalized 4-5 sentence cardiovascular disease prevention plan:
            1. Acknowledge their risk level honestly
            2. Top 2 most urgent lifestyle changes they should make
            3. Specific screening tests they should get
            4. One motivational closing statement
            Be direct, specific and actionable.
            End with: Consult a cardiologist for a comprehensive evaluation.
            """
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            )
            insight = response.choices[0].message.content
            st.markdown(f"""
            <div class="ai-insight">
                <div class="ai-insight-header">🤖 AI Prevention Plan</div>
                <div class="ai-insight-text">{insight}</div>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown('<div class="disclaimer">⚠️ For educational purposes only. Always consult a qualified doctor.</div>', unsafe_allow_html=True)
