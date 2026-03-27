import streamlit as st
from groq import Groq
from fpdf import FPDF
import tempfile
import os
from datetime import date
import sys
sys.path.append('.')
from utils.sidebar import load_sidebar

st.set_page_config(page_title="Patient Report", page_icon="📄", layout="wide")
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
.preview-card { background: white; border: 1px solid #e0ece0; border-radius: 16px; padding: 2rem; margin-bottom: 1rem; }
.preview-header { background: linear-gradient(135deg,#1a3a1a,#3b6d11); border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; }
.preview-section { margin-bottom: 1.25rem; padding-bottom: 1.25rem; border-bottom: 1px solid #e0ece0; }
.preview-section:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
.preview-section-title { font-size: 11px; font-weight: 600; color: #639922; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }
.preview-grid { display: grid; grid-template-columns: repeat(2,1fr); gap: 8px; }
.preview-field { background: #f8faf8; border-radius: 8px; padding: 8px 12px; }
.preview-field-label { font-size: 10px; color: #7a8f7a; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 2px; }
.preview-field-value { font-size: 13px; font-weight: 600; color: #1a3a1a; }
.disclaimer { background: #fff8e1; border: 1px solid #f0c040; border-radius: 10px; padding: 0.75rem 1rem; font-size: 11px; color: #7a6000; margin-top: 1rem; }
div[data-testid="stButton"] button { background: linear-gradient(135deg,#3b6d11,#639922) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; font-size: 13px !important; padding: 0.6rem 1.5rem !important; }
label { color: #1a3a1a !important; }
p { color: #1a3a1a !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="topbar">
    <div>
        <div class="topbar-title">📄 Patient Report Generator</div>
        <div class="topbar-sub">AI-written professional medical reports with PDF export</div>
    </div>
    <div class="ai-badge"><span class="ai-dot"></span> Groq AI Active</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="form-card"><div class="form-header"><h2>👤 Patient Information</h2><span class="form-tag">Required</span></div><div class="form-body">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    name = st.text_input("Full Name", placeholder="John Doe")
    age = st.number_input("Age", min_value=1, max_value=120, value=30)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
with col2:
    blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
    height = st.number_input("Height (cm)", value=170)
    weight = st.number_input("Weight (kg)", value=70)
with col3:
    contact = st.text_input("Contact Number", placeholder="+1 234 567 8900")
    doctor_name = st.text_input("Doctor Name", placeholder="Dr. Smith")
    report_date = st.date_input("Report Date", value=date.today())
st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown('<div class="form-card"><div class="form-header"><h2>🩺 Medical Information</h2><span class="form-tag">Clinical Data</span></div><div class="form-body">', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    diagnosis = st.text_area("Diagnosis / Condition", height=100, placeholder="Primary diagnosis...")
    medications = st.text_area("Medications Prescribed", height=100, placeholder="List medications and dosages...")
    heart_risk = st.selectbox("Heart Disease Risk", ["Not assessed", "Low Risk", "Moderate Risk", "High Risk"])
with col2:
    xray_result = st.selectbox("X-Ray Result", ["Not done", "Normal", "Pneumonia Detected"])
    symptoms = st.text_area("Presenting Symptoms", height=100, placeholder="List main symptoms...")
    vitals = st.text_area("Vital Signs", height=100, placeholder="BP, Heart Rate, Temperature, etc...")
st.markdown('</div></div>', unsafe_allow_html=True)

if st.button("👁️ Preview & Generate AI Notes"):
    if not name:
        st.error("Please enter patient name.")
    else:
        bmi = weight / ((height / 100) ** 2)
        with st.spinner("🤖 AI writing doctor notes..."):
            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                prompt = f"""Write professional doctor notes for: {name}, {age}yo {gender}, BMI {bmi:.1f},
                Diagnosis: {diagnosis or 'Not specified'}, Symptoms: {symptoms or 'Not specified'},
                Medications: {medications or 'None'}, Heart Risk: {heart_risk}, X-Ray: {xray_result}, Vitals: {vitals or 'Not recorded'}.
                Write 3-4 sentences of formal clinical notes summarizing condition, AI findings, and follow-up care."""
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=250
                )
                ai_notes = response.choices[0].message.content
                st.session_state.ai_notes = ai_notes
                st.session_state.report_ready = True
                st.session_state.report_data = {
                    "name": name, "age": age, "gender": gender, "blood_group": blood_group,
                    "height": height, "weight": weight, "bmi": bmi, "contact": contact,
                    "doctor_name": doctor_name, "report_date": str(report_date),
                    "diagnosis": diagnosis, "medications": medications, "heart_risk": heart_risk,
                    "xray_result": xray_result, "symptoms": symptoms, "vitals": vitals, "ai_notes": ai_notes
                }
            except Exception as e:
                st.error(f"Error: {e}")

if "report_ready" in st.session_state and st.session_state.report_ready:
    d = st.session_state.report_data
    st.markdown("### 👁️ Report Preview")
    st.markdown(f"""
    <div class="preview-card">
        <div class="preview-header">
            <div style="font-size:20px;font-weight:700;color:white;">⚕ Smart Health Companion</div>
            <div style="font-size:12px;color:#97c459;">AI-Powered Medical Report · {d['report_date']}</div>
        </div>
        <div class="preview-section">
            <div class="preview-section-title">Patient Information</div>
            <div class="preview-grid">
                <div class="preview-field"><div class="preview-field-label">Full Name</div><div class="preview-field-value">{d['name']}</div></div>
                <div class="preview-field"><div class="preview-field-label">Age / Gender</div><div class="preview-field-value">{d['age']} years · {d['gender']}</div></div>
                <div class="preview-field"><div class="preview-field-label">Blood Group</div><div class="preview-field-value">{d['blood_group']}</div></div>
                <div class="preview-field"><div class="preview-field-label">BMI</div><div class="preview-field-value">{d['bmi']:.1f} kg/m²</div></div>
                <div class="preview-field"><div class="preview-field-label">Height / Weight</div><div class="preview-field-value">{d['height']} cm · {d['weight']} kg</div></div>
                <div class="preview-field"><div class="preview-field-label">Doctor</div><div class="preview-field-value">{d['doctor_name'] if d['doctor_name'] else 'Not specified'}</div></div>
            </div>
        </div>
        <div class="preview-section">
            <div class="preview-section-title">AI Analysis Results</div>
            <div class="preview-grid">
                <div class="preview-field"><div class="preview-field-label">Heart Disease Risk</div><div class="preview-field-value">{d['heart_risk']}</div></div>
                <div class="preview-field"><div class="preview-field-label">X-Ray Result</div><div class="preview-field-value">{d['xray_result']}</div></div>
            </div>
        </div>
        <div class="preview-section">
            <div class="preview-section-title">Diagnosis & Treatment</div>
            <div class="preview-field" style="margin-bottom:8px;"><div class="preview-field-label">Diagnosis</div><div class="preview-field-value">{d['diagnosis'] if d['diagnosis'] else 'Not specified'}</div></div>
            <div class="preview-field" style="margin-bottom:8px;"><div class="preview-field-label">Medications</div><div class="preview-field-value">{d['medications'] if d['medications'] else 'None prescribed'}</div></div>
            <div class="preview-field"><div class="preview-field-label">Symptoms</div><div class="preview-field-value">{d['symptoms'] if d['symptoms'] else 'Not recorded'}</div></div>
        </div>
        <div class="preview-section">
            <div class="preview-section-title">AI Doctor Notes</div>
            <div style="background:#f5f9f0;border:1px solid #d4edbe;border-radius:10px;padding:1rem;">
                <div style="font-size:11px;font-weight:600;color:#639922;margin-bottom:6px;">🤖 Generated by Groq AI</div>
                <div style="font-size:12px;color:#3a4a3a;line-height:1.7;">{d['ai_notes']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("⬇️ Download PDF Report"):
        try:
            d = st.session_state.report_data
            pdf = FPDF()
            pdf.add_page()

            pdf.set_fill_color(26, 58, 26)
            pdf.rect(0, 0, 210, 35, 'F')
            pdf.set_font('Helvetica', 'B', 18)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(0, 12, '', ln=True)
            pdf.cell(0, 8, 'SMART HEALTH COMPANION', align='C', ln=True)
            pdf.set_font('Helvetica', '', 9)
            pdf.set_text_color(151, 196, 89)
            pdf.cell(0, 6, 'AI-Powered Medical Report', align='C', ln=True)
            pdf.ln(8)
            pdf.set_text_color(0, 0, 0)

            def section_title(title):
                pdf.set_font('Helvetica', 'B', 11)
                pdf.set_text_color(59, 109, 17)
                pdf.cell(0, 8, title, ln=True)
                pdf.set_draw_color(151, 196, 89)
                pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                pdf.ln(3)
                pdf.set_text_color(0, 0, 0)

            def field_row(label, value):
                pdf.set_font('Helvetica', 'B', 9)
                pdf.set_text_color(100, 100, 100)
                pdf.cell(50, 7, label + ':', border=0)
                pdf.set_font('Helvetica', '', 9)
                pdf.set_text_color(0, 0, 0)
                pdf.cell(0, 7, str(value), border=0, ln=True)

            section_title('PATIENT INFORMATION')
            field_row('Full Name', d['name'])
            field_row('Age / Gender', f"{d['age']} years / {d['gender']}")
            field_row('Blood Group', d['blood_group'])
            field_row('Height / Weight', f"{d['height']} cm / {d['weight']} kg")
            field_row('BMI', f"{d['bmi']:.1f} kg/m²")
            field_row('Contact', d['contact'] if d['contact'] else 'Not provided')
            field_row('Doctor', d['doctor_name'] if d['doctor_name'] else 'Not specified')
            field_row('Report Date', d['report_date'])
            pdf.ln(4)

            section_title('AI ANALYSIS RESULTS')
            field_row('Heart Disease Risk', d['heart_risk'])
            field_row('X-Ray Result', d['xray_result'])
            pdf.ln(4)

            section_title('DIAGNOSIS & TREATMENT')
            field_row('Diagnosis', d['diagnosis'] if d['diagnosis'] else 'Not specified')
            field_row('Symptoms', d['symptoms'] if d['symptoms'] else 'Not recorded')
            field_row('Vitals', d['vitals'] if d['vitals'] else 'Not recorded')
            pdf.ln(2)
            pdf.set_font('Helvetica', 'B', 9)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(0, 7, 'Medications:', ln=True)
            pdf.set_font('Helvetica', '', 9)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(0, 6, d['medications'] if d['medications'] else 'None prescribed')
            pdf.ln(4)

            section_title('AI DOCTOR NOTES')
            pdf.set_font('Helvetica', '', 9)
            pdf.set_fill_color(240, 248, 235)
            pdf.set_text_color(40, 80, 10)
            pdf.multi_cell(0, 6, d['ai_notes'], fill=True)

            pdf.set_y(-20)
            pdf.set_font('Helvetica', 'I', 7)
            pdf.set_text_color(150, 150, 150)
            pdf.cell(0, 5, f'Generated by Smart Health Companion AI · {d["report_date"]} · For educational purposes only', align='C', ln=True)
            pdf.cell(0, 5, 'This report is NOT a substitute for professional medical advice. Always consult a qualified doctor.', align='C')

            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                pdf.output(tmp.name)
                with open(tmp.name, 'rb') as f:
                    pdf_data = f.read()
                os.unlink(tmp.name)

            st.download_button(
                label="📥 Click here to download your PDF",
                data=pdf_data,
                file_name=f"health_report_{d['name'].replace(' ', '_')}_{d['report_date']}.pdf",
                mime="application/pdf"
            )
            st.success("✅ PDF generated successfully!")
        except Exception as e:
            st.error(f"Error generating PDF: {e}")

st.markdown('<div class="disclaimer">⚠️ For educational purposes only. This report should not replace professional medical consultation.</div>', unsafe_allow_html=True)
