import streamlit as st
import numpy as np
from PIL import Image
import onnxruntime as ort

st.set_page_config(page_title="X-Ray Analysis", page_icon="🫁", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');
    .stApp {
        background: linear-gradient(135deg, #0a0a1a 0%, #0d1b2a 40%, #1a0a2e 100%);
        font-family: 'Rajdhani', sans-serif;
    }
    .page-title {
        font-family: 'Orbitron', monospace;
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00d4ff, #7b2ff7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: glow 3s ease-in-out infinite alternate;
    }
    @keyframes glow {
        from { filter: drop-shadow(0 0 10px #00d4ff); }
        to { filter: drop-shadow(0 0 30px #7b2ff7); }
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        animation: slideUp 0.8s ease-out;
    }
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(40px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stButton > button {
        background: linear-gradient(90deg, #00d4ff, #7b2ff7) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 3rem !important;
        font-family: 'Orbitron', monospace !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
        width: 100% !important;
        margin-top: 1rem !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 30px rgba(123, 47, 247, 0.5) !important;
    }
    .result-high {
        background: rgba(255, 0, 110, 0.15);
        border: 1px solid rgba(255, 0, 110, 0.5);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        color: #ff006e;
        font-family: 'Orbitron', monospace;
        font-size: 1.2rem;
        animation: pulse 2s infinite;
    }
    .result-low {
        background: rgba(0, 255, 150, 0.15);
        border: 1px solid rgba(0, 255, 150, 0.5);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        color: #00ff96;
        font-family: 'Orbitron', monospace;
        font-size: 1.2rem;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(0, 212, 255, 0.4); }
        70% { box-shadow: 0 0 0 15px rgba(0, 212, 255, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 212, 255, 0); }
    }
    [data-testid="stSidebar"] {
        background: rgba(10, 10, 26, 0.95) !important;
        border-right: 1px solid rgba(0, 212, 255, 0.2) !important;
    }
    [data-testid="stSidebar"] * { color: white !important; }
    p, label { color: rgba(255,255,255,0.8) !important; }
</style>

<div class="page-title">🫁 X-RAY ANALYSIS</div>
<p style="color: #00d4ff; letter-spacing: 2px; text-transform: uppercase; font-size: 0.9rem;">
    Upload a chest X-ray for AI-powered pneumonia detection
</p>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    session = ort.InferenceSession('models/xray_model.onnx')
    return session

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

uploaded_file = st.file_uploader("📂 Upload Chest X-Ray Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    col1, col2 = st.columns([1, 1])
    with col1:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded X-Ray", use_column_width=True)
    with col2:
        st.markdown("""
        <div style="padding: 2rem; color: rgba(255,255,255,0.7);">
            <h3 style="color: #00d4ff; font-family: Orbitron;">Image Loaded ✓</h3>
            <p>Your X-Ray has been uploaded successfully.</p>
            <p>Click <b>Analyze</b> to run the CNN model.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("⚡ ANALYZE X-RAY"):
            with st.spinner("Running deep learning analysis..."):
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
                            ⚠️ PNEUMONIA DETECTED<br>
                            <span style="font-size:2rem">{probability*100:.1f}%</span><br>
                            <span style="font-size:0.8rem">Confidence Level</span>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="result-low">
                            ✅ NORMAL<br>
                            <span style="font-size:2rem">{(1-probability)*100:.1f}%</span><br>
                            <span style="font-size:0.8rem">Confidence Level</span>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown("""
                    <div style="text-align:center; color: rgba(255,255,255,0.5);
                    margin-top:1rem; font-size:0.8rem;">
                        ⚕️ Always consult a qualified doctor for proper diagnosis
                    </div>
                    """, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Error: {e}")

st.markdown('</div>', unsafe_allow_html=True)
