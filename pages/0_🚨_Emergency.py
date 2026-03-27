import streamlit as st
from groq import Groq
import sys
sys.path.append('.')
from utils.sidebar import load_sidebar

st.set_page_config(page_title="Emergency SOS", page_icon="🚨", layout="wide")
load_sidebar()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: #f0f4f0 !important; }
.emergency-hero { background: linear-gradient(135deg, #7f0000, #c0392b); border-radius: 20px; padding: 2rem 2.5rem; margin-bottom: 1.5rem; }
.emergency-hero h1 { font-size: 2rem; font-weight: 700; color: white; margin-bottom: 0.5rem; }
.emergency-hero p { font-size: 13px; color: rgba(255,255,255,0.8); line-height: 1.6; max-width: 600px; }
.emergency-badge { display: inline-flex; align-items: center; gap: 6px; background: rgba(255,255,255,0.2); border: 1px solid rgba(255,255,255,0.3); border-radius: 20px; padding: 4px 12px; font-size: 11px; color: #ffcccc; font-weight: 600; letter-spacing: 1px; margin-bottom: 1rem; }
.sos-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 12px; margin-bottom: 1.5rem; }
.sos-card { background: white; border: 2px solid #ffb3b3; border-radius: 16px; padding: 1.25rem; text-align: center; transition: all 0.2s; }
.sos-card:hover { border-color: #c0392b; box-shadow: 0 4px 20px rgba(192,57,43,0.15); transform: translateY(-2px); }
.sos-icon { font-size: 2.5rem; margin-bottom: 0.75rem; }
.sos-title { font-size: 14px; font-weight: 700; color: #1a3a1a; margin-bottom: 4px; }
.sos-number { font-size: 20px; font-weight: 700; color: #c0392b; }
.sos-desc { font-size: 11px; color: #7a8f7a; margin-top: 4px; }
.warning-signs { display: grid; grid-template-columns: repeat(2,1fr); gap: 10px; margin-bottom: 1.5rem; }
.warning-card { background: white; border: 1px solid #ffb3b3; border-radius: 12px; padding: 1rem; display: flex; align-items: center; gap: 10px; }
.warning-icon { font-size: 1.5rem; flex-shrink: 0; }
.warning-text { font-size: 13px; font-weight: 600; color: #c0392b; }
.warning-sub { font-size: 11px; color: #7a8f7a; margin-top: 2px; }
.form-card { background: white; border: 1px solid #e0ece0; border-radius: 16px; overflow: hidden; margin-bottom: 1rem; }
.form-header { padding: 1rem 1.25rem; background: linear-gradient(135deg,#fff0f0,#ffe0e0); border-bottom: 1px solid #ffb3b3; display: flex; align-items: center; justify-content: space-between; }
.form-header h2 { font-size: 14px; font-weight: 600; color: #c0392b; }
.form-tag { font-size: 10px; color: #c0392b; background: #ffcccc; padding: 2px 8px; border-radius: 20px; font-weight: 600; }
.form-body { padding: 1.25rem; }
.ai-insight { background: white; border: 1px solid #ffb3b3; border-radius: 12px; padding: 1rem; margin-top: 1rem; }
.ai-insight-header { font-size: 11px; font-weight: 600; color: #c0392b; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }
.ai-insight-text { font-size: 13px; color: #3a4a3a; line-height: 1.7; }
.steps-card { background: linear-gradient(135deg,#7f0000,#c0392b); border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem; }
.steps-title { font-size: 13px; font-weight: 700; color: white; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 1px; }
.step-item { display: flex; align-items: flex-start; gap: 10px; margin-bottom: 10px; }
.step-num { width: 24px; height: 24px; border-radius: 50%; background: rgba(255,255,255,0.2); display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; color: white; flex-shrink: 0; }
.step-text { font-size: 12px; color: rgba(255,255,255,0.9); line-height: 1.5; }
.disclaimer { background: #fff8e1; border: 1px solid #f0c040; border-radius: 10px; padding: 0.75rem 1rem; font-size: 11px; color: #7a6000; margin-top: 1rem; }
div[data-testid="stButton"] button { background: linear-gradient(135deg,#7f0000,#c0392b) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; font-size: 13px !important; padding: 0.6rem 1.5rem !important; }
div[data-testid="stButton"] button:hover { background: linear-gradient(135deg,#5c0000,#a93226) !important; box-shadow: 0 4px 15px rgba(192,57,43,0.4) !important; }
label { color: #1a3a1a !important; }
p { color: #1a3a1a !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="emergency-hero">
    <div class="emergency-badge">🚨 EMERGENCY GUIDE</div>
    <h1>🚨 Emergency SOS & First Aid</h1>
    <p>Immediate guidance for medical emergencies. Describe your emergency below for instant AI-powered first aid instructions. Always call emergency services first in life-threatening situations.</p>
</div>
""", unsafe_allow_html=True)

# Emergency numbers
st.markdown("### 📞 Emergency Numbers")
st.markdown("""
<div class="sos-grid">
    <div class="sos-card">
        <div class="sos-icon">🚑</div>
        <div class="sos-title">Ambulance</div>
        <div class="sos-number">999 / 911 / 112</div>
        <div class="sos-desc">Life-threatening emergencies</div>
    </div>
    <div class="sos-card">
        <div class="sos-icon">🚒</div>
        <div class="sos-title">Fire & Rescue</div>
        <div class="sos-number">997 / 911</div>
        <div class="sos-desc">Fire, accidents, entrapment</div>
    </div>
    <div class="sos-card">
        <div class="sos-icon">👮</div>
        <div class="sos-title">Police</div>
        <div class="sos-number">999 / 911 / 112</div>
        <div class="sos-desc">Crime, violence, accidents</div>
    </div>
    <div class="sos-card">
        <div class="sos-icon">☎️</div>
        <div class="sos-title">UAE Emergency</div>
        <div class="sos-number">999</div>
        <div class="sos-desc">All emergencies in UAE</div>
    </div>
    <div class="sos-card">
        <div class="sos-icon">🏥</div>
        <div class="sos-title">Poison Control</div>
        <div class="sos-number">800-424-8802</div>
        <div class="sos-desc">Poisoning & overdose</div>
    </div>
    <div class="sos-card">
        <div class="sos-icon">🧠</div>
        <div class="sos-title">Mental Health Crisis</div>
        <div class="sos-number">800-HOPE</div>
        <div class="sos-desc">Suicide & mental health crisis</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Warning signs
st.markdown("### ⚠️ Call Emergency Services Immediately If You See:")
st.markdown("""
<div class="warning-signs">
    <div class="warning-card">
        <div class="warning-icon">💔</div>
        <div>
            <div class="warning-text">Chest pain or pressure</div>
            <div class="warning-sub">Could be a heart attack — every second counts</div>
        </div>
    </div>
    <div class="warning-card">
        <div class="warning-icon">🫁</div>
        <div>
            <div class="warning-text">Difficulty breathing</div>
            <div class="warning-sub">Severe shortness of breath or choking</div>
        </div>
    </div>
    <div class="warning-card">
        <div class="warning-icon">🧠</div>
        <div>
            <div class="warning-text">Sudden confusion or stroke signs</div>
            <div class="warning-sub">Face drooping, arm weakness, speech difficulty</div>
        </div>
    </div>
    <div class="warning-card">
        <div class="warning-icon">🩸</div>
        <div>
            <div class="warning-text">Severe bleeding</div>
            <div class="warning-sub">Uncontrolled bleeding from any wound</div>
        </div>
    </div>
    <div class="warning-card">
        <div class="warning-icon">😵</div>
        <div>
            <div class="warning-text">Loss of consciousness</div>
            <div class="warning-sub">Person is unresponsive or unconscious</div>
        </div>
    </div>
    <div class="warning-card">
        <div class="warning-icon">🤢</div>
        <div>
            <div class="warning-text">Severe allergic reaction</div>
            <div class="warning-sub">Swelling of throat, difficulty swallowing</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# AI Emergency Guide
st.markdown('<div class="form-card"><div class="form-header"><h2>🤖 AI Emergency First Aid Guide</h2><span class="form-tag">Instant Help</span></div><div class="form-body">', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    emergency_type = st.selectbox("Emergency Type", [
        "Heart Attack",
        "Stroke",
        "Choking",
        "Severe Bleeding",
        "Burns",
        "Fracture / Broken Bone",
        "Allergic Reaction / Anaphylaxis",
        "Seizure / Epilepsy",
        "Drowning",
        "Electric Shock",
        "Poisoning / Overdose",
        "Diabetic Emergency",
        "Asthma Attack",
        "Head Injury",
        "Loss of Consciousness",
        "Other Emergency"
    ])
with col2:
    patient_age = st.selectbox("Patient Age Group", ["Adult (18+)", "Child (5-17)", "Infant (0-4)", "Elderly (65+)"])
    conscious = st.selectbox("Is the patient conscious?", ["Yes - Awake and responsive", "Semi-conscious - Drowsy", "No - Unconscious"])

situation = st.text_area("Describe the emergency situation:", placeholder="e.g. Person collapsed, not breathing, pale skin, happened 2 minutes ago...", height=100)

st.markdown('</div></div>', unsafe_allow_html=True)

if st.button("🚨 GET IMMEDIATE FIRST AID INSTRUCTIONS"):
    with st.spinner("🤖 Getting emergency instructions..."):
        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            prompt = f"""
            MEDICAL EMERGENCY - Provide immediate first aid instructions.

            Emergency: {emergency_type}
            Patient: {patient_age}, {conscious}
            Situation: {situation if situation else 'Not described'}

            Provide IMMEDIATE step-by-step first aid instructions:

            ⚠️ FIRST: State if this requires calling emergency services immediately

            STEP-BY-STEP FIRST AID:
            Give clear numbered steps (1-8) that a non-medical person can follow RIGHT NOW.
            Each step should be simple, clear and actionable.

            DO NOT DO:
            List 3-4 things to absolutely avoid doing

            WHEN TO CALL AMBULANCE:
            Clear criteria for when to call emergency services

            WHAT TO TELL THE DISPATCHER:
            Key information to give when calling emergency services

            Be clear, calm and practical. Lives may depend on this information.
            Always emphasize calling emergency services for serious emergencies.
            End with: This is first aid guidance only. Professional medical care is essential.
            """
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.3
            )
            result = response.choices[0].message.content

            st.markdown(f"""
            <div class="ai-insight">
                <div class="ai-insight-header">🚨 Emergency First Aid — {emergency_type}</div>
                <div class="ai-insight-text">{result.replace(chr(10), '<br>')}</div>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {e}")

# CPR Guide
st.markdown("### 🫀 Quick CPR Reference")
st.markdown("""
<div class="steps-card">
    <div class="steps-title">🫀 CPR Steps (Adult)</div>
    <div class="step-item">
        <div class="step-num">1</div>
        <div class="step-text">Check the scene is safe. Check if person is responsive by tapping shoulders and shouting "Are you okay?"</div>
    </div>
    <div class="step-item">
        <div class="step-num">2</div>
        <div class="step-text">Call emergency services immediately (999/911/112) or ask someone else to call while you start CPR</div>
    </div>
    <div class="step-item">
        <div class="step-num">3</div>
        <div class="step-text">Place heel of hand on center of chest (lower half of breastbone). Place other hand on top, interlace fingers</div>
    </div>
    <div class="step-item">
        <div class="step-num">4</div>
        <div class="step-text">Push hard and fast — compress chest at least 5-6cm deep at rate of 100-120 per minute (to beat of "Stayin' Alive")</div>
    </div>
    <div class="step-item">
        <div class="step-num">5</div>
        <div class="step-text">Give 2 rescue breaths after every 30 compressions (if trained). If not trained, continue compressions only</div>
    </div>
    <div class="step-item">
        <div class="step-num">6</div>
        <div class="step-text">Continue until ambulance arrives, person starts breathing, or you are physically unable to continue</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="disclaimer">⚠️ This app provides first aid guidance for educational purposes only. Always call emergency services (999/911/112) immediately in life-threatening situations. Do not delay calling for help. Professional medical care is always required.</div>', unsafe_allow_html=True)
