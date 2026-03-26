import streamlit as st

st.set_page_config(
    page_title="Smart Health Companion",
    page_icon="🏥",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');

    .stApp {
        background: linear-gradient(135deg, #0a0a1a 0%, #0d1b2a 40%, #1a0a2e 100%);
        font-family: 'Rajdhani', sans-serif;
    }

    .main-title {
        font-family: 'Orbitron', monospace;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #00d4ff, #7b2ff7, #ff006e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: glow 3s ease-in-out infinite alternate;
        margin-bottom: 0.5rem;
    }

    @keyframes glow {
        from { filter: drop-shadow(0 0 10px #00d4ff); }
        to { filter: drop-shadow(0 0 30px #7b2ff7); }
    }

    .subtitle {
        text-align: center;
        color: #00d4ff;
        font-size: 1.2rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 3rem;
        animation: fadeIn 2s ease-in;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        animation: slideUp 0.8s ease-out;
    }

    @keyframes slideUp {
        from { opacity: 0; transform: translateY(40px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .glass-card:hover {
        border-color: rgba(123, 47, 247, 0.6);
        box-shadow: 0 8px 40px rgba(123, 47, 247, 0.3);
        transform: translateY(-5px);
    }

    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
        text-align: center;
    }

    .feature-title {
        font-family: 'Orbitron', monospace;
        color: #00d4ff;
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }

    .feature-desc {
        color: rgba(255,255,255,0.7);
        text-align: center;
        font-size: 0.95rem;
    }

    .warning-box {
        background: rgba(255, 0, 110, 0.1);
        border: 1px solid rgba(255, 0, 110, 0.3);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        color: #ff006e;
        margin-top: 2rem;
        font-size: 0.9rem;
    }

    .pulse {
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: rgba(10, 10, 26, 0.95);
        border-right: 1px solid rgba(0, 212, 255, 0.2);
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }
</style>

<div class="main-title">⚕ SMART HEALTH COMPANION</div>
<div class="subtitle">AI-Powered Disease Prediction System</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="glass-card">
        <span class="feature-icon pulse">🫀</span>
        <div class="feature-title">HEART DISEASE PREDICTION</div>
        <div class="feature-desc">Advanced ML algorithms analyze your cardiac data to predict disease risk with 92% AUC accuracy</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card">
        <span class="feature-icon pulse">🫁</span>
        <div class="feature-title">X-RAY ANALYSIS</div>
        <div class="feature-desc">Deep Learning CNN model analyzes chest X-rays to detect Pneumonia with 95% training accuracy</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="glass-card">
        <span class="feature-icon pulse">🤖</span>
        <div class="feature-title">AI HEALTH CHATBOT</div>
        <div class="feature-desc">LLM-powered assistant understands your symptoms and provides intelligent health guidance</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="warning-box">
    ⚠️ This system is for educational purposes only. Always consult a qualified medical professional for diagnosis.
</div>
""", unsafe_allow_html=True)
