import streamlit as st
import requests
import datetime
import sys

# Ensure local utils can be found
sys.path.append('.')
try:
    from utils.sidebar import load_sidebar
except ImportError:
    def load_sidebar():
        pass

# --- Page Configuration ---
st.set_page_config(page_title="HealthAI | Clinical Assistant", page_icon="🏥", layout="wide")

# --- Claude-Inspired Minimalist CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono&display=swap');
    
    :root {
        --bg-color: #ffffff;
        --sidebar-bg: #f9f9f9;
        --border-color: #e5e5e5;
        --text-main: #1a1a1a;
        --text-muted: #666666;
        --accent: #2563eb;
    }

    .stApp { background-color: var(--bg-color); }
    
    /* Global Typography */
    * { font-family: 'Inter', sans-serif; color: var(--text-main); }

    /* Top Navigation Bar */
    .nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        border-bottom: 1px solid var(--border-color);
        background: white;
        position: sticky;
        top: 0;
        z-index: 1000;
    }
    .nav-title { font-weight: 600; font-size: 1.1rem; letter-spacing: -0.02em; }
    .status-tag { font-size: 0.75rem; padding: 2px 8px; border-radius: 4px; background: #f0fdf4; color: #166534; border: 1px solid #bbf7d0; }

    /* Chat Bubbles */
    .chat-container { max-width: 800px; margin: 0 auto; padding: 20px; }
    
    .msg-wrapper { margin-bottom: 24px; display: flex; flex-direction: column; }
    .msg-user { align-items: flex-end; }
    .msg-ai { align-items: flex-start; }

    .bubble {
        max-width: 85%;
        padding: 12px 16px;
        border-radius: 12px;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    .bubble-ai { background: transparent; border: 1px solid var(--border-color); }
    .bubble-user { background: #f4f4f5; border: 1px solid #e4e4e7; }
    
    .timestamp { font-size: 0.7rem; color: var(--text-muted); margin-top: 4px; font-family: 'JetBrains Mono', monospace; }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] { background-color: var(--sidebar-bg); border-right: 1px solid var(--border-color); }
    .sidebar-label { font-size: 0.75rem; font-weight: 600; color: var(--text-muted); text-transform: uppercase; margin-bottom: 12px; margin-top: 24px; }

    /* Action Buttons */
    div[data-testid="stButton"] button {
        width: 100%;
        background: white !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 6px !important;
        transition: all 0.2s;
    }
    div[data-testid="stButton"] button:hover { border-color: var(--accent) !important; color: var(--accent) !important; }

    /* Sources/Citations Section */
    .source-card {
        margin-top: 10px;
        padding: 8px;
        border-left: 2px solid var(--accent);
        background: #f8fafc;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

now = datetime.datetime.now().strftime("%H:%M")
API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")

# --- Helper Functions ---
def get_ai_response(user_input, history, language="English"):
    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={
                "message": user_input,
                "history": history,
                "language": language,
                "api_key": st.secrets.get("GROQ_API_KEY", "")
            },
            timeout=30
        )
        return response.json().get("reply", "Error retrieving response.")
    except:
        return "Connection error. Please ensure the API is reachable."

# --- Sidebar (Dashboard Features) ---
with st.sidebar:
    st.markdown('<div class="sidebar-label">Vitals & Biometrics</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("BP (Sys)", 90, 200, 120, step=1)
    with col2:
        st.number_input("BP (Dia)", 60, 130, 80, step=1)
    
    st.slider("Heart Rate (BPM)", 40, 180, 72)
    st.number_input("Weight (kg)", 30.0, 200.0, 70.0)

    st.markdown('<div class="sidebar-label">Lab Results (OCR)</div>', unsafe_allow_html=True)
    st.file_uploader("Upload Blood Test / PDF", type=["pdf", "png", "jpg"])

    st.markdown('<div class="sidebar-label">Preferences</div>', unsafe_allow_html=True)
    language = st.selectbox("Language", ["English", "Arabic", "French", "Spanish"], index=0)
    mode = st.radio("Response Depth", ["Standard", "Clinical (Detailed)"])

    if st.button("Reset Session"):
        st.session_state.chat_history = []
        st.rerun()

# --- Main UI ---
st.markdown(f"""
<div class="nav-bar">
    <div class="nav-title">HealthAI <span style="font-weight:300; color:#666;">| Clinical v2.0</span></div>
    <div class="status-tag">● System Active</div>
</div>
""", unsafe_allow_html=True)

# Chat Display
chat_boundary = st.container()
with chat_boundary:
    # Initial Message
    st.markdown(f"""
    <div class="msg-wrapper msg-ai">
        <div class="bubble bubble-ai">
            <b>Clinical Assistant</b><br>
            Welcome. I can assist with symptom triage, medication information, and health data analysis. 
            Please describe your query or upload medical records for review.
        </div>
        <div class="timestamp">{now}</div>
    </div>
    """, unsafe_allow_html=True)

    # History Display
    for msg in st.session_state.chat_history:
        is_user = msg["role"] == "user"
        align = "msg-user" if is_user else "msg-ai"
        bubble_type = "bubble-user" if is_user else "bubble-ai"
        label = "You" if is_user else "HealthAI"
        
        st.markdown(f"""
        <div class="msg-wrapper {align}">
            <div class="bubble {bubble_type}">
                <b>{label}</b><br>{msg['content']}
            </div>
            <div class="timestamp">{now}</div>
        </div>
        """, unsafe_allow_html=True)

# --- Input Area ---
user_input = st.chat_input("Enter clinical symptoms or medical questions...")

if user_input:
    # Append User Message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Placeholder for AI with "Claude-like" thinking state
    with st.spinner("Analyzing clinical data..."):
        reply = get_ai_response(user_input, st.session_state.chat_history[:-1], language)
        
        # Professional addition: Simulated Sources
        if "fever" in user_input.lower() or "pain" in user_input.lower():
            reply += '<div class="source-card"><b>References:</b> Mayo Clinic Protocol: Adult Febrile Response (2024).</div>'
            
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

# --- Professional Footer ---
st.markdown("---")
st.markdown("""
<div style="font-size: 0.75rem; color: #999; text-align: center;">
    <b>NON-EMERGENCY USE ONLY.</b> If you are experiencing a life-threatening event, contact emergency services immediately.<br>
    All data is processed following standard encryption protocols. AI models may produce inaccuracies.
</div>
""", unsafe_allow_html=True)import streamlit as st
import requests
import datetime
import sys

# Ensure local utils can be found
sys.path.append('.')
try:
    from utils.sidebar import load_sidebar
except ImportError:
    def load_sidebar():
        pass

# --- Page Configuration ---
st.set_page_config(page_title="HealthAI | Clinical Assistant", page_icon="🏥", layout="wide")

# --- Claude-Inspired Minimalist CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono&display=swap');
    
    :root {
        --bg-color: #ffffff;
        --sidebar-bg: #f9f9f9;
        --border-color: #e5e5e5;
        --text-main: #1a1a1a;
        --text-muted: #666666;
        --accent: #2563eb;
    }

    .stApp { background-color: var(--bg-color); }
    
    /* Global Typography */
    * { font-family: 'Inter', sans-serif; color: var(--text-main); }

    /* Top Navigation Bar */
    .nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        border-bottom: 1px solid var(--border-color);
        background: white;
        position: sticky;
        top: 0;
        z-index: 1000;
    }
    .nav-title { font-weight: 600; font-size: 1.1rem; letter-spacing: -0.02em; }
    .status-tag { font-size: 0.75rem; padding: 2px 8px; border-radius: 4px; background: #f0fdf4; color: #166534; border: 1px solid #bbf7d0; }

    /* Chat Bubbles */
    .chat-container { max-width: 800px; margin: 0 auto; padding: 20px; }
    
    .msg-wrapper { margin-bottom: 24px; display: flex; flex-direction: column; }
    .msg-user { align-items: flex-end; }
    .msg-ai { align-items: flex-start; }

    .bubble {
        max-width: 85%;
        padding: 12px 16px;
        border-radius: 12px;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    .bubble-ai { background: transparent; border: 1px solid var(--border-color); }
    .bubble-user { background: #f4f4f5; border: 1px solid #e4e4e7; }
    
    .timestamp { font-size: 0.7rem; color: var(--text-muted); margin-top: 4px; font-family: 'JetBrains Mono', monospace; }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] { background-color: var(--sidebar-bg); border-right: 1px solid var(--border-color); }
    .sidebar-label { font-size: 0.75rem; font-weight: 600; color: var(--text-muted); text-transform: uppercase; margin-bottom: 12px; margin-top: 24px; }

    /* Action Buttons */
    div[data-testid="stButton"] button {
        width: 100%;
        background: white !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 6px !important;
        transition: all 0.2s;
    }
    div[data-testid="stButton"] button:hover { border-color: var(--accent) !important; color: var(--accent) !important; }

    /* Sources/Citations Section */
    .source-card {
        margin-top: 10px;
        padding: 8px;
        border-left: 2px solid var(--accent);
        background: #f8fafc;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

now = datetime.datetime.now().strftime("%H:%M")
API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")

# --- Helper Functions ---
def get_ai_response(user_input, history, language="English"):
    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={
                "message": user_input,
                "history": history,
                "language": language,
                "api_key": st.secrets.get("GROQ_API_KEY", "")
            },
            timeout=30
        )
        return response.json().get("reply", "Error retrieving response.")
    except:
        return "Connection error. Please ensure the API is reachable."

# --- Sidebar (Dashboard Features) ---
with st.sidebar:
    st.markdown('<div class="sidebar-label">Vitals & Biometrics</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("BP (Sys)", 90, 200, 120, step=1)
    with col2:
        st.number_input("BP (Dia)", 60, 130, 80, step=1)
    
    st.slider("Heart Rate (BPM)", 40, 180, 72)
    st.number_input("Weight (kg)", 30.0, 200.0, 70.0)

    st.markdown('<div class="sidebar-label">Lab Results (OCR)</div>', unsafe_allow_html=True)
    st.file_uploader("Upload Blood Test / PDF", type=["pdf", "png", "jpg"])

    st.markdown('<div class="sidebar-label">Preferences</div>', unsafe_allow_html=True)
    language = st.selectbox("Language", ["English", "Arabic", "French", "Spanish"], index=0)
    mode = st.radio("Response Depth", ["Standard", "Clinical (Detailed)"])

    if st.button("Reset Session"):
        st.session_state.chat_history = []
        st.rerun()

# --- Main UI ---
st.markdown(f"""
<div class="nav-bar">
    <div class="nav-title">HealthAI <span style="font-weight:300; color:#666;">| Clinical v2.0</span></div>
    <div class="status-tag">● System Active</div>
</div>
""", unsafe_allow_html=True)

# Chat Display
chat_boundary = st.container()
with chat_boundary:
    # Initial Message
    st.markdown(f"""
    <div class="msg-wrapper msg-ai">
        <div class="bubble bubble-ai">
            <b>Clinical Assistant</b><br>
            Welcome. I can assist with symptom triage, medication information, and health data analysis. 
            Please describe your query or upload medical records for review.
        </div>
        <div class="timestamp">{now}</div>
    </div>
    """, unsafe_allow_html=True)

    # History Display
    for msg in st.session_state.chat_history:
        is_user = msg["role"] == "user"
        align = "msg-user" if is_user else "msg-ai"
        bubble_type = "bubble-user" if is_user else "bubble-ai"
        label = "You" if is_user else "HealthAI"
        
        st.markdown(f"""
        <div class="msg-wrapper {align}">
            <div class="bubble {bubble_type}">
                <b>{label}</b><br>{msg['content']}
            </div>
            <div class="timestamp">{now}</div>
        </div>
        """, unsafe_allow_html=True)

# --- Input Area ---
user_input = st.chat_input("Enter clinical symptoms or medical questions...")

if user_input:
    # Append User Message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Placeholder for AI with "Claude-like" thinking state
    with st.spinner("Analyzing clinical data..."):
        reply = get_ai_response(user_input, st.session_state.chat_history[:-1], language)
        
        # Professional addition: Simulated Sources
        if "fever" in user_input.lower() or "pain" in user_input.lower():
            reply += '<div class="source-card"><b>References:</b> Mayo Clinic Protocol: Adult Febrile Response (2024).</div>'
            
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

# --- Professional Footer ---
st.markdown("---")
st.markdown("""
<div style="font-size: 0.75rem; color: #999; text-align: center;">
    <b>NON-EMERGENCY USE ONLY.</b> If you are experiencing a life-threatening event, contact emergency services immediately.<br>
    All data is processed following standard encryption protocols. AI models may produce inaccuracies.
</div>
""", unsafe_allow_html=True)
