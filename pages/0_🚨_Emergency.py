import streamlit as st
import requests
import sys
sys.path.append('.')
from utils.sidebar import load_sidebar

st.set_page_config(page_title="Emergency SOS", page_icon="🚨", layout="wide")
load_sidebar()

API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: #f0f4f0 !important; }
.emergency-hero { background: linear-gradient(135deg, #7f0000, #c0392b); border-radius: 20px; padding: 2rem 2.5rem; margin-bottom: 1.5rem; }
.emergency-hero h1 { font-size: 2rem; font-weight: 700; color: white; margin-bottom: 0.5rem; }
.emergency-hero p { font-size: 13px; color: rgba(255,255,255,0.8); line-height: 1.6; max-width: 600px; }
.emergency-badge { display: inline-flex; align-items: center; gap: 6px; background: rgba(255,255,255,0.2); border: 1px solid rgba(255,255,255,0.3); border-radius: 20px; padding: 4px 12px; font-size: 11px; color: #ffcccc; font-weight: 600; letter-spacing: 1px; margin-bottom: 1rem; }
.country-card { background: white; border: 1px solid #e0ece0; border-radius: 12px; padding: 1rem; margin-bottom: 8px; display: flex; align-items: center; gap: 12px; }
.country-flag { font-size: 1.5rem; flex-shrink: 0; }
.country-name { font-size: 13px; font-weight: 700; color: #1a3a1a; margin-bottom: 2px; }
.country-numbers { font-size: 12px; color: #5a6b5a; }
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
.step-item { display: flex; align-items: flex-start; gap: 10px; margin-bottom: 10px; }
.step-num { width: 24px; height: 24px; border-radius: 50%; background: rgba(255,255,255,0.2); display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; color: white; flex-shrink: 0; }
.step-text { font-size: 12px; color: rgba(255,255,255,0.9); line-height: 1.5; }
.disclaimer { background: #fff8e1; border: 1px solid #f0c040; border-radius: 10px; padding: 0.75rem 1rem; font-size: 11px; color: #7a6000; margin-top: 1rem; }
div[data-testid="stButton"] button { background: linear-gradient(135deg,#7f0000,#c0392b) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; font-size: 13px !important; padding: 0.6rem 1.5rem !important; }
label { color: #1a3a1a !important; }
p { color: #1a3a1a !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="emergency-hero">
    <div class="emergency-badge">🚨 EMERGENCY GUIDE</div>
    <h1>🚨 Emergency SOS & First Aid</h1>
    <p>Immediate guidance for medical emergencies worldwide. Find emergency numbers for your country and get instant AI-powered first aid instructions via FastAPI.</p>
</div>
""", unsafe_allow_html=True)

# Emergency numbers by region
st.markdown("### 📞 Emergency Numbers by Country")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🌍 Middle East", "🌍 Europe", "🌎 Americas", "🌏 Asia Pacific", "🌍 Africa", "🌐 Universal"
])

with tab1:
    countries_me = [
        ("🇦🇪", "UAE", "Police: 999 | Ambulance: 998 | Fire: 997"),
        ("🇸🇦", "Saudi Arabia", "Police: 999 | Ambulance: 911 | Fire: 998"),
        ("🇶🇦", "Qatar", "All: 999"),
        ("🇰🇼", "Kuwait", "All: 112"),
        ("🇧🇭", "Bahrain", "All: 999"),
        ("🇴🇲", "Oman", "All: 9999"),
        ("🇯🇴", "Jordan", "All: 911"),
        ("🇱🇧", "Lebanon", "Police: 112 | Ambulance: 140 | Fire: 175"),
        ("🇪🇬", "Egypt", "Police: 122 | Ambulance: 123 | Fire: 180"),
        ("🇮🇷", "Iran", "Police: 110 | Ambulance: 115 | Fire: 125"),
        ("🇹🇷", "Turkey", "Police: 155 | Ambulance: 112 | Fire: 110"),
        ("🇲🇦", "Morocco", "Police: 19 | Ambulance: 150 | Fire: 15"),
        ("🇵🇰", "Pakistan", "Police: 15 | Ambulance: 1122 | Rescue: 1122"),
    ]
    for flag, country, numbers in countries_me:
        st.markdown(f"""
        <div class="country-card">
            <div class="country-flag">{flag}</div>
            <div>
                <div class="country-name">{country}</div>
                <div class="country-numbers">{numbers}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    countries_eu = [
        ("🇬🇧", "United Kingdom", "Police: 999 | All: 112"),
        ("🇩🇪", "Germany", "Police: 110 | Ambulance: 112"),
        ("🇫🇷", "France", "Police: 17 | Ambulance: 15 | Fire: 18"),
        ("🇮🇹", "Italy", "Police: 113 | Ambulance: 118 | Fire: 115"),
        ("🇪🇸", "Spain", "Police: 091 | All: 112"),
        ("🇳🇱", "Netherlands", "All: 112"),
        ("🇧🇪", "Belgium", "Police: 101 | Ambulance: 100"),
        ("🇨🇭", "Switzerland", "Police: 117 | Ambulance: 144 | Fire: 118"),
        ("🇸🇪", "Sweden", "All: 112"),
        ("🇵🇱", "Poland", "Police: 997 | Ambulance: 999 | Fire: 998"),
        ("🇷🇺", "Russia", "Police: 102 | Ambulance: 103 | Fire: 101"),
        ("🇬🇷", "Greece", "Police: 100 | Ambulance: 166 | Fire: 199"),
    ]
    for flag, country, numbers in countries_eu:
        st.markdown(f"""
        <div class="country-card">
            <div class="country-flag">{flag}</div>
            <div>
                <div class="country-name">{country}</div>
                <div class="country-numbers">{numbers}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    countries_am = [
        ("🇺🇸", "United States", "All: 911"),
        ("🇨🇦", "Canada", "All: 911"),
        ("🇲🇽", "Mexico", "All: 911"),
        ("🇧🇷", "Brazil", "Police: 190 | Ambulance: 192 | Fire: 193"),
        ("🇦🇷", "Argentina", "Police: 911 | Ambulance: 107 | Fire: 100"),
        ("🇨🇴", "Colombia", "All: 123"),
        ("🇨🇱", "Chile", "Police: 133 | Ambulance: 131 | Fire: 132"),
        ("🇵🇪", "Peru", "Police: 105 | Ambulance: 117 | Fire: 116"),
    ]
    for flag, country, numbers in countries_am:
        st.markdown(f"""
        <div class="country-card">
            <div class="country-flag">{flag}</div>
            <div>
                <div class="country-name">{country}</div>
                <div class="country-numbers">{numbers}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab4:
    countries_ap = [
        ("🇮🇳", "India", "Police: 100 | Ambulance: 108 | All: 112"),
        ("🇧🇩", "Bangladesh", "All: 999"),
        ("🇱🇰", "Sri Lanka", "Police: 119 | Ambulance: 110"),
        ("🇨🇳", "China", "Police: 110 | Ambulance: 120 | Fire: 119"),
        ("🇯🇵", "Japan", "Police: 110 | Ambulance: 119"),
        ("🇰🇷", "South Korea", "Police: 112 | Ambulance: 119"),
        ("🇦🇺", "Australia", "All: 000"),
        ("🇳🇿", "New Zealand", "All: 111"),
        ("🇸🇬", "Singapore", "Police: 999 | Ambulance: 995"),
        ("🇲🇾", "Malaysia", "All: 999"),
        ("🇮🇩", "Indonesia", "Police: 110 | Ambulance: 118"),
        ("🇵🇭", "Philippines", "All: 911"),
        ("🇹🇭", "Thailand", "Police: 191 | Ambulance: 1669"),
    ]
    for flag, country, numbers in countries_ap:
        st.markdown(f"""
        <div class="country-card">
            <div class="country-flag">{flag}</div>
            <div>
                <div class="country-name">{country}</div>
                <div class="country-numbers">{numbers}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab5:
    countries_af = [
        ("🇿🇦", "South Africa", "Police: 10111 | Ambulance: 10177 | All: 112"),
        ("🇳🇬", "Nigeria", "All: 199"),
        ("🇰🇪", "Kenya", "All: 999"),
        ("🇬🇭", "Ghana", "Police: 191 | Ambulance: 193 | Fire: 192"),
        ("🇪🇹", "Ethiopia", "Police: 991 | Ambulance: 907"),
        ("🇹🇿", "Tanzania", "All: 112"),
        ("🇷🇼", "Rwanda", "Police: 112 | Ambulance: 912"),
        ("🇿🇲", "Zambia", "Police: 999 | Ambulance: 991"),
    ]
    for flag, country, numbers in countries_af:
        st.markdown(f"""
        <div class="country-card">
            <div class="country-flag">{flag}</div>
            <div>
                <div class="country-name">{country}</div>
                <div class="country-numbers">{numbers}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab6:
    st.markdown("""
    <div class="country-card" style="border-color:#c0392b;background:#fff0f0;">
        <div class="country-flag">🌐</div>
        <div>
            <div class="country-name" style="color:#c0392b;">Universal Emergency Number</div>
            <div class="country-numbers"><b>112</b> — Works in most countries worldwide</div>
        </div>
    </div>
    <div class="country-card">
        <div class="country-flag">📱</div>
        <div>
            <div class="country-name">Mobile Emergency</div>
            <div class="country-numbers">112 works even without SIM card on most phones</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Warning signs
st.markdown("### ⚠️ Call Emergency Services Immediately If:")
st.markdown("""
<div class="warning-signs">
    <div class="warning-card"><div class="warning-icon">💔</div><div><div class="warning-text">Chest pain or pressure</div><div class="warning-sub">Could be heart attack — every second counts</div></div></div>
    <div class="warning-card"><div class="warning-icon">🫁</div><div><div class="warning-text">Difficulty breathing</div><div class="warning-sub">Severe shortness of breath or choking</div></div></div>
    <div class="warning-card"><div class="warning-icon">🧠</div><div><div class="warning-text">Stroke signs (FAST)</div><div class="warning-sub">Face drooping, Arm weakness, Speech difficulty</div></div></div>
    <div class="warning-card"><div class="warning-icon">🩸</div><div><div class="warning-text">Severe bleeding</div><div class="warning-sub">Uncontrolled bleeding from any wound</div></div></div>
    <div class="warning-card"><div class="warning-icon">😵</div><div><div class="warning-text">Loss of consciousness</div><div class="warning-sub">Person is unresponsive or unconscious</div></div></div>
    <div class="warning-card"><div class="warning-icon">🤢</div><div><div class="warning-text">Severe allergic reaction</div><div class="warning-sub">Swelling of throat, difficulty swallowing</div></div></div>
</div>
""", unsafe_allow_html=True)

# AI First Aid
st.markdown('<div class="form-card"><div class="form-header"><h2>🤖 AI Emergency First Aid Guide</h2><span class="form-tag">FastAPI Powered</span></div><div class="form-body">', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    emergency_type = st.selectbox("Emergency Type", [
        "Heart Attack", "Stroke", "Choking", "Severe Bleeding",
        "Burns", "Fracture / Broken Bone", "Allergic Reaction",
        "Seizure / Epilepsy", "Drowning", "Electric Shock",
        "Poisoning / Overdose", "Diabetic Emergency", "Asthma Attack",
        "Head Injury", "Loss of Consciousness", "Snake / Animal Bite",
        "Heat Stroke", "Hypothermia", "Panic Attack", "Other Emergency"
    ])
    country = st.text_input("Your Country", placeholder="e.g. UAE, UK, Pakistan...")
with col2:
    patient_age = st.selectbox("Patient Age Group", ["Adult (18+)", "Child (5-17)", "Infant (0-4)", "Elderly (65+)"])
    conscious = st.selectbox("Is patient conscious?", ["Yes - Awake", "Semi-conscious", "No - Unconscious"])

situation = st.text_area("Describe the emergency:", placeholder="e.g. Person collapsed, not breathing...", height=80)
st.markdown('</div></div>', unsafe_allow_html=True)

if st.button("🚨 GET IMMEDIATE FIRST AID INSTRUCTIONS"):
    with st.spinner("🤖 FastAPI getting emergency instructions..."):
        try:
            response = requests.post(
                f"{API_URL}/emergency/firstaid",
                json={
                    "emergency_type": emergency_type,
                    "country": country,
                    "patient_age": patient_age,
                    "conscious": conscious,
                    "situation": situation,
                    "api_key": st.secrets.get("GROQ_API_KEY", "")
                },
                timeout=30
            )
            result = response.json()

            if "error" in result:
                st.error(f"API Error: {result['error']}")
            else:
                st.markdown(f"""
                <div class="ai-insight">
                    <div class="ai-insight-header">🚨 Emergency First Aid via FastAPI — {emergency_type}</div>
                    <div class="ai-insight-text">{result['instructions'].replace(chr(10), '<br>')}</div>
                </div>
                """, unsafe_allow_html=True)

        except requests.exceptions.Timeout:
            st.error("⏱️ API timeout — please try again")
        except Exception as e:
            st.error(f"Error: {e}")

# CPR Guide
st.markdown("### 🫀 Quick CPR Reference")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="steps-card">
        <div style="font-size:13px;font-weight:700;color:white;margin-bottom:1rem;text-transform:uppercase;letter-spacing:1px;">🫀 CPR Steps (Adult)</div>
        <div class="step-item"><div class="step-num">1</div><div class="step-text">Check scene is safe. Tap shoulders and shout "Are you okay?"</div></div>
        <div class="step-item"><div class="step-num">2</div><div class="step-text">Call emergency services immediately</div></div>
        <div class="step-item"><div class="step-num">3</div><div class="step-text">Place heel of hand on center of chest, other hand on top</div></div>
        <div class="step-item"><div class="step-num">4</div><div class="step-text">Push hard and fast — 5-6cm deep, 100-120 per minute</div></div>
        <div class="step-item"><div class="step-num">5</div><div class="step-text">Give 2 rescue breaths after every 30 compressions if trained</div></div>
        <div class="step-item"><div class="step-num">6</div><div class="step-text">Continue until ambulance arrives or person starts breathing</div></div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="steps-card">
        <div style="font-size:13px;font-weight:700;color:white;margin-bottom:1rem;text-transform:uppercase;letter-spacing:1px;">🧠 FAST Stroke Test</div>
        <div class="step-item"><div class="step-num">F</div><div class="step-text">FACE — Ask them to smile. Does one side droop?</div></div>
        <div class="step-item"><div class="step-num">A</div><div class="step-text">ARMS — Raise both arms. Does one drift downward?</div></div>
        <div class="step-item"><div class="step-num">S</div><div class="step-text">SPEECH — Repeat a phrase. Is it slurred or strange?</div></div>
        <div class="step-item"><div class="step-num">T</div><div class="step-text">TIME — If ANY sign, call emergency services IMMEDIATELY</div></div>
        <br/>
        <div style="font-size:13px;font-weight:700;color:white;margin-bottom:0.5rem;">🩸 Severe Bleeding</div>
        <div class="step-item"><div class="step-num">1</div><div class="step-text">Apply firm direct pressure with clean cloth</div></div>
        <div class="step-item"><div class="step-num">2</div><div class="step-text">Do not remove cloth — add more on top if soaked</div></div>
        <div class="step-item"><div class="step-num">3</div><div class="step-text">Elevate injured area above heart level if possible</div></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="disclaimer">⚠️ For educational purposes only. Always call emergency services immediately in life-threatening situations. Do not delay calling for help.</div>', unsafe_allow_html=True)
