import streamlit as st
import requests
from fpdf import FPDF
import tempfile
import os
from datetime import date
import sys
sys.path.append('.')
from utils.sidebar import load_sidebar

st.set_page_config(page_title="Patient Report", page_icon="📄", layout="wide")
load_sidebar()

API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: #0a0f0a !important; }
.topbar { background: #0d120d; border: 1px solid #1a2e1a; border-radius: 16px; padding: 1.25rem 1.5rem; margin-bottom: 1.25rem; display: flex; align-items: center; justify-content: space-between; }
.topbar-title { font-size: 20px; font-weight: 700; color: #ffffff; }
.topbar-sub { font-size: 12px; color: rgba(255,255,255,0.4); margin-top: 2px; }
.ai-badge { display: inline-flex; align-items: center; gap: 6px; background: rgba(74,222,128,0.1); border: 1px solid rgba(74,222,128,0.2); border-radius: 20px; padding: 5px 12px; font-size: 11px; color: #4ade80; font-weight: 600; }
.ai-dot { width: 6px; height: 6px; border-radius: 50%; background: #4ade80; display: inline-block; animation: blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }
.form-card { background: #0d120d; border: 1px solid #1a2e1a; border-radius: 16px; overflow: hidden; margin-bottom: 1rem; }
.form-header { padding: 1rem 1.25rem; background: #0f1a0f; border-bottom: 1px solid #1a2e1a; display: flex; align-items: center; justify-content: space-between; }
.form-header h2 { font-size: 14px; font-weight: 600; color: #ffffff; }
.form-tag { font-size: 10px; color: #4ade80; background: rgba(74,222,128,0.1); border: 1px solid rgba(74,222,128,0.2); padding: 2px 8px; border-radius: 20px; font-weight: 600; }
.form-body { padding: 1.25rem; }
.preview-card { background: #0d120d; border: 1px solid #1a2e1a; border-radius: 16px; padding: 2rem; margin-bottom: 1rem; }
.disclaimer { background: rgba(255,200,0,0.05); border: 1px solid rgba(255,200,0,0.15); border-radius: 10px; padding: 0.75rem 1rem; font-size: 11px; color: rgba(255,200,0,0.7); margin-top: 1rem; }
div[data-testid="stButton"] button { background: linear-gradient(135deg,#166534,#4ade80) !important; color: #0a0f0a !important; border: none !important; border-radius: 8px !important; font-weight: 700 !important; font-size: 13px !important; padding: 0.6rem 1.5rem !important; }
label { color: rgba(255,255,255,0.7) !important; }
p { color: rgba(255,255,255,0.5) !important; }
.stSelectbox > div > div { background: #0f1a0f !important; border-color: #1a2e1a !important; color: white !important; }
.stNumberInput > div > div > input { background: #0f1a0f !important; border-color: #1a2e1a !important; color: white !important; }
.stTextInput > div > div > input { background: #0f1a0f !important; border-color: #1a2e1a !important; color: white !important; }
.stTextArea > div > div > textarea { background: #0f1a0f !important; border-color: #1a2e1a !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="topbar">
    <div>
        <div class="topbar-title">📄 Patient Report Generator</div>
        <div class="topbar-sub">AI-written medical reports with PDF export via FastAPI</div>
    </div>
    <div class="ai-badge"><span class="ai-dot"></span> FastAPI + Groq AI Active</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="form-card"><div class="form-header"><h2>👤 Patient Information</h2><span class="form-tag">Required</span></div><div class="form-body">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    name = st.text_input("Full Name", placeholder="John Doe")
    age = st.number_input("Age", min_value=1, max_value=120, value=30)
    gender = st.selectbox("Gender", ["Male","Female","Other"])
with col2:
    blood_group = st.selectbox("Blood Group", ["A+","A-","B+","B-","AB+","AB-","O+","O-"])
    height = st.number_input("Height (cm)", value=170)
    weight = st.number_input("Weight (kg)", value=70)
with col3:
    contact = st.text_input("Contact Number")
    doctor_name = st.text_input("Doctor Name")
    report_date = st.date_input("Report Date", value=date.today())
st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown('<div class="form-card"><div class="form-header"><h2>🩺 Medical Information</h2><span class="form-tag">Clinical Data</span></div><div class="form-body">', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    diagnosis = st.text_area("Diagnosis / Condition", height=100)
    medications = st.text_area("Medications Prescribed", height=100)
    heart_risk = st.selectbox("Heart Disease Risk", ["Not assessed","Low Risk","Moderate Risk","High Risk"])
with col2:
    xray_result = st.selectbox("X-Ray Result", ["Not done","Normal","Pneumonia Detected"])
    symptoms = st.text_area("Presenting Symptoms", height=100)
    vitals = st.text_area("Vital Signs", height=100)
st.markdown('</div></div>', unsafe_allow_html=True)

if st.button("👁️ Preview & Generate AI Notes"):
    if not name:
        st.error("Please enter patient name.")
    else:
        bmi = weight / ((height/100)**2)
        with st.spinner("🤖 FastAPI generating AI notes..."):
            try:
                response = requests.post(f"{API_URL}/report/notes", json={"name": name, "age": int(age), "gender": gender, "bmi": round(bmi,1), "diagnosis": diagnosis, "symptoms": symptoms, "medications": medications, "heart_risk": heart_risk, "xray_result": xray_result, "vitals": vitals, "api_key": st.secrets.get("GROQ_API_KEY", "")}, timeout=30)
                result = response.json()
                ai_notes = result.get("notes", "Notes generation failed.")
                st.session_state.report_ready = True
                st.session_state.report_data = {"name": name, "age": age, "gender": gender, "blood_group": blood_group, "height": height, "weight": weight, "bmi": round(bmi,1), "contact": contact, "doctor_name": doctor_name, "report_date": str(report_date), "diagnosis": diagnosis, "medications": medications, "heart_risk": heart_risk, "xray_result": xray_result, "symptoms": symptoms, "vitals": vitals, "ai_notes": ai_notes}
            except Exception as e:
                st.error(f"Error: {e}")

if "report_ready" in st.session_state and st.session_state.report_ready:
    d = st.session_state.report_data
    st.markdown(f"""
    <div class="preview-card">
        <div style="background:linear-gradient(135deg,#0d1f0d,#0f2510);border:1px solid #1a3a1a;border-radius:12px;padding:1.5rem;margin-bottom:1.5rem;">
            <div style="font-size:20px;font-weight:700;color:#4ade80;">⚕ ClinIQ — Smart Health Companion</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.4);">AI-Powered Medical Report · {d["report_date"]}</div>
        </div>
        <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin-bottom:1rem;">
            <div style="background:#0f1a0f;border:1px solid #1a2e1a;border-radius:8px;padding:8px 12px;"><div style="font-size:10px;color:rgba(255,255,255,0.4);text-transform:uppercase;">Name</div><div style="font-size:13px;font-weight:600;color:#ffffff;">{d["name"]}</div></div>
            <div style="background:#0f1a0f;border:1px solid #1a2e1a;border-radius:8px;padding:8px 12px;"><div style="font-size:10px;color:rgba(255,255,255,0.4);text-transform:uppercase;">Age / Gender</div><div style="font-size:13px;font-weight:600;color:#ffffff;">{d["age"]} · {d["gender"]}</div></div>
            <div style="background:#0f1a0f;border:1px solid #1a2e1a;border-radius:8px;padding:8px 12px;"><div style="font-size:10px;color:rgba(255,255,255,0.4);text-transform:uppercase;">BMI</div><div style="font-size:13px;font-weight:600;color:#ffffff;">{d["bmi"]} kg/m²</div></div>
            <div style="background:#0f1a0f;border:1px solid #1a2e1a;border-radius:8px;padding:8px 12px;"><div style="font-size:10px;color:rgba(255,255,255,0.4);text-transform:uppercase;">Heart Risk</div><div style="font-size:13px;font-weight:600;color:#ffffff;">{d["heart_risk"]}</div></div>
        </div>
        <div style="background:#0f1a0f;border:1px solid rgba(74,222,128,0.2);border-radius:10px;padding:1rem;">
            <div style="font-size:11px;font-weight:600;color:#4ade80;margin-bottom:6px;">🤖 AI Doctor Notes</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.7);line-height:1.7;">{d["ai_notes"]}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("⬇️ Download PDF Report"):
        try:
            d = st.session_state.report_data
            pdf = FPDF()
            pdf.add_page()
            pdf.set_fill_color(13, 18, 13)
            pdf.rect(0, 0, 210, 35, 'F')
            pdf.set_font('Helvetica', 'B', 18)
            pdf.set_text_color(74, 222, 128)
            pdf.cell(0, 12, '', ln=True)
            pdf.cell(0, 8, 'CLINIQ — SMART HEALTH COMPANION', align='C', ln=True)
            pdf.set_font('Helvetica', '', 9)
            pdf.set_text_color(150, 200, 150)
            pdf.cell(0, 6, 'AI-Powered Medical Report', align='C', ln=True)
            pdf.ln(8)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('Helvetica', 'B', 11)
            pdf.set_text_color(59, 109, 17)
            pdf.cell(0, 8, 'PATIENT INFORMATION', ln=True)
            pdf.set_draw_color(74, 222, 128)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(3)
            pdf.set_text_color(0, 0, 0)
            for label, value in [("Name", d['name']), ("Age/Gender", f"{d['age']} / {d['gender']}"), ("BMI", f"{d['bmi']} kg/m²"), ("Heart Risk", d['heart_risk']), ("X-Ray", d['xray_result']), ("Doctor", d['doctor_name'] or 'N/A'), ("Date", d['report_date'])]:
                pdf.set_font('Helvetica', 'B', 9)
                pdf.set_text_color(100, 100, 100)
                pdf.cell(50, 7, f"{label}:", border=0)
                pdf.set_font('Helvetica', '', 9)
                pdf.set_text_color(0, 0, 0)
                pdf.cell(0, 7, str(value), border=0, ln=True)
            pdf.ln(4)
            pdf.set_font('Helvetica', 'B', 11)
            pdf.set_text_color(59, 109, 17)
            pdf.cell(0, 8, 'AI DOCTOR NOTES', ln=True)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(3)
            pdf.set_font('Helvetica', '', 9)
            pdf.set_fill_color(240, 248, 235)
            pdf.set_text_color(40, 80, 10)
            pdf.multi_cell(0, 6, d['ai_notes'], fill=True)
            pdf.set_y(-20)
            pdf.set_font('Helvetica', 'I', 7)
            pdf.set_text_color(150, 150, 150)
            pdf.cell(0, 5, 'Generated by ClinIQ AI · For educational purposes only', align='C')
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                pdf.output(tmp.name)
                with open(tmp.name, 'rb') as f:
                    pdf_data = f.read()
                os.unlink(tmp.name)
            st.download_button(label="📥 Download PDF", data=pdf_data, file_name=f"cliniq_report_{d['name'].replace(' ','_')}.pdf", mime="application/pdf")
            st.success("✅ PDF generated!")
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown('<div class="disclaimer">⚠️ For educational purposes only.</div>', unsafe_allow_html=True)
