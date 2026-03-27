import streamlit as st

st.set_page_config(
    page_title="HealthAI — Smart Health Companion",
    page_icon="🩺",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
[data-testid="stSidebarCollapsedControl"] { display: none !important; }
[data-testid="stSidebarNav"] { display: none !important; }
[data-testid="stSidebar"] { min-width: 220px !important; max-width: 220px !important; background: #ffffff !important; border-right: 1px solid #e0ece0 !important; }
[data-testid="stSidebar"] * { color: #1a3a1a !important; }
.stApp { background: #f0f4f0 !important; }
.hero { background: linear-gradient(135deg, #1a3a1a 0%, #2d5a1a 50%, #3b6d11 100%); border-radius: 20px; padding: 3rem 2.5rem; margin-bottom: 1.5rem; }
.hero-badge { display: inline-flex; align-items: center; gap: 6px; background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.2); border-radius: 20px; padding: 4px 12px; font-size: 11px; color: #97c459; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 1.5rem; }
.hero h1 { font-size: 2.8rem; font-weight: 700; color: #ffffff; letter-spacing: -1px; line-height: 1.15; margin-bottom: 1rem; }
.hero h1 span { color: #97c459; }
.hero p { font-size: 1rem; color: rgba(255,255,255,0.7); line-height: 1.7; max-width: 500px; }
.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 1.5rem; }
.stat-card { background: white; border: 1px solid #e0ece0; border-radius: 14px; padding: 1.25rem; position: relative; overflow: hidden; }
.stat-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #639922, #97c459); }
.stat-label { font-size: 11px; color: #7a8f7a; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500; margin-bottom: 6px; }
.stat-value { font-size: 24px; font-weight: 700; color: #1a3a1a; letter-spacing: -0.5px; }
.stat-sub { font-size: 11px; color: #639922; margin-top: 3px; font-weight: 500; }
.feature-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 1.5rem; }
.feature-card { background: white; border: 1px solid #e0ece0; border-radius: 16px; padding: 1.5rem; transition: all 0.2s; }
.feature-card:hover { border-color: #97c459; box-shadow: 0 4px 20px rgba(99,153,34,0.1); transform: translateY(-2px); }
.feature-icon { width: 44px; height: 44px; border-radius: 12px; background: linear-gradient(135deg, #eaf3de, #d4edbe); display: flex; align-items: center; justify-content: center; font-size: 20px; margin-bottom: 1rem; }
.feature-title { font-size: 14px; font-weight: 600; color: #1a3a1a; margin-bottom: 6px; }
.feature-desc { font-size: 12px; color: #7a8f7a; line-height: 1.6; }
.feature-tag { display: inline-block; font-size: 10px; background: #eaf3de; color: #3b6d11; padding: 3px 8px; border-radius: 20px; font-weight: 600; margin-top: 10px; }
.disclaimer { background: #fff8e1; border: 1px solid #f0c040; border-radius: 12px; padding: 1rem 1.25rem; font-size: 12px; color: #7a6000; }
.sidebar-logo { padding: 0.5rem 0 1rem 0; border-bottom: 1px solid #e0ece0; margin-bottom: 0.5rem; }
.sidebar-brand { font-size: 15px; font-weight: 700; color: #1a3a1a !important; display: flex; align-items: center; gap: 8px; }
.sidebar-brand-dot { width: 10px; height: 10px; border-radius: 50%; background: linear-gradient(135deg,#639922,#97c459); flex-shrink: 0; }
.sidebar-brand-sub { font-size: 10px; color: #639922 !important; letter-spacing: 1px; text-transform: uppercase; margin-top: 3px; padding-left: 18px; }
.sidebar-section { font-size: 10px; color: #97c459 !important; letter-spacing: 1px; text-transform: uppercase; font-weight: 600; padding: 10px 10px 4px 10px; }
.sidebar-divider { border: none; border-top: 1px solid #e0ece0; margin: 4px 0; }

[data-testid="stPageLink"] {
    border-radius: 8px !important;
    margin-bottom: 2px !important;
    padding: 2px 4px !important;
}
[data-testid="stPageLink"]:hover {
    background: #f5f9f0 !important;
}
[data-testid="stPageLink"] p {
    font-size: 13px !important;
    color: #5a6b5a !important;
    font-weight: 400 !important;
}
[data-testid="stPageLink"][aria-current="page"] p {
    color: #27500a !important;
    font-weight: 600 !important;
}
[data-testid="stPageLink"][aria-current="page"] {
    background: linear-gradient(135deg,#eaf3de,#d4edbe) !important;
}
</style>

<div class="hero">
    <div class="hero-badge">⚡ AI-Powered · 2026</div>
    <h1>Smart <span>Health</span><br/>Companion</h1>
    <p>Advanced AI-powered disease prediction and health analysis system. Get instant insights powered by Machine Learning, Deep Learning, and LLM technology.</p>
</div>

<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-label">ML Accuracy</div>
        <div class="stat-value">92%</div>
        <div class="stat-sub">AUC Score</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">CNN Accuracy</div>
        <div class="stat-value">95%</div>
        <div class="stat-sub">X-Ray Model</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">AI Model</div>
        <div class="stat-value">LLaMA</div>
        <div class="stat-sub">3.3 70B via Groq</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Features</div>
        <div class="stat-value">9</div>
        <div class="stat-sub">AI-powered tools</div>
    </div>
</div>

<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-icon">🫀</div>
        <div class="feature-title">Heart Disease Prediction</div>
        <div class="feature-desc">Random Forest ML model analyzes 15 cardiac features to predict disease risk.</div>
        <span class="feature-tag">ML · 92% AUC</span>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🫁</div>
        <div class="feature-title">X-Ray Analysis</div>
        <div class="feature-desc">CNN deep learning model detects pneumonia from chest X-ray images.</div>
        <span class="feature-tag">CNN · 95% Accuracy</span>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">AI Health Chatbot</div>
        <div class="feature-desc">LLaMA 3.3 70B powered chatbot for symptom analysis and health guidance.</div>
        <span class="feature-tag">LLM · Groq Powered</span>
    </div>
    <div class="feature-card">
        <div class="feature-icon">⚖️</div>
        <div class="feature-title">BMI & Vitals Calculator</div>
        <div class="feature-desc">Calculate BMI, BMR, ideal weight and get AI-powered health advice.</div>
        <span class="feature-tag">AI Insights</span>
    </div>
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Disease Risk Gauge</div>
        <div class="feature-desc">Visual risk assessment with interactive gauge and AI recommendations.</div>
        <span class="feature-tag">Interactive</span>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <div class="feature-title">Symptom Checker</div>
        <div class="feature-desc">AI-powered symptom analysis with possible conditions and urgency levels.</div>
        <span class="feature-tag">AI Powered</span>
    </div>
</div>

<div class="disclaimer">
    ⚠️ This system is for educational purposes only. Always consult a qualified medical professional for proper diagnosis and treatment.
</div>
""", unsafe_allow_html=True)

# Sidebar branding
st.sidebar.markdown("""
<div class="sidebar-logo">
    <div class="sidebar-brand">
        <div class="sidebar-brand-dot"></div>
        HealthAI
    </div>
    <div class="sidebar-brand-sub">Smart Companion · 2026</div>
</div>
""", unsafe_allow_html=True)

# Diagnostics section
st.sidebar.markdown('<div class="sidebar-section">⚕ Diagnostics</div>', unsafe_allow_html=True)
st.sidebar.page_link("app.py", label="🏠 Home")
st.sidebar.page_link("pages/1_Heart_Disease.py", label="🫀 Heart Disease")
st.sidebar.page_link("pages/2_Xray_Analysis.py", label="🫁 X-Ray Analysis")
st.sidebar.page_link("pages/7_Symptom_Checker.py", label="🔍 Symptom Checker")

# Tools section
st.sidebar.markdown('<hr class="sidebar-divider"/><div class="sidebar-section">🔧 Tools</div>', unsafe_allow_html=True)
st.sidebar.page_link("pages/3_Health_Chatbot.py", label="🤖 AI Chatbot")
st.sidebar.page_link("pages/4_BMI_Calculator.py", label="⚖️ BMI Calculator")
st.sidebar.page_link("pages/6_Risk_Gauge.py", label="📊 Risk Gauge")

# Records section
st.sidebar.markdown('<hr class="sidebar-divider"/><div class="sidebar-section">📁 Records</div>', unsafe_allow_html=True)
st.sidebar.page_link("pages/5_Health_Tips.py", label="💡 Health Tips")
st.sidebar.page_link("pages/8_Medical_History.py", label="📋 Medical History")
st.sidebar.page_link("pages/9_Patient_Report.py", label="📄 Patient Report")
