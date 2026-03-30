import streamlit as st

st.set_page_config(
    page_title="ClinIQ — Smart Health Companion",
    page_icon="🩺",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; margin: 0; padding: 0; box-sizing: border-box; }

.stApp { background: #0a0f0a !important; }
[data-testid="stSidebar"] { background: #0d120d !important; border-right: 1px solid #1a2e1a !important; min-width: 220px !important; max-width: 220px !important; }
[data-testid="stSidebar"] * { color: #e0f0e0 !important; }
[data-testid="stSidebarNav"] { display: none !important; }
[data-testid="stSidebarCollapsedControl"] { display: none !important; }

.sidebar-brand { padding: 1.25rem 1rem 1rem 1rem; border-bottom: 1px solid #1a2e1a; margin-bottom: 0.5rem; }
.sidebar-brand-name { font-size: 16px; font-weight: 700; color: #4ade80 !important; display: flex; align-items: center; gap: 8px; }
.sidebar-brand-dot { width: 10px; height: 10px; border-radius: 50%; background: linear-gradient(135deg,#4ade80,#22c55e); flex-shrink: 0; }
.sidebar-brand-sub { font-size: 10px; color: #4ade80 !important; letter-spacing: 1px; text-transform: uppercase; margin-top: 3px; padding-left: 18px; opacity: 0.7; }
.sidebar-section { font-size: 10px; color: #4ade80 !important; letter-spacing: 1px; text-transform: uppercase; font-weight: 600; padding: 10px 10px 4px 10px; opacity: 0.6; }
.sidebar-divider { border: none; border-top: 1px solid #1a2e1a; margin: 4px 0; }

[data-testid="stPageLink"] { border-radius: 8px !important; margin-bottom: 2px !important; padding: 2px 4px !important; }
[data-testid="stPageLink"]:hover { background: #1a2e1a !important; }
[data-testid="stPageLink"] p { font-size: 13px !important; color: #a0b8a0 !important; font-weight: 400 !important; }
[data-testid="stPageLink"][aria-current="page"] p { color: #4ade80 !important; font-weight: 600 !important; }
[data-testid="stPageLink"][aria-current="page"] { background: linear-gradient(135deg,#1a2e1a,#0f2010) !important; }

.hero { background: linear-gradient(135deg, #0d1f0d 0%, #0f2510 40%, #0a1a0a 100%); border: 1px solid #1a3a1a; border-radius: 24px; padding: 3rem 2.5rem; margin-bottom: 1.5rem; position: relative; overflow: hidden; }
.hero::before { content: ''; position: absolute; top: -50%; right: -10%; width: 400px; height: 400px; background: radial-gradient(circle, rgba(74,222,128,0.06) 0%, transparent 70%); border-radius: 50%; }
.hero::after { content: ''; position: absolute; bottom: -30%; left: 20%; width: 300px; height: 300px; background: radial-gradient(circle, rgba(34,197,94,0.04) 0%, transparent 70%); border-radius: 50%; }
.hero-badge { display: inline-flex; align-items: center; gap: 6px; background: rgba(74,222,128,0.1); border: 1px solid rgba(74,222,128,0.2); border-radius: 20px; padding: 4px 12px; font-size: 11px; color: #4ade80; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 1.5rem; }
.hero h1 { font-size: 3rem; font-weight: 800; color: #ffffff; letter-spacing: -1.5px; line-height: 1.1; margin-bottom: 1rem; }
.hero h1 span { color: #4ade80; }
.hero p { font-size: 1rem; color: rgba(255,255,255,0.5); line-height: 1.7; max-width: 500px; }
.hero-icon-box { width: 72px; height: 72px; background: rgba(74,222,128,0.08); border: 1px solid rgba(74,222,128,0.15); border-radius: 18px; display: flex; align-items: center; justify-content: center; font-size: 2rem; transition: all 0.3s ease; }
.hero-icon-box:hover { background: rgba(74,222,128,0.15); transform: translateY(-4px); border-color: rgba(74,222,128,0.3); }

@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-6px)} }

.stats-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 12px; margin-bottom: 1.5rem; }
.stat-card { background: #0d120d; border: 1px solid #1a2e1a; border-radius: 16px; padding: 1.25rem; position: relative; overflow: hidden; }
.stat-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg,#4ade80,#22c55e); }
.stat-label { font-size: 11px; color: rgba(255,255,255,0.4); text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500; margin-bottom: 6px; }
.stat-value { font-size: 26px; font-weight: 700; color: #ffffff; letter-spacing: -0.5px; }
.stat-sub { font-size: 11px; color: #4ade80; margin-top: 3px; font-weight: 500; }

.feature-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 12px; margin-bottom: 1.5rem; }
.feature-card { background: #0d120d; border: 1px solid #1a2e1a; border-radius: 18px; padding: 1.5rem; transition: all 0.2s; cursor: pointer; }
.feature-card:hover { border-color: #4ade80; background: #0f1a0f; transform: translateY(-2px); box-shadow: 0 8px 32px rgba(74,222,128,0.08); }
.feature-icon { width: 44px; height: 44px; border-radius: 12px; background: rgba(74,222,128,0.1); border: 1px solid rgba(74,222,128,0.15); display: flex; align-items: center; justify-content: center; font-size: 20px; margin-bottom: 1rem; }
.feature-title { font-size: 14px; font-weight: 600; color: #ffffff; margin-bottom: 6px; }
.feature-desc { font-size: 12px; color: rgba(255,255,255,0.4); line-height: 1.6; }
.feature-tag { display: inline-block; font-size: 10px; background: rgba(74,222,128,0.1); color: #4ade80; border: 1px solid rgba(74,222,128,0.15); padding: 3px 8px; border-radius: 20px; font-weight: 600; margin-top: 10px; }

.disclaimer { background: rgba(255,200,0,0.05); border: 1px solid rgba(255,200,0,0.15); border-radius: 12px; padding: 1rem 1.25rem; font-size: 12px; color: rgba(255,200,0,0.7); }

p { color: rgba(255,255,255,0.5) !important; }
label { color: #e0f0e0 !important; }
</style>

<div class="hero">
    <div style="display:flex;align-items:center;justify-content:space-between;gap:2rem;">
        <div style="flex:1;">
            <div class="hero-badge">⚡ AI-Powered · 2026</div>
            <h1>Smart <span>Health</span><br/>Companion</h1>
            <p>Advanced AI-powered disease prediction and health analysis. Get instant insights powered by Machine Learning, Deep Learning and LLM technology.</p>
        </div>
        <div style="display:flex;flex-direction:column;gap:12px;flex-shrink:0;">
            <div style="display:flex;gap:12px;">
                <div class="hero-icon-box" style="animation:float 3s ease-in-out infinite;">🏥</div>
                <div class="hero-icon-box" style="animation:float 3s ease-in-out infinite 0.3s;">👨‍⚕️</div>
                <div class="hero-icon-box" style="animation:float 3s ease-in-out infinite 0.6s;">🩺</div>
            </div>
            <div style="display:flex;gap:12px;">
                <div class="hero-icon-box" style="animation:float 3s ease-in-out infinite 0.9s;">🧬</div>
                <div class="hero-icon-box" style="animation:float 3s ease-in-out infinite 1.2s;">💊</div>
                <div class="hero-icon-box" style="animation:float 3s ease-in-out infinite 1.5s;">🔬</div>
            </div>
            <div style="display:flex;gap:12px;">
                <div class="hero-icon-box" style="animation:float 3s ease-in-out infinite 1.8s;">🫀</div>
                <div class="hero-icon-box" style="animation:float 3s ease-in-out infinite 2.1s;">🫁</div>
                <div class="hero-icon-box" style="animation:float 3s ease-in-out infinite 2.4s;">🧠</div>
            </div>
        </div>
    </div>
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
        <div class="stat-value">11</div>
        <div class="stat-sub">AI-powered tools</div>
    </div>
</div>

<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-icon">🚨</div>
        <div class="feature-title">Emergency SOS</div>
        <div class="feature-desc">Instant first aid instructions and emergency numbers for 80+ countries worldwide.</div>
        <span class="feature-tag">Emergency · AI</span>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🫀</div>
        <div class="feature-title">Heart Disease Prediction</div>
        <div class="feature-desc">Random Forest ML model analyzes 15 cardiac features to predict disease risk.</div>
        <span class="feature-tag">ML · 92% AUC</span>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🫁</div>
        <div class="feature-title">X-Ray Analysis</div>
        <div class="feature-desc">CNN deep learning model detects pneumonia from chest X-ray images instantly.</div>
        <span class="feature-tag">CNN · 95% Accuracy</span>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">AI Health Chatbot</div>
        <div class="feature-desc">LLaMA 3.3 70B powered chatbot for symptom analysis and health guidance.</div>
        <span class="feature-tag">LLM · Groq</span>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <div class="feature-title">Symptom Checker</div>
        <div class="feature-desc">AI-powered symptom analysis with possible conditions and urgency levels.</div>
        <span class="feature-tag">AI Powered</span>
    </div>
    <div class="feature-card">
        <div class="feature-icon">👨‍⚕️</div>
        <div class="feature-title">Find a Doctor</div>
        <div class="feature-desc">AI recommends best doctors and hospitals for your specific condition.</div>
        <span class="feature-tag">AI Directory</span>
    </div>
    <div class="feature-card">
        <div class="feature-icon">⚖️</div>
        <div class="feature-title">BMI Calculator</div>
        <div class="feature-desc">Calculate BMI, BMR, ideal weight with AI-powered personalized health plan.</div>
        <span class="feature-tag">AI Insights</span>
    </div>
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Risk Gauge</div>
        <div class="feature-desc">Visual cardiovascular risk assessment with interactive gauge and AI prevention plan.</div>
        <span class="feature-tag">Interactive</span>
    </div>
    <div class="feature-card">
        <div class="feature-icon">📄</div>
        <div class="feature-title">Patient Report PDF</div>
        <div class="feature-desc">Generate professional AI-written medical reports with one-click PDF download.</div>
        <span class="feature-tag">AI Generated</span>
    </div>
</div>

<div class="disclaimer">
    ⚠️ This system is for educational purposes only. Always consult a qualified medical professional. In emergencies call 999/911/112 immediately.
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("""
<div class="sidebar-brand">
    <div class="sidebar-brand-name">
        <div class="sidebar-brand-dot"></div>
        ClinIQ
    </div>
    <div class="sidebar-brand-sub">Smart Companion · 2026</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-section" style="color:#ff6b6b !important;">🚨 Emergency</div>', unsafe_allow_html=True)
st.sidebar.page_link("pages/0_🚨_Emergency.py", label="🚨 Emergency SOS")

st.sidebar.markdown('<hr class="sidebar-divider"/><div class="sidebar-section">⚕ Diagnostics</div>', unsafe_allow_html=True)
st.sidebar.page_link("app.py", label="🏠 Home")
st.sidebar.page_link("pages/1_Heart_Disease.py", label="🫀 Heart Disease")
st.sidebar.page_link("pages/2_Xray_Analysis.py", label="🫁 X-Ray Analysis")
st.sidebar.page_link("pages/7_Symptom_Checker.py", label="🔍 Symptom Checker")

st.sidebar.markdown('<hr class="sidebar-divider"/><div class="sidebar-section">🔧 Tools</div>', unsafe_allow_html=True)
st.sidebar.page_link("pages/3_Health_Chatbot.py", label="🤖 AI Chatbot")
st.sidebar.page_link("pages/4_BMI_Calculator.py", label="⚖️ BMI Calculator")
st.sidebar.page_link("pages/6_Risk_Gauge.py", label="📊 Risk Gauge")

st.sidebar.markdown('<hr class="sidebar-divider"/><div class="sidebar-section">📁 Records</div>', unsafe_allow_html=True)
st.sidebar.page_link("pages/5_Health_Tips.py", label="💡 Health Tips")
st.sidebar.page_link("pages/8_Medical_History.py", label="📋 Medical History")
st.sidebar.page_link("pages/9_Patient_Report.py", label="📄 Patient Report")

st.sidebar.markdown('<hr class="sidebar-divider"/><div class="sidebar-section">🌍 Directory</div>', unsafe_allow_html=True)
st.sidebar.page_link("pages/10_Find_Doctor.py", label="👨‍⚕️ Find a Doctor")
