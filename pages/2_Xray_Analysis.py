import streamlit as st
import requests
from PIL import Image
import sys
sys.path.append('.')
from utils.sidebar import load_sidebar

st.set_page_config(page_title="X-Ray Analysis", page_icon="🫁", layout="wide")
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
.stats-row { display: grid; grid-template-columns: repeat(3,1fr); gap: 10px; margin-bottom: 1.25rem; }
.stat-card { background: #0d120d; border: 1px solid #1a2e1a; border-radius: 12px; padding: 1rem; position: relative; overflow: hidden; }
.stat-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg,#4ade80,#22c55e); }
.stat-label { font-size: 10px; color: rgba(255,255,255,0.4); text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500; margin-bottom: 4px; }
.stat-value { font-size: 20px; font-weight: 700; color: #ffffff; }
.stat-sub { font-size: 10px; color: #4ade80; margin-top: 2px; font-weight: 500; }
.upload-card { background: #0d120d; border: 2px dashed #1a2e1a; border-radius: 16px; padding: 2rem; margin-bottom: 1rem; text-align: center; }
.result-high { background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.2); border-radius: 14px; padding: 1.25rem; margin-top: 1rem; }
.result-low { background: rgba(74,222,128,0.08); border: 1px solid rgba(74,222,128,0.2); border-radius: 14px; padding: 1.25rem; margin-top: 1rem; }
.ai-insight { background: #0d120d; border: 1px solid #1a2e1a; border-radius: 12px; padding: 1rem; margin-top: 1rem; }
.ai-insight-header { font-size: 11px; font-weight: 600; color: #4ade80; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }
.ai-insight-text { font-size: 13px; color: rgba(255,255,255,0.7); line-height: 1.7; }
.disclaimer { background: rgba(255,200,0,0.05); border: 1px solid rgba(255,200,0,0.15); border-radius: 10px; padding: 0.75rem 1rem; font-size: 11px; color: rgba(255,200,0,0.7); margin-top: 1rem; }
div[data-testid="stButton"] button { background: linear-gradient(135deg,#166534,#4ade80) !important; color: #0a0f0a !important; border: none !important; border-radius: 8px !important; font-weight: 700 !important; font-size: 13px !important; padding: 0.6rem 1.5rem !important; }
label { color: rgba(255,255,255,0.7) !important; }
p { color: rgba(255,255,255,0.5) !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="topbar">
    <div>
        <div class="topbar-title">🫁 X-Ray Analysis</div>
        <div class="topbar-sub">Deep Learning CNN model for pneumonia detection</div>
    </div>
    <div class="ai-badge"><span class="ai-dot"></span> FastAPI + CNN Active</div>
</div>
<div class="stats-row">
    <div class="stat-card"><div class="stat-label">Model</div><div class="stat-value">CNN</div><div class="stat-sub">Deep Learning</div></div>
    <div class="stat-card"><div class="stat-label">Training Accuracy</div><div class="stat-value">95%</div><div class="stat-sub">5216 Images</div></div>
    <div class="stat-card"><div class="stat-label">Classes</div><div class="stat-value">2</div><div class="stat-sub">Normal · Pneumonia</div></div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1,1])
with col1:
    st.markdown("""
    <div class="upload-card">
        <div style="font-size:3rem;margin-bottom:1rem;">🫁</div>
        <div style="font-size:14px;font-weight:600;color:#ffffff;margin-bottom:6px;">Upload Chest X-Ray</div>
        <div style="font-size:12px;color:rgba(255,255,255,0.4);">Supports JPG, JPEG, PNG formats</div>
    </div>
    """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose X-Ray image", type=["jpg","jpeg","png"], label_visibility="collapsed")
with col2:
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded X-Ray", use_column_width=True)

if uploaded_file and st.button("⚡ Analyze X-Ray"):
    with st.spinner("🤖 FastAPI CNN analyzing..."):
        try:
            img_bytes = uploaded_file.getvalue()
            response = requests.post(f"{API_URL}/predict/xray", files={"file": ("xray.jpg", img_bytes, "image/jpeg")}, timeout=60)
            result = response.json()
            if "error" in result:
                st.error(f"API Error: {result['error']}")
            else:
                probability = result["probability"]
                is_pneumonia = result["is_pneumonia"]
                if is_pneumonia:
                    st.markdown(f'<div class="result-high"><div style="font-size:16px;font-weight:700;color:#ef4444;">⚠️ Pneumonia Detected</div><div style="font-size:32px;font-weight:800;color:#ef4444;">{probability*100:.1f}%</div><div style="font-size:12px;color:rgba(239,68,68,0.7);margin-top:4px;">Confidence Level</div></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="result-low"><div style="font-size:16px;font-weight:700;color:#4ade80;">✅ Normal</div><div style="font-size:32px;font-weight:800;color:#4ade80;">{(1-probability)*100:.1f}%</div><div style="font-size:12px;color:rgba(74,222,128,0.7);margin-top:4px;">Confidence Level</div></div>', unsafe_allow_html=True)
                if "ai_insight" in result:
                    st.markdown(f'<div class="ai-insight"><div class="ai-insight-header">🤖 AI Medical Insight</div><div class="ai-insight-text">{result["ai_insight"]}</div></div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown('<div class="disclaimer">⚠️ For educational purposes only. Always consult a qualified doctor.</div>', unsafe_allow_html=True)
