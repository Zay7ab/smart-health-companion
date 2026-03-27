import streamlit as st
from groq import Groq

st.set_page_config(page_title="Symptom Checker", page_icon="🔍", layout="wide")

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
.condition-card { background: white; border-radius: 14px; padding: 1.25rem; margin-bottom: 10px; border-left: 4px solid; }
.condition-title { font-size: 14px; font-weight: 700; margin-bottom: 4px; }
.condition-urgency { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }
.condition-desc { font-size: 12px; color: #5a6b5a; line-height: 1.6; margin-bottom: 8px; }
.condition-action { font-size: 12px; font-weight: 600; }
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
        <div class="topbar-title">🔍 Symptom Checker</div>
        <div class="topbar-sub">AI-powered symptom analysis via Groq LLaMA</div>
    </div>
    <div class="ai-badge"><span class="ai-dot"></span> Groq AI Active</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="form-card"><div class="form-header"><h2>🩺 Patient Information</h2><span class="form-tag">AI Powered</span></div><div class="form-body">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    age = st.number_input("Age", min_value=1, max_value=120, value=30)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
with col2:
    duration = st.selectbox("Duration of Symptoms", [
        "Less than 24 hours",
        "1-3 days",
        "3-7 days",
        "1-2 weeks",
        "More than 2 weeks"
    ])
    severity = st.select_slider("Severity", options=["Mild", "Moderate", "Severe", "Very Severe"])
with col3:
    existing = st.multiselect("Existing Conditions", [
        "Diabetes", "Hypertension", "Heart Disease",
        "Asthma", "None"
    ], default=["None"])
    medications = st.text_input("Current Medications (optional)")

st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown('<div class="form-card"><div class="form-header"><h2>🤒 Select Your Symptoms</h2><span class="form-tag">Multiple Selection</span></div><div class="form-body">', unsafe_allow_html=True)

all_symptoms = [
    "Fever", "Headache", "Chest Pain", "Shortness of Breath",
    "Cough", "Fatigue", "Dizziness", "Nausea", "Vomiting",
    "Abdominal Pain", "Back Pain", "Joint Pain", "Muscle Pain",
    "Sore Throat", "Runny Nose", "Loss of Appetite", "Weight Loss",
    "Night Sweats", "Swollen Lymph Nodes", "Skin Rash",
    "Blurred Vision", "Frequent Urination", "Excessive Thirst",
    "Numbness", "Palpitations", "Swollen Legs", "Difficulty Swallowing"
]

col1, col2, col3, col4 = st.columns(4)
selected_symptoms = []
symptoms_per_col = len(all_symptoms) // 4 + 1

for i, symptom in enumerate(all_symptoms):
    col = [col1, col2, col3, col4][i % 4]
    with col:
        if st.checkbox(symptom, key=f"sym_{i}"):
            selected_symptoms.append(symptom)

additional = st.text_area("Any additional symptoms or details?", placeholder="Describe any other symptoms or relevant information...")

st.markdown('</div></div>', unsafe_allow_html=True)

if st.button("⚡ Analyze Symptoms with AI"):
    if not selected_symptoms:
        st.warning("Please select at least one symptom.")
    else:
        with st.spinner("🤖 AI analyzing your symptoms..."):
            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                prompt = f"""
                Patient symptom analysis:
                - Age: {age}, Gender: {gender}
                - Symptoms: {', '.join(selected_symptoms)}
                - Duration: {duration}
                - Severity: {severity}
                - Existing conditions: {', '.join(existing)}
                - Current medications: {medications if medications else 'None'}
                - Additional info: {additional if additional else 'None'}

                Provide a structured medical analysis:

                1. TOP 3 POSSIBLE CONDITIONS (most likely first):
                For each condition provide:
                - Condition name
                - Urgency level (Emergency/Urgent/Moderate/Low)
                - Why these symptoms match
                - Recommended immediate action

                2. RED FLAGS: List any symptoms that require immediate emergency care

                3. NEXT STEPS: What the patient should do in the next 24 hours

                Be professional, clear and appropriately cautious.
                End with: This is not a medical diagnosis. Please consult a qualified doctor immediately.
                """
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=600
                )
                result = response.choices[0].message.content

                st.markdown("### 🔬 AI Analysis Results")
                st.markdown(f"""
                <div class="ai-insight">
                    <div class="ai-insight-header">🤖 AI Symptom Analysis — {', '.join(selected_symptoms[:3])}{'...' if len(selected_symptoms) > 3 else ''}</div>
                    <div class="ai-insight-text">{result.replace(chr(10), '<br>')}</div>
                </div>
                """, unsafe_allow_html=True)

                # Urgency warning
                if severity in ["Severe", "Very Severe"] or "Chest Pain" in selected_symptoms or "Shortness of Breath" in selected_symptoms:
                    st.markdown("""
                    <div style="background:linear-gradient(135deg,#fff0f0,#ffe0e0); border:1px solid #ffb3b3;
                    border-radius:12px; padding:1rem 1.25rem; margin-top:1rem;">
                        <div style="font-size:14px; font-weight:700; color:#c0392b; margin-bottom:4px;">
                            🚨 Urgent Medical Attention Recommended
                        </div>
                        <div style="font-size:12px; color:#7a3a3a;">
                            Your symptoms suggest you should seek medical care immediately.
                            Please visit your nearest emergency room or call emergency services.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown('<div class="disclaimer">⚠️ For educational purposes only. Always consult a qualified doctor immediately for medical emergencies.</div>', unsafe_allow_html=True)
