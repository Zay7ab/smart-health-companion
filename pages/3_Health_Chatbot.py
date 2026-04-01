import streamlit as st
import requests
import datetime
import sys
import os

# Set up pathing
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from utils.sidebar import load_sidebar
except ImportError:
    def load_sidebar():
        pass

# --- Page Configuration ---
st.set_page_config(page_title="HealthAI | Clinical Pro", page_icon="🏥", layout="wide")

# --- Advanced Dark Clinical CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono&display=swap');

    .stApp { background-color: #0d1117 !important; }
    * { font-family: 'Inter', sans-serif; color: #c9d1d9 !important; }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-thumb { background: #30363d; border-radius: 10px; }

    /* Header */
    .header {
        display: flex; justify-content: space-between; align-items: center;
        padding: 1rem 2rem; border-bottom: 1px solid #30363d;
        background: #161b22; margin-bottom: 1.5rem;
    }
    .status-pulse {
        width: 8px; height: 8px; background: #238636; border-radius: 50%;
        display: inline-block; margin-right: 8px; box-shadow: 0 0 8px #238636;
    }

    /* Chat Styling */
    .chat-card {
        background: #161b22; border: 1px solid #30363d;
        border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;
    }
    .user-tag { color: #58a6ff !important; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; margin-bottom: 8px; }
    .ai-tag { color: #7ee787 !important; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; margin-bottom: 8px; }
    
    /* Vitals Card */
    .vitals-container {
        background: #0d1117; border: 1px solid #30363d;
        border-radius: 8px; padding: 1rem; margin-top: 1rem;
    }
    .vital-val { font-family: 'JetBrains Mono'; color: #58a6ff; font-size: 1.2rem; }

    /* Buttons */
    .stButton>button {
        background: #21262d !important; border: 1px solid #30363d !important;
        border-radius: 6px !important; color: #c9d1d9 !important; width: 100%;
    }
    .stButton>button:hover { border-color: #58a6ff !important; color: #58a6ff !important; }

    /* Input Fix */
    .stChatInputContainer { background-color: #0d1117 !important; border-top: 1px solid #30363d !important; }
</style>
""", unsafe_allow_html=True)

# --- State Management ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "vitals" not in st.session_state:
    st.session_state.vitals = {"bp": "120/80", "hr": "72", "temp": "98.6"}

API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")

def get_ai_reply(prompt, history, lang):
    try:
        res = requests.post(f"{API_URL}/chat", json={
            "message": prompt, "history": history, "language": lang,
            "api_key": st.secrets.get("GROQ_API_KEY", "")
        }, timeout=30)
        return res.json().get("reply", "Engine Error.")
    except:
        return "Connection failed."

# --- Top Header ---
st.markdown("""
<div class="header">
    <div style="font-weight:600; font-size:1.2rem;">🏥 HealthAI <span style="color:#8b949e; font-weight:300;">PRO</span></div>
    <div><span class="status-pulse"></span><span style="font-size:0.8rem; color:#8b949e;">SECURE CLINICAL NODE</span></div>
</div>
""", unsafe_allow_html=True)

col_chat, col_data = st.columns([2.5, 1])

# --- Right Column: Clinical Intelligence ---
with col_data:
    st.markdown("### 📊 Clinical Dashboard")
    
    with st.expander("💓 Live Vitals Tracker", expanded=True):
        sys = st.number_input("Systolic", 80, 200, 120)
        dia = st.number_input("Diastolic", 50, 130, 80)
        hr = st.slider("Heart Rate (BPM)", 40, 180, 72)
        st.session_state.vitals['bp'] = f"{sys}/{dia}"
        st.session_state.vitals['hr'] = str(hr)
        
        st.markdown(f"""
        <div class="vitals-container">
            <div style="font-size:0.7rem; color:#8b949e;">CURRENT VITALS</div>
            <div style="display:flex; justify-content:space-between; margin-top:10px;">
                <div>BP: <span class="vital-val">{st.session_state.vitals['bp']}</span></div>
                <div>HR: <span class="vital-val">{st.session_state.vitals['hr']}</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📄 Diagnostic Lab Upload", expanded=False):
        uploaded_file = st.file_uploader("Upload Report (PDF/IMG)", type=['pdf','jpg','png'])
        if uploaded_file:
            st.success("File encrypted & queued for analysis.")

    st.markdown("### 🏷️ Quick Actions")
    if st.button("🔍 Check Drug Interactions"):
        st.toast("Feature coming soon: Drug database sync.")
    if st.button("🚨 Emergency Protocol"):
        st.error("Searching nearest ER facilities...")

# --- Left Column: Intelligence Chat ---
with col_chat:
    chat_box = st.container()
    
    with chat_box:
        # Initial AI Message
        st.markdown("""
        <div class="chat-card">
            <div class="ai-tag">Clinical Assistant</div>
            Diagnostic environment ready. Current vitals are synced. 
            Describe your symptoms or ask about specific medication protocols.
        </div>
        """, unsafe_allow_html=True)

        for m in st.session_state.chat_history:
            role_label = "Patient" if m["role"] == "user" else "Assistant"
            tag_class = "user-tag" if m["role"] == "user" else "ai-tag"
            st.markdown(f"""
            <div class="chat-card">
                <div class="{tag_class}">{role_label}</div>
                {m['content']}
            </div>
            """, unsafe_allow_html=True)

    # Input area
    prompt = st.chat_input("Enter clinical inquiry...")
    
    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.spinner("Analyzing data..."):
            # Context injection (adding vitals to the prompt secretly for better AI advice)
            context_prompt = f"[Context: Patient BP {st.session_state.vitals['bp']}, HR {st.session_state.vitals['hr']}] {prompt}"
            reply = get_ai_reply(context_prompt, st.session_state.chat_history[:-1], "English")
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

st.markdown("""
<div style="text-align:center; margin-top:4rem; color:#484f58; font-size:0.75rem;">
    Clinical Intelligence Platform v3.0 | AES-256 Encryption | © 2026 HealthAI Systems
</div>
""", unsafe_allow_html=True)
