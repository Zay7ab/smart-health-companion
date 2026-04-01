import streamlit as st
import requests
import datetime
import sys
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="ClinIQ | AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar Logic (Copied from your provided code) ---
# Note: Ensure 'utils/sidebar.py' exists in your project
sys.path.append('.')
try:
    from utils.sidebar import load_sidebar
    load_sidebar()
except ImportError:
    def load_sidebar():
        st.sidebar.warning("Sidebar utility not found.")

# --- Dark Neon Styling (Merged from your Heart Disease page) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* Global Background */
.stApp { 
    background: #0a0f0a !important; 
}

* { 
    font-family: 'Inter', sans-serif; 
}

/* Custom Header Bar */
.topbar { 
    background: #0d120d; 
    border: 1px solid #1a2e1a; 
    border-radius: 16px; 
    padding: 1.25rem 1.5rem; 
    margin-bottom: 1.25rem; 
    display: flex; 
    align-items: center; 
    justify-content: space-between; 
}
.topbar-title { font-size: 20px; font-weight: 700; color: #ffffff; }
.topbar-sub { font-size: 12px; color: rgba(255,255,255,0.4); margin-top: 2px; }

/* AI Badge Styling */
.ai-badge { 
    display: inline-flex; 
    align-items: center; 
    gap: 6px; 
    background: rgba(74,222,128,0.1); 
    border: 1px solid rgba(74,222,128,0.2); 
    border-radius: 20px; 
    padding: 5px 12px; 
    font-size: 11px; 
    color: #4ade80; 
    font-weight: 600; 
}
.ai-dot { 
    width: 6px; height: 6px; border-radius: 50%; 
    background: #4ade80; display: inline-block; 
    animation: blink 2s infinite; 
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* Chat Bubbles Styling */
.bubble {
    padding: 1.2rem;
    border-radius: 14px;
    margin-bottom: 1rem;
    line-height: 1.6;
    font-size: 0.95rem;
    max-width: 85%;
}
.bubble-ai {
    background: #0d120d;
    border: 1px solid #1a2e1a;
    border-left: 3px solid #4ade80;
    color: rgba(255,255,255,0.9);
}
.bubble-user {
    background: #0f1a0f;
    border: 1px solid #1a2e1a;
    margin-left: auto;
    border-right: 3px solid #58a6ff;
    color: #ffffff;
}
.role-label {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 6px;
    letter-spacing: 0.5px;
}

/* Chat Input Styling */
div[data-testid="stChatInput"] {
    background-color: #0d120d !important;
    border: 1px solid #1a2e1a !important;
    border-radius: 12px !important;
}

/* Disclaimer Styling */
.disclaimer { 
    background: rgba(255,200,0,0.05); 
    border: 1px solid rgba(255,200,0,0.15); 
    border-radius: 10px; 
    padding: 0.75rem 1rem; 
    font-size: 11px; 
    color: rgba(255,200,0,0.7); 
    margin-top: 1rem; 
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# --- App Logic & API ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")
now = datetime.datetime.now().strftime("%H:%M")

def get_clinical_response(msg, history):
    try:
        payload = {
            "message": msg,
            "history": history,
            "api_key": st.secrets.get("GROQ_API_KEY", "")
        }
        res = requests.post(f"{API_URL}/chat", json=payload, timeout=25)
        return res.json().get("reply", "Clinical AI is currently processing other data.")
    except Exception:
        return "⏱️ API timeout or connection error. Please try again."

# --- Main UI ---

# Custom Topbar from your Heart Disease page
st.markdown(f"""
<div class="topbar">
    <div>
        <div class="topbar-title">🤖 AI Clinical Chatbot</div>
        <div class="topbar-sub">Powered by Llama 3.3 via Groq Systems</div>
    </div>
    <div class="ai-badge"><span class="ai-dot"></span> FastAPI + Groq AI Active</div>
</div>
""", unsafe_allow_html=True)

# Chat Area Container
chat_box = st.container()

with chat_box:
    # Initial Assistant Greeting
    st.markdown(f"""
    <div class="bubble bubble-ai">
        <div class="role-label" style="color:#4ade80;">ClinIQ Assistant</div>
        Welcome. I am optimized for clinical analysis and medical inquiries. 
        How can I assist your health workflow today?
    </div>
    """, unsafe_allow_html=True)

    # Render History
    for msg in st.session_state.chat_history:
        is_user = msg["role"] == "user"
        cls = "bubble-user" if is_user else "bubble-ai"
        lbl = "Patient Query" if is_user else "AI Insight"
        color = "#58a6ff" if is_user else "#4ade80"
        
        st.markdown(f"""
        <div class="bubble {cls}">
            <div class="role-label" style="color:{color};">{lbl}</div>
            {msg['content']}
        </div>
        """, unsafe_allow_html=True)

# --- Interaction Area ---
user_query = st.chat_input("Enter clinical symptoms or medical data...")

if user_query:
    # Save User Message
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    
    with st.spinner("🤖 Analyzing clinical context..."):
        # Get Response
        reply = get_clinical_response(user_query, st.session_state.chat_history[:-1])
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

# Disclaimer (Styled like your provided code)
st.markdown("""
<div class="disclaimer">
    ⚠️ <b>Educational Purposes Only:</b> ClinIQ provides health information for context. 
    Always consult a qualified medical professional for diagnosis.
</div>
""", unsafe_allow_html=True)import streamlit as st
import requests
import datetime
import sys
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="ClinIQ | AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar Logic (Copied from your provided code) ---
# Note: Ensure 'utils/sidebar.py' exists in your project
sys.path.append('.')
try:
    from utils.sidebar import load_sidebar
    load_sidebar()
except ImportError:
    def load_sidebar():
        st.sidebar.warning("Sidebar utility not found.")

# --- Dark Neon Styling (Merged from your Heart Disease page) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* Global Background */
.stApp { 
    background: #0a0f0a !important; 
}

* { 
    font-family: 'Inter', sans-serif; 
}

/* Custom Header Bar */
.topbar { 
    background: #0d120d; 
    border: 1px solid #1a2e1a; 
    border-radius: 16px; 
    padding: 1.25rem 1.5rem; 
    margin-bottom: 1.25rem; 
    display: flex; 
    align-items: center; 
    justify-content: space-between; 
}
.topbar-title { font-size: 20px; font-weight: 700; color: #ffffff; }
.topbar-sub { font-size: 12px; color: rgba(255,255,255,0.4); margin-top: 2px; }

/* AI Badge Styling */
.ai-badge { 
    display: inline-flex; 
    align-items: center; 
    gap: 6px; 
    background: rgba(74,222,128,0.1); 
    border: 1px solid rgba(74,222,128,0.2); 
    border-radius: 20px; 
    padding: 5px 12px; 
    font-size: 11px; 
    color: #4ade80; 
    font-weight: 600; 
}
.ai-dot { 
    width: 6px; height: 6px; border-radius: 50%; 
    background: #4ade80; display: inline-block; 
    animation: blink 2s infinite; 
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* Chat Bubbles Styling */
.bubble {
    padding: 1.2rem;
    border-radius: 14px;
    margin-bottom: 1rem;
    line-height: 1.6;
    font-size: 0.95rem;
    max-width: 85%;
}
.bubble-ai {
    background: #0d120d;
    border: 1px solid #1a2e1a;
    border-left: 3px solid #4ade80;
    color: rgba(255,255,255,0.9);
}
.bubble-user {
    background: #0f1a0f;
    border: 1px solid #1a2e1a;
    margin-left: auto;
    border-right: 3px solid #58a6ff;
    color: #ffffff;
}
.role-label {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 6px;
    letter-spacing: 0.5px;
}

/* Chat Input Styling */
div[data-testid="stChatInput"] {
    background-color: #0d120d !important;
    border: 1px solid #1a2e1a !important;
    border-radius: 12px !important;
}

/* Disclaimer Styling */
.disclaimer { 
    background: rgba(255,200,0,0.05); 
    border: 1px solid rgba(255,200,0,0.15); 
    border-radius: 10px; 
    padding: 0.75rem 1rem; 
    font-size: 11px; 
    color: rgba(255,200,0,0.7); 
    margin-top: 1rem; 
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# --- App Logic & API ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")
now = datetime.datetime.now().strftime("%H:%M")

def get_clinical_response(msg, history):
    try:
        payload = {
            "message": msg,
            "history": history,
            "api_key": st.secrets.get("GROQ_API_KEY", "")
        }
        res = requests.post(f"{API_URL}/chat", json=payload, timeout=25)
        return res.json().get("reply", "Clinical AI is currently processing other data.")
    except Exception:
        return "⏱️ API timeout or connection error. Please try again."

# --- Main UI ---

# Custom Topbar from your Heart Disease page
st.markdown(f"""
<div class="topbar">
    <div>
        <div class="topbar-title">🤖 AI Clinical Chatbot</div>
        <div class="topbar-sub">Powered by Llama 3.3 via Groq Systems</div>
    </div>
    <div class="ai-badge"><span class="ai-dot"></span> FastAPI + Groq AI Active</div>
</div>
""", unsafe_allow_html=True)

# Chat Area Container
chat_box = st.container()

with chat_box:
    # Initial Assistant Greeting
    st.markdown(f"""
    <div class="bubble bubble-ai">
        <div class="role-label" style="color:#4ade80;">ClinIQ Assistant</div>
        Welcome. I am optimized for clinical analysis and medical inquiries. 
        How can I assist your health workflow today?
    </div>
    """, unsafe_allow_html=True)

    # Render History
    for msg in st.session_state.chat_history:
        is_user = msg["role"] == "user"
        cls = "bubble-user" if is_user else "bubble-ai"
        lbl = "Patient Query" if is_user else "AI Insight"
        color = "#58a6ff" if is_user else "#4ade80"
        
        st.markdown(f"""
        <div class="bubble {cls}">
            <div class="role-label" style="color:{color};">{lbl}</div>
            {msg['content']}
        </div>
        """, unsafe_allow_html=True)

# --- Interaction Area ---
user_query = st.chat_input("Enter clinical symptoms or medical data...")

if user_query:
    # Save User Message
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    
    with st.spinner("🤖 Analyzing clinical context..."):
        # Get Response
        reply = get_clinical_response(user_query, st.session_state.chat_history[:-1])
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

# Disclaimer (Styled like your provided code)
st.markdown("""
<div class="disclaimer">
    ⚠️ <b>Educational Purposes Only:</b> ClinIQ provides health information for context. 
    Always consult a qualified medical professional for diagnosis.
</div>
""", unsafe_allow_html=True)
