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
.country-card { background: white; border: 1px solid #e0ece0; border-radius: 12px; padding: 1rem; margin-bottom: 8px; display: flex; align-items: center; gap: 12px; }
.country-flag { font-size: 1.5rem; flex-shrink: 0; }
.country-name { font-size: 13px; font-weight: 700; color: #1a3a1a; margin-bottom: 2px; }
.country-numbers { font-size: 12px; color: #5a6b5a; }
.country-highlight { color: #c0392b; font-weight: 700; }
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
div[data-testid="stButton"] button:hover { background: linear-gradient(135deg,#5c0000,#a93226) !important; }
label { color: #1a3a1a !important; }
p { color: #1a3a1a !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="emergency-hero">
    <div class="emergency-badge">🚨 EMERGENCY GUIDE</div>
    <h1>🚨 Emergency SOS & First Aid</h1>
    <p>Immediate guidance for medical emergencies worldwide. Find emergency numbers for your country and get instant AI-powered first aid instructions. Always call emergency services first!</p>
</div>
""", unsafe_allow_html=True)

# Emergency numbers by region
st.markdown("### 📞 Emergency Numbers by Country")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🌍 Middle East", "🌍 Europe", "🌎 Americas", "🌏 Asia Pacific", "🌍 Africa", "🌐 Universal"
])

with tab1:
    st.markdown("#### Middle East & North Africa")
    countries_me = [
        ("🇦🇪", "UAE", "Police: 999 | Ambulance: 998 | Fire: 997 | Coast Guard: 996"),
        ("🇸🇦", "Saudi Arabia", "Police: 999 | Ambulance: 911 | Fire: 998 | Traffic: 993"),
        ("🇶🇦", "Qatar", "Police: 999 | Ambulance: 999 | Fire: 999 | All: 999"),
        ("🇰🇼", "Kuwait", "Police: 112 | Ambulance: 112 | Fire: 112 | All: 112"),
        ("🇧🇭", "Bahrain", "Police: 999 | Ambulance: 999 | Fire: 999 | All: 999"),
        ("🇴🇲", "Oman", "Police: 9999 | Ambulance: 9999 | Fire: 9999 | All: 9999"),
        ("🇯🇴", "Jordan", "Police: 911 | Ambulance: 911 | Fire: 911 | All: 911"),
        ("🇱🇧", "Lebanon", "Police: 112 | Ambulance: 140 | Fire: 175 | Red Cross: 140"),
        ("🇪🇬", "Egypt", "Police: 122 | Ambulance: 123 | Fire: 180 | Tourism Police: 126"),
        ("🇮🇶", "Iraq", "Police: 104 | Ambulance: 115 | Fire: 115"),
        ("🇾🇪", "Yemen", "Police: 194 | Ambulance: 191 | Fire: 191"),
        ("🇸🇾", "Syria", "Police: 112 | Ambulance: 110 | Fire: 113"),
        ("🇮🇱", "Israel", "Police: 100 | Ambulance: 101 | Fire: 102 | All: 112"),
        ("🇵🇸", "Palestine", "Police: 100 | Ambulance: 101 | Fire: 102"),
        ("🇮🇷", "Iran", "Police: 110 | Ambulance: 115 | Fire: 125 | Emergency: 115"),
        ("🇹🇷", "Turkey", "Police: 155 | Ambulance: 112 | Fire: 110 | Emergency: 112"),
        ("🇲🇦", "Morocco", "Police: 19 | Ambulance: 150 | Fire: 15 | Gendarmerie: 177"),
        ("🇹🇳", "Tunisia", "Police: 197 | Ambulance: 190 | Fire: 198 | National Guard: 193"),
        ("🇱🇾", "Libya", "Police: 1515 | Ambulance: 1515 | Fire: 1515"),
        ("🇩🇿", "Algeria", "Police: 17 | Ambulance: 14 | Fire: 14 | Emergency: 14"),
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
    st.markdown("#### Europe")
    countries_eu = [
        ("🇬🇧", "United Kingdom", "Police: 999 | Ambulance: 999 | Fire: 999 | All: 112"),
        ("🇩🇪", "Germany", "Police: 110 | Ambulance: 112 | Fire: 112 | All: 112"),
        ("🇫🇷", "France", "Police: 17 | Ambulance: 15 | Fire: 18 | All: 112"),
        ("🇮🇹", "Italy", "Police: 113 | Ambulance: 118 | Fire: 115 | All: 112"),
        ("🇪🇸", "Spain", "Police: 091 | Ambulance: 112 | Fire: 080 | All: 112"),
        ("🇵🇹", "Portugal", "Police: 112 | Ambulance: 112 | Fire: 112 | All: 112"),
        ("🇳🇱", "Netherlands", "Police: 112 | Ambulance: 112 | Fire: 112 | All: 112"),
        ("🇧🇪", "Belgium", "Police: 101 | Ambulance: 100 | Fire: 100 | All: 112"),
        ("🇨🇭", "Switzerland", "Police: 117 | Ambulance: 144 | Fire: 118 | All: 112"),
        ("🇦🇹", "Austria", "Police: 133 | Ambulance: 144 | Fire: 122 | All: 112"),
        ("🇸🇪", "Sweden", "Police: 112 | Ambulance: 112 | Fire: 112 | All: 112"),
        ("🇳🇴", "Norway", "Police: 112 | Ambulance: 113 | Fire: 110 | All: 112"),
        ("🇩🇰", "Denmark", "Police: 112 | Ambulance: 112 | Fire: 112 | All: 112"),
        ("🇫🇮", "Finland", "Police: 112 | Ambulance: 112 | Fire: 112 | All: 112"),
        ("🇵🇱", "Poland", "Police: 997 | Ambulance: 999 | Fire: 998 | All: 112"),
        ("🇷🇺", "Russia", "Police: 102 | Ambulance: 103 | Fire: 101 | All: 112"),
        ("🇺🇦", "Ukraine", "Police: 102 | Ambulance: 103 | Fire: 101 | All: 112"),
        ("🇬🇷", "Greece", "Police: 100 | Ambulance: 166 | Fire: 199 | All: 112"),
        ("🇷🇴", "Romania", "Police: 112 | Ambulance: 112 | Fire: 112 | All: 112"),
        ("🇨🇿", "Czech Republic", "Police: 158 | Ambulance: 155 | Fire: 150 | All: 112"),
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
    st.markdown("#### Americas")
    countries_am = [
        ("🇺🇸", "United States", "Police: 911 | Ambulance: 911 | Fire: 911 | All: 911"),
        ("🇨🇦", "Canada", "Police: 911 | Ambulance: 911 | Fire: 911 | All: 911"),
        ("🇲🇽", "Mexico", "Police: 911 | Ambulance: 911 | Fire: 911 | All: 911"),
        ("🇧🇷", "Brazil", "Police: 190 | Ambulance: 192 | Fire: 193 | Civil Defense: 199"),
        ("🇦🇷", "Argentina", "Police: 911 | Ambulance: 107 | Fire: 100 | All: 911"),
        ("🇨🇴", "Colombia", "Police: 112 | Ambulance: 132 | Fire: 119 | All: 123"),
        ("🇨🇱", "Chile", "Police: 133 | Ambulance: 131 | Fire: 132 | All: 131"),
        ("🇵🇪", "Peru", "Police: 105 | Ambulance: 117 | Fire: 116 | All: 105"),
        ("🇻🇪", "Venezuela", "Police: 171 | Ambulance: 171 | Fire: 171 | All: 171"),
        ("🇨🇺", "Cuba", "Police: 106 | Ambulance: 104 | Fire: 105 | All: 104"),
        ("🇯🇲", "Jamaica", "Police: 119 | Ambulance: 110 | Fire: 110 | All: 119"),
        ("🇵🇦", "Panama", "Police: 104 | Ambulance: 911 | Fire: 103 | All: 911"),
        ("🇨🇷", "Costa Rica", "Police: 911 | Ambulance: 911 | Fire: 911 | All: 911"),
        ("🇬🇹", "Guatemala", "Police: 110 | Ambulance: 122 | Fire: 122 | All: 110"),
        ("🇧🇴", "Bolivia", "Police: 110 | Ambulance: 118 | Fire: 119 | All: 110"),
        ("🇪🇨", "Ecuador", "Police: 101 | Ambulance: 131 | Fire: 102 | All: 911"),
        ("🇺🇾", "Uruguay", "Police: 911 | Ambulance: 105 | Fire: 104 | All: 911"),
        ("🇵🇾", "Paraguay", "Police: 911 | Ambulance: 911 | Fire: 911 | All: 911"),
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
    st.markdown("#### Asia Pacific")
    countries_ap = [
        ("🇵🇰", "Pakistan", "Police: 15 | Ambulance: 1122 | Fire: 16 | Rescue: 1122"),
        ("🇮🇳", "India", "Police: 100 | Ambulance: 108 | Fire: 101 | All: 112"),
        ("🇧🇩", "Bangladesh", "Police: 999 | Ambulance: 999 | Fire: 999 | All: 999"),
        ("🇱🇰", "Sri Lanka", "Police: 119 | Ambulance: 110 | Fire: 111 | All: 119"),
        ("🇳🇵", "Nepal", "Police: 100 | Ambulance: 102 | Fire: 101 | All: 100"),
        ("🇨🇳", "China", "Police: 110 | Ambulance: 120 | Fire: 119 | Traffic: 122"),
        ("🇯🇵", "Japan", "Police: 110 | Ambulance: 119 | Fire: 119 | All: 110"),
        ("🇰🇷", "South Korea", "Police: 112 | Ambulance: 119 | Fire: 119 | All: 119"),
        ("🇦🇺", "Australia", "Police: 000 | Ambulance: 000 | Fire: 000 | All: 000"),
        ("🇳🇿", "New Zealand", "Police: 111 | Ambulance: 111 | Fire: 111 | All: 111"),
        ("🇸🇬", "Singapore", "Police: 999 | Ambulance: 995 | Fire: 995 | All: 995"),
        ("🇲🇾", "Malaysia", "Police: 999 | Ambulance: 999 | Fire: 994 | All: 999"),
        ("🇮🇩", "Indonesia", "Police: 110 | Ambulance: 118 | Fire: 113 | All: 112"),
        ("🇵🇭", "Philippines", "Police: 911 | Ambulance: 911 | Fire: 911 | All: 911"),
        ("🇹🇭", "Thailand", "Police: 191 | Ambulance: 1669 | Fire: 199 | Tourist: 1155"),
        ("🇻🇳", "Vietnam", "Police: 113 | Ambulance: 115 | Fire: 114 | All: 112"),
        ("🇲🇻", "Maldives", "Police: 119 | Ambulance: 102 | Fire: 118 | All: 119"),
        ("🇦🇫", "Afghanistan", "Police: 119 | Ambulance: 112 | Fire: 119 | All: 112"),
        ("🇰🇿", "Kazakhstan", "Police: 102 | Ambulance: 103 | Fire: 101 | All: 112"),
        ("🇺🇿", "Uzbekistan", "Police: 102 | Ambulance: 103 | Fire: 101 | All: 112"),
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
    st.markdown("#### Africa")
    countries_af = [
        ("🇿🇦", "South Africa", "Police: 10111 | Ambulance: 10177 | Fire: 10177 | All: 112"),
        ("🇳🇬", "Nigeria", "Police: 199 | Ambulance: 199 | Fire: 199 | All: 199"),
        ("🇰🇪", "Kenya", "Police: 999 | Ambulance: 999 | Fire: 999 | All: 999"),
        ("🇬🇭", "Ghana", "Police: 191 | Ambulance: 193 | Fire: 192 | All: 112"),
        ("🇪🇹", "Ethiopia", "Police: 991 | Ambulance: 907 | Fire: 939 | All: 907"),
        ("🇹🇿", "Tanzania", "Police: 112 | Ambulance: 112 | Fire: 112 | All: 112"),
        ("🇺🇬", "Uganda", "Police: 999 | Ambulance: 999 | Fire: 999 | All: 999"),
        ("🇷🇼", "Rwanda", "Police: 112 | Ambulance: 912 | Fire: 112 | All: 112"),
        ("🇿🇲", "Zambia", "Police: 999 | Ambulance: 991 | Fire: 993 | All: 999"),
        ("🇿🇼", "Zimbabwe", "Police: 999 | Ambulance: 994 | Fire: 993 | All: 999"),
        ("🇸🇳", "Senegal", "Police: 17 | Ambulance: 15 | Fire: 18 | All: 112"),
        ("🇨🇮", "Ivory Coast", "Police: 110 | Ambulance: 185 | Fire: 180 | All: 110"),
        ("🇨🇲", "Cameroon", "Police: 117 | Ambulance: 119 | Fire: 118 | All: 117"),
        ("🇦🇴", "Angola", "Police: 113 | Ambulance: 112 | Fire: 115 | All: 113"),
        ("🇲🇿", "Mozambique", "Police: 119 | Ambulance: 117 | Fire: 198 | All: 119"),
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
    st.markdown("#### Universal Emergency Numbers")
    st.markdown("""
    <div class="country-card" style="border-color:#c0392b;background:#fff0f0;">
        <div class="country-flag">🌐</div>
        <div>
            <div class="country-name" style="color:#c0392b;">Universal Emergency Number</div>
            <div class="country-numbers"><span class="country-highlight">112</span> — Works in most countries worldwide, especially in Europe and when roaming</div>
        </div>
    </div>
    <div class="country-card" style="border-color:#c0392b;background:#fff0f0;">
        <div class="country-flag">📱</div>
        <div>
            <div class="country-name" style="color:#c0392b;">Mobile Emergency</div>
            <div class="country-numbers"><span class="country-highlight">112</span> — Works even without SIM card or network signal on most phones</div>
        </div>
    </div>
    <div class="country-card">
        <div class="country-flag">✈️</div>
        <div>
            <div class="country-name">When Travelling</div>
            <div class="country-numbers">Save local emergency number before travelling. 112 works in 80+ countries as backup</div>
        </div>
    </div>
    <div class="country-card">
        <div class="country-flag">🏨</div>
        <div>
            <div class="country-name">Hotel Emergency</div>
            <div class="country-numbers">Call hotel front desk first — they can connect you to local emergency services faster</div>
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
            <div class="warning-text">Stroke signs (FAST)</div>
            <div class="warning-sub">Face drooping, Arm weakness, Speech difficulty, Time to call</div>
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
    <div class="warning-card">
        <div class="warning-icon">🔥</div>
        <div>
            <div class="warning-text">Severe burns</div>
            <div class="warning-sub">Large area or deep burns requiring immediate care</div>
        </div>
    </div>
    <div class="warning-card">
        <div class="warning-icon">👶</div>
        <div>
            <div class="warning-text">Child not breathing</div>
            <div class="warning-sub">Any infant or child not breathing or unresponsive</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# AI First Aid
st.markdown('<div class="form-card"><div class="form-header"><h2>🤖 AI Emergency First Aid Guide</h2><span class="form-tag">Instant Help</span></div><div class="form-body">', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    emergency_type = st.selectbox("Emergency Type", [
        "Heart Attack", "Stroke", "Choking", "Severe Bleeding",
        "Burns", "Fracture / Broken Bone", "Allergic Reaction / Anaphylaxis",
        "Seizure / Epilepsy", "Drowning", "Electric Shock",
        "Poisoning / Overdose", "Diabetic Emergency", "Asthma Attack",
        "Head Injury", "Spinal Injury", "Eye Injury", "Tooth Knocked Out",
        "Snake / Animal Bite", "Heat Stroke", "Hypothermia / Frostbite",
        "Loss of Consciousness", "Panic Attack", "Childbirth Emergency",
        "Other Emergency"
    ])
    country = st.text_input("Your Country", placeholder="e.g. UAE, UK, USA, Pakistan...")
with col2:
    patient_age = st.selectbox("Patient Age Group", ["Adult (18+)", "Child (5-17)", "Infant (0-4)", "Elderly (65+)"])
    conscious = st.selectbox("Is the patient conscious?", ["Yes - Awake and responsive", "Semi-conscious - Drowsy", "No - Unconscious"])

situation = st.text_area("Describe the emergency:", placeholder="e.g. Person collapsed, not breathing, pale skin, happened 2 minutes ago...", height=80)
st.markdown('</div></div>', unsafe_allow_html=True)

if st.button("🚨 GET IMMEDIATE FIRST AID INSTRUCTIONS"):
    with st.spinner("🤖 Getting emergency instructions..."):
        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            prompt = f"""
            MEDICAL EMERGENCY - Provide immediate first aid instructions.

            Emergency: {emergency_type}
            Country: {country if country else 'Not specified'}
            Patient: {patient_age}, {conscious}
            Situation: {situation if situation else 'Not described'}

            Provide IMMEDIATE instructions:

            ⚠️ CALL EMERGENCY SERVICES: State the emergency number for {country if country else 'their country'} and if they should call NOW

            STEP-BY-STEP FIRST AID (1-8 steps):
            Clear numbered steps a non-medical person can follow RIGHT NOW.

            DO NOT DO:
            3-4 things to absolutely avoid

            WHAT TO TELL DISPATCHER:
            Exact words to say when calling emergency services

            WHEN TO STOP AND WAIT:
            When to stop first aid and just wait for ambulance

            Be clear, calm and life-saving. Lives depend on this.
            End with: This is first aid guidance only. Professional medical care is essential.
            """
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.3
            )
            st.markdown(f"""
            <div class="ai-insight">
                <div class="ai-insight-header">🚨 Emergency First Aid — {emergency_type}</div>
                <div class="ai-insight-text">{response.choices[0].message.content.replace(chr(10), '<br>')}</div>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")

# CPR Guide
st.markdown("### 🫀 Quick CPR & First Aid Reference")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="steps-card">
        <div style="font-size:13px;font-weight:700;color:white;margin-bottom:1rem;text-transform:uppercase;letter-spacing:1px;">🫀 CPR Steps (Adult)</div>
        <div class="step-item"><div class="step-num">1</div><div class="step-text">Check scene is safe. Tap shoulders — shout "Are you okay?"</div></div>
        <div class="step-item"><div class="step-num">2</div><div class="step-text">Call emergency services immediately or ask someone to call</div></div>
        <div class="step-item"><div class="step-num">3</div><div class="step-text">Place heel of hand on center of chest, other hand on top, interlace fingers</div></div>
        <div class="step-item"><div class="step-num">4</div><div class="step-text">Push hard and fast — 5-6cm deep, 100-120 per minute (Stayin' Alive beat)</div></div>
        <div class="step-item"><div class="step-num">5</div><div class="step-text">Give 2 rescue breaths after every 30 compressions (if trained)</div></div>
        <div class="step-item"><div class="step-num">6</div><div class="step-text">Continue until ambulance arrives or person starts breathing</div></div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="steps-card">
        <div style="font-size:13px;font-weight:700;color:white;margin-bottom:1rem;text-transform:uppercase;letter-spacing:1px;">🧠 FAST Stroke Test</div>
        <div class="step-item"><div class="step-num">F</div><div class="step-text">FACE — Ask them to smile. Does one side droop?</div></div>
        <div class="step-item"><div class="step-num">A</div><div class="step-text">ARMS — Ask them to raise both arms. Does one drift downward?</div></div>
        <div class="step-item"><div class="step-num">S</div><div class="step-text">SPEECH — Ask them to repeat a phrase. Is it slurred or strange?</div></div>
        <div class="step-item"><div class="step-num">T</div><div class="step-text">TIME — If ANY of these, call emergency services IMMEDIATELY</div></div>
        <br/>
        <div style="font-size:13px;font-weight:700;color:white;margin-bottom:0.5rem;">🩸 Severe Bleeding</div>
        <div class="step-item"><div class="step-num">1</div><div class="step-text">Apply firm direct pressure with clean cloth</div></div>
        <div class="step-item"><div class="step-num">2</div><div class="step-text">Do not remove cloth — add more on top if soaked</div></div>
        <div class="step-item"><div class="step-num">3</div><div class="step-text">Elevate the injured area above heart level if possible</div></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="disclaimer">⚠️ This app provides first aid guidance for educational purposes only. Always call emergency services immediately in life-threatening situations. Do not delay calling for help. Professional medical care is always required.</div>', unsafe_allow_html=True)
