import streamlit as st
from groq import Groq
import sys
sys.path.append('.')
from utils.sidebar import load_sidebar

st.set_page_config(page_title="Find a Doctor", page_icon="👨‍⚕️", layout="wide")
load_sidebar()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: #f0f4f0 !important; }
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
.doctor-card { background: white; border: 1px solid #e0ece0; border-radius: 14px; padding: 1.25rem; margin-bottom: 10px; display: flex; gap: 1rem; align-items: flex-start; transition: all 0.2s; }
.doctor-card:hover { border-color: #97c459; box-shadow: 0 4px 15px rgba(99,153,34,0.1); transform: translateY(-2px); }
.doctor-avatar { width: 48px; height: 48px; border-radius: 50%; background: linear-gradient(135deg,#eaf3de,#d4edbe); display: flex; align-items: center; justify-content: center; font-size: 20px; flex-shrink: 0; }
.doctor-info { flex: 1; }
.doctor-name { font-size: 14px; font-weight: 700; color: #1a3a1a; margin-bottom: 2px; }
.doctor-specialty { font-size: 12px; color: #639922; font-weight: 600; margin-bottom: 4px; }
.doctor-details { font-size: 12px; color: #5a6b5a; line-height: 1.6; }
.doctor-badge { display: inline-block; font-size: 10px; background: #eaf3de; color: #3b6d11; padding: 2px 8px; border-radius: 20px; font-weight: 600; margin-top: 6px; margin-right: 4px; }
.hospital-card { background: white; border: 1px solid #e0ece0; border-radius: 14px; padding: 1.25rem; margin-bottom: 10px; border-left: 4px solid #639922; }
.hospital-name { font-size: 15px; font-weight: 700; color: #1a3a1a; margin-bottom: 4px; }
.hospital-type { font-size: 11px; color: #639922; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }
.hospital-details { font-size: 12px; color: #5a6b5a; line-height: 1.6; }
.ai-insight { background: white; border: 1px solid #e0ece0; border-radius: 12px; padding: 1rem; margin-top: 1rem; }
.ai-insight-header { font-size: 11px; font-weight: 600; color: #639922; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }
.ai-insight-text { font-size: 13px; color: #3a4a3a; line-height: 1.7; }
.disclaimer { background: #fff8e1; border: 1px solid #f0c040; border-radius: 10px; padding: 0.75rem 1rem; font-size: 11px; color: #7a6000; margin-top: 1rem; }
div[data-testid="stButton"] button { background: linear-gradient(135deg,#3b6d11,#639922) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; font-size: 13px !important; padding: 0.6rem 1.5rem !important; }
label { color: #1a3a1a !important; }
p { color: #1a3a1a !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="topbar">
    <div>
        <div class="topbar-title">👨‍⚕️ Find a Doctor & Hospital</div>
        <div class="topbar-sub">AI-powered recommendations for your health condition</div>
    </div>
    <div class="ai-badge"><span class="ai-dot"></span> Groq AI Active</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="form-card"><div class="form-header"><h2>🔍 Search Criteria</h2><span class="form-tag">AI Powered</span></div><div class="form-body">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    condition = st.text_input("Health Condition", placeholder="e.g. Heart Disease, Pneumonia, Diabetes...")
    city = st.text_input("City / Country", placeholder="e.g. Dubai, London, New York...")
with col2:
    specialty = st.selectbox("Medical Specialty", [
        "Auto-detect from condition",
        "Cardiologist",
        "Pulmonologist",
        "Neurologist",
        "Oncologist",
        "Orthopedic Surgeon",
        "Gastroenterologist",
        "Endocrinologist",
        "Dermatologist",
        "Psychiatrist",
        "General Physician",
        "Pediatrician",
        "Gynecologist",
        "Urologist",
        "Ophthalmologist"
    ])
    urgency = st.selectbox("Urgency", ["Routine (within weeks)", "Soon (within days)", "Urgent (within 24 hours)", "Emergency"])
with col3:
    budget = st.selectbox("Budget Range", ["Any", "Budget-friendly", "Mid-range", "Premium / Private"])
    insurance = st.selectbox("Insurance", ["Not specified", "Private Insurance", "Government/Public", "No Insurance"])
    language = st.text_input("Preferred Language", placeholder="e.g. English, Arabic, Urdu...")

st.markdown('</div></div>', unsafe_allow_html=True)

additional_info = st.text_area("Any additional requirements?", placeholder="e.g. Female doctor preferred, wheelchair accessible, near public transport...")

if st.button("⚡ Find Best Doctors & Hospitals"):
    if not condition:
        st.warning("⚠️ Please enter your health condition.")
    elif not city:
        st.warning("⚠️ Please enter your city or country.")
    else:
        with st.spinner("🤖 AI finding the best doctors and hospitals for you..."):
            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])

                prompt = f"""
                A patient needs medical help. Find the best doctors and hospitals for them.

                Patient Details:
                - Health Condition: {condition}
                - Location: {city}
                - Specialty needed: {specialty}
                - Urgency: {urgency}
                - Budget: {budget}
                - Insurance: {insurance}
                - Preferred Language: {language if language else 'Any'}
                - Additional requirements: {additional_info if additional_info else 'None'}

                Please provide:

                ## SPECIALIST TYPE NEEDED
                What type of doctor/specialist they need and why.

                ## TOP 3 RECOMMENDED DOCTORS
                For each doctor provide:
                DOCTOR: [Name]
                SPECIALTY: [Their specialty]
                EXPERIENCE: [Years of experience and expertise]
                WHY RECOMMENDED: [Why this doctor is good for this condition]
                HOW TO FIND: [How to search/find this type of doctor in {city}]
                WHAT TO ASK: [Key questions to ask during consultation]

                ## TOP 3 RECOMMENDED HOSPITALS/CLINICS
                For each hospital:
                HOSPITAL: [Name or type of hospital]
                TYPE: [Government/Private/Specialist Center]
                WHY RECOMMENDED: [Why this hospital is good for this condition]
                DEPARTMENTS: [Relevant departments to visit]
                TIP: [Practical tip for visiting]

                ## PREPARATION CHECKLIST
                5 things the patient should do before their appointment.

                ## RED FLAGS
                Warning signs that mean they need emergency care immediately.

                Be specific to {city} where possible. If you don't know specific doctors by name,
                recommend the type of specialist and how to find them in that city.
                Be practical, helpful and compassionate.
                End with: Always verify doctor credentials and read reviews before booking an appointment.
                """

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1000
                )

                result = response.choices[0].message.content

                st.markdown("### 🏥 AI Recommendations")
                st.markdown(f"""
                <div class="ai-insight">
                    <div class="ai-insight-header">🤖 AI Doctor & Hospital Finder — {condition} in {city}</div>
                    <div class="ai-insight-text">{result.replace(chr(10), '<br>')}</div>
                </div>
                """, unsafe_allow_html=True)

                # Quick tips box
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#1a3a1a,#2d5a1a);border-radius:16px;padding:1.5rem;margin-top:1rem;">
                    <div style="font-size:11px;color:#97c459;font-weight:600;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">
                        ⚡ Quick Action Steps for {condition}
                    </div>
                    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;">
                        <div style="background:rgba(255,255,255,0.1);border-radius:10px;padding:0.75rem;text-align:center;">
                            <div style="font-size:1.5rem;margin-bottom:4px;">📞</div>
                            <div style="font-size:11px;color:white;font-weight:600;">Call First</div>
                            <div style="font-size:10px;color:rgba(255,255,255,0.7);">Book appointment before visiting</div>
                        </div>
                        <div style="background:rgba(255,255,255,0.1);border-radius:10px;padding:0.75rem;text-align:center;">
                            <div style="font-size:1.5rem;margin-bottom:4px;">📋</div>
                            <div style="font-size:11px;color:white;font-weight:600;">Bring Records</div>
                            <div style="font-size:10px;color:rgba(255,255,255,0.7);">Previous tests and medications</div>
                        </div>
                        <div style="background:rgba(255,255,255,0.1);border-radius:10px;padding:0.75rem;text-align:center;">
                            <div style="font-size:1.5rem;margin-bottom:4px;">⭐</div>
                            <div style="font-size:11px;color:white;font-weight:600;">Check Reviews</div>
                            <div style="font-size:10px;color:rgba(255,255,255,0.7);">Verify credentials online</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown('<div class="disclaimer">⚠️ These are AI-generated recommendations for guidance only. Always verify doctor credentials, check reviews, and consult with medical professionals directly. In emergencies call local emergency services immediately.</div>', unsafe_allow_html=True)
