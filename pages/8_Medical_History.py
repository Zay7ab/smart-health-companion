import streamlit as st
import requests
import pandas as pd
from datetime import date
import sys
sys.path.append('.')
from utils.sidebar import load_sidebar

st.set_page_config(page_title="Medical History", page_icon="📋", layout="wide")
load_sidebar()

API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")

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
.stats-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 10px; margin-bottom: 1.25rem; }
.stat-card { background: white; border: 1px solid #e0ece0; border-radius: 12px; padding: 1rem; position: relative; overflow: hidden; }
.stat-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg,#639922,#97c459); }
.stat-label { font-size: 10px; color: #7a8f7a; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500; margin-bottom: 4px; }
.stat-value { font-size: 20px; font-weight: 700; color: #1a3a1a; }
.stat-sub { font-size: 10px; color: #639922; margin-top: 2px; font-weight: 500; }
.form-card { background: white; border: 1px solid #e0ece0; border-radius: 16px; overflow: hidden; margin-bottom: 1rem; }
.form-header { padding: 1rem 1.25rem; background: linear-gradient(135deg,#f5f9f0,#eaf3de); border-bottom: 1px solid #e0ece0; display: flex; align-items: center; justify-content: space-between; }
.form-header h2 { font-size: 14px; font-weight: 600; color: #1a3a1a; }
.form-tag { font-size: 10px; color: #3b6d11; background: #d4edbe; padding: 2px 8px; border-radius: 20px; font-weight: 600; }
.form-body { padding: 1.25rem; }
.record-card { background: white; border: 1px solid #e0ece0; border-radius: 12px; padding: 1rem 1.25rem; margin-bottom: 8px; display: flex; align-items: center; gap: 1rem; }
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
        <div class="topbar-title">📋 Medical History</div>
        <div class="topbar-sub">Track and analyze your medical records with AI</div>
    </div>
    <div class="ai-badge"><span class="ai-dot"></span> FastAPI + Groq AI Active</div>
</div>
""", unsafe_allow_html=True)

if "medical_records" not in st.session_state:
    st.session_state.medical_records = []

total = len(st.session_state.medical_records)
consultations = len([r for r in st.session_state.medical_records if r["Type"] == "Consultation"])
medications_count = len([r for r in st.session_state.medical_records if r["Type"] == "Medication"])
tests = len([r for r in st.session_state.medical_records if r["Type"] == "Lab Test"])

st.markdown(f"""
<div class="stats-row">
    <div class="stat-card"><div class="stat-label">Total Records</div><div class="stat-value">{total}</div><div class="stat-sub">All time</div></div>
    <div class="stat-card"><div class="stat-label">Consultations</div><div class="stat-value">{consultations}</div><div class="stat-sub">Doctor visits</div></div>
    <div class="stat-card"><div class="stat-label">Medications</div><div class="stat-value">{medications_count}</div><div class="stat-sub">Prescribed</div></div>
    <div class="stat-card"><div class="stat-label">Lab Tests</div><div class="stat-value">{tests}</div><div class="stat-sub">Completed</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="form-card"><div class="form-header"><h2>➕ Add New Record</h2><span class="form-tag">New Entry</span></div><div class="form-body">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    record_date = st.date_input("Date", value=date.today())
    record_type = st.selectbox("Record Type", ["Consultation", "Lab Test", "Surgery", "Medication", "Vaccination", "Imaging", "Other"])
with col2:
    condition = st.text_input("Condition / Diagnosis")
    doctor = st.text_input("Doctor / Hospital")
with col3:
    medications = st.text_input("Medications Prescribed")
    notes = st.text_area("Notes", height=80)
st.markdown('</div></div>', unsafe_allow_html=True)

type_colors = {
    "Consultation": ("#27500a", "#eaf3de"), "Lab Test": ("#185fa5", "#e6f1fb"),
    "Surgery": ("#c0392b", "#fff0f0"), "Medication": ("#d97706", "#fffbeb"),
    "Vaccination": ("#0f6e56", "#e1f5ee"), "Imaging": ("#534ab7", "#eeedfe"), "Other": ("#5f5e5a", "#f1efe8")
}

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("➕ Add Record"):
        if condition:
            st.session_state.medical_records.append({
                "Date": str(record_date), "Type": record_type,
                "Condition": condition, "Doctor": doctor,
                "Medications": medications, "Notes": notes
            })
            st.success("✅ Record added!")
            st.rerun()
        else:
            st.error("Please enter a condition.")

if st.session_state.medical_records:
    st.markdown("### 📊 Medical History")
    col1, col2 = st.columns([3, 1])
    with col2:
        filter_type = st.selectbox("Filter", ["All"] + list(type_colors.keys()))

    records_to_show = st.session_state.medical_records
    if filter_type != "All":
        records_to_show = [r for r in records_to_show if r["Type"] == filter_type]

    for record in reversed(records_to_show):
        color, bg = type_colors.get(record["Type"], ("#5f5e5a", "#f1efe8"))
        st.markdown(f"""
        <div class="record-card">
            <span style="background:{bg};color:{color};padding:4px 10px;border-radius:20px;font-size:10px;font-weight:600;flex-shrink:0;">{record["Type"]}</span>
            <div style="flex:1;">
                <div style="font-size:14px;font-weight:600;color:#1a3a1a;">{record["Condition"]}</div>
                <div style="font-size:11px;color:#7a8f7a;">📅 {record["Date"]} · 👨‍⚕️ {record["Doctor"] if record["Doctor"] else "Not specified"}</div>
                {f'<div style="font-size:12px;color:#5a6b5a;">💊 {record["Medications"]}</div>' if record["Medications"] else ''}
                {f'<div style="font-size:12px;color:#5a6b5a;">📝 {record["Notes"]}</div>' if record["Notes"] else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)

    if len(st.session_state.medical_records) >= 2:
        if st.button("🤖 Get AI Pattern Analysis"):
            with st.spinner("🤖 FastAPI analyzing history..."):
                try:
                    response = requests.post(
                        f"{API_URL}/history/analyze",
                        json={
                            "records": st.session_state.medical_records,
                            "api_key": st.secrets.get("GROQ_API_KEY", "")
                        },
                        timeout=30
                    )
                    result = response.json()
                    st.markdown(f"""
                    <div class="ai-insight">
                        <div class="ai-insight-header">🤖 AI Health Pattern Analysis (via FastAPI)</div>
                        <div class="ai-insight-text">{result['analysis'].replace(chr(10), '<br>')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")

    if st.button("🗑️ Clear All Records"):
        st.session_state.medical_records = []
        st.rerun()
else:
    st.markdown("""
    <div style="text-align:center;padding:3rem;color:#7a8f7a;">
        <div style="font-size:3rem;margin-bottom:1rem;">📋</div>
        <div style="font-size:15px;font-weight:600;color:#1a3a1a;">No Records Yet</div>
        <div style="font-size:12px;">Add your first medical record above</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="disclaimer">⚠️ For educational purposes only.</div>', unsafe_allow_html=True)
