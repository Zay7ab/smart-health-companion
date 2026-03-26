import streamlit as st
import joblib
import numpy as np

st.set_page_config(page_title="Heart Disease Prediction", page_icon="🫀", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');

    .stApp {
        background: linear-gradient(135deg, #0a0a1a 0%, #0d1b2a 40%, #1a0a2e 100%);
        font-family: 'Rajdhani', sans-serif;
    }
    .page-title {
        font-family: 'Orbitron', monospace;
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00d4ff, #7b2ff7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: glow 3s ease-in-out infinite alternate;
        margin-bottom: 0.5rem;
    }
    @keyframes glow {
        from { filter: drop-shadow(0 0 10px #00d4ff); }
        to { filter: drop-shadow(0 0 30px #7b2ff7); }
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        animation: slideUp 0.8s ease-out;
    }
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(40px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stSelectbox label, .stNumberInput label {
        color: #00d4ff !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1rem !important;
        letter-spacing: 1px !important;
    }
    div[data-testid="stSelectbox"] > div,
    div[data-testid="stNumberInput"] > div > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    .stButton > button {
        background: linear-gradient(90deg, #00d4ff, #7b2ff7) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 3rem !important;
        font-family: 'Orbitron', monospace !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin-top: 1rem !important;
    }
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 30px rgba(123, 47, 247, 0.5) !important;
    }
    .result-high {
        background: rgba(255, 0, 110, 0.15);
        border: 1px solid rgba(255, 0, 110, 0.5);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        color: #ff006e;
        font-family: 'Orbitron', monospace;
        font-size: 1.2rem;
        animation: pulse 2s infinite;
    }
    .result-low {
        background: rgba(0, 255, 150, 0.15);
        border: 1px solid rgba(0, 255, 150, 0.5);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        color: #00ff96;
        font-family: 'Orbitron', monospace;
        font-size: 1.2rem;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(0, 212, 255, 0.4); }
        70% { box-shadow: 0 0 0 15px rgba(0, 212, 255, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 212, 255, 0); }
    }
    [data-testid="stSidebar"] {
        background: rgba(10, 10, 26, 0.95) !important;
        border-right: 1px solid rgba(0, 212, 255, 0.2) !important;
    }
    [data-testid="stSidebar"] * { color: white !important; }
    p, label { color: rgba(255,255,255,0.8) !important; }
</style>

<div class="page-title">🫀 HEART DISEASE PREDICTION</div>
<p style="color: #00d4ff; letter-spacing: 2px; text-transform: uppercase; font-size: 0.9rem;">
    Enter your health data below for AI-powered analysis
</p>
""", unsafe_allow_html=True)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    id = st.number_input("Patient ID", value=1)
    age = st.number_input("Age", min_value=1, max_value=120, value=50)
    sex = st.selectbox("Sex", ["Male", "Female"])
    dataset = st.selectbox("Dataset Source", [0, 1, 2, 3])
    cp = st.selectbox("Chest Pain Type", [0, 1, 2, 3])
    trestbps = st.number_input("Resting Blood Pressure", value=120)
    chol = st.number_input("Cholesterol", value=200)
    fbs = st.selectbox("Fasting Blood Sugar > 120mg/dl", [0, 1])

with col2:
    restecg = st.selectbox("Resting ECG", [0, 1, 2])
    thalach = st.number_input("Max Heart Rate", value=150)
    exang = st.selectbox("Exercise Induced Angina", [0, 1])
    oldpeak = st.number_input("ST Depression", value=0.0)
    slope = st.selectbox("Slope", [0, 1, 2])
    ca = st.selectbox("Number of Major Vessels", [0, 1, 2, 3])
    thal = st.selectbox("Thal", [0, 1, 2, 3])

st.markdown('</div>', unsafe_allow_html=True)

if st.button("⚡ ANALYZE NOW"):
    try:
        model = joblib.load('models/rf_model.pkl')
        scaler = joblib.load('models/scaler.pkl')

        sex_val = 1 if sex == "Male" else 0
        input_data = np.array([[id, age, sex_val, dataset, cp, trestbps,
                                 chol, fbs, restecg, thalach, exang,
                                 oldpeak, slope, ca, thal]])

        input_scaled = scaler.transform(input_data)
        prediction = model.predict(input_scaled)
        probability = model.predict_proba(input_scaled)[0][1]

        if prediction[0] == 1:
            st.markdown(f"""
            <div class="result-high">
                ⚠️ HIGH RISK DETECTED<br>
                <span style="font-size:2rem">{probability*100:.1f}%</span><br>
                <span style="font-size:0.8rem">Probability of Heart Disease</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-low">
                ✅ LOW RISK<br>
                <span style="font-size:2rem">{(1-probability)*100:.1f}%</span><br>
                <span style="font-size:0.8rem">Probability of Being Healthy</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align:center; color: rgba(255,255,255,0.5); 
        margin-top:1rem; font-size:0.8rem;">
            ⚕️ Always consult a qualified doctor for proper diagnosis
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error: {e}")
