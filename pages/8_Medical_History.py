import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Medical History", page_icon="📋", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');
    .stApp { background: linear-gradient(135deg, #0a0a1a 0%, #0d1b2a 40%, #1a0a2e 100%); font-family: 'Rajdhani', sans-serif; }
    .page-title { font-family: 'Orbitron', monospace; font-size: 2.5rem; font-weight: 900; background: linear-gradient(90deg, #00d4ff, #7b2ff7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; animation: glow 3s ease-in-out infinite alternate; }
    @keyframes glow { from { filter: drop-shadow(0 0 10px #00d4ff); } to { filter: drop-shadow(0 0 30px #7b2ff7); } }
    .glass-card { background: rgba(255,255,255,0.05); backdrop-filter: blur(20px); border: 1px solid rgba(0,212,255,0.2); border-radius: 20px; padding: 2rem; margin: 1rem 0; }
    .stButton > button { background: linear-gradient(90deg, #00d4ff, #7b2ff7) !important; color: white !important; border: none !important; border-radius: 12px !important; padding: 0.8rem 3rem !important; font-family: 'Orbitron', monospace !important; font-weight: 700 !important; width: 100% !important; margin-top: 1rem !important; }
    .stTextInput label, .stTextArea label, .stSelectbox label, .stDateInput label { color: #00d4ff !important; }
    [data-testid="stSidebar"] { background: rgba(10,10,26,0.95) !important; border-right: 1px solid rgba(0,212,255,0.2) !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    p, label { color: rgba(255,255,255,0.8) !important; }
</style>
<div class="page-title">📋 MEDICAL HISTORY</div>
<p style="color: #00d4ff; letter-spacing: 2px; text-transform: uppercase; font-size: 0.9rem;">Track and manage your medical records</p>
""", unsafe_allow_html=True)

if "medical_records" not in st.session_state:
    st.session_state.medical_records = []

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("### ➕ Add New Record")

col1, col2 = st.columns(2)
with col1:
    record_date = st.date_input("Date", value=date.today())
    condition = st.text_input("Condition / Diagnosis")
    doctor = st.text_input("Doctor / Hospital")

with col2:
    record_type = st.selectbox("Record Type", ["Consultation", "Lab Test", "Surgery", "Medication", "Vaccination", "Other"])
    medications = st.text_input("Medications Prescribed")
    notes = st.text_area("Notes", height=100)

st.markdown('</div>', unsafe_allow_html=True)

if st.button("➕ ADD RECORD"):
    if condition:
        st.session_state.medical_records.append({
            "Date": str(record_date),
            "Type": record_type,
            "Condition": condition,
            "Doctor": doctor,
            "Medications": medications,
            "Notes": notes
        })
        st.success("✅ Record added successfully!")
    else:
        st.error("Please enter a condition/diagnosis.")

if st.session_state.medical_records:
    st.markdown("### 📊 Your Medical History")
    df = pd.DataFrame(st.session_state.medical_records)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    if st.button("🗑️ CLEAR ALL RECORDS"):
        st.session_state.medical_records = []
        st.rerun()
else:
    st.markdown("""
    <div style="text-align: center; color: rgba(255,255,255,0.4); padding: 3rem;">
        <div style="font-size: 3rem;">📋</div>
        <div style="font-family: Orbitron; margin-top: 1rem;">NO RECORDS YET</div>
        <div style="margin-top: 0.5rem; font-size: 0.9rem;">Add your first medical record above</div>
    </div>
    """, unsafe_allow_html=True)
