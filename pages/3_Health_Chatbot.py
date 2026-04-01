# --- Updated CSS for Sidebar & Icons (Add this to your style block) ---
st.markdown("""
<style>
    /* Sidebar Navigation Styling */
    [data-testid="stSidebar"] {
        background-color: #050a05 !important;
        border-right: 1px solid #1a2e1a;
    }
    .nav-header {
        font-size: 10px; font-weight: 800; color: #4ade80; 
        margin: 20px 0 10px 10px; letter-spacing: 1px; opacity: 0.8;
    }
    .brand-section {
        padding: 1.5rem 1rem; margin-bottom: 1rem;
    }
    .brand-title { 
        color: #4ade80; font-size: 24px; font-weight: 800; 
        display: flex; align-items: center; gap: 10px;
    }
    .brand-sub { font-size: 10px; color: rgba(255,255,255,0.4); letter-spacing: 1px; }
    
    /* Active & Hover States for Sidebar Buttons */
    div[data-testid="stVerticalBlock"] > div > button {
        background-color: transparent !important;
        border: none !important;
        color: rgba(255,255,255,0.7) !important;
        text-align: left !important;
        justify-content: flex-start !important;
        width: 100% !important;
        padding: 0.5rem 1rem !important;
    }
    div[data-testid="stVerticalBlock"] > div > button:hover {
        color: #4ade80 !important;
        background: rgba(74,222,128,0.05) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar Logic according to Image ---
with st.sidebar:
    # Brand Identity
    st.markdown("""
        <div class="brand-section">
            <div class="brand-title">🟢 ClinIQ</div>
            <div class="brand-sub">SMART COMPANION • 2026</div>
        </div>
        <hr style="border-color: #1a2e1a; margin: 0 10px;">
    """, unsafe_allow_html=True)

    # Emergency Section
    st.markdown('<div class="nav-header">🚨 EMERGENCY</div>', unsafe_allow_html=True)
    if st.button("🚨 Emergency SOS", use_container_width=True):
        st.error("Emergency protocol initiated! (Mock)")

    st.markdown('<hr style="border-color: #1a2e1a; margin: 10px;">', unsafe_allow_html=True)

    # Diagnostics Section
    st.markdown('<div class="nav-header">⚕️ DIAGNOSTICS</div>', unsafe_allow_html=True)
    page = "Home" # Default
    if st.button("🏠 Home", use_container_width=True): page = "Home"
    if st.button("🫀 Heart Disease", use_container_width=True): page = "Heart"
    if st.button("🫁 X-Ray Analysis", use_container_width=True): page = "Xray"
    if st.button("🔍 Symptom Checker", use_container_width=True): page = "Symptom"

    st.markdown('<hr style="border-color: #1a2e1a; margin: 10px;">', unsafe_allow_html=True)

    # Tools Section
    st.markdown('<div class="nav-header">🛠️ TOOLS</div>', unsafe_allow_header=True)
    if st.button("🤖 AI Chatbot", use_container_width=True): page = "Chat"
    if st.button("⚖️ BMI Calculator", use_container_width=True): page = "BMI"
    if st.button("📊 Risk Gauge", use_container_width=True): page = "Risk"

    st.markdown('<hr style="border-color: #1a2e1a; margin: 10px;">', unsafe_allow_html=True)

    # Records Section
    st.markdown('<div class="nav-header">📁 RECORDS</div>', unsafe_allow_html=True)
    if st.button("💡 Health Tips", use_container_width=True): page = "Tips"
    if st.button("📋 Medical History", use_container_width=True): page = "History"
    if st.button("📄 Patient Report", use_container_width=True): page = "Report"
