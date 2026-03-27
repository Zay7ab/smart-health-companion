import streamlit as st
from fpdf import FPDF
import tempfile
import os
from datetime import date

st.set_page_config(page_title="Patient Report", page_icon="📄", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');
    .stApp { background: linear-gradient(135deg, #0a0a1a 0%, #0d1b2a 40%, #1a0a2e 100%); font-family: 'Rajdhani', sans-serif; }
    .page-title { font-family: 'Orbitron', monospace; font-size: 2.5rem; font-weight: 900; background: linear-gradient(90deg, #00d4ff, #7b2ff7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; animation: glow 3s ease-in-out infinite alternate; }
    @keyframes glow { from { filter: drop-shadow(0 0 10px #00d4ff); } to { filter: drop-shadow(0 0 30px #7b2ff7); } }
    .glass-card { background: rgba(255,255,255,0.05); backdrop-filter: blur(20px); border: 1px solid rgba(0,212,255,0.2); border-radius: 20px; padding: 2rem; margin: 1rem 0; }
    .stButton > button { background: linear-gradient(90deg, #00d4ff, #7b2ff7) !important; color: white !important; border: none !important; border-radius: 12px !important; padding: 0.8rem 3rem !important; font-family: 'Orbitron', monospace !important; font-weight: 700 !important; width: 100% !important; margin-top: 1rem !important; }
    .stTextInput label, .stTextArea label, .stSelectbox label, .stNumberInput label { color: #00d4ff !important; }
    [data-testid="stSidebar"] { background: rgba(10,10,26,0.95) !important; border-right: 1px solid rgba(0,212,255,0.2) !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    p, label { color: rgba(255,255,255,0.8) !important; }
</style>
<div class="page-title">📄 PATIENT REPORT GENERATOR</div>
<p style="color: #00d4ff; letter-spacing: 2px; text-transform: uppercase; font-size: 0.9rem;">Generate a professional PDF health report</p>
""", unsafe_allow_html=True)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("### 👤 Patient Information")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=1, max_value=120, value=30)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])

with col2:
    height = st.number_input("Height (cm)", value=170)
    weight = st.number_input("Weight (kg)", value=70)
    contact = st.text_input("Contact Number")
    doctor_name = st.text_input("Doctor Name")

st.markdown("### 🩺 Medical Information")
col3, col4 = st.columns(2)
with col3:
    diagnosis = st.text_area("Diagnosis / Condition", height=100)
    medications = st.text_area("Medications", height=100)

with col4:
    heart_risk = st.selectbox("Heart Disease Risk", ["Low", "Moderate", "High"])
    xray_result = st.selectbox("X-Ray Result", ["Normal", "Pneumonia Detected", "Not Done"])
    notes = st.text_area("Doctor Notes", height=100)

st.markdown('</div>', unsafe_allow_html=True)

if st.button("📄 GENERATE PDF REPORT"):
    if name:
        bmi = weight / ((height/100) ** 2)

        pdf = FPDF()
        pdf.add_page()

        # Header
        pdf.set_fill_color(10, 10, 26)
        pdf.rect(0, 0, 210, 40, 'F')
        pdf.set_font('Helvetica', 'B', 22)
        pdf.set_text_color(0, 212, 255)
        pdf.cell(0, 15, '', ln=True)
        pdf.cell(0, 10, 'SMART HEALTH COMPANION', align='C', ln=True)
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(150, 150, 200)
        pdf.cell(0, 8, 'AI-Powered Medical Report', align='C', ln=True)

        pdf.ln(10)
        pdf.set_text_color(0, 0, 0)

        # Patient Info
        pdf.set_font('Helvetica', 'B', 14)
        pdf.set_text_color(10, 10, 80)
        pdf.cell(0, 10, 'PATIENT INFORMATION', ln=True)
        pdf.set_draw_color(0, 212, 255)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)

        pdf.set_font('Helvetica', '', 11)
        pdf.set_text_color(0, 0, 0)
        info = [
            ("Name", name), ("Age", str(age)), ("Gender", gender),
            ("Blood Group", blood_group), ("Height", f"{height} cm"),
            ("Weight", f"{weight} kg"), ("BMI", f"{bmi:.1f}"),
            ("Contact", contact), ("Report Date", str(date.today())),
            ("Doctor", doctor_name)
        ]
        for i in range(0, len(info), 2):
            pdf.cell(95, 8, f"{info[i][0]}: {info[i][1]}", border=0)
            if i+1 < len(info):
                pdf.cell(95, 8, f"{info[i+1][0]}: {info[i+1][1]}", border=0)
            pdf.ln()

        pdf.ln(5)

        # Medical Info
        pdf.set_font('Helvetica', 'B', 14)
        pdf.set_text_color(10, 10, 80)
        pdf.cell(0, 10, 'MEDICAL INFORMATION', ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)

        pdf.set_font('Helvetica', '', 11)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 8, f"Heart Disease Risk: {heart_risk}", ln=True)
        pdf.cell(0, 8, f"X-Ray Result: {xray_result}", ln=True)
        pdf.ln(3)

        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(0, 8, "Diagnosis:", ln=True)
        pdf.set_font('Helvetica', '', 11)
        pdf.multi_cell(0, 7, diagnosis if diagnosis else "N/A")
        pdf.ln(3)

        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(0, 8, "Medications:", ln=True)
        pdf.set_font('Helvetica', '', 11)
        pdf.multi_cell(0, 7, medications if medications else "N/A")
        pdf.ln(3)

        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(0, 8, "Doctor Notes:", ln=True)
        pdf.set_font('Helvetica', '', 11)
        pdf.multi_cell(0, 7, notes if notes else "N/A")

        # Footer
        pdf.set_y(-20)
        pdf.set_font('Helvetica', 'I', 8)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 10, 'This report is generated by Smart Health Companion AI. For educational purposes only. Consult a qualified doctor.', align='C')

        # Save and download
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            pdf.output(tmp.name)
            with open(tmp.name, 'rb') as f:
                pdf_data = f.read()
            os.unlink(tmp.name)

        st.download_button(
            label="⬇️ DOWNLOAD PDF REPORT",
            data=pdf_data,
            file_name=f"health_report_{name.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
        st.success("✅ Report generated successfully!")
    else:
        st.error("Please enter patient name.")
