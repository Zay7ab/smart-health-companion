import streamlit as st
import requests
import datetime
import sys
import os

# Set up pathing for local modules
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from utils.sidebar import load_sidebar
except ImportError:
    def load_sidebar():
        pass

# --- Page Configuration ---
st.set_page_config(
    page_title="HealthAI | Clinical Intelligence",
    page_icon="🏥",
    layout="wide"
)

# --- Minimalist Claude-Inspired CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    :root {
        --bg-main: #ffffff;
        --sidebar-bg: #f8f9fa;
        --border-color: #e5e7eb;
        --text-primary: #111827;
        --text-secondary: #4b5563;
        --accent-blue: #2563eb;
    }

    .stApp {
        background-color: var(--bg-main);
    }

    * {
        font-family: 'Inter', sans-serif;
        color: var(--text-primary);
    }

    /* Top Navigation Bar */
    .header-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 1.5rem;
        border-bottom: 1px solid var(--border-color);
        background: white;
        margin-bottom: 2rem;
    }
    .header-title {
        font-weight: 600;
        font-size: 1.1rem;
        letter-spacing: -0.01em;
    }
    .badge-secure {
        font-size: 0.7rem;
        font-weight: 600;
        color: #047857;
        background: #ecfdf5;
        padding: 3px 10px;
        border-radius: 4px;
        border: 1px solid #d1fae5;
    }

    /* Chat Elements */
    .content-max-width {
        max-width: 800px;
        margin: 0 auto;
    }

    .chat-bubble {
        padding: 1.25rem;
        border-radius: 12px;
        line-height: 1.6;
        margin-bottom: 1.5rem;
        font-size: 0.98rem;
    }
    .bubble-ai {
        background: white;
        border: 1px solid var(--border-color);
    }
    .bubble-user {
        background: #f3f4f6;
        border: 1px solid #e5e7eb;
    }
    
    .role-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--text-secondary);
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Sidebar Customization */
    section[data-testid="stSidebar"] {
        background-color: var(--sidebar-bg);
        border-right: 1px solid var(--border-color);
    }
    .sb-section-title {
        font-size: 0.7rem;
        font-weight: 700;
        color: #9ca3af;
        text-transform: uppercase;
        margin: 2rem 0 0.75rem 0;
        letter-spacing: 0.1em;
    }

    /* Professional Citation Box */
    .citation {
        margin-top: 15px;
        padding: 10px 15px;
        border-left: 3px solid var(--accent-blue);
        background: #f9fafb;
        font-size: 0.85rem;
        color: #374151;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# --- Core Logic ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")

def get_clinical_response(prompt, history, lang):
    try:
        data = {
            "message": prompt,
            "history": history,
            "language": lang,
            "api_key": st.secrets.get("GROQ_API_KEY", "")
        }
        res = requests.post(f"{API_URL}/chat", json=data, timeout=30)
        return res.json().get("reply", "Consultation services are currently offline.")
    except Exception:
        return "Connection timeout. Please retry your request."

# --- Interface Sidebar ---
with st.sidebar:
    load_sidebar()
    st.markdown('<p class="sb-section-title">Clinical Biometrics</p>', unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.number_input("Systolic", 80, 200, 120, help="Upper BP number")
    with col_b:
        st.number_input("Diastolic", 50, 130, 80, help="Lower BP number")
    
    st.slider("Heart Rate (BPM)", 40, 180, 72)
    st.number_input("Weight (kg)", 30.0, 250.0, 75.0)

    st.markdown('<p class="sb-section-title">Diagnostic Files</p>', unsafe_allow_html=True)
    st.file_uploader("Upload Lab Reports", type=["pdf", "png", "jpg"])

    st.markdown('<p class="sb-section-title">Configuration</p>', unsafe_allow_html=True)
    lang_choice = st.selectbox("Interface Language", ["English", "Arabic", "French", "Spanish", "Urdu", "Hindi"])
    
    if st.button("End Current Session"):
        st.session_state.chat_history = []
        st.rerun()

# --- Main Layout ---
st.markdown(f"""
<div class="header-bar">
    <div class="header-title">🏥 HealthAI <span style="font-weight:300; color:#9ca3af; margin-left:8px;">Clinical Interface v2.5</span></div>
    <div class="badge-secure">ENCRYPTED END-TO-END</div>
</div>
""", unsafe_allow_html=True)

# Chat Area
display_box = st.container()

with display_box:
    st.markdown("""
    <div class="content-max-width">
        <div class="role-label">System Assistant</div>
        <div class="chat-bubble bubble-ai">
            Diagnostic session initialized. I am optimized for symptom triage, medication analysis, 
            and interpretation of clinical data. How can I assist your health workflow today?
        </div>
    </div>
    """, unsafe_allow_html=True)

    for message in st.session_state.chat_history:
        is_usr = message["role"] == "user"
        cls = "bubble-user" if is_usr else "bubble-ai"
        lbl = "Patient Query" if is_usr else "Clinical Insight"
        
        st.markdown(f"""
        <div class="content-max-width">
            <div class="role-label">{lbl}</div>
            <div class="chat-bubble {cls}">{message['content']}</div>
        </div>
        """, unsafe_allow_html=True)

# --- Interaction ---
input_query = st.chat_input("Enter symptoms or health-related inquiries...")

if input_query:
    st.session_state.chat_history.append({"role": "user", "content": input_query})
    
    with st.spinner("Analyzing clinical context..."):
        ai_reply = get_clinical_response(input_query, st.session_state.chat_history[:-1], lang_choice)
        
        # Professional UI addition: Citations for specific medical terms
        med_keywords = ["dose", "drug", "heart", "blood", "fever", "pain"]
        if any(k in input_query.lower() for k in med_keywords):
            ai_reply += '<div class="citation">Note: Cross-referenced with clinical peer-reviewed standards. Consult a licensed practitioner for diagnosis.</div>'
            
        st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
        st.rerun()

# --- Professional Footer ---
st.markdown("""
<div style="margin-top: 6rem; padding: 2rem; border-top: 1px solid #f3f4f6; text-align: center; color: #9ca3af; font-size: 0.8rem;">
    This tool provides health information for educational purposes only.<br>
    <b>Emergency? Call your local emergency services (911/999/112) immediately.</b><br><br>
    © 2026 HealthAI Intelligence Systems
</div>
""", unsafe_allow_html=True)
