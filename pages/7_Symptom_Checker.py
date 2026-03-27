import streamlit as st

st.set_page_config(page_title="Symptom Checker", page_icon="🔍", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');
    .stApp { background: linear-gradient(135deg, #0a0a1a 0%, #0d1b2a 40%, #1a0a2e 100%); font-family: 'Rajdhani', sans-serif; }
    .page-title { font-family: 'Orbitron', monospace; font-size: 2.5rem; font-weight: 900; background: linear-gradient(90deg, #00d4ff, #7b2ff7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; animation: glow 3s ease-in-out infinite alternate; }
    @keyframes glow { from { filter: drop-shadow(0 0 10px #00d4ff); } to { filter: drop-shadow(0 0 30px #7b2ff7); } }
    .glass-card { background: rgba(255,255,255,0.05); backdrop-filter: blur(20px); border: 1px solid rgba(0,212,255,0.2); border-radius: 20px; padding: 2rem; margin: 1rem 0; }
    .symptom-tag { display: inline-block; background: rgba(0,212,255,0.15); border: 1px solid rgba(0,212,255,0.4); border-radius: 25px; padding: 0.4rem 1rem; margin: 0.3rem; color: #00d4ff; font-size: 0.9rem; }
    .condition-card { background: rgba(255,255,255,0.05); border: 1px solid rgba(123,47,247,0.3); border-radius: 15px; padding: 1.5rem; margin: 0.8rem 0; animation: slideUp 0.5s ease-out; }
    @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    .stButton > button { background: linear-gradient(90deg, #00d4ff, #7b2ff7) !important; color: white !important; border: none !important; border-radius: 12px !important; padding: 0.8rem 3rem !important; font-family: 'Orbitron', monospace !important; font-weight: 700 !important; width: 100% !important; margin-top: 1rem !important; }
    [data-testid="stSidebar"] { background: rgba(10,10,26,0.95) !important; border-right: 1px solid rgba(0,212,255,0.2) !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    p, label { color: rgba(255,255,255,0.8) !important; }
</style>
<div class="page-title">🔍 SYMPTOM CHECKER</div>
<p style="color: #00d4ff; letter-spacing: 2px; text-transform: uppercase; font-size: 0.9rem;">Select your symptoms for AI-powered analysis</p>
""", unsafe_allow_html=True)

symptom_conditions = {
    ("chest pain", "shortness of breath", "dizziness"): {"condition": "Possible Cardiac Issue", "urgency": "🔴 URGENT", "color": "#ff006e", "advice": "Seek emergency medical attention immediately."},
    ("fever", "cough", "shortness of breath"): {"condition": "Possible Respiratory Infection / Pneumonia", "urgency": "🟠 HIGH", "color": "#ff6600", "advice": "Visit a doctor within 24 hours. Rest and stay hydrated."},
    ("headache", "fever", "stiff neck"): {"condition": "Possible Meningitis", "urgency": "🔴 URGENT", "color": "#ff006e", "advice": "Seek emergency medical attention immediately."},
    ("fatigue", "excessive thirst", "frequent urination"): {"condition": "Possible Diabetes", "urgency": "🟡 MODERATE", "color": "#ffaa00", "advice": "Schedule a blood glucose test with your doctor."},
    ("headache", "nausea", "sensitivity to light"): {"condition": "Possible Migraine", "urgency": "🟡 MODERATE", "color": "#ffaa00", "advice": "Rest in a dark room. Consult a doctor if recurring."},
    ("joint pain", "fatigue", "fever"): {"condition": "Possible Arthritis or Lupus", "urgency": "🟡 MODERATE", "color": "#ffaa00", "advice": "Consult a rheumatologist for proper evaluation."},
    ("abdominal pain", "nausea", "vomiting"): {"condition": "Possible Gastroenteritis or Appendicitis", "urgency": "🟠 HIGH", "color": "#ff6600", "advice": "Monitor symptoms. Seek care if pain worsens."},
    ("cough", "fever", "fatigue"): {"condition": "Possible Flu or COVID-19", "urgency": "🟡 MODERATE", "color": "#ffaa00", "advice": "Get tested. Isolate and rest at home."},
}

all_symptoms = sorted(set(s for combo in symptom_conditions.keys() for s in combo))

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
selected = st.multiselect("🩺 Select your symptoms:", all_symptoms)
duration = st.selectbox("⏱ Duration of symptoms:", ["Less than 24 hours", "1-3 days", "3-7 days", "More than a week"])
severity = st.select_slider("📊 Severity:", options=["Mild", "Moderate", "Severe", "Very Severe"])
st.markdown('</div>', unsafe_allow_html=True)

if st.button("⚡ CHECK SYMPTOMS") and selected:
    matched = []
    for combo, info in symptom_conditions.items():
        overlap = len(set(selected) & set(combo))
        if overlap >= 2:
            matched.append((overlap, info, combo))

    matched.sort(reverse=True)

    if matched:
        st.markdown("### 🔬 Possible Conditions")
        for _, info, combo in matched[:3]:
            st.markdown(f"""
            <div class="condition-card">
                <div style="font-family: Orbitron; color: {info['color']}; font-size: 1rem; margin-bottom: 0.5rem;">
                    {info['urgency']} — {info['condition']}
                </div>
                <div style="color: rgba(255,255,255,0.7); margin-bottom: 0.5rem;">
                    🔗 Matching symptoms: {', '.join(combo)}
                </div>
                <div style="color: rgba(255,255,255,0.9);">
                    💊 {info['advice']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="condition-card">
            <div style="color: #00ff96; font-family: Orbitron;">✅ NO SERIOUS MATCHES FOUND</div>
            <div style="color: rgba(255,255,255,0.7); margin-top: 0.5rem;">
                Your symptoms don't match serious conditions in our database.
                Monitor your symptoms and consult a doctor if they worsen.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; color:rgba(255,255,255,0.5); margin-top:1rem; font-size:0.8rem;">
        ⚕️ This is not a medical diagnosis. Always consult a qualified doctor.
    </div>
    """, unsafe_allow_html=True)
