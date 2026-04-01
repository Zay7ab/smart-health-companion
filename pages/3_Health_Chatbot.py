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

# --- Sidebar Loading (Copying your Navigation settings) ---
sys.path.append('.')
try:
    from utils.sidebar import load_sidebar
    load_sidebar()
except Exception:
    pass

# --- Heart Disease Page Style Integration ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp { 
    background: #0a0f0a !important; 
}

/* Header Bar */
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

/* AI Badge */
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

/* Chat Bubbles */
.chat-container {
    margin-bottom: 20px;
}
.bubble {
    padding: 1.25rem;
    border-radius: 14px;
    margin-bottom: 1rem;
    line-height: 1.7;
    font-size: 14px;
    max-width: 85%;
}
.bubble-ai {
    background: #0d120d;
    border: 1px solid #1a2e1a;
    border-left: 4px solid #4ade80;
    color: rgba(255,255,255,0.8);
}
.bubble-user {
    background: #0f1a0f;
    border: 1px solid #1a2e1a;
    margin-left: auto;
    border-right: 4px solid #58a6ff;
    color: #ffffff;
}
.role-meta {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
}

/* Input Area */
div[data-testid="stChatInput"] {
    background-color: #0d120d !important;
    border: 1px solid #1a2e1a !important;
}

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

# --- App Logic ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")

def get_response(msg, history):
    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={
                "message": msg,
                "history": history,
                "api_key": st.secrets.get("GROQ_API_KEY", "")
            },
            timeout=30
        )
        return response.json().get("reply", "System Calibrating...")
    except:
        return "⏱️ API timeout. Please check connectivity."

# --- UI Header ---
st.markdown(f"""
<div class="topbar">
    <div>
        <div class="topbar-title">🤖 AI Clinical Chatbot</div>
        <div class="topbar-sub">Powered by ClinIQ Intelligence Systems v2.5</div>
    </div>
    <div class="ai-badge"><span class="ai-dot"></span> FastAPI + Groq AI Active</div>
</div>
""", unsafe_allow_html=True)

# Chat Display
display_area = st.container()

with display_area:
    # Welcome Message
    st.markdown("""
    <div class="bubble bubble-ai">
        <div class="role-meta" style="color:#4ade80;">ClinIQ Assistant</div>
        Hello. I am optimized for clinical triage and medical data interpretation. 
        How can I assist your health query today?
    </div>
    """, unsafe_allow_html=True)

    for m in st.session_state.chat_history:
        is_user = m["role"] == "user"
        cls = "bubble-user" if is_user else "bubble-ai"
        lbl = "Patient" if is_user else "AI Insight"
        clr = "#58a6ff" if is_user else "#4ade80"
        
        st.markdown(f"""
        <div class="bubble {cls}">
            <div class="role-meta" style="color:{clr};">{lbl}</div>
            {m['content']}
        </div>
        """, unsafe_allow_html=True)

# --- Interaction ---
query = st.chat_input("Ask a clinical question...")

if query:
    st.session_state.chat_history.append({"role": "user", "content": query})
    with st.spinner("🤖 Processing..."):
        reply = get_response(query, st.session_state.chat_history[:-1])
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

st.markdown("""
<div class="disclaimer">
    ⚠️ <b>Note:</b> ClinIQ provides health information for context. Always consult a qualified medical professional for diagnosis.
</div>
""", unsafe_allow_html=True)
