import streamlit as st
import requests
import sys
sys.path.append('.')
from utils.sidebar import load_sidebar

st.set_page_config(page_title="AI Health Chatbot", page_icon="🤖", layout="wide")
load_sidebar()

API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; box-sizing: border-box; margin: 0; padding: 0; }
.stApp { background: #f0f4f0 !important; }

.chat-app { max-width: 900px; margin: 0 auto; background: white; border-radius: 24px; border: 1px solid #e0ece0; overflow: hidden; box-shadow: 0 4px 24px rgba(0,0,0,0.06); }

.chat-topbar { background: white; padding: 1rem 1.5rem; border-bottom: 1px solid #f0f4f0; display: flex; align-items: center; gap: 12px; }
.chat-topbar-avatar { width: 42px; height: 42px; border-radius: 50%; background: linear-gradient(135deg,#2d5a1a,#639922); display: flex; align-items: center; justify-content: center; font-size: 1.2rem; flex-shrink: 0; }
.chat-topbar-info { flex: 1; }
.chat-topbar-name { font-size: 16px; font-weight: 700; color: #1a3a1a; }
.chat-topbar-status { font-size: 11px; color: #639922; display: flex; align-items: center; gap: 4px; }
.online-dot { width: 6px; height: 6px; border-radius: 50%; background: #639922; display: inline-block; animation: blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }
.chat-topbar-badge { background: #eaf3de; color: #27500a; font-size: 10px; font-weight: 600; padding: 4px 10px; border-radius: 20px; border: 1px solid #d4edbe; }

.chat-date-badge { text-align: center; margin: 1rem 0; }
.chat-date-badge span { background: #f0f4f0; color: #7a8f7a; font-size: 11px; padding: 4px 12px; border-radius: 20px; }

.chat-messages { padding: 1rem 1.5rem; min-height: 400px; max-height: 480px; overflow-y: auto; background: #fafcfa; }

.msg-row-ai { display: flex; align-items: flex-end; gap: 8px; margin-bottom: 16px; }
.msg-ai-avatar { width: 34px; height: 34px; border-radius: 50%; background: linear-gradient(135deg,#2d5a1a,#639922); display: flex; align-items: center; justify-content: center; font-size: 14px; flex-shrink: 0; }
.msg-bubble-ai { background: white; border: 1px solid #e8f0e8; border-radius: 4px 18px 18px 18px; padding: 10px 14px; max-width: 70%; box-shadow: 0 1px 4px rgba(0,0,0,0.04); }
.msg-text-ai { font-size: 13px; color: #1a3a1a; line-height: 1.7; }
.msg-time-ai { font-size: 10px; color: #aab8aa; margin-top: 4px; }

.msg-row-user { display: flex; justify-content: flex-end; align-items: flex-end; gap: 8px; margin-bottom: 16px; }
.msg-user-avatar { width: 34px; height: 34px; border-radius: 50%; background: #d4edbe; display: flex; align-items: center; justify-content: center; font-size: 14px; flex-shrink: 0; }
.msg-bubble-user { background: linear-gradient(135deg,#2d5a1a,#4a8520); border-radius: 18px 4px 18px 18px; padding: 10px 14px; max-width: 70%; }
.msg-text-user { font-size: 13px; color: white; line-height: 1.6; }
.msg-time-user { font-size: 10px; color: rgba(255,255,255,0.6); margin-top: 4px; text-align: right; }

.chat-input-bar { background: white; border-top: 1px solid #f0f4f0; padding: 1rem 1.5rem; display: flex; align-items: center; gap: 10px; }

.symptom-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 10px; padding: 1rem 1.5rem; background: #fafcfa; border-top: 1px solid #f0f4f0; }
.symptom-card { background: white; border: 2px solid #e0ece0; border-radius: 14px; padding: 1rem; text-align: center; cursor: pointer; transition: all 0.2s; }
.symptom-card:hover { border-color: #639922; background: #f5f9f0; }
.symptom-card.selected { border-color: #639922; background: #eaf3de; }
.symptom-icon { font-size: 1.8rem; margin-bottom: 6px; }
.symptom-name { font-size: 12px; font-weight: 600; color: #1a3a1a; }

.quick-pills { display: flex; flex-wrap: wrap; gap: 8px; padding: 1rem 1.5rem; background: white; border-top: 1px solid #f0f4f0; }
.quick-pill { background: #f5f9f0; border: 1px solid #d4edbe; color: #27500a; border-radius: 20px; padding: 6px 14px; font-size: 12px; font-weight: 500; cursor: pointer; transition: all 0.15s; white-space: nowrap; }
.quick-pill:hover { background: #eaf3de; border-color: #97c459; }

.lang-bar { background: white; border-top: 1px solid #f0f4f0; padding: 0.75rem 1.5rem; display: flex; align-items: center; gap: 10px; }
.lang-label { font-size: 12px; color: #7a8f7a; font-weight: 500; white-space: nowrap; }

.action-bar { background: white; border-top: 1px solid #f0f4f0; padding: 0.75rem 1.5rem; display: flex; gap: 8px; }

.disclaimer { background: #fff8e1; border: 1px solid #f0c040; border-radius: 10px; padding: 0.75rem 1rem; font-size: 11px; color: #7a6000; margin-top: 1rem; }

div[data-testid="stButton"] button { background: linear-gradient(135deg,#3b6d11,#639922) !important; color: white !important; border: none !important; border-radius: 20px !important; font-weight: 600 !important; font-size: 12px !important; padding: 0.4rem 1rem !important; }
div[data-testid="stButton"] button:hover { background: linear-gradient(135deg,#27500a,#3b6d11) !important; }
label { color: #1a3a1a !important; }
p { color: #1a3a1a !important; }
</style>
""", unsafe_allow_html=True)

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

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
        result = response.json()
        if "error" in result:
            return "Sorry, I encountered an error. Please try again."
        return result["reply"]
    except:
        return "Connection error. Please try again."

import datetime
now = datetime.datetime.now().strftime("%I:%M %p")

# Main chat app
st.markdown("""
<div class="chat-app">
    <div class="chat-topbar">
        <div class="chat-topbar-avatar">🤖</div>
        <div class="chat-topbar-info">
            <div class="chat-topbar-name">HealthAI Assistant</div>
            <div class="chat-topbar-status">
                <span class="online-dot"></span>
                Your Health Assistant · Online
            </div>
        </div>
        <div class="chat-topbar-badge">FastAPI + LLaMA 3.3</div>
    </div>
""", unsafe_allow_html=True)

# Messages area
st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
st.markdown("""
<div class="chat-date-badge"><span>Today</span></div>
""", unsafe_allow_html=True)

if not st.session_state.chat_history:
    st.markdown(f"""
    <div class="msg-row-ai">
        <div class="msg-ai-avatar">🤖</div>
        <div class="msg-bubble-ai">
            <div class="msg-text-ai">Hi! I am HealthAI Assistant. I am here to help you with health questions, symptom analysis, medication information and wellness advice.<br/><br/>How can I help you today?</div>
            <div class="msg-time-ai">{now}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="msg-row-ai">
        <div class="msg-ai-avatar">🤖</div>
        <div class="msg-bubble-ai">
            <div class="msg-text-ai">Hi! I am HealthAI Assistant. How can I help you today?</div>
            <div class="msg-time-ai">{now}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="msg-row-user">
                <div class="msg-bubble-user">
                    <div class="msg-text-user">{message["content"]}</div>
                    <div class="msg-time-user">{now}</div>
                </div>
                <div class="msg-user-avatar">👤</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-row-ai">
                <div class="msg-ai-avatar">🤖</div>
                <div class="msg-bubble-ai">
                    <div class="msg-text-ai">{message["content"]}</div>
                    <div class="msg-time-ai">{now}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Quick symptom pills
st.markdown("""
<div class="quick-pills">
    <span style="font-size:11px;font-weight:600;color:#7a8f7a;align-self:center;">Quick questions:</span>
</div>
""", unsafe_allow_html=True)

# Quick questions as pills
quick_questions = [
    ("🫀", "Signs of heart attack?"),
    ("🩸", "Blood sugar control"),
    ("🧠", "Anxiety relief tips"),
    ("💊", "Drug interactions"),
    ("🤒", "Fever and body aches"),
    ("😴", "Better sleep tips"),
    ("🏃", "Exercise for beginners"),
    ("🥗", "Anti-inflammatory foods"),
]

cols = st.columns(4)
for i, (icon, question) in enumerate(quick_questions):
    with cols[i % 4]:
        if st.button(f"{icon} {question}", key=f"pill_{i}"):
            st.session_state.chat_history.append({"role": "user", "content": question})
            with st.spinner(""):
                reply = get_ai_response(question, st.session_state.chat_history[:-1])
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.rerun()

# Symptom selector
st.markdown("""
<div style="padding: 0.5rem 0; border-top: 1px solid #f0f4f0; margin-top: 0.5rem;">
    <div style="font-size:11px;font-weight:600;color:#7a8f7a;margin-bottom:8px;">🩺 Select Symptoms:</div>
</div>
""", unsafe_allow_html=True)

symptoms_list = [
    ("🌡️", "Fever"), ("🤒", "Headache"), ("💔", "Chest Pain"),
    ("😮‍💨", "Breathlessness"), ("🤢", "Nausea"), ("😴", "Fatigue"),
    ("🩸", "Bleeding"), ("🦴", "Joint Pain"), ("👁️", "Blurred Vision"),
]

selected_symptoms = []
sym_cols = st.columns(3)
for i, (icon, symptom) in enumerate(symptoms_list):
    with sym_cols[i % 3]:
        if st.checkbox(f"{icon} {symptom}", key=f"sym_{symptom}"):
            selected_symptoms.append(symptom)

if selected_symptoms:
    st.markdown(f"""
    <div style="background:#eaf3de;border:1px solid #97c459;border-radius:10px;padding:0.6rem 1rem;margin:0.5rem 0;font-size:12px;color:#27500a;">
        <b>Selected:</b> {', '.join(selected_symptoms)}
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔍 Analyze Selected Symptoms"):
        msg = f"I have these symptoms: {', '.join(selected_symptoms)}. What could be wrong?"
        st.session_state.chat_history.append({"role": "user", "content": msg})
        with st.spinner("HealthAI is analyzing..."):
            reply = get_ai_response(msg, st.session_state.chat_history[:-1])
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Language + input
col_lang, col_input = st.columns([1, 3])
with col_lang:
    language = st.selectbox("🌐 Language", [
        "English", "Arabic", "Urdu", "Hindi", "French",
        "Spanish", "German", "Turkish", "Persian", "Malay"
    ], label_visibility="visible")

with col_input:
    user_input = st.chat_input("Type your health question here...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.spinner("HealthAI is thinking..."):
        reply = get_ai_response(user_input, st.session_state.chat_history[:-1], language)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

# Action buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
with col2:
    if st.session_state.chat_history:
        chat_text = "\n\n".join([
            f"{'You' if m['role']=='user' else 'HealthAI'}: {m['content']}"
            for m in st.session_state.chat_history
        ])
        st.download_button("💾 Save Chat", data=chat_text, file_name="health_chat.txt", mime="text/plain")
with col3:
    if st.button("🔄 New Session"):
        st.session_state.chat_history = []
        st.rerun()

st.markdown('<div class="disclaimer">⚠️ HealthAI provides general health information only. Always consult a qualified doctor. In emergencies call 999/911/112 immediately.</div>', unsafe_allow_html=True)
