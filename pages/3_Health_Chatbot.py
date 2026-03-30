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
* { font-family: 'Inter', sans-serif; box-sizing: border-box; }
.stApp { background: #f0f4f0 !important; }

.chat-header { background: linear-gradient(135deg, #1a3a1a 0%, #2d5a1a 50%, #3b6d11 100%); border-radius: 20px; padding: 1.5rem 2rem; margin-bottom: 1.25rem; }
.chat-header-inner { display: flex; align-items: center; justify-content: space-between; }
.chat-avatar-wrap { display: flex; align-items: center; gap: 16px; }
.chat-avatar { width: 52px; height: 52px; border-radius: 14px; background: rgba(255,255,255,0.15); border: 2px solid rgba(255,255,255,0.25); display: flex; align-items: center; justify-content: center; font-size: 1.6rem; }
.chat-title { font-size: 18px; font-weight: 700; color: white; }
.chat-subtitle { font-size: 12px; color: rgba(255,255,255,0.65); margin-top: 2px; }
.status-pill { display: inline-flex; align-items: center; gap: 6px; background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.2); border-radius: 20px; padding: 6px 14px; font-size: 11px; color: #97c459; font-weight: 600; }
.status-dot { width: 7px; height: 7px; border-radius: 50%; background: #97c459; display: inline-block; animation: blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

.stats-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 10px; margin-bottom: 1.25rem; }
.stat-box { background: white; border: 1px solid #e0ece0; border-radius: 12px; padding: 0.875rem; text-align: center; position: relative; overflow: hidden; }
.stat-box::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; background: linear-gradient(90deg,#639922,#97c459); }
.stat-box-label { font-size: 10px; color: #7a8f7a; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500; }
.stat-box-value { font-size: 18px; font-weight: 700; color: #1a3a1a; margin: 4px 0 2px; }
.stat-box-sub { font-size: 10px; color: #639922; font-weight: 500; }

.chat-layout { display: grid; grid-template-columns: 1fr 260px; gap: 1rem; align-items: start; }

.chat-window { background: white; border: 1px solid #e0ece0; border-radius: 16px; overflow: hidden; }
.chat-win-header { background: #f8faf8; border-bottom: 1px solid #e0ece0; padding: 0.875rem 1.25rem; display: flex; align-items: center; justify-content: space-between; }
.chat-win-title { font-size: 13px; font-weight: 600; color: #1a3a1a; }
.chat-win-badge { font-size: 10px; color: #639922; background: #eaf3de; padding: 2px 8px; border-radius: 20px; font-weight: 600; }
.chat-body { padding: 1.25rem; min-height: 360px; }

.empty-state { text-align: center; padding: 2.5rem 1rem; }
.empty-icon { font-size: 2.5rem; margin-bottom: 0.75rem; }
.empty-title { font-size: 15px; font-weight: 600; color: #1a3a1a; margin-bottom: 6px; }
.empty-sub { font-size: 12px; color: #7a8f7a; line-height: 1.6; }

.msg-row-user { display: flex; justify-content: flex-end; margin-bottom: 14px; }
.msg-bubble-user { background: linear-gradient(135deg,#2d5a1a,#4a8520); border-radius: 16px 16px 4px 16px; padding: 10px 14px; max-width: 72%; }
.msg-sender-user { font-size: 10px; color: rgba(255,255,255,0.65); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; text-align: right; }
.msg-text-user { font-size: 13px; color: white; line-height: 1.6; }

.msg-row-ai { display: flex; gap: 10px; margin-bottom: 14px; align-items: flex-start; }
.msg-ai-icon { width: 30px; height: 30px; border-radius: 8px; background: #eaf3de; display: flex; align-items: center; justify-content: center; font-size: 15px; flex-shrink: 0; margin-top: 2px; }
.msg-bubble-ai { background: #f5f7f5; border: 1px solid #e4ece4; border-radius: 4px 16px 16px 16px; padding: 10px 14px; max-width: 80%; }
.msg-sender-ai { font-size: 10px; color: #639922; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
.msg-text-ai { font-size: 13px; color: #1a3a1a; line-height: 1.7; }

.side-panel { display: flex; flex-direction: column; gap: 12px; }
.panel-card { background: white; border: 1px solid #e0ece0; border-radius: 14px; overflow: hidden; }
.panel-card-header { background: #f8faf8; border-bottom: 1px solid #e0ece0; padding: 0.75rem 1rem; font-size: 11px; font-weight: 600; color: #1a3a1a; text-transform: uppercase; letter-spacing: 0.5px; }
.panel-card-body { padding: 0.75rem; }

.topic-tag { display: inline-block; background: #f0f4f0; border: 1px solid #d4edbe; color: #3b6d11; border-radius: 20px; padding: 4px 10px; font-size: 11px; font-weight: 500; margin: 3px; cursor: pointer; }
.topic-tag:hover { background: #eaf3de; border-color: #97c459; }

.capability-item { display: flex; align-items: center; gap: 8px; padding: 5px 0; border-bottom: 1px solid #f5f7f5; font-size: 12px; color: #3a4a3a; }
.capability-item:last-child { border-bottom: none; }
.cap-dot { width: 6px; height: 6px; border-radius: 50%; background: #639922; flex-shrink: 0; }

.disclaimer { background: #fff8e1; border: 1px solid #f0c040; border-radius: 10px; padding: 0.75rem 1rem; font-size: 11px; color: #7a6000; margin-top: 1rem; }

div[data-testid="stButton"] button {
    background: linear-gradient(135deg,#3b6d11,#639922) !important;
    color: white !important; border: none !important;
    border-radius: 8px !important; font-weight: 600 !important;
    font-size: 12px !important; padding: 0.5rem 1rem !important;
    width: 100% !important; text-align: left !important;
    margin-bottom: 4px !important;
}
div[data-testid="stButton"] button:hover {
    background: linear-gradient(135deg,#27500a,#3b6d11) !important;
}
label { color: #1a3a1a !important; }
p { color: #1a3a1a !important; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="chat-header">
    <div class="chat-header-inner">
        <div class="chat-avatar-wrap">
            <div class="chat-avatar">🤖</div>
            <div>
                <div class="chat-title">HealthAI Assistant</div>
                <div class="chat-subtitle">FastAPI + LLaMA 3.3 70B via Groq · 50+ Languages</div>
            </div>
        </div>
        <div class="status-pill">
            <span class="status-dot"></span>
            Online · Ready
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

msg_count = len(st.session_state.chat_history)
user_msgs = len([m for m in st.session_state.chat_history if m["role"] == "user"])

# Stats
st.markdown(f"""
<div class="stats-grid">
    <div class="stat-box">
        <div class="stat-box-label">Messages</div>
        <div class="stat-box-value">{msg_count}</div>
        <div class="stat-box-sub">This session</div>
    </div>
    <div class="stat-box">
        <div class="stat-box-label">AI Model</div>
        <div class="stat-box-value">70B</div>
        <div class="stat-box-sub">LLaMA 3.3</div>
    </div>
    <div class="stat-box">
        <div class="stat-box-label">Backend</div>
        <div class="stat-box-value">FastAPI</div>
        <div class="stat-box-sub">HuggingFace</div>
    </div>
    <div class="stat-box">
        <div class="stat-box-label">Languages</div>
        <div class="stat-box-value">50+</div>
        <div class="stat-box-sub">Supported</div>
    </div>
</div>
""", unsafe_allow_html=True)

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
            return f"Sorry, I encountered an error. Please try again."
        return result["reply"]
    except Exception as e:
        return f"Connection error. Please try again."

# Main layout
col_chat, col_side = st.columns([2, 1])

with col_side:
    st.markdown("""
    <div class="side-panel">
        <div class="panel-card">
            <div class="panel-card-header">💬 Quick Questions</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    quick_questions = [
        ("🫀", "Signs of a heart attack?"),
        ("🩸", "How to control blood sugar?"),
        ("🧠", "Stress and anxiety relief"),
        ("💊", "Common drug interactions"),
        ("🤒", "Fever and body aches"),
        ("😴", "Tips for better sleep"),
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

    st.markdown("""
    <div class="panel-card" style="margin-top:12px;">
        <div class="panel-card-header">✨ AI Capabilities</div>
        <div class="panel-card-body">
            <div class="capability-item"><div class="cap-dot"></div>Symptom analysis</div>
            <div class="capability-item"><div class="cap-dot"></div>Drug information</div>
            <div class="capability-item"><div class="cap-dot"></div>Mental health support</div>
            <div class="capability-item"><div class="cap-dot"></div>Nutrition advice</div>
            <div class="capability-item"><div class="cap-dot"></div>Emergency guidance</div>
            <div class="capability-item"><div class="cap-dot"></div>Lab result explanations</div>
            <div class="capability-item"><div class="cap-dot"></div>50+ languages</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**🌐 Language:**")
    language = st.selectbox("", [
        "English", "Arabic", "Urdu", "Hindi", "French",
        "Spanish", "German", "Turkish", "Persian", "Malay"
    ], label_visibility="collapsed")

    st.markdown("""
    <div class="panel-card" style="margin-top:12px;">
        <div class="panel-card-header">🏷️ Popular Topics</div>
        <div class="panel-card-body">
            <span class="topic-tag">Heart Health</span>
            <span class="topic-tag">Diabetes</span>
            <span class="topic-tag">Blood Pressure</span>
            <span class="topic-tag">Mental Health</span>
            <span class="topic-tag">Nutrition</span>
            <span class="topic-tag">Sleep</span>
            <span class="topic-tag">Pregnancy</span>
            <span class="topic-tag">Allergies</span>
            <span class="topic-tag">COVID-19</span>
            <span class="topic-tag">Skin Care</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_chat:
    st.markdown('<div class="chat-window">', unsafe_allow_html=True)
    st.markdown("""
    <div class="chat-win-header">
        <span class="chat-win-title">💬 Conversation</span>
        <span class="chat-win-badge">FastAPI Powered</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="chat-body">', unsafe_allow_html=True)

    if not st.session_state.chat_history:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🤖</div>
            <div class="empty-title">Hello! I am HealthAI Assistant</div>
            <div class="empty-sub">
                Ask me about symptoms, medications,<br/>
                nutrition, mental health or any health concern.<br/><br/>
                <span style="color:#639922;font-weight:600;">
                    Use quick questions on the right or type below!
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="msg-row-user">
                    <div class="msg-bubble-user">
                        <div class="msg-sender-user">You</div>
                        <div class="msg-text-user">{message["content"]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="msg-row-ai">
                    <div class="msg-ai-icon">🤖</div>
                    <div class="msg-bubble-ai">
                        <div class="msg-sender-ai">HealthAI Assistant</div>
                        <div class="msg-text-ai">{message["content"]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)

    # Input
    user_input = st.chat_input("Ask me anything about your health...")
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
            if st.button("🗑️ Clear Chat", key="clear"):
                st.session_state.chat_history = []
                st.rerun()
    with col2:
        if st.session_state.chat_history:
            chat_text = "\n\n".join([
                f"{'You' if m['role']=='user' else 'HealthAI'}: {m['content']}"
                for m in st.session_state.chat_history
            ])
            st.download_button(
                "💾 Save Chat",
                data=chat_text,
                file_name="health_chat.txt",
                mime="text/plain",
                key="save"
            )
    with col3:
        if st.button("🔄 New Session", key="new"):
            st.session_state.chat_history = []
            st.rerun()

st.markdown('<div class="disclaimer">⚠️ HealthAI provides general health information only. Always consult a qualified doctor for medical advice. In emergencies call 999/911/112 immediately.</div>', unsafe_allow_html=True)
