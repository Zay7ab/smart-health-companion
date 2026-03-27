import streamlit as st

def load_sidebar():
    st.markdown("""
    <style>
    [data-testid="stSidebarCollapsedControl"] { display: none !important; }
    [data-testid="stSidebarNav"] { display: none !important; }
    [data-testid="stSidebar"] { min-width: 220px !important; max-width: 220px !important; background: #ffffff !important; border-right: 1px solid #e0ece0 !important; }
    [data-testid="stSidebar"] * { color: #1a3a1a !important; }
    .sidebar-logo { padding: 0.5rem 0 1rem 0; border-bottom: 1px solid #e0ece0; margin-bottom: 0.5rem; }
    .sidebar-brand { font-size: 15px; font-weight: 700; color: #1a3a1a !important; display: flex; align-items: center; gap: 8px; }
    .sidebar-brand-dot { width: 10px; height: 10px; border-radius: 50%; background: linear-gradient(135deg,#639922,#97c459); flex-shrink: 0; }
    .sidebar-brand-sub { font-size: 10px; color: #639922 !important; letter-spacing: 1px; text-transform: uppercase; margin-top: 3px; padding-left: 18px; }
    .sidebar-section { font-size: 10px; color: #97c459 !important; letter-spacing: 1px; text-transform: uppercase; font-weight: 600; padding: 10px 10px 4px 10px; }
    .sidebar-divider { border: none; border-top: 1px solid #e0ece0; margin: 4px 0; }
    [data-testid="stPageLink"] { border-radius: 8px !important; margin-bottom: 2px !important; padding: 2px 4px !important; }
    [data-testid="stPageLink"]:hover { background: #f5f9f0 !important; }
    [data-testid="stPageLink"] p { font-size: 13px !important; color: #5a6b5a !important; font-weight: 400 !important; }
    [data-testid="stPageLink"][aria-current="page"] p { color: #27500a !important; font-weight: 600 !important; }
    [data-testid="stPageLink"][aria-current="page"] { background: linear-gradient(135deg,#eaf3de,#d4edbe) !important; }
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-brand">
            <div class="sidebar-brand-dot"></div>
            HealthAI
        </div>
        <div class="sidebar-brand-sub">Smart Companion · 2026</div>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown('<div class="sidebar-section">⚕ Diagnostics</div>', unsafe_allow_html=True)
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
