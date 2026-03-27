import streamlit as st
import numpy as np
from PIL import Image
import onnxruntime as ort
from groq import Groq
import sys
sys.path.append('.')
from utils.sidebar import load_sidebar

st.set_page_config(page_title="X-Ray Analysis", page_icon="🫁", layout="wide")
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
.stats-row { display: grid; grid-template-columns: repeat(3,1fr); gap: 10px; margin-bottom: 1.25rem; }
.stat-card { background: white; border: 1px solid #e0ece0; border-radius: 12px; padding: 1rem; position: relative; overflow: hidden; }
.stat-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg,#639922,#97c459); }
.stat-label { font-size: 10px; color: #7a8f7a; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500; margin-bottom: 4px; }
.stat-value { font-size: 20px; font-weight: 700; color: #1a3a1a; }
.stat-sub { font-size: 10px; color: #639922; margin-top: 2px; font-weight: 500; }
.upload-card { background: white; border: 2px dashed #97c459; border-radius: 16px; padding: 2rem; margin-bottom: 1rem; text-align: center; }
.result-high { background: linear-gradient(135deg,#fff0f0,#ffe0e0); border: 1px solid #ffb3b3; border-radius: 14px; padding: 1.25rem; margin-top: 1rem; }
.result-low { background: linear-gradient(135deg,#f0fff4,#e0ffe8); border: 1px solid #97c459; border-radius: 14px; padding: 1.25rem; margin-top: 1rem; }
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
        <div class="topbar-title">🫁 X-Ray Analysis</div>
        <div class="topbar-sub">Deep Learning CNN model for pneumonia detection</div>
    </div>
    <div class="ai-badge"><span class="ai-dot"></span> Groq AI Active</div>
</div>
<div class="stats-row">
    <div class="stat-card">
        <div class="stat-label">Model</div>
        <div class="stat-value">CNN</div>
        <div class="stat-sub">Deep Learning</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Training Accuracy</div>
        <div class="stat-value">95%</div>
        <div class="stat-sub">5216 Images</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Classes</div>
        <div class="stat-value">2</div>
        <div class="stat-sub">Normal · Pneumonia</div>
    </div>
</div>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return ort.InferenceSession('models/xray_model.onnx')

col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("""
    <div class="upload-card">
        <div style="font-size:3rem;margin-bottom:1rem;">🫁</div>
        <div style="font-size:14px;font-weight:600;color:#1a3a1a;margin-bottom:6px;">Upload Chest X-Ray</div>
        <div style="font-size:12px;color:#7a8f7a;">Supports JPG, JPEG, PNG formats</div>
    </div>
    """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose X-Ray image", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

with col2:
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded X-Ray", use_column_width=True)

if uploaded_file and st.button("⚡ Analyze X-Ray"):
    with st.spinner("Running CNN analysis..."):
        try:
            session = load_model()
            img = image.convert('RGB')
            img = img.resize((150, 150))
            img_array = np.array(img, dtype=np.float32) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            input_name = session.get_inputs()[0].name
            prediction = session.run(None, {input_name: img_array})[0]
            probability = prediction[0][0]

            if probability > 0.5:
                st.markdown(f"""
                <div class="result-high">
                    <div style="font-size:16px;font-weight:700;color:#c0392b">⚠️ Pneumonia Detected</div>
                    <div style="font-size:28px;font-weight:700;color:#c0392b">{probability*100:.1f}%</div>
                    <div style="font-size:12px;color:#7a3a3a;margin-top:4px">Confidence Level</div>
                </div>
                """, unsafe_allow_html=True)
                result = "pneumonia detected"
            else:
                st.markdown(f"""
                <div class="result-low">
                    <div style="font-size:16px;font-weight:700;color:#27500a">✅ Normal</div>
                    <div style="font-size:28px;font-weight:700;color:#27500a">{(1-probability)*100:.1f}%</div>
                    <div style="font-size:12px;color:#3b6d11;margin-top:4px">Confidence Level</div>
                </div>
                """, unsafe_allow_html=True)
                result = "normal, no pneumonia detected"

            with st.spinner("🤖 Getting AI insights..."):
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                prompt = f"""A chest X-ray CNN model detected: {result} with {probability*100:.1f}% confidence.
                Give a brief 3-4 sentence professional medical insight, what it means and next steps.
                End with: Always consult a qualified radiologist or pulmonologist."""
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=200
                )
                insight = response.choices[0].message.content
                st.markdown(f"""
                <div class="ai-insight">
                    <div class="ai-insight-header">🤖 AI Medical Insight</div>
                    <div class="ai-insight-text">{insight}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('<div class="disclaimer">⚠️ For educational purposes only. Always consult a qualified doctor.</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {e}")
