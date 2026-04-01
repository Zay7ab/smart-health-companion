import streamlit as st
import requests
import datetime
import sys
sys.path.append('.')
from utils.sidebar import load_sidebar

st.set_page_config(page_title="AI Health Chatbot", page_icon="🤖", layout="wide")
load_sidebar()

API_URL = st.secrets.get("API_BASE_URL", "https://zay7ab-health-ai-api.hf.space")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; box-sizing: border-box; }
.stApp { background: #0a0f0a !important; }
.chat-topbar { background: #0d120d; border-radius: 16px; padding: 1rem 1.5rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 12px; border: 1px solid #1a2e1a; }
.chat-topbar-avatar { width: 44px; height: 44px; border-radius: 50%; background: linear-gradient(135deg,#166534,#4ade80); display: flex; align-items: center; justify-content: center; font-size: 1.3rem; flex-shrink: 0; }
.chat-topbar-name { font-size: 16px; font-weight: 700; color: #ffffff; }
.chat-topbar-status { font-size: 11px; color: #4ade80; display: flex; align-items: center; gap: 4px; margin-top: 2px; }
.online-dot { width: 6px; height: 6px; border-radius: 50%; background: #4ade80; display: inline-block; animation: blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }
.topbar-badge { background: rgba(74,222,128,0.1); color: #4ade80; font-size: 10px; font-weight: 600; padding: 4px 10px; border-radius: 20px; border: 1px solid rgba(74,222,128,0.2); margin-left: auto; }
.msg-ai { display: flex; align-items: flex-end; gap: 8px; margin-bottom: 14px; }
.msg-ai-ava { width: 32px; height: 32px; border-radius: 50%; background: linear-gradient(135deg,#166534,#4ade80); display: flex; align-items: center; justify-content: center; font-size: 13px; flex-shrink: 0; }
.msg-ai-bubble { background: #0d120d; border: 1px solid #1a2e1a; border-radius: 4px 16px 16px 16px; padding: 10px 14px; max-width: 75%; }
.msg-ai-text { font-size: 13px; color: rgba(255,255,255,0.85); line-height: 1.7; }
.msg-time { font-size: 10px; color: rgba(255,255,255,0.25); margin-top: 4px; }
.msg-user { display: flex; justify-content: flex-end; align-items: flex-end; gap: 8px; margin-bottom: 14px; }
.msg-user-ava { width: 32px; height: 32px; border-radius: 50%; background: rgba(74,222,128,0.15); display: flex; align-items: center; justify-content: center; font-size: 13px; flex-shrink: 0; }
.msg-user-bubble { background: linear-gradient(135deg,#166534,#15803d); border-radius: 16px 4px 16px 16px; padding: 10px 14px; max-width: 75%; }
.msg-user-text { font-size: 13px; color: white; line-height: 1.6; }
.msg-time-user { font-size: 10px; color: rgba(255,255,255,0.4); margin-top: 4px; text-align: right; }
.date-badge { text-align: center; margin-bottom: 12px; }
.date-badge span { background: #0f1a0f; color: rgba(255,255,255,0.3); font-size: 11px; padding: 3px 12px; border-radius: 20px; border: 1px solid #1a2e1a; }
.chat-box-header { background: #0d120d; border: 1px solid #1a2e1a; border-bottom: none; border-radius: 16px 16px 0 0; padding: 0.75rem 1.25rem; display: flex; align-items: center; justify-content: space-between; }
.chat-box-title { font-size: 13px; font-weight: 600; color: #ffffff; }
.chat-box-badge { font-size: 10px; color: #4ade80; background: rgba(74,222,128,0.1); padding: 2px 8px; border-radius: 20px; border: 1px solid rgba(74,222,128,0.2); }
.symptom-card-wrap { background: #0d120d; border: 1.5px solid #1a2e1a; border-radius: 12px; padding: 0.75rem 0.5rem; text-align: center; transition: all 0.15s; }
.symptom-card-wrap:hover { border-color: #4ade80; background: #0f1a0f; }
.symptom-icon { font-size: 1.5rem; }
.symptom-name { font-size: 11px; font-weight: 600; color: rgba(255,255,255,0.7); margin-top: 4px; }
.section-label { font-size: 11px; font-weight: 600; color: rgba(255,255,255,0.3); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; margin-top: 1rem; }
.cap-item { display: flex; align-items: center; gap: 8px; padding: 5px 0; border-bottom: 1px solid #0f1a0f; font-size: 12px; color: rgba(255,255,255,0.6); }
.cap-item:last-child { border-bottom: none; }
.cap-dot { width: 6px; height: 6px; border-radius: 50%; background: #4ade80; flex-shrink: 0; }
.disclaimer { background: rgba(255,200,0,0.05); border: 1px solid rgba(255,200,0,0.15); border-radius: 10px; padding: 0.75rem 1rem; font-size: 11px; color: rgba(255,200,0,0.7); margin-top: 1rem; }
div[data-testid="stButton"] button { background: rgba(74,222,128,0.1) !important; color: #4ade80 !important; border: 1px solid rgba(74,222,128,0.2) !important; border-radius: 20px !important; font-weight: 500 !important; font-size: 12px !important; padding: 0.4rem 1rem !important; }
div[data-testid="stButton"] button:hover { background: rgba(74,222,128,0.2) !important; border-color: #4ade80 !important; }
label { color: rgba(255,255,255,0.7) !important; }
p { color: rgba(255,255,255,0.5) !important; }
.stSelectbox > div > div { background: #0f1a0f !important; border-color: #1a2e1a !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

now = datetime.datetime.now().strftime("%I:%M %p")

def get_ai_response(user_input, history, language="English"):
    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={"message": user_input, "history": history, "language": language, "api_key": st.secrets.get("GROQ_API_KEY", "")},
            timeout=30
        )
        result = response.json()
        if "error" in result:
            return "Sorry, I encountered an error. Please try again."
        return result["reply"]
    except:
        return "Connection error. Please try again."

st.markdown(f"""
<div class="chat-topbar">
    <div class="chat-topbar-avatar">🤖</div>
    <div>
        <div class="chat-topbar-name">HealthAI Assistant</div>
        <div class="chat-topbar-status"><span class="online-dot"></span> Your Health Assistant · Online</div>
    </div>
    <div class="topbar-badge">FastAPI + LLaMA 3.3</div>
</div>
""", unsafe_allow_html=True)

col_main, col_side = st.columns([3, 1])

with col_side:
    st.markdown('<div class="section-label">💬 Quick Questions</div>', unsafe_allow_html=True)
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
    for icon, question in quick_questions:
        if st.button(f"{icon}  {question}", key=f"qq_{question}"):
            st.session_state.chat_history.append({"role": "user", "content": question})
            with st.spinner(""):
                reply = get_ai_response(question, st.session_state.chat_history[:-1])
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.rerun()

    st.markdown('<div class="section-label">✨ Capabilities</div>', unsafe_allow_html=True)
    for cap in ["Symptom analysis", "Drug information", "Mental health", "Nutrition advice", "Emergency guidance", "Lab results", "50+ languages"]:
        st.markdown(f'<div class="cap-item"><div class="cap-dot"></div>{cap}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">🏷️ Topics</div>', unsafe_allow_html=True)
    topics_html = ""
    for t in ["Heart Health", "Diabetes", "Blood Pressure", "Mental Health", "Nutrition", "Sleep", "Pregnancy", "Allergies"]:
        topics_html += f'<span style="display:inline-block;background:rgba(74,222,128,0.08);border:1px solid rgba(74,222,128,0.15);color:#4ade80;border-radius:20px;padding:3px 9px;font-size:11px;margin:2px;">{t}</span>'
    st.markdown(f'<div style="line-height:2.2;">{topics_html}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">🌐 Language</div>', unsafe_allow_html=True)
    language = st.selectbox("", ["English","Arabic","Urdu","Hindi","French","Spanish","German","Turkish","Persian","Malay"], label_visibility="collapsed")

with col_main:
    st.markdown("""
    <div class="chat-box-header">
        <span class="chat-box-title">💬 Conversation</span>
        <span class="chat-box-badge">FastAPI Powered</span>
    </div>
    """, unsafe_allow_html=True)

    chat_area = st.container(height=450, border=True)

    with chat_area:
        st.markdown('<div class="date-badge"><span>Today</span></div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="msg-ai">
            <div class="msg-ai-ava">🤖</div>
            <div class="msg-ai-bubble">
                <div class="msg-ai-text">Hi! I am <b style="color:#4ade80;">HealthAI Assistant</b>. I am here to help with health questions, symptom analysis, medication information and wellness advice.<br/><br/>How can I help you today?</div>
                <div class="msg-time">{now}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="msg-user">
                    <div class="msg-user-bubble">
                        <div class="msg-user-text">{message["content"]}</div>
                        <div class="msg-time-user">{now}</div>
                    </div>
                    <div class="msg-user-ava">👤</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="msg-ai">
                    <div class="msg-ai-ava">🤖</div>
                    <div class="msg-ai-bubble">
                        <div class="msg-ai-text">{message["content"]}</div>
                        <div class="msg-time">{now}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">🩺 Select Symptoms</div>', unsafe_allow_html=True)
    symptoms_list = [
        ("🌡️","Fever"), ("🤒","Headache"), ("💔","Chest Pain"),
        ("😮‍💨","Breathless"), ("🤢","Nausea"), ("😴","Fatigue"),
        ("🩸","Bleeding"), ("🦴","Joint Pain"), ("👁️","Blurred Vision"),
    ]
    selected_symptoms = []
    sym_cols = st.columns(9)
    for i, (icon, symptom) in enumerate(symptoms_list):
        with sym_cols[i]:
            st.markdown(f"""
            <div class="symptom-card-wrap">
                <div class="symptom-icon">{icon}</div>
                <div class="symptom-name">{symptom}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.checkbox("", key=f"sym_{symptom}", label_visibility="collapsed"):
                selected_symptoms.append(symptom)

    if selected_symptoms:
        st.markdown(f"""
        <div style="background:rgba(74,222,128,0.08);border:1px solid rgba(74,222,128,0.2);border-radius:10px;padding:0.6rem 1rem;margin-top:0.5rem;font-size:12px;color:#4ade80;">
            <b>Selected:</b> {', '.join(selected_symptoms)}
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔍 Analyze These Symptoms"):
            msg = f"I have these symptoms: {', '.join(selected_symptoms)}. What could be wrong?"
            st.session_state.chat_history.append({"role": "user", "content": msg})
            with st.spinner("HealthAI is analyzing..."):
                reply = get_ai_response(msg, st.session_state.chat_history[:-1])
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.rerun()

    user_input = st.chat_input("Type your health question here...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("HealthAI is thinking..."):
            reply = get_ai_response(user_input, st.session_state.chat_history[:-1], language)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

    if st.session_state.chat_history:
        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("🗑️ Clear Chat"):
                st.session_state.chat_history = []
                st.rerun()
        with b2:
            chat_text = "\n\n".join([f"{'You' if m['role']=='user' else 'HealthAI'}: {m['content']}" for m in st.session_state.chat_history])
            st.download_button("💾 Save Chat", data=chat_text, file_name="health_chat.txt", mime="text/plain")
        with b3:
            if st.button("🔄 New Session"):
                st.session_state.chat_history = []
                st.rerun()

st.markdown('<div class="disclaimer">⚠️ HealthAI provides general health information only. Always consult a qualified doctor. In emergencies call 999/911/112 immediately.</div>', unsafe_allow_html=True)
