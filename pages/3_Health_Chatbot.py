import streamlit as st
import requests
import datetime
import pdfplumber  # PDF reading ke liye
from fpdf import FPDF
from utils.sidebar import load_sidebar

# --- Page Configuration ---
st.set_page_config(
    page_title="ClinIQ | Clinical Intelligence",
    page_icon="🤖",
    layout="wide"
)

load_sidebar()

# --- Full Dark Neon CSS (Keeping your original style) ---
st.markdown("""
<style>
    /* ... (Aapka original CSS yahan rahega) ... */
    .stApp { background: #0a0f0a !important; }
    .bubble { padding: 1.25rem; border-radius: 14px; margin-bottom: 1rem; font-size: 14px; }
    .bubble-ai { background: #0d120d; border-left: 4px solid #4ade80; color: rgba(255,255,255,0.8); }
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "report_analysis" not in st.session_state:
    st.session_state.report_analysis = ""

API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")

# --- Function: Extract Text from PDF ---
def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# --- Tabs ---
tab_chat, tab_reports, tab_tools = st.tabs(["💬 Clinical Chat", "📄 Diagnostic Reports", "🛠️ Clinical Tools"])

with tab_reports:
    st.markdown("### 📄 Diagnostic Report Hub")
    
    uploaded_file = st.file_uploader("Upload Lab Reports (PDF)", type=["pdf"])

    if uploaded_file is not None:
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")
        
        if st.button("🔍 Run AI Document Analysis"):
            with st.spinner("🤖 Clinical AI is reading your report..."):
                # 1. PDF se text nikalo
                report_text = extract_text_from_pdf(uploaded_file)
                
                if report_text.strip():
                    # 2. AI ko context ke saath bhejo
                    analysis_prompt = f"Analyze this medical report and summarize findings, abnormal values, and recommendations: \n\n {report_text}"
                    
                    try:
                        res = requests.post(
                            f"{API_URL}/chat",
                            json={
                                "message": analysis_prompt,
                                "history": [],
                                "api_key": st.secrets.get("GROQ_API_KEY", "fallback_key"),
                            },
                            timeout=30
                        )
                        result = res.json().get("reply", "Analysis failed.")
                        st.session_state.report_analysis = result
                    except Exception as e:
                        st.error(f"Connection Error: {e}")
                else:
                    st.warning("PDF se text nahi mil saka. Shayad ye scanned image ho.")

    # Display Analysis Result
    if st.session_state.report_analysis:
        st.markdown("---")
        st.markdown("#### 🩺 AI Analysis Result:")
        st.info(st.session_state.report_analysis)

with tab_chat:
    # (Aapka baaki chat logic yahan rahega...)
    st.write("Chat interface ready.")
